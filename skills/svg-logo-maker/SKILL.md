---
name: svg-logo-maker
description: |
  Design a logo as hand-written SVG and deliver the whole asset set. Use when
  the user asks to "create a logo", "design a logo", "make a logo/icon/favicon",
  "brand mark", "wordmark", "monogram", "logotype", asks for a logo for a repo
  or product, wants to iterate on an existing SVG logo, or needs a logo prepared
  for print. Produces colour variants, favicons, a multi-resolution .ico, and a
  print handoff with text converted to paths. Needs no API key and no account.
license: MIT
---

# SVG Logo Maker

Draw the logo as SVG by hand, measure it, iterate on it, then ship the set a
brand handoff is actually made of.

Two commitments shape everything below. **No paid service is ever called** —
every step runs on tools the user can install for free, and any missing tool
degrades one feature rather than blocking the run. And **quality claims get
measured** wherever a measurement exists, because "this works at small sizes"
is an opinion until something renders it at 16px and reports a number.

## The shape of a run

    1  Brief      what it is for, which style, what it must survive
    2  Explore    3 to 5 genuinely different concepts, as files
    3  Measure    lint, colour, one-colour test, size test, then a review page
    4  Refine     iterate on one direction, ids stable so changes are traceable
    5  Deliver    outline, variants, icon, favicons, .ico, print, guidelines

Do not skip 3. It is the step that separates this from generating five SVGs and
hoping.

---

## 1. Brief

**Gather what is already known before asking anything.** If the user points at
a repo, read the README, `package.json`, any CSS custom properties or Tailwind
config, and any existing icon. Extract name, what it does, who it is for,
existing colours, existing type. Summarise what you found, then ask only what
is still missing.

Use `AskUserQuestion` and batch related questions. Four things decide the work:

**Format.** Icon only, wordmark only, or combination mark. If the user does not
know, ask what it has to appear on. A GitHub avatar and a favicon mean icon; a
website header and a business card mean a lockup.

**Style.** Read the matching module and follow it. One of:

| Style | Module | Fits |
|---|---|---|
| Geometric mark | `references/style-geometric.md` | software, infrastructure, dev tools |
| Wordmark | `references/style-wordmark.md` | young companies, short names, B2B |
| Monogram | `references/style-monogram.md` | long names needing a square mark |
| Emblem / badge | `references/style-emblem.md` | craft, heritage, membership, packaging |
| Mascot (geometric) | `references/style-mascot-lite.md` | consumer, community, playful |

If the user has no view, say what you would pick and why in one sentence, then
pick it. A young company with a short name should hear that a wordmark is
usually the right answer even when they came asking for a symbol.

**Colour.** Existing palette, a described mood, or your choice. Ask for the
darkest background the logo will sit on, because that decides the reversed
variant. **Ask whether it will ever be printed**, because that decides whether
the accent has to live inside the CMYK gamut, and it is much cheaper to know
now than after someone has learned the colour. `references/colour.md` has the
rest, and it is the module people skip.

**Where it has to survive.** Favicon, app icon, embroidery, signage, one-colour
print, laser engraving. This sets the constraints and it is the question nobody
asks. A logo destined for a stamp is a different drawing from one destined for
a website header.

Read `references/00-invariants.md` before writing any SVG. It applies to every
style and it is short.

---

## 2. Explore

Write 3 to 5 concepts to `logos/concepts/concept-N.svg`. Each takes a
**different creative direction**, not a different parameter value. Recolouring
the same mark four times is one concept with four fills.

Give each concept a one-line rationale when you present it, and make the
rationale about the brand rather than about the shape. "Two counters that read
as a bracket, because the product is a parser" is a rationale. "A modern
geometric mark" is not.

### SVG conventions

- `viewBox` only, no `width`/`height` on the root. 512x512 for icons and
  monograms, 1024x512 for wordmarks and lockups.
- Self-contained. No external font, no `@import`, no linked image, no `<use>`
  pointing at another file.
- Name the groups: `<g id="icon">`, `<g id="wordmark">`. Iteration depends on
  it and so does `icon-extract.py`.
- Primitives over paths wherever a primitive will do.
- Flat fills by default. A gradient has to earn its place, and the one-colour
  test in step 3 is where it gets asked to.
- Comment each element with why it is there, not what it is. `<!-- gap is the
  idea; keep it at 24 -->` survives an iteration. `<!-- circle -->` does not.
- Live `<text>` is fine here and only here. It becomes paths at delivery.

Concepts can be written one after another, or dispatched in parallel if the
host supports subagents. If dispatching, give each agent the full brief, the
conventions above, its own creative direction and its own output path, since
agents do not share context.

---

## 3. Measure

Run all of them. They take seconds and they catch what looking at a grid does
not.

    python3 scripts/check.py     --favicon-size 16 logos/concepts/*.svg
    python3 scripts/contrast.py  logos/concepts/*.svg --bg '#PAPER,#PLATE'
    python3 scripts/gamut.py     '#INK' '#ACCENT' --find
    scripts/legibility.sh        logos/concepts/concept-1.svg
    python3 scripts/preview.py   logos/concepts/ --title "Concepts"

`check.py` is a gate: external references, embedded bitmaps, live text at
delivery time, a missing viewBox and a stroke that vanishes at 16px are all
reported, and it exits non-zero on the errors.

`contrast.py` and `gamut.py` measure the palette rather than the drawing, so
they run once for the set unless the concepts disagree about colour. The first
asks whether every ink clears its background and whether the pair survives
greyscale and dichromacy; the second asks whether a press can reach the colour
at all, which nothing else here can see. Read `references/colour.md` before
acting on either.

`legibility.sh` reports two numbers per concept. *Structure kept in one colour*
below 0.25 means colour is doing the work. *Detail loss* at 16px says whether
the mark survives a favicon. Read them across concepts, not against a fixed
bar — the point is which concept holds up best.

`preview.py` writes a page with the concepts on light and on dark, the
one-colour versions, and a 64/32/16 favicon strip. Tell the user to open it,
describe each concept in one sentence, and ask which direction to take — or
what they dislike across all of them, which is often more useful.

**Report the numbers to the user.** A concept that scores 0.11 on one colour is
not disqualified, but the user should choose it knowing that its one-colour
version is a different mark.

---

## 4. Refine

Copy the chosen concept to `logos/iterations/iteration-1.svg` and work forward
from there, one file per iteration.

**Keep group ids stable across iterations.** That is what makes "make the icon
bigger" a traceable change rather than a redraw.

For a single piece of feedback, edit and write the next iteration. For
exploring several directions at once — five colour palettes, three counter
shapes — write them as consecutive iterations, or dispatch them in parallel
with the full base SVG in each prompt.

Regenerate the preview after each round:

    python3 scripts/preview.py logos/iterations/ --title "Iterations"

Say what changed in one sentence and ask for the next note. When something
stops working, "go back to iteration 4" should be an instruction you can honour,
so do not delete iterations.

Re-run the measurements whenever the geometry changes, not only at the end. A
stroke that got thinner during refinement is easier to catch now.

---

## 5. Deliver

    scripts/outline.sh logos/final.svg logos/final-outlined.svg
    python3 scripts/variants.py     logos/final-outlined.svg out/digital/ --bg
    python3 scripts/icon-extract.py logos/final-outlined.svg out/digital/icon.svg
    scripts/render.sh out/digital/final-outlined-full.svg out/digital/
    scripts/ico.sh    out/digital/icon.svg out/digital/favicon.ico
    scripts/print.sh  logos/final.svg out/print/

**Outline first, and deliver from the outlined file.** Running `variants.py`
on the live-text master puts live text into every digital SVG that ships, and
`check.py` fails all of them — invariant 10 is not a print-only rule. The
master keeps its live text and stays out of `out/`.

That produces the colour variants, the extracted square icon, the PNG ladder
from 16 to 2048, a real multi-resolution `.ico`, and the outlined SVG plus PDF
and EPS.

**Read what `print.sh` prints at the end.** Colour separation, spot colours and
rich-black decisions stay manual, because SVG has no CMYK and no tool in this
chain can do it honestly. Passing that list on to the user is part of the job.

**Then write `guidelines.md`** — the one deliverable no script produces.
Minimum size, clear space, colour values in every space the brand needs, and
misuse rules written about this specific mark. `references/print-handoff.md`
has the numbers and the structure.

### Putting it in a repository

If the user wants the logo committed: find the icon files the project already
has (`public/favicon.*`, `apple-touch-icon.png`, `pwa-*.png`, the iOS
`AppIcon.appiconset`, `manifest.json`) and replace only those. Do not add icon
files a project does not use. Branch, commit, open a PR describing what was
replaced.

---

## Tools, and what happens without them

Nothing here needs an account. The scripts detect what is installed and say
what a missing tool costs.

| Tool | Needed for | Without it |
|---|---|---|
| resvg *or* Inkscape *or* librsvg *or* ImageMagick | any PNG output | SVG generation still works; nothing rasterises |
| Inkscape | text-to-path, PDF, EPS, icon extraction | scripts refuse and say why, rather than shipping live text |
| ImageMagick | `.ico`, the legibility measurements | those two features only |
| fontconfig | the font-substitution audit | outlining proceeds unaudited |
| liblcms2-utils | the CMYK gamut check | `gamut.py` says so and skips; contrast is unaffected |

resvg is the lightest: one 4.6 MB binary from
`github.com/linebender/resvg/releases`, no dependencies. Install Inkscape as
well if the logo is going to print.

---

## Things this skill will not do

**No image generation.** No Gemini, no Recraft, no background removal service.
Nothing here needs a key.

**No auto-tracing.** A logo traced from a raster comes out as hundreds of path
nodes that nobody can edit and no printer can separate cleanly. `check.py`
flags a file shaped like one.

**No illustrated mascots.** `style-mascot-lite.md` covers characters buildable
from primitives and says plainly where its ceiling is. A drawn mascot is an
illustration commission.
