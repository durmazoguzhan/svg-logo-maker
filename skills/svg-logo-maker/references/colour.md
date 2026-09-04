# Colour

Everywhere else in this repository colour appears as a risk to be removed. Do
not let hue carry structure. Turn the gradient off and see whether the mark
dies. Test it in one ink. That instinct is right and it is half the subject,
because a logo also has to have colours, and choosing them badly is a way to
fail that no amount of one-colour discipline catches.

This file is the other half. It is short on taste and long on the three
questions that have answers, because a design rule nobody can test is a
preference and this skill does not ship preferences.

---

## What a logo palette is not

Almost everything written about colour theory is written for interfaces. Five
to eight coordinated hues, a neutral ramp, semantic states, hover and disabled.
Those articles teach schemes that generate four, five and six harmonious hues,
and they are solving a problem a logo does not have.

**A logo carries one, two or three inks.** Past three it stops being a mark and
starts being an illustration, it stops separating cleanly, and it stops
surviving the places a logo has to go. So most of the classical schemes are
answering a question you are not asking.

Of the seven usually listed, two do real work here:

**Monochromatic** — one hue, varied in lightness. This is what "ink plus a
tint" already is, and it is the safest palette a mark can have, because
lightness is the dimension that survives one-colour printing, greyscale,
engraving and every colour vision deficiency. If a mark works and you cannot
say why, this is often it.

**Complementary, or better split-complementary** — one dominant ink and one
accent from across the wheel. This is the shape of nearly every two-colour
logo. Split-complementary (the accent taken from beside the true complement
rather than on it) is usually the better choice, because a true complement at
similar lightness vibrates at the edge where the two shapes meet.

The other five — analogous, triadic, tetradic, square, and the various
rectangles — generate more hues than a logo can carry. They are worth knowing
so you can recognise when a brief is really asking for an identity system
rather than a mark. Use them for the system, not for the mark.

**Analogous deserves one warning of its own.** Neighbouring hues are pleasant
and they are the classic way to build a mark that dies in one colour: adjacent
hues frequently sit at similar lightness, so the shapes merge the moment hue is
removed. If you go analogous, separate the two by lightness deliberately and
then run the one-colour test rather than assuming.

---

## 1. Every ink has to clear what it sits on

A logo is a graphical object, so **WCAG 1.4.11 asks 3:1** against every surface
it is approved for. A wordmark is read, so hold it to **4.5:1**; people are
recovering the product's name from it and that is text behaviour whatever the
markup says.

**Check:** `scripts/contrast.py logo.svg --bg '#YOURPAPER,#YOURPLATE'`. It
errors on a surface you named and warns on one you did not.

**Test the surfaces the brand does not own, too.** White, black and mid grey
are in the default set because a mark meets them whether or not anyone chose
them: a partner's press release, a conference slide template, a dark-mode
README, a grey card in someone's deck.

**Mid grey is a routing instruction, not a gate.** To clear 3:1 against
`#808080` an ink needs relative luminance above 0.747 or below 0.039, so no
saturated mid-tone can pass it — that is arithmetic, not a fault in your
accent. A naive reading of a failure here pushes people to desaturate a
perfectly good brand colour. The correct response is to say which variant that
surface gets.

---

## 2. The press has to be able to reach it

A hex chosen on a monitor is a promise the press may not keep, and the failure
is silent. The separation moves the colour, and the first anyone sees of it is
a proof that looks wrong for reasons nobody can name.

sRGB is larger than four-colour process in exactly the places brand colours get
chosen: saturated oranges, vivid reds, bright greens and most purples. A colour
outside the gamut is not merely approximated. It is **unstable** — it will
differ between presses, papers and days, and its spot version and its process
version will never agree with each other.

**Check:** `scripts/gamut.py '#C8442A'`. It converts into a CMYK profile and
back and reports CIEDE2000. Under 1.0 the colour prints as itself; past about
3.5 the press cannot reach it.

**When a colour fails, do not desaturate until it passes.** Hold the hue and
walk the chroma down to the boundary — `gamut.py --find` does this and reports
how much chroma survived. The difference matters: one of those is losing the
brand colour, the other is locating it.

Lightness usually survives the walk untouched, which means the mark's optical
balance does not change. That is the argument for fixing gamut by chroma rather
than by picking a new colour.

### Near-black is a substrate limit, not a bad choice

A near-black will fail this check and you should not fix it. Coated process
printing bottoms out around L\* 18; screen black is L\* 0 and a brand ink at
L\* 8 is simply darker than paper and ink can go. Lightening the ink until it
round-trips will cost you the contrast between the ink and everything else
before it buys anything.

**No press reaches screen black.** The answer is the build, and it goes in the
guideline document rather than in the hex:

- **100% K alone** for small type and any thin element. Four plates on a
  hairline misregister and the edge goes fuzzy.
- **Rich black** for large solid areas, so they read as black rather than as
  dark grey. The printer has a house build; ask for it.

### Pantone

**Do not write a Pantone number you have not seen on paper.** Pantone's colour
data is licensed and closed, no free conversion is authoritative, and a wrong
spot colour is more expensive than no spot colour. Anything derived from a hex
is a guess wearing a specification's clothes.

What you can do is make a Pantone match possible, and it is the same work as
above: **a colour outside the CMYK gamut can never agree with its own process
build.** Get inside the gamut first. Then take the hex and its separation to a
Pantone Color Bridge guide, which prints each Pantone beside its process
equivalent, and choose under the printer's viewing light. Write the number into
the guidelines when it exists and not before.

---

## 3. It has to survive being seen differently

Two inks separated only by hue are two inks that merge for a large number of
readers, and in every process that keeps luminance and drops the rest.

**Greyscale is the blunt version and it is the one that bites.** A single print
plate, an engraving, a laser etch, a fax and a photocopy all see luminance.
Two colours of equal lightness become one colour. This is not the same as the
one-colour test in invariant 1: that one collapses every ink into a single ink
and asks whether the geometry holds. This one keeps the difference between the
inks and asks whether there was ever a difference to keep.

**Then the dichromacies.** Protanopia, deuteranopia and tritanopia together
cover most colour vision deficiency, and red against green is the pair that
collapses.

**Check:** `scripts/contrast.py` reports both. It flags a pair that merges in
greyscale, and it simulates the three dichromacies and reports how much of the
pair's separation survives — as a proportion, because a pair that starts far
apart and lands close has lost everything even when the remainder clears an
absolute floor.

**The fix is always the same: separate them by lightness.** A palette built on
lightness differences needs no accessibility exception, because every one of
these processes preserves lightness. Hue is decoration on top of it.

---

## Choosing, in the order that works

Constraint first. Aesthetics last. Reversing this is how a brand ends up with a
colour it cannot print and a redesign eighteen months later.

1. **Where does it have to work?** List the surfaces and the processes. Screen
   only is a legitimate answer and it removes half of this file — but it has to
   be a decision, not an oversight, because it is expensive to reverse.
2. **How dark and how light?** Fix the ink and the paper before the hue. These
   two carry the contrast and therefore the legibility.
3. **One accent, and only if it has a job.** An accent that marks nothing is
   decoration, and the one-colour test will remove it for you.
4. **Now pick the hue**, from monochromatic or split-complementary.
5. **Run all three checks before showing anyone.** Contrast, gamut, deficiency.
6. **If gamut fails, walk the chroma, do not change the plan.**

---

## What these checks do not measure

Required reading before quoting a number from them at anyone.

**Whether the colour is any good.** All three are floors. A palette that clears
every one of them can still be ugly, wrong for the category, or too close to a
competitor's. Nothing here has an opinion about that.

**Your press.** The gamut number comes from a generic coated-process profile.
Ink, paper, screen ruling, press condition and the operator's day all move it.
Uncoated stock moves it a great deal, and the profile does not model uncoated
at all. Re-run with the printer's profile when there is a job, and believe the
proof over any of this.

**Perceived contrast, as opposed to a luminance ratio.** WCAG's formula is a
ratio of relative luminance and it is known to be weak on dark backgrounds: a
light-on-dark pair can clear 4.5:1 and still read worse than a dark-on-light
pair at the same number. It is used here because it is the shared standard, not
because it is the last word. If a mark passes and still looks thin reversed,
trust your eyes and add weight.

**Partial colour vision deficiency.** The simulations are the three
dichromacies at full severity, which is the severe end. Anomalous trichromacy
is far more common and these overstate its effect. They also say nothing about
low vision, cataract, or the way a screen's own calibration shifts everything.
Passing is evidence, not a clearance.

**Viewing conditions.** Everything assumes a standard illuminant and a
reflective surface. A backlit sign, an LED wall, a sodium-lit car park and an
embroidered patch each behave differently, and none of them are modelled.

**What the colour means.** Category conventions, cultural associations and
whatever the nearest competitor already owns. Invariant 7 covers the last of
those and it is a person's job.

---

## Failure modes

*The gradient rescue.* Covered in `style-geometric.md` and it belongs here too.
A weak silhouette given a purple-to-pink gradient. Turn it off; if the mark
dies, the gradient was the design.

*Harmony instead of contrast.* Two colours can be perfectly harmonious and
perfectly illegible. Harmony is a hue relationship and it says nothing about
lightness. Run the numbers on any palette that came out of a wheel.

*The screen-picked accent.* Choosing on a monitor and discovering at print
time. `gamut.py` costs one second and it is the only check here that looks at
a process rather than at a person.

*Desaturating to pass.* A brand colour weakened until every check goes quiet is
a brand colour nobody will recognise. Locate the boundary and stand on it.

*Colour carrying meaning that nothing else carries.* If the only thing telling
two elements apart is that one is red, then for a single-plate print, an
engraving, a greyscale render and a protanope there is one element. Invariant 1
is the general form of this and it outranks anything in this file.
