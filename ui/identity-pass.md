# An identity pass, through the whole app

How to give a product a stronger identity, and how to carry it into every
screen. It is written to be followed step by step, by a person or a coding
agent. The rules for the drawing itself (outlines, stroke ends, type
sizes) are in [visual-craft.md](visual-craft.md).

The lessons come from three passes in one day (2026-11-11): Obálka (a
bland app, pushed far), Crake (a strong identity, polished) and tern (a
strong identity, first wrongly limited to its logo). Product details here
are labelled examples. The rules hold for any product.

## The bar: serious, with one physical idea

**What.** An identity pass gives a product its own look and feel: drawn
icons, a material or a physical metaphor, considered buttons and sections,
and one or two signature motions. It stays serious. It is playful but never
gamified, because people trust these apps with their mail, money or
network.

**Why.** The owner judged three apps against two references: a sibling
app with a strong look, and the company website (an envelope, a cellophane
window). Next to them the apps "lacked identity". One proposal then went
too far: dates drawn as rubber stamps on a government mail app's inbox
rows. The owner called it "taking it too far". A serious product that
looks like a toy loses trust.

**Apply.**
1. Name the references the owner holds up, and look at them first.
2. Find the product's one physical idea in its own name or job. Examples:
   printed matter for a postal app (envelope, window, stamp, postmark); a
   line the product keeps to, for a VPN that routes traffic; a seabird
   that brings mail home, for a mail client.
3. List the objects that idea gives you. Give each object exactly one
   job. Example: the envelope's window shows who it's from; the postmark
   shows when it came.
4. Put identity into those few objects only, never into every piece of
   data. A date stays a date.
5. Test each idea against "would I trust this app with my bank's
   letters?". If not, cut it.

**Check.** You can name the idea in one sentence and list its objects,
each with its one job. No object appears without a job.

## Scale of change follows the identity; scope is always the whole app

**What.** Judge how much identity the product already has before you
propose anything. A bland product gets pushed far. A product with a
working identity keeps its look and tokens and gets precise polish, plus
one or two objects that grow out of what is already there. Either way,
you review every screen.

**Why.** Crake already had a strong look: a line along its left edge. The
pass kept the look and grew that line into a timeline with marks. The
owner praised it for "staying true to the product", with "merely very
good polishes". Tern also had a defined design, so the pass first redrew
only its bird (logo, icon, tray, two empty states). The owner called that
"very naive": a defined design can still be improved. The full review
then found real gaps. The identity was missing from the screens used most
often. Boxes were creeping in. One flow looked like another app. The
canvas had drifted from the code.

**Apply.**
1. Rate the product: bland, partial, or strong. Write one sentence on why.
2. Bland: propose a new idea and its objects (see the bar above).
3. Partial or strong: keep the palette, type, tokens and voice. Find what
   is already there that can carry more meaning. Grow one or two objects
   out of it.
4. In every case, run the whole process below on every screen. "Polish
   only" sets how big the changes are, not whether you look.
5. Finding nothing to change is a valid result. Skipping the look is not.

**Check.** The proposal states the rating and lists every screen that
was reviewed, with a verdict for each.

## The first pass: idea, showcase screens, pick

**What.** The first pass settles the direction. It applies the idea to
the screens that define the product and to the logo. Variants go
side by side on the design canvas, the owner picks, and the pick is
polished into the spec.

**Why.** On Obálka and Crake, the first pass redesigned only some screens.
That is enough to agree on the idea and the polished spec. It is not
enough to call the product done; that is the second pass.

**Apply.**
1. Survey every screen and board first. Read each one's source, not only
   its picture. Note where the identity is strong, generic, or missing.
2. Run an independent critique of the whole surface before proposing:
   two isolated reviewers, one doing a design review and one running an
   automated detector. Neither sees the other's output.
3. Verify every factual claim in the critique against the code before you
   report it. Reviewers get facts wrong. On tern, a reviewer said three
   undo windows disagreed. They were one window caught at three moments.
   Another said a flow looked like another app. The app already framed
   it correctly; only the canvas lagged.
4. Draw two or three variants for each open choice, in place, with real
   context. Real context means the real header, the real status bar, real
   copy, both themes. The owner judges spacing from it.
5. Recommend one variant per choice and say why in one line.
6. Ask with concrete options. Ask at most four questions at a time.
7. After the pick, remove the other variants and their labels from the
   canvas ([design-before-build.md](design-before-build.md)).
8. Polish the picked design: a second critique, then fixes, then look at
   it again.

**Check.** Every choice on the canvas has exactly one design left. The
critique report and its verdicts are saved where the next pass can read
them.

## The second pass: audit the entire app against the spec

**What.** After the first pass is chosen and polished, audit the whole
application against that spec. Redraw everything that falls short. Show
it to the owner and take their tweaks. The pass is done when the whole
app matches the spec, not when the showcase screens do.

**Why.** The owner, after the three first passes: the first pass shows
"the idea of how we want to take the product further". What must follow
is an audit of "the entire application, its all sections, clickity-
clacketies, modals, animations, processes".

**Apply.**
1. Build an inventory from the code, not from the canvas. List every
   route, window, view, dialog and popover.
2. For each, list its states: empty, loading, partial, full, error,
   offline, read-only, first run, signed out.
3. List every control and its states: rest, hover, pressed, focus,
   selected, disabled, busy.
4. List every transient surface: toasts, menus, tooltips, confirmations,
   notifications, the tray or menu-bar icon, the app icon at every size.
5. List every process end to end: onboarding, sign-in, adding an account,
   sending, syncing, undo, deleting, settings changes, quitting.
6. List every motion: transitions, progress, empty-state scenes, and what
   reduced motion shows instead.
7. Walk the list in both themes and in every shipped language, including
   a pseudo-locale for long strings.
8. Grade each item against the spec: matches, drifts, or misses the
   identity. Use the rules in [visual-craft.md](visual-craft.md).
9. Redraw what drifts or misses. Put it on the canvas with variants when
   the choice is open. Ask the owner. Strip the losers.
10. Fix canvas-versus-code drift as you find it: stale states, leftovers,
    features the canvas still calls "soon".
11. Build the agreed designs one to one, then capture the app and compare
    it with the canvas ([design-before-build.md](design-before-build.md)).

**Check.** The inventory exists as a checklist, and every line is marked
matches or fixed. The owner has seen every redrawn item.

## Where the product's mark appears

**What.** The product's own drawn mark (a mascot, an emblem) appears only
at meaningful moments. Those are usually the moments its idea is about.
Everywhere else the interface stays quiet.

**Why.** Tern's bird stands for bringing mail home. It was there for
fetching mail, but absent at inbox zero (the moment people remember,
by the peak-end rule) and when mail is sent. Inbox zero showed a joke
line instead: "Go touch some grass." The owner picked the bird landing on
the shore for inbox zero, and a small bird carrying the letter in the
sending countdown. Nothing else got the bird.

**Apply.**
1. List the moments the idea is about. For a mail client: mail arriving,
   mail leaving, everything handled.
2. Give the mark those moments, and only those.
3. Let the copy go quiet where the mark speaks. Prefer a calm line in the
   product's voice to a joke. A joke next to a bank statement reads wrong.
4. Use one motion per moment, played once. Then rest. Loop only while
   something is actually working.

**Check.** You can list every place the mark appears, and each one is one
of the idea's moments.

## Before you show anything

**What.** A short pass over every page you are about to show the owner.

**Why.** The owner zooms in. They found leftover thin lines, a stroke
with one round end and one square end, a stray word printed on a board,
and a designer's note inside a mock's progress card. Each one costs trust
in the whole proposal.

**Apply.**
1. Look at the rendered page, not the source. Zoom into every mark.
2. Count the borders and boxes. Remove each one that tone, shadow or
   spacing could replace.
3. Check the top 200 px of each screen for dead space, and the bottom of
   each board.
4. Search the page for leftovers: placeholders, `[N]`, notes to yourself,
   text in the wrong language, states the code no longer has.
5. Check every claim in captions against the code.

**Check.** The handoff message says these checks ran.
