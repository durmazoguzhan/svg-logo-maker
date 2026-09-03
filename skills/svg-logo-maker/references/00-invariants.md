# Invariants

These hold whatever the style is. A geometric mark, a serif wordmark and a
badge disagree about almost everything, and they agree about this.

Each one names how to check it, because a design rule nobody can test is a
preference. Where a script can decide, the script is named. Where only a person
can decide, the test is written so two people would reach the same answer.

---

## 1. The mark survives one colour

Print it in one ink and the shapes must still be separate shapes. Colour is
allowed to carry meaning; it is not allowed to carry structure.

This is not a print-only concern, though print is where it bites hardest.
Engraving, embossing, a stamp, a watermark, a dark-mode UI and a 16px favicon
are all one colour or close to it.

**Check:** `scripts/legibility.sh logo.svg` reports *structure kept in one
colour*. Below 0.25 the one-colour version is a different mark. An app icon
sitting on a coloured plate scores low by design and that is fine — what is not
fine is a wordmark or a standalone symbol scoring low.

**The usual cause:** two adjacent shapes with different hues and no gap between
them. Put a gap in, or overlap them and knock one out.

---

## 2. Nothing important is thinner than one device pixel at the smallest size

A stroke is a line until it drops under a pixel, and then it is a grey
suggestion. Work it out rather than squinting at it: at a 512 viewBox rendered
into 16px, the scale is 0.031, so a 4-unit stroke lands at 0.125px.

**Check:** `scripts/check.py --favicon-size 16 logo.svg` computes the thinnest
stroke in device pixels and says whether it survives.

**The fix is rarely "make it thicker".** A logo that needs hairlines at large
sizes and blocks at small ones wants two drawings, not one compromise. Ship a
simplified small variant and say where the cutover is.

---

## 3. Every mark has one place the eye lands first

Two elements of equal visual weight make the reader choose, and they will
choose differently each time, which is the opposite of a logo.

**Check, and it is a person's job:** look at the 32px render for one second,
then look away and say what you saw. If the answer is a list, there is no
focal point.

Weight comes from size, from solidity, and from isolation. The largest shape is
not automatically the focus — a small solid dot inside a large thin ring reads
as the focus, because solidity beats area.

---

## 4. The empty space is drawn, not left over

Negative space is a shape and it has to be as deliberate as the ink. Gaps
between elements should look chosen: equal where they mean equal, and clearly
unequal where they mean different. Nearly-equal is the failure — a 9-unit gap
beside an 11-unit gap reads as a mistake, while 8 beside 16 reads as a decision.

**Check:** list every gap in the drawing. If two of them differ by less than
20% and are not meant to be identical, make them identical or make them
obviously different.

---

## 5. The construction is regular even when the result is not

Pick a unit and hold it. Coordinates on a grid, radii in a small set, angles
from a small set, strokes from a small set. A mark built from 3, 6 and 12 with
one deliberate exception reads as designed; a mark built from 3.4, 6.1 and 11.7
reads as dragged into place.

**Check:** collect every number in the file. Ask how many distinct values there
are and whether the odd one out is odd on purpose.

Symmetry is a separate question from regularity, and perfect symmetry is not a
goal. A regular construction with one intentional break is usually more alive
than a mirror.

---

## 6. It looks like itself and not like something else

Two failures here. Resembling an existing brand is the loud one. The quiet one
is resembling the category: every AI company with a hexagon and a node graph,
every fintech with a rising bar chart, every delivery app with a swoosh.

**Check:** describe the mark in one sentence without naming the company. If
that sentence would fit twenty other companies in the same industry, it is a
category badge, not an identity.

---

## 7. The file is editable by whoever comes next

Groups carry ids. Repeated elements come from `<defs>` and `<use>`. Numbers
have as few decimals as the drawing needs. Nobody should have to reverse
engineer a path to move the icon.

**Check:** `scripts/check.py` flags a missing named group and reports the path
node count. Past roughly 250 nodes you are looking at a traced bitmap and
neither you nor anyone else will edit it.

---

## 8. The file carries nothing it cannot carry with it

No external font, no `@import`, no linked image, no `<use href="other.svg#x">`.
A logo lands on machines you will never see.

**Check:** `scripts/check.py` reports external references as errors. Live
`<text>` is an error too: it renders with whatever font the opening machine
resolves, which is a different logo.

---

## 9. Text becomes paths before it leaves

Delivery only. Keep the live-text version as your editable master, because a
wordmark you cannot retype is a wordmark you cannot fix.

**Check:** `scripts/outline.sh` converts and, before it does, reports what
fontconfig actually resolved. If you asked for Helvetica and the machine has
Nimbus Sans, outlining freezes Nimbus Sans and the file will look right to you
and wrong to the foundry.

**Licensing lives here too.** Outlining does not launder a font licence.
Many licences allow embedding or outlining in a logo and some do not; check
before it becomes a trademark.

---

## 10. The set is delivered, not the file

One SVG is not a logo, it is one view of one. What ships:

  primary lockup, full colour
  one colour dark, one colour light (reversed)
  square icon, extracted rather than squeezed
  favicon PNGs and a multi-resolution .ico
  outlined SVG plus PDF and EPS for print
  a page saying minimum size, clear space and what not to do

**Check:** `scripts/variants.py`, `icon-extract.py`, `render.sh`, `ico.sh` and
`print.sh` produce all but the last one, and the last one is writing.

---

## How to use these while designing

Run them as a gate, not as inspiration. Draw first, then walk the list. Rules
1, 2 and 8 have scripts and take seconds. Rules 3, 4, 5 and 6 need a person and
are where the actual judgement is.

If a design fails 3 or 6, start again. Those are decisions about what the mark
*is*, and no amount of adjusting stroke weights repairs them.
