# Brand files

A regular form, interrupted once, with the interruption measured. That is the
skill's argument in one shape: its rules are not opinions, each one names a
check, and what a check returns is a margin. So the ring is not merely broken —
the gap holds a block that clears it above and below.

`guidelines.md` has the rest: minimum sizes, clear space, the colour values,
which variant belongs on which surface, and what may not be done to it. Read it
before using any of these somewhere new.

## Which file

| File | For |
|---|---|
| `logo.svg` | the default. Full colour, on light surfaces |
| `logo-reversed.svg` | dark surfaces. Still two colours: the ink becomes paper and the accent stays itself, measured at 4.26:1 on GitHub's dark background |
| `logo-mono-light.svg` | mid-tone surfaces, and anywhere the reproduction is one ink whatever you send |
| `logo-mono-dark.svg` | one plate, engraving, embossing, on a light surface |
| `icon.svg` | square, transparent. Favicons and anywhere the name is not needed |
| `avatar.svg` | square, full bleed on the plate. GitHub avatars, which are cropped to a circle |
| `favicon.ico` | seven resolutions, 16 to 256 |
| `logo.png`, `logo-dark.png` | README embedding, 1200px wide |
| `lockup-master.svg` | **the editable master.** Live text, not for delivery |
| `icon-master.svg` | the mark alone, in its own 512 field |

`lockup-master.svg` is the only file here that fails `check.py`, and it fails on
purpose: it keeps live `<text>` so the wordmark can be retyped. Everything else
is outlined.

## This is not `examples/self/`

`examples/self/` is a worked example, kept because a skill that claims a process
should be able to show one. Its brief names a different product and its numbers
document that run. It is a record and it stays one; these files are the brand.

## Regenerating

Made with this repository's own scripts. Every number in `guidelines.md` was
measured by them rather than asserted, including the two that changed the work:
the accent was chosen from inside the CMYK gamut rather than corrected into it,
and the icon's box was measured by rendering after being derived wrongly from
the arc's geometry.
