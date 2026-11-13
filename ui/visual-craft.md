# Visual craft

The rules for drawing an interface that looks made, not generated. They
apply to any product and any toolkit. The process that uses them is in
[identity-pass.md](identity-pass.md).

Each rule names the incident behind it. Product details are labelled
examples.

## Tone, not outlines

**What.** Separate things with tone, shadow, type and spacing, not with
borders and boxes. Anything at rest gets a step of tone. A line means
focus, and nothing else. Floating surfaces (menus, popovers) carry a
shadow, not a hairline. Lists stay unboxed. Nested cards are always
wrong.

**Why.** The owner warned that putting everything into boxes and borders
is an AI tell, and design review tools flag it. Tern's audit found 1 px
rings on resting tabs, secondary buttons, time pills, per-message actions
and palette chips, and a hairline around every popover. The owner took
the tone-only version of all of them.

**Apply.**
1. Resting control on the page background: fill it one tone step darker
   than the background. On a white sheet: one step darker than white.
2. Selected: a strong fill (ink, or the accent), never a ring.
3. Focus: a 2 px line in the ink or accent colour. This is the only
   ring.
4. Keep a ring only where it carries meaning: an unticked checkbox,
   today's date in a calendar.
5. Floating surface: a two-layer shadow (a tight one plus a soft one), no
   hairline. In the dark theme, also lift its fill one step above the
   ground, so its edge holds where shadows are weak.
6. Before showing a design, count every border. Justify each one that
   remains, or replace it.

**Check.** Search the styles for borders and inset rings. Each one left
is a focus ring, a checkbox, or has a written reason.

## Every stroke end matches

**What.** Every end of a drawn mark uses the same cap as its family,
usually round, at every zoom. Connecting lines are drawn under the marks,
never over them.

**Why.** On Crake's timeline, a branch had a flat end where it left the
line and a round end at its tick. The line's segment was drawn over the
branch's round cap. The owner zoomed in and caught it: both ends must be
round, "to match the roundness" of the logo.

**Apply.**
1. Set the cap and join once for the whole icon family (for example
   round and round), and use it on every path.
2. Draw connecting lines first and marks on top.
3. Zoom to 400 % on every mark before showing it. Look at each end.

**Check.** A zoomed capture of each mark, with every end the same shape.

## One object, one drawing

**What.** An object that appears in several places is drawn the same way
everywhere: the same proportions, line weight, corner radius and details.
If it moves from one place to another on screen, it must stay the same
thing.

**Why.** Tern's bird carries a letter onto a pile while mail downloads.
The carried letter was the bird's own icon letter: almost square, with a
5 px line. The pile was flat envelopes with a 1.6 px line. Once the
letter landed it looked like a different object. The owner: it "looks
weird, like the brought envelope is designed completely different from
the rest". The fix drew one envelope, in a 3.5 px round line, for both
places.

**Apply.**
1. List every object that appears in more than one place or that moves
   between places.
2. Give each one drawing, in one source file, at one line weight in
   pixels. Choose a weight that sits well next to the marks it travels
   with.
3. When an object scales, keep its line weight in pixels. Do not let the
   line scale with it.
4. Animate the object itself from place to place. Never swap it for a
   different drawing at the hand-off.

**Check.** Put every appearance of the object side by side at its real
size. They read as the same thing.

## A drawing over an object reaches its edges

**What.** Folds, seams, tints and sheens drawn over an object span the
object's whole box, not the room left inside its padding. A line that
runs to a corner ends on the corner.

**Why.** Obálka's envelope draws two folds from its bottom corners. The
drawing sat inside the envelope with a width and height of 100 %. In
React Native those resolve inside the padding. So each fold started 16
to 18 px in from its corner, on every envelope in the app. Tests passed
and the shape looked right at a glance. The owner saw it on a phone: the
creases were "borked".

**Apply.**
1. Put the drawing in its own layer, pinned to all four edges of the
   object (absolute, 0 on every side), outside the content's padding.
2. Size the drawing to that layer. Never size it from the content box.
3. Give the drawing the object's own outline in its coordinates: the
   corners in the path are the object's corners.
4. Check this on every object that carries a drawing, not just the one
   that showed the fault. One shared component fixed three screens.

**Check.** A full-resolution crop of each corner where a line ends. The
line meets the corner, with no gap. A test asserts the drawing's layer
has no padding and sits at 0 on every side.

## A line weight per family

**What.** Marks shown together share a line weight. A mascot drawn at
64 px and the 16 px icons beside it are different families. Each family
has its own weight, chosen on purpose.

**Why.** The envelope incident above. A thin object next to a heavy
mascot reads as a wisp. A heavy object on a thin pile reads as a foreign
body.

**Apply.** Write down each family and its weight: icons (for example
2 px at 24), the mascot, the objects the mascot handles. Check new marks
against the list.

**Check.** The design doc lists the families and their weights.

## A drawn icon set, grown from the idea

**What.** Every icon in the product comes from one drawn family. The
family grows from what the product already draws (its site, its app
icon, its printed material) and from the objects the idea is about. Stock
icons, or a mix of sets, are a placeholder, not a design.

**Why.** A proposal's screens kept the mark rare, as the identity pass
asks, and used system symbols everywhere else. The owner's verdict: "Where
are some icons? That adds identity to the app." With the mark held back,
the icons are the part of the identity the user sees on every screen.

**Apply.**
1. Facts first: collect the product's existing drawings and note their
   line weight, caps, corners and colour. Keep what identifies them.
2. List every icon the screens need, from the inventory, not from memory.
3. Pick the family's rules: grid (for example 24), weight (for example
   2 px), caps and joins, fill or line, the one colour and when it changes.
   Give the idea's object (the thing the mark carries or hands over) a
   place inside the icons that are about it.
4. Draw at least two families, each over the whole list, and recommend
   one. Show each at its real sizes, in both themes, and in a real screen.
5. Third-party marks (bank, card or store logos) are not redrawn. Use the
   real ones the product already has the right to show, each on its own
   neutral tile, and say where they came from.

**Check.** No icon on any screen is a system or stock symbol unless the
design doc says why. Each icon of the family, side by side at 24 and at
48, reads as one hand. The weight is in the families list above.

## The system's own sign for the system's own act

**What.** A control that stands for something the operating system does
shows the sign that system uses for it. Unlocking shows Face ID's face on
an iPhone and a fingerprint on Android. Sharing shows each system's share
sign. The sign is drawn in the product's own icon family, not taken from
a stock set.

**Why.** Obálka's lock screen board drew the Face ID face, on an iPhone
mock-up. Built as it was, Android phones that unlock with a fingerprint
showed a face (2026-11-12). The owner's rule: the platform's own sign
reads as native. The first fix took a stock fingerprint, which no longer
matched the board's face; both are now drawn in one frame at one weight
(1068694).

**Apply.**
1. List the controls that stand for a system act: unlock, share, open in
   another app, add to the calendar, the system's settings.
2. For each, draw one glyph per system, in the product's family: the same
   frame, line weight and stroke ends. The system changes what is drawn,
   never how.
3. Choose the glyph in one place, by the platform, with the platform as
   an argument so a test can ask for each.
4. A board drawn for one system shows that system's sign; note the other
   system's on the canvas, so the design holds both.

**Check.** A test renders each such glyph for every platform and expects
different drawings in the same frame. Walk the screen on each platform
and look at the sign.

## Compact, not breathy

**What.** Content or the main control starts right under the window's
header. Decoration takes only the room it needs and overlaps the chrome
instead of pushing content down. Boards and proposal pages end where
their content ends.

**Why.** Drafts kept coming out "breathy". One inbox proposal's decorative
flap took about a fifth of the screen before the first control. The owner
has corrected this on three products. These are tools people open to get
something done.

**Apply.**
1. Look at the top 200 px of every screen. Anything there that isn't
   content or a control needs a reason.
2. Use the smaller of two spacing steps when unsure.
3. Measure the content's height and size the board to it.

**Check.** No band of empty space above the first content, and none at
the bottom of a board.

## Rank what the screen says

**What.** Text that carries different facts is split and ranked, not run
together. What a person looks for leads. What can wait goes quieter,
shorter, or behind a tap. Nothing is dropped: the full fact stays one tap
away, and a screen reader always hears it whole.

**Why.** On Obálka, a data-box service sends a self-employed sender as one
string: "Jan Novák - podnikající fyzická osoba". The envelope printed it
as one heading. The legal form was as loud as the name and took three
lines of a 120 px block. The owner asked for the name first, and a rule:
too much at once confuses, so detail comes when it is needed, and what
shows when is chosen with care (obalka 556e19e).

**Apply.**
1. For each text, list the facts in it: a name, a legal form, an ID, a
   date, a place.
2. Rank them by what the reader is looking for on this screen. A list row
   needs the name. A detail may need the ID.
3. Give the first fact the strong role. Put the rest on a quieter line, in
   a smaller role and a softer colour.
4. Shorten what readers know by its short form ("PFO", not "podnikající
   fyzická osoba"). A tap, a tooltip or a long press shows it in full.
5. Never drop a fact to save room. The screen reader's label says it in
   full, and one tap or one level deeper shows it.
6. Rank by what tells things apart, not by habit. Obálka's address keeps
   the town bold and the street quiet: the town tells three Jan Nováks
   apart.
7. Decide what shows where, and when, on purpose. Write the ranking down
   in the design doc, with the reason.

**Check.** No text block mixes facts at one weight. For each quieter or
shortened fact, show where the full one is: the tap, the next screen, the
spoken label.

## Nothing anyone reads under 11 px

**What.** Text that carries information is at least 11 px: dates, tags,
counts, key hints. Monospace is for data and measurements, not for
decoration.

**Why.** An automated scan of tern's canvas found about twenty labels at
9.5 to 10.5 px, among them date headers, row dates, status tags and key
hints. Uppercase monospace at that size blurs on a 1x screen, and those
labels carry real information.

**Apply.** Set an 11 px floor in the type scale. Smaller sizes may only
draw glyphs that sit inside a shape, like an avatar's initials.

**Check.** Search the styles for font sizes under 11. Each hit is a glyph
inside a shape.

## One anatomy per job

**What.** Each job has one component with one anatomy. Every toast looks
the same. Every secondary button looks the same. Variation lives in the
words, not the shape.

**Why.** Tern had two toasts: an ink pill for "done", and a white card
with a progress bar for "sending". Same job, two looks. The owner picked
the ink pill for all toasts; the sending one counts down in words.

**Apply.**
1. For each component, list every place it is used.
2. If two places use different anatomies for the same job, pick one and
   redraw the other.
3. Write the anatomy down: parts, order, sizes, the action's place.

**Check.** The design doc lists each component's anatomy, and the canvas
shows no second version.

## Show it in real context

**What.** Proposals are drawn inside the real frame: the real window
header (with the system's own window buttons on macOS), a phone's real
status bar, the real neighbours, real copy, both themes, and the longest
shipped language.

**Why.** On a phone app, the owner asked for real status-bar icons before
choosing, to judge the spacing. On tern, a flow drawn as loose cards
looked like "another app". In the app it already sat in the right frame,
and the drawing misled the review.

**Apply.** Copy the frame from the live design or the app. Never redraw
it from memory. Show a pseudo-locale for the longest strings.

**Check.** Every proposal shows its frame and both themes.

## Words in the product's voice

**What.** Screens speak in the product's own voice. Dialogs use little
text and a button that names and does the action. Serious moments get
calm words, not jokes.

**Why.** Tern's first-run lines carry its idea ("Bring your mail home.",
"Only you hold the key."). Its inbox zero carried a meme, which a review
flagged as wrong next to a bank statement. The owner chose "All home.
Nothing waits on you."

**Apply.**
1. Write buttons as verbs with their object: "Empty Trash", not "OK".
2. Keep body text to one or two short lines.
3. Read every line aloud next to the most serious message the product
   handles. If it jars, rewrite it.
4. Translate it, and check the translation for the same tone.

**Check.** No "OK" or "Yes" buttons. No jokes on screens that can show
sensitive content.

## Motion with a reason

**What.** A motion tells a small story tied to the product's idea, plays
at the moment it is about, then rests. Every motion has a reduced-motion
form.

**Why.** Tern's bird pecks pebbles at the shore on an empty list, and
carries a letter like a fish while mail downloads. Both are tied to its
idea, so they read as serious and specific. A generic spinner would
have said nothing.

**Apply.**
1. Use the product's own mark or objects instead of a generic spinner
   wherever it waits.
2. Play one-off moments once. Loop only while work is actually
   happening.
3. Give every motion a still frame for reduced motion that still makes
   sense.

**Check.** Turn on reduced motion. Every screen still reads correctly.
