# Print handoff

What a printer needs, what this repository can produce, and what stays manual.
The last part is short and it is the part that gets skipped.

---

## What the scripts produce

    scripts/print.sh logo.svg handoff/

An outlined SVG, a PDF and an EPS, all RGB, with the font audit printed first.
The outlined file is a delivery artefact and never your master.

## What stays manual, and why no script here does it

**Colour separation.** SVG has no CMYK. There is no colour space in the format,
no ICC profile attachment that printers honour, and every tool in this chain
outputs RGB. Converting in a vector editor with the printer's profile is the
only correct route. A script that silently mapped RGB to CMYK would produce
numbers that look like an answer and are not.

**Spot colours.** If the brand owns Pantone numbers, they go in the guideline
document as numbers. A hex value converted to CMYK is an approximation that
moves between presses, papers and days. Two-colour and one-colour spot versions
should be named explicitly, not derived.

**Rich black against 100K.** Large solid areas want a rich black built from
several plates. Small text and thin rules want 100% K alone, because four
plates on a hairline misregister and the edge goes fuzzy. This is a per-element
decision.

**Overprint and trapping.** The printer's problem, but they need to be told
which elements are which.

---

## Numbers the guideline document has to state

**Minimum size.** Give it in both units and derive it rather than guessing.
Take the smallest element that must remain visible, decide how many
millimetres or pixels it needs, and scale the whole mark from that.

A defensible starting point for a mark with no element thinner than 1/20 of its
width: 20mm wide for print, 24px for screen. A wordmark is governed by its
smallest letter, so it is usually larger.

**Clear space.** Express it as a fraction of the mark, never as an absolute,
so it scales. A standard that holds up: clear space equals the height of the
mark's dominant element — the cap height for a wordmark, the icon height for a
lockup. If you built on the grid in `style-geometric.md`, the 64-unit margin
around a 384 mark in a 512 viewBox is already your clear space.

**Colour values, all of them.** Hex for screen, RGB for screen, CMYK for
process print, Pantone for spot, and a note saying which is authoritative. It
is usually the Pantone.

---

## The deliverable set

    logo/
      master/                 editable, live text, do not ship
        logo.svg
      digital/
        logo-full.svg         primary lockup, colour
        logo-mono-dark.svg    one colour, for light backgrounds
        logo-mono-light.svg   reversed, for dark backgrounds
        icon.svg              square, extracted
        favicon.ico           multi-resolution
        logo-{16..2048}.png
      print/
        logo-outlined.svg     text as paths
        logo.pdf
        logo.eps
      guidelines.md           minimum size, clear space, colour values, misuse

Everything above `guidelines.md` is produced by:

    python3 scripts/variants.py master/logo.svg digital/ --bg
    python3 scripts/icon-extract.py master/logo.svg digital/icon.svg
    scripts/render.sh digital/logo-full.svg digital/
    scripts/ico.sh digital/icon.svg digital/favicon.ico
    scripts/print.sh master/logo.svg print/

---

## Misuse rules worth writing down

Every guideline document lists these and every one of them exists because
somebody did it: do not stretch, do not recolour outside the palette, do not
add effects, do not rotate, do not place on a busy photograph without a clear
field, do not rebuild the lockup with different spacing, do not use the full
emblem below its stated minimum.

Write them as sentences about your specific mark rather than as a generic list.
"The icon and the wordmark are one object; do not re-space them" is a rule
somebody can follow. "Maintain brand integrity" is not.
