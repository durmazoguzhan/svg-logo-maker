# Prior art

Five Claude Code logo skills, read in September 2026. Every number below was
measured by running something, not read off a README.

This exists because "we looked at the alternatives" is worth nothing without
the measurements, and because anyone deciding whether to use this skill should
be able to check whether the criticism is fair.

## Eight links, five skills

The skills circulate through aggregator sites under different names. Deduplicated:

| Source | Actually |
|---|---|
| `explainx.ai/skills/rknall/...`, `awesomeskill.ai/skill/rknall-...`, `mcpmarket.com/tools/skills/svg-logo-designer` | rknall/claude-skills · `svg-logo-designer` |
| `lobehub.com/skills/sennabruno-claude-skills-svg-logo-designer` | sennabruno/claude-skills — an abridged copy of the above, 215 lines against 639 |
| `skills.re/skills/ReScienceLab/opc-skills/logo-creator` | ReScienceLab/opc-skills · `logo-creator` |

## The five

| Skill | Stars | Last push | Licence | Output |
|---|---|---|---|---|
| [op7418/logo-generator-skill](https://github.com/op7418/logo-generator-skill) | 2066 | 2026-04-15 | none declared | SVG icons, then AI showcase mockups |
| [ReScienceLab/opc-skills](https://github.com/ReScienceLab/opc-skills) `logo-creator` | 1754 (whole repo) | 2026-09-03 | Apache-2.0 | raster, then auto-traced to SVG |
| [neonwatty/logo-designer-skill](https://github.com/neonwatty/logo-designer-skill) | 79 | 2026-08-26 | MIT | SVG |
| [rknall/claude-skills](https://github.com/rknall/claude-skills) `svg-logo-designer` | 66 | 2025-10-20 | none declared | SVG |
| [sennabruno/claude-skills](https://github.com/sennabruno/claude-skills) | 1 | 2026-03-14 | none declared | SVG |

Star count and quality run in opposite directions here, which is why the survey
was done by reading the files.

---

## What each one gets right

**op7418** has the best design writing of the five. `references/design_patterns.md`
is 722 lines and carries actual rules: proportions of negative space, stroke
weight bands, single focal point, deliberate asymmetry. It is the only one of
the five that tries to encode taste rather than process.

**neonwatty** has the only serious production pipeline. Font fallbacks, a
64/32/16 favicon strip in the preview, a separate square icon extracted from the
`#icon` group for combination marks, a five-way converter fallback for PNG
export, stable group ids across iterations, tests and a CI workflow. Its
`examples/bleep-that-shit` contains 11 concepts and 37 iterations, which is real
evidence rather than a claim.

**rknall** is the only one that knows print exists. CMYK, Pantone, spot colour,
clear space, minimum sizes, reversed and monochrome variants, and a taxonomy of
seven logo types.

**ReScienceLab** is the only one that can produce a mascot or a pixel-art mark,
because it generates rasters first. It is also the most actively maintained.

---

## What each one gets wrong

### Live text in the delivered file

**rknall**, in its own worked example:

```xml
<text x="85" y="45" font-family="Arial, sans-serif" font-size="28" ...>COMPANY</text>
```

The document a few hundred lines above correctly explains spot colour and print
minimums. The example contradicts it. An SVG whose wordmark is still `<text>`
renders with whatever font resolves on the opening machine.

How bad that is, measured on a stock Ubuntu 24.04 box:

```
$ fc-match Arial
LiberationSans-Regular.ttf: "Liberation Sans" "Regular"
```

There is no Arial. Anything outlining that file freezes Liberation Sans.

### A traced bitmap presented as a vector logo

**ReScienceLab**'s pipeline is Gemini → 20 rasters → crop → remove.bg →
Recraft vectorise. Its own committed final output, `examples/images/opc-logo-final.svg`:

| | |
|---|---|
| size | 17 959 bytes |
| `<path>` elements | 41 |
| path nodes | ~500 |
| primitives (`circle`, `rect`, …) | 0 |
| named groups | 0 |

That is the shape of a trace, not a drawing. It cannot be recoloured by hand,
cannot be separated cleanly, and no designer will edit it.

### Nobody measures anything

**neonwatty**'s own `iteration-37.svg` uses `stroke-width="4"` in a 512
viewBox. At a 16px favicon that is:

```
4 × (16 / 512) = 0.125 device pixels
```

The skill's own guidance says to use 6 or more. Its favicon strip would have
shown a person the problem, if a person looked. Nothing computes it.

The same file, run through this repository's one-colour test:

```
colour dependence  structure kept in one colour: 0.07
```

Seven percent of its internal structure is geometric; the rest is hue. For an
app icon on a coloured plate that is a legitimate choice — but it should be a
choice, and no skill in the survey surfaces it.

### A recommended install command for a package that does not exist

**neonwatty**'s `scripts/export.sh` tries `npx --yes @aspect-build/resvg`, and
its failure message tells the user to run
`npm install -g @aspect-build/resvg (recommended)`.

```
$ curl -o /dev/null -w '%{http_code}' https://registry.npmjs.org/@aspect-build%2fresvg
404
```

The real packages are `resvg`, `@resvg/resvg-js` and `@resvg/resvg-js-cli`. The
branch fails silently because four other fallbacks catch it, so the bug is
invisible until every fallback is missing — which is exactly the machine the
install message was written for.

### Paid API keys

| Skill | Keys required |
|---|---|
| ReScienceLab | `GEMINI_API_KEY`, `REMOVE_BG_API_KEY`, `RECRAFT_API_KEY` |
| op7418 | `GEMINI_API_KEY`, for the showcase phase |
| neonwatty, rknall, sennabruno | none |

### Gaps common to all five

None of the five produces a `.ico`, a one-colour variant, a reversed variant,
or a PDF/EPS print handoff. None converts text to paths. None checks a font
licence. None measures small-size survival numerically.

op7418 additionally produces no wordmarks at all — the string `<text>` does not
appear anywhere in the skill — and its final phase generates marketing mockups
rather than deliverables.

---

## Licences, and what that meant here

op7418 and rknall ship **no licence file**, so the default is all rights
reserved and their text could not be copied into an MIT repository regardless
of how good it is. op7418's design doctrine is the strongest single artefact in
the survey and none of it is in this repository; `references/00-invariants.md`
was written from scratch, organised around checks rather than principles.

neonwatty (MIT) and ReScienceLab (Apache-2.0) could have been reused. They were
not, but two ideas here come from neonwatty and are named in
[`../NOTICE.md`](../NOTICE.md): the favicon size strip, and detecting a
converter rather than requiring one.

## Reproducing this

Everything above is a few commands. Clone the repositories, then:

```bash
python3 skills/svg-logo-maker/scripts/check.py <their-example>.svg
skills/svg-logo-maker/scripts/legibility.sh <their-example>.svg
fc-match Arial
curl -o /dev/null -w '%{http_code}\n' https://registry.npmjs.org/@aspect-build%2fresvg
```

If any of it is wrong, open an issue and it gets corrected.
