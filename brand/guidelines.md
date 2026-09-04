# svg-logo-maker — logo guidelines

Every number below is derived from the drawing and the type, and the derivation
is shown so you can check it or change the input and redo it. Where a number
was measured by rendering rather than calculated, it says so.

---

## What the mark says

A regular form, interrupted once, with the interruption measured.

That is the argument of the whole skill in one shape. Its rules are not
opinions; each one names a check and returns a number, and the thing a check
returns is a margin. So the ring is not merely broken — the gap holds a block
that clears it above and below, because a margin nobody measured is a margin
being guessed at.

Interrupting a regular series only works when the interruption is obviously
deliberate. This one is 44 degrees. At half that it would read as a rendering
slip.

**It is drawn once and used at every size.** There is no simplified small
variant, because the ring's wall is 1/5.5 of the mark's width and survives a
16px favicon at 2.9 device pixels.

---

## Files

    brand/
      logo.svg                 primary lockup, full colour, for light surfaces
      logo-reversed.svg        full colour for dark surfaces: the ink becomes
                               paper and the accent stays itself
      logo-mono-dark.svg       one ink, dark, single plate and engraving
      logo-mono-light.svg      one ink, reversed, for mid-tone surfaces
      icon.svg                 square icon, transparent, for favicons
      avatar.svg               square, full bleed on the plate, for a circle crop
      favicon.ico              7 resolutions, 16 to 256
      logo.png, logo-dark.png  1200px wide, for README embedding
      icon-*.png, avatar-*.png
      lockup-master.svg        the editable master, live text, not for delivery
      icon-master.svg          the mark alone, in its own 512 field

The print set (outlined SVG, PDF, EPS) is derived and large, so it is
regenerated on demand rather than committed. The command is at the bottom.

`lockup-master.svg` is the only file that fails the linter, and it fails on one
rule for one reason: it keeps live `<text>` so the wordmark stays editable.
Everything shipped is outlined.

---

## Type

**Lato Bold (700)**, SIL Open Font License 1.1, which permits outlining and
embedding in a mark. On the machine that built this, `fc-match Lato` resolved
to Lato itself, so the outlined paths are Lato and not a substitute. Check that
on any machine that regenerates these: outlining freezes whatever fontconfig
resolved, not what you asked for.

Set at font-size 128 in a 1366-unit lockup, tracking unchanged.

The wordmark carries no device. The mark does the work and the name is set
plainly, which is the right division when the name is long.

---

## Construction

Two relationships hold the lockup together and both answer to the type rather
than to the canvas:

- **Icon height = 2 cap heights.**
- **Gap between icon and wordmark = 1 cap height.**

The icon's box was **measured by rendering, not derived from the arc**. A
stroked path's bounds are not its geometry's: the first attempt computed them
from the centre and radius, placed the icon 137 units off, and put the ring on
top of the letter s.

The same round of work produced the other bug worth recording. The arc was
written with `A 144 144 0 1 0`, and with sweep 0 the arc is computed around the
far centre, so the ring left the canvas entirely and rendered as a fragment.
The flag is 1.

---

## Minimum size

Derived from the smallest element that has to survive, then confirmed by
rendering.

**Icon.** The thinnest element is the ring's wall: 64 units of the mark's 352,
which is 1/5.5.

| | minimum | the wall lands at |
|---|---|---|
| screen | **16 px** wide | 2.9 px |
| print | **8 mm** wide | 1.45 mm |

Detail loss at 16px measures 0.033, which is the best of any concept drawn for
this project. A chunky ring is what buys that; it is not a compliment to the
idea.

**Lockup.** Governed by the wordmark. Cap height is 92.16 of the lockup's 1366
width, which is 1/14.8.

| | minimum | cap height lands at |
|---|---|---|
| screen | **140 px** wide | 9.4 px |
| print | **30 mm** wide | 2 mm |

Checked by rendering rather than by arithmetic alone: at 110px the wordmark
crowds and the accent block drops to a speck. At 140px both hold.

---

## Clear space

Expressed as a ratio so it scales.

**Lockup:** one cap height on all four sides, which is 1/14.8 of the lockup's
width. At 800px wide that is 54px.

**Icon:** one quarter of the icon's width on all four sides.

Nothing enters that space. Not a border, not a tagline, not another logo.

---

## Colour

| role | hex | RGB | L\*a\*b\* | where it is authoritative |
|---|---|---|---|---|
| ink | `#14171A` | 20, 23, 26 | 7.52, −0.79, −2.64 | screen |
| accent | `#108864` | 16, 136, 100 | 50.15, −38.74, 10.35 | screen |
| paper | `#FAF7F2` | 250, 247, 242 | 97.36, 0.39, 2.78 | screen |

The ink and the paper are shared with
[turkish-humanify](https://github.com/durmazoguzhan/turkish-humanify); only the
accent differs. The two accents sit at the same lightness on purpose, so the
pair reads as one family at one tonal weight. They are never adjacent inside a
mark, so the 1.09:1 between them is not a contrast failure — each mark's
internal contrast is 4:1 or better and that is the number that governs.

### The accent was chosen by the press, not by the screen

Picked from inside the CMYK gamut rather than corrected into it afterwards.
The whole hue circle was measured for colours that clear 3:1 against **both**
paper and the brand plate and round-trip under ΔE2000 1.0; `#108864` came out
of that set, at L\* 50 where the two contrasts balance at 4.16 and 4.05.

Round trip: **ΔE2000 0.25 — prints as itself.** Measured against Ghostscript's
*Artifex CMYK SWOP* profile, which represents coated process printing but is
not FOGRA39 and is not your printer's. Re-run `gamut.py` with theirs when there
is a job.

Deep blue was measured too and rejected without measurement deciding it: it
clears everything and it is what every developer tool already looks like.

### The ink is a substrate limit, not a bad choice

`#14171A` round-trips at ΔE 6.32 and no adjustment fixes that honestly. Coated
process bottoms out near L\* 18; screen black is L\* 0. **No press reaches
screen black.** The answer is the build, not the colour:

- **100% K alone** for the wordmark at small sizes and any thin element.
- **Rich black** for large solid areas. Ask the printer for their house build.

### Pantone

**None is specified, and one cannot be specified from here.** Pantone's data is
licensed and closed; a number written from memory is a guess wearing a
specification's clothes.

What has been done is the part that makes a match possible: a colour outside
the CMYK gamut can never agree with its own process build, so the spot and the
four-colour versions would differ on every job. `#108864` is inside it. To
finish, take it and its separation to a **Pantone Color Bridge** guide and
choose under the printer's light, then write the number into this table.

**CMYK is the printer's to derive.** The SWOP separation measured here is
`90/24/79/10` for the accent and `76/68/64/89` for the ink; a ranking, not a
specification.

### Which variant on which surface

Measured with WCAG contrast, floor 3:1 for a graphic.

| surface | `logo` | `logo-reversed` | `logo-mono-light` |
|---|---|---|---|
| paper `#FAF7F2` | **4.16:1** ✓ | 1.00 ✗ | 1.00 ✗ |
| white | **4.44:1** ✓ | 1.07 ✗ | 1.07 ✗ |
| brand plate `#14171A` | 1.00 ✗ | **4.05:1** ✓ | **16.84:1** ✓ |
| GitHub dark `#0D1117` | 1.05 ✗ | **4.26:1** ✓ | **17.71:1** ✓ |
| black | 1.17 ✗ | **4.73:1** ✓ | **19.65:1** ✓ |
| mid grey `#808080` | 1.12 ✗ | 1.12 ✗ | **3.70:1** ✓ |

**On dark, prefer `logo-reversed`.** It clears 3:1 on every dark surface
measured and it keeps the accent, which the one-ink version throws away. Fall
back to `logo-mono-light` for mid-tone surfaces and anywhere the reproduction
is one ink whatever you send.

### Colour vision

The two inks are separated by lightness rather than hue, so the mark survives
dichromacy: the closest pair keeps 81% of its separation under protanopia and
72% under deuteranopia. It holds in greyscale at 4.05:1, which is what a single
plate, an engraving and a fax all see.

---

## Misuse

1. **Do not close the gap.** The interruption is the mark. A complete ring is a
   different and much emptier idea.
2. **Do not make the gap smaller.** At half of 44 degrees it stops reading as a
   decision and starts reading as a rendering error.
3. **Do not let the block fill the gap.** The clearance above and below it is
   the point: something was measured rather than assumed.
4. **Do not rotate it.** The gap sits on the right, where the eye leaves the
   mark and enters the name.
5. **Do not put `logo.svg` on a dark or mid-tone surface.** Measured at 1.00:1
   and 1.12:1. Use `logo-reversed.svg` on dark and `logo-mono-light.svg` on
   mid-tone.
6. **Do not reset the wordmark in another face**, and do not add a tagline
   inside the clear space.
7. **Do not add a stroke, shadow, gradient or bevel.** The silhouette carries
   the mark in one ink, which is the property all of those destroy.
8. **Do not use the lockup where a square is wanted.** Use `avatar.svg`.

---

## Regenerating

`$S` is the `skills/svg-logo-maker/scripts` directory of this repository. Run
from the repository root after editing `brand/lockup-master.svg`.

    S=skills/svg-logo-maker/scripts
    python3 $S/check.py --favicon-size 16 brand/lockup-master.svg
    bash    $S/outline.sh brand/lockup-master.svg /tmp/outlined.svg
    python3 $S/variants.py /tmp/outlined.svg /tmp/v \
            --dark '#14171A' --light '#FAF7F2'
    cp /tmp/v/outlined-full.svg       brand/logo.svg
    cp /tmp/v/outlined-mono-dark.svg  brand/logo-mono-dark.svg
    cp /tmp/v/outlined-mono-light.svg brand/logo-mono-light.svg
    python3 $S/icon-extract.py /tmp/outlined.svg brand/icon.svg
    bash    $S/ico.sh brand/icon.svg brand/favicon.ico

    # variants.py offers one ink or a plate and nothing between, so the
    # two-colour reversed lockup is made by swapping the ink for the paper.
    sed 's/#14171[Aa]/#FAF7F2/g' brand/logo.svg > brand/logo-reversed.svg

    resvg --width 1200 brand/logo.svg          brand/logo.png
    resvg --width 1200 brand/logo-reversed.svg brand/logo-dark.png
    for s in 512 256 128 64; do
      resvg --width $s --height $s brand/avatar.svg brand/avatar-$s.png
    done

Then re-run the gates, all of which have to come back clean:

    python3 $S/check.py --favicon-size 16 brand/logo*.svg brand/icon.svg brand/avatar.svg
    python3 $S/contrast.py brand/logo.svg --bg '#FAF7F2'
    python3 $S/contrast.py brand/logo-reversed.svg --bg '#14171A,#0D1117'
    python3 $S/gamut.py '#14171A' '#108864'
    bash    $S/legibility.sh brand/icon.svg

For print, which is derived and not committed:

    bash $S/print.sh brand/lockup-master.svg out/print/

**Outline before variants, not after.** Running `variants.py` on the live-text
master puts live text into every delivered SVG and `check.py` fails all of them.

---

## A note on how this one was drawn

Eleven concepts were drawn and measured before this one, across two rounds. The
measurements eliminated none of them: every concept passed the linter, the
one-colour test and the size test. **Every elimination came from invariant 7,
by eye**, and each one has a name — hamburger menu, scan frame, record button,
laptop, power button, the letter C, play button, stop button, window collapse.

That is worth recording because it is a property of the space and not bad luck.
Simple arrangements of two or three primitives are almost all occupied by forty
years of interface iconography, and a logo tool's own logo sits squarely in
that space. What escapes it is not the simple form but the specific one.

The first round's concepts were also, correctly, called out as looking like
they were drawn in Paint. That is a real defect in this skill's doctrine:
`style-geometric.md` prefers primitives to paths, the invariants all push
toward chunky gap-separated forms, and `legibility.sh` rewards big simple
blocks over finely drawn ones. Nothing in the skill is about drawing well. The
gap is written up in the pull request that brought this logo in.
