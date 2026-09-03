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

### As a plugin (recommended)

Two commands in Claude Code. The first registers this repository as a
marketplace, the second installs the plugin from it.

```
/plugin marketplace add durmazoguzhan/svg-logo-maker
/plugin install svg-logo-maker@durmazoguzhan-design
```

Then start a new session and ask for a logo. The skill triggers on phrases like
*"design a logo for this repo"*, *"make me a favicon"*, *"I need a wordmark"*.

Updates arrive when the version in `.claude-plugin/plugin.json` changes, which
happens on every merge, because the version is the commit count. To pull one:

```
/plugin marketplace update durmazoguzhan-design
```

### As a plain skill

If you would rather not install a plugin, copy the skill directory into any
project:

```bash
git clone https://github.com/durmazoguzhan/svg-logo-maker /tmp/slm
mkdir -p .claude/skills
cp -r /tmp/slm/skills/svg-logo-maker .claude/skills/
```

It works the same way. You lose only the update path.

### Reading it before you install

It is plain text and short: `skills/svg-logo-maker/SKILL.md` is the whole
workflow in about 230 lines, `references/00-invariants.md` is the design
doctrine, and the longest script is under 200 lines. A skill is instructions
your assistant will follow and this one also ships scripts it will offer to
run, so reading first is reasonable. See [`SECURITY.md`](SECURITY.md).

### Then the tools it drives

None are mandatory, but see [Tools](#tools) below: with none of them installed
you get SVG files and nothing rendered.

## Tools

The scripts detect what exists and say what a missing one costs.

| Tool | Gives you | Without it |
|---|---|---|
| **resvg** | PNG rendering, and the safest renderer here: no script execution, no external resource loading | falls through to Inkscape, then librsvg, then ImageMagick |
| **Inkscape** | text-to-path, PDF, EPS, icon extraction | those four refuse and say why, rather than shipping live text to a printer |
| **ImageMagick** | `.ico`, and the legibility measurements | those two features only |
| **fontconfig** | the font-substitution audit | outlining proceeds unaudited |

Debian or Ubuntu:

```bash
sudo apt-get install -y inkscape imagemagick
curl -sL https://github.com/linebender/resvg/releases/latest/download/resvg-linux-x86_64.tar.gz \
  | tar xz -C /tmp && sudo install -m755 /tmp/resvg /usr/local/bin/resvg
```

macOS:

```bash
brew install inkscape imagemagick resvg
```

Check what got picked up:

```bash
$ skills/svg-logo-maker/scripts/render.sh examples/self/logos/final.svg /tmp/out 512
  final-512.png                6103 bytes
rendered with: resvg
```

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

## Contributing

Pull requests are welcome and [`CONTRIBUTING.md`](CONTRIBUTING.md) is worth
reading first, because two of its rules are unusual: a design rule has to name
how it is checked, and a metric has to name what it does not measure. Both of
this repository's metrics were wrong on the first attempt in exactly that
second way.

Anyone can review and approve a pull request. Merging is the maintainer's, the
merge is always a squash, and one pull request is one commit is one PATCH.

## Versioning

[WendtVer](https://wendtver.org) — the version is the commit count, computed by
`scripts/version.sh` and enforced by CI rather than maintained by hand. Every
merge to `main` tags a release. [`CHANGELOG.md`](CHANGELOG.md) says what moved.

## Licence

MIT. Prior art and licence status of the skills surveyed:
[`NOTICE.md`](NOTICE.md). Conduct: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
Vulnerabilities: [`SECURITY.md`](SECURITY.md).
