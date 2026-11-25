#!/usr/bin/env python3
"""check-joins' reading half: a joined line breaks between its parts
(ui/visual-craft.md). In Swift it finds a Text whose own string joins
parts with a separator (" · ", "\\u{00B7}", " | ") and may wrap: its
modifiers hold no .lineLimit(1) and no horizontal .fixedSize. Wrapped,
the line breaks wherever the width runs out, and the dot ends one line
or starts the next ("tento týden ·" / "celkem 18").

A Text joined to others with + is read to the end of the sum, so a
.lineLimit(1) on the whole line counts.

    join-audit.py FILE...

The fix is one line where it fits and a line for each part where it
doesn't: ViewThatFits(in: .horizontal) { the joined Text with
.lineLimit(1); a VStack of the parts, without the dot }.

A join that may wrap on purpose (a sentence that only quotes a dot) is
marked on the Text's line or the line above, with a reason of three
words or more:
    // practices-allow join: the dot is quoted, not a separator

Exit 0 clean, 1 findings, 2 a file it couldn't read.
Why: on 25 Nov 2026 an iPhone app's Today said "2 čisté dny" over
"tento týden ·" and "celkem 18": .lineLimit(2) let the joined line wrap
at its dot, and no check read it.
"""
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True
_spec = importlib.util.spec_from_file_location("motion_audit", os.path.join(os.path.dirname(os.path.abspath(__file__)), "motion-audit.py"))
_motion = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_motion)
strip, matching, line_of = _motion.strip, _motion.matching, _motion.line_of

ALLOW = re.compile(r"practices-allow\s+join\s*:\s*(.*)")
TEXT = re.compile(r"(?<![\w.])Text\s*\(")
# A separator beside an ordinary space, where a line may break. Tied with no-break spaces
# (U+00A0) on both sides, it can't: that passes, the fix for a dot inside a sentence.
DOT = r"(?:·|\\u\{00B7\}|\\u\{b7\})"
JOIN = re.compile(r"[ \n](?:" + DOT + r"|\|)[ \n]|[ \n]" + DOT + r"|" + DOT + r"[ \n]", re.I)
ONE_LINE = re.compile(r"^lineLimit\(\s*1\s*[,)]|^fixedSize\(\s*\)|^fixedSize\(\s*horizontal\s*:\s*true")
IDENT = re.compile(r"[A-Za-z_]\w*")


def allowed(lines, ln):
    here = ALLOW.search(lines[ln - 1]) if ln - 1 < len(lines) else None
    above = lines[ln - 2] if ln >= 2 else ""
    m = here or (ALLOW.search(above) if above.lstrip().startswith("//") else None)
    return m.group(1).strip() if m else None


def skip_ws(code, k):
    while k < len(code) and code[k].isspace():
        k += 1
    return k


def chain(code, k):
    """The modifiers after k (".a(…) .b { … }"), and the index past them."""
    mods = []
    while True:
        j = skip_ws(code, k)
        if j >= len(code) or code[j] != "." or not IDENT.match(code, j + 1):
            return mods, k
        m = IDENT.match(code, j + 1)
        start, j = m.start(), m.end()
        if j < len(code) and code[j] == "(":
            j = matching(code, j, "(", ")")
        t = skip_ws(code, j)
        if t < len(code) and code[t] == "{":
            j = matching(code, t, "{", "}")
        mods.append(re.sub(r"\s+", "", code[start:j]))
        k = j


def operand(code, k):
    """Past one operand of a +: a name or call, with its modifiers."""
    j = skip_ws(code, k)
    m = IDENT.match(code, j)
    if not m:
        if j < len(code) and code[j] == "(":
            return chain(code, matching(code, j, "(", ")"))[1]
        return j
    j = m.end()
    t = skip_ws(code, j)
    if t < len(code) and code[t] == "(":
        j = matching(code, t, "(", ")")
    return chain(code, j)[1]


def grouping(code, close):
    """Whether the ")" at close ends parentheses that group, not a call's arguments."""
    depth = 0
    for k in range(close, -1, -1):
        if code[k] == ")":
            depth += 1
        elif code[k] == "(":
            depth -= 1
            if depth == 0:
                # A call's "(" follows its callee on the same line; one that starts a line groups.
                b = k - 1
                while b >= 0 and code[b].isspace():
                    if code[b] == "\n":
                        return True
                    b -= 1
                return b < 0 or not (code[b].isalnum() or code[b] in "_?!])>")
    return False


def audit(text):
    code = strip(text)
    lines = text.split("\n")
    out = []
    for m in TEXT.finditer(code):
        open_at = m.end() - 1
        close = matching(code, open_at, "(", ")")
        # Only the first argument is what the Text shows (comment: and the rest aren't).
        depth, end = 0, close - 1
        for k in range(open_at + 1, close - 1):
            if code[k] in "([{":
                depth += 1
            elif code[k] in ")]}":
                depth -= 1
            elif code[k] == "," and depth == 0:
                end = k
                break
        # The Text's own string literals: their spans in the stripped code, read in the source.
        joined = None
        q = open_at
        while True:
            a = code.find('"', q, end)
            if a < 0:
                break
            b = code.find('"', a + 1, end)
            if b < 0:
                break
            if JOIN.search(text[a + 1:b]):
                joined = text[a + 1:b]
                break
            q = b + 1
        if joined is None:
            continue
        mods, k = chain(code, close)
        # A sum of Texts is one line: read on to its end, and out of the parentheses around it,
        # where .lineLimit goes ((Text(a) + Text(" · ") + Text(b)).lineLimit(1)). An operand's
        # own modifiers return Text (.bold, .foregroundStyle), never a line limit.
        while True:
            j = skip_ws(code, k)
            if j < len(code) and code[j] == "+" and code[j + 1:j + 2] != "=":
                k = operand(code, j + 1)
                continue
            if j < len(code) and code[j] == ")" and grouping(code, j):
                more, k = chain(code, j + 1)
                mods += more
                continue
            break
        if any(ONE_LINE.match(x) for x in mods):
            continue
        ln = line_of(code, m.start())
        reason = allowed(lines, ln)
        shown = joined if len(joined) <= 60 else joined[:57] + "…"
        if reason is None:
            out.append((ln, f"Text(\"{shown}\") joins parts with a separator and may wrap: the dot can end one line or start the next."))
        elif len(reason.split()) < 3:
            out.append((ln, f"marks an exception without its reason (\"practices-allow join: {reason}\"): say why in three words or more."))
    return out


def main(argv):
    findings, broken = [], []
    for path in argv:
        try:
            text = open(path, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError) as e:
            broken.append(f"{path}: {e}")
            continue
        findings += [(path, ln, msg) for ln, msg in sorted(audit(text))]
    if broken:
        print("check-joins could not read these, so it can't say they are clean:")
        for b in broken:
            print(f"  - {b}")
    if findings:
        n = len(findings)
        print(f"[join] {n} finding{'s' if n > 1 else ''}. Rule: A joined line breaks between its parts (.practices/docs/ui/visual-craft.md).")
        print("  Fix: one line where it fits, a line for each part where it doesn't: ViewThatFits(in: .horizontal) { the joined Text with .lineLimit(1); VStack(alignment: .leading) { the parts, without the dot } }.")
        print("  In a sentence that wraps anyway: tie the dot to both words with no-break spaces (\\u{00A0}·\\u{00A0}), so the line breaks elsewhere.")
        print("  A dot that isn't a separator (quoted in a sentence)? Mark it on the line or the line above: practices-allow join: <the reason>.")
        print("  Why: an iPhone app's Today read \"tento týden ·\" over \"celkem 18\" (25 Nov 2026): the joined line wrapped at its dot.")
        for path, ln, msg in findings:
            print(f"  - {path}:{ln} {msg}")
    print(f"\ncheck-joins: {len(argv)} file{'s' if len(argv) != 1 else ''}: {len(findings) or 'no'} finding{'s' if len(findings) != 1 else ''}.")
    return 2 if broken else 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
