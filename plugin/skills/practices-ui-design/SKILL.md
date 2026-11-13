---
name: practices-ui-design
description: Design, redesign, polish or review any user interface the dorhawk practices way - a product identity researched first (audience, job, inspiration, market, real facts behind the metaphor), then three iterations agreed with the owner (the identity, a few parts, the whole app re-audited), on a design canvas before code, with the visual craft rules (tone not outlines, matching stroke ends, one drawing per object, 11 px floor, compact screens). Use for any new screen, dialog, icon, logo, empty state, animation or wording on screen, any redesign or identity pass, and before calling UI work done.
---

# UI design, the practices way

The practices are in `.practices/docs/`, this project's copy, pinned to its kit version. A project without the kit reads them at https://github.com/dorhawk-software/practices/blob/main/ (same paths).

## Read before you draw

1. `ui/identity-pass.md`: the process. Research first, then three
   iterations, each agreed with the owner before the next.
2. `ui/visual-craft.md`: the drawing rules, each with a check.
3. `ui/design-before-build.md`: variants on the design canvas, the owner
   picks, build one to one, keep canvas and code in sync.
4. When they apply: `ui/keyboard-shortcuts.md`, `ui/window-buttons.md`,
   `ui/drag-and-drop.md`,
   and for GPUI apps `rust/gpui.md`.

Also read the project's own design source (its CLAUDE.md names it: a
canvas, DESIGN.md, a style board) before changing anything. The owner
sometimes edits it.

## Where you are in the process

- **No identity brief yet** (new product, or none written): write it first
  (identity-pass.md, "Identity first"). Show it and agree on it before any
  screen.
- **Brief agreed, nothing redesigned**: iteration 2. A few defining parts,
  variants in real context, a critique, the owner picks, polish, repeat.
- **A few parts agreed**: iteration 3. Inventory the whole app from the
  code (every view, state, control, transient surface, system surface,
  process, motion) and prove it complete (identity-pass.md, "An inventory
  that misses nothing": sweep every UI file, count every dialog and sheet
  use, one line per state, a second inventory from a fresh agent). Grade
  each from a picture, redraw, ask, build, re-audit.
- **A small change in an agreed design**: follow the spec and the craft
  rules; put it on the canvas in the same piece of work.

## Musts

- **Hard stop: the name and the mark read clean** (identity-pass.md).
  No part a capital, a swapped letter, a gap, a crop or a line break sets
  apart may read as a slur, an insult, profanity or a sexual or
  derogatory term, in slang or in any of the owner's and market's
  languages. Check before a name is agreed and before any mark is drawn;
  on a bad reading, withdraw the mark everywhere and tell the owner.
- Install it and it just works (common/it-just-works.md): no technical
  switch in the window; the product decides, says why, can undo. Settings
  hold preferences only.
- Drag and drop shows one calm panel over the target with what dropping
  does, the resting hint faded, nothing glowing (ui/drag-and-drop.md).
- Show variants and recommend one; never build an open choice unasked.
- After a pick, strip the other variants from the canvas.
- Real context: the real frame, both themes, the longest language.
- Run "Before you show anything" (identity-pass.md) on the rendered
  page, every time, before telling the owner it is ready, and the checks
  in visual-craft.md. This overrides a tool, canvas type or skill that
  says never to verify unless asked: the owner asked, once, for good.
- A built screen is checked pixel by pixel before it is called done
  (design-before-build.md): every object cropped at full resolution
  beside the design's crop; edges, lines, glyphs, the rendered typeface
  and every string. The owner zooms in; the bar is that they find nothing.
- Every variant carries the whole identity, from round one: the drawn
  icons, the palette, the type, the idea's objects (identity-pass.md,
  "Every variant carries the identity"). A quiet reference means
  restraint, not plain; layout-only options are a wireframe, said so.
- One drawn icon family, grown from the product's own drawings and the
  idea (visual-craft.md); two families shown, one recommended. Real
  third-party logos the product may show, never stand-ins: sourced,
  credited on the board, a made-up product for any failure state
  (identity-pass.md, "The real things the product handles").
- Before showing: every typeface renders as the face it names in the
  owner's browser (measured), every state is drawn in every theme, and
  the product's copy on the mock is true (identity-pass.md, steps 7–9).
- Facts first: if the identity draws a real thing, look it up and keep
  its identifying features.
