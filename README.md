# svg-logo-maker

A Claude Code skill that designs logos as hand-written SVG and delivers the
whole asset set: colour variants, a square icon, favicons, a real
multi-resolution `.ico`, and a print handoff with the text converted to paths.

**No API key, no account, no paid service.** Every step runs on free tools, and
a missing tool costs one feature instead of blocking the run.

## Why another one

Five logo skills already exist for Claude Code. They were read, measured and
written up in [`docs/prior-art.md`](docs/prior-art.md). The short version:

- Two of them produce **live `<text>` in the delivered file**, which renders
  with whatever font the opening machine happens to resolve.
- One produces a **traced bitmap** — its own example output is 41 paths and
  ~500 nodes, uneditable and impossible to separate cleanly for print.
- **None** produces a `.ico`, a one-colour variant, or a reversed variant.
- **None** measures anything. Small-size legibility is checked by looking at a
  grid, which is how a stroke that computes to 0.12 device pixels at 16px ends
  up shipped.
- Three of the five need paid API keys.

This one closes those gaps and states plainly what it still cannot do.

## What it adds

**A font-substitution audit before outlining.** Text-to-path freezes the font
*fontconfig actually resolved*, not the one the file names. Ask for Arial on a
machine without Arial and you outline Liberation Sans, the metrics match, and
the letterforms are wrong.

```
$ scripts/outline.sh wordmark.svg
Font audit — what this machine would freeze:
  Arial                        -> Liberation Sans   <-- SUBSTITUTED
```

**A one-colour test that is a number.** Count the internal edges in the
full-colour render, count them again in one colour, divide. Colour is allowed
to carry meaning; it is not allowed to carry structure.

```
colour dependence  structure kept in one colour: 0.07
  -- colour is doing the work; the one-colour version is a different mark
```

**A linter that gates delivery.** External references, embedded bitmaps, live
text, missing viewBox, and strokes that vanish at 16px — computed, not eyeballed.

**The variants a handoff is actually made of.** One-colour dark, one-colour
light (reversed), plated versions, extracted square icon, PNG ladder,
multi-resolution `.ico`, outlined SVG, PDF, EPS.

**A design doctrine split into invariants and styles.** Ten style-agnostic
rules, each with a named check, plus separate modules for geometric marks,
wordmarks, monograms, emblems and geometric mascots — so the skill does not
push every brand toward the same minimal-geometric house style.

## Install

```bash
/plugin marketplace add durmazoguzhan/svg-logo-maker
/plugin install svg-logo-maker
```

Or copy `skills/svg-logo-maker/` into `.claude/skills/` in any project.

Then just ask: *"design a logo for this repo"*.

## Tools

Nothing is mandatory. The scripts detect what exists and say what is missing.

| Tool | Gives you | Install |
|---|---|---|
| **resvg** | PNG rendering (lightest option) | one 4.6 MB binary from [releases](https://github.com/linebender/resvg/releases) |
| **Inkscape** | text-to-path, PDF, EPS, icon extraction | `apt install inkscape` · `brew install inkscape` |
| **ImageMagick** | `.ico`, the legibility measurements | `apt install imagemagick` · `brew install imagemagick` |
| **fontconfig** | the font-substitution audit | usually already present on Linux |

Install resvg and Inkscape and everything works.

## Scripts

Each runs standalone, so they are useful outside the skill too.

| Script | Does |
|---|---|
| `check.py` | lint an SVG logo; exits non-zero on errors |
| `legibility.sh` | one-colour dependence and detail loss at small sizes |
| `variants.py` | full colour, one-colour dark, one-colour light, plated |
| `icon-extract.py` | lift `<g id="icon">` into a standalone square SVG |
| `render.sh` | PNG ladder at any set of widths |
| `ico.sh` | multi-resolution `.ico` from a square SVG |
| `outline.sh` | text to paths, with the font audit first |
| `print.sh` | outlined SVG + PDF + EPS, and what stays manual |
| `preview.py` | review page: light, dark, one-colour, favicon strip |

## What it will not do

**No image generation and no auto-tracing.** Both produce files that cannot be
edited or separated for print.

**No illustrated mascots.** The mascot module covers characters buildable from
primitives and says where its ceiling is.

**No CMYK.** SVG has no CMYK, and neither does any tool in this chain. The
separation happens in a vector editor against the printer's profile, and
`print.sh` says so instead of pretending.

## Licence

MIT. Prior art and licence status of the skills surveyed:
[`NOTICE.md`](NOTICE.md).
