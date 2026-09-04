# Changelog

## 0.0.4 — colour, which the skill had been treating as a risk and never as a choice

Found by using the skill on a second project. The review page put a near-black
mark on a near-black plate, presented it as a colourway, and said nothing; the
contrast there is 1.01:1.

- **`references/colour.md`.** The skill mentioned colour only as something to
  remove — do not let hue carry structure, turn the gradient off, test it in one
  ink. Correct, and half the subject. `contrast`, `WCAG`, `luminance`,
  `harmonious`, `complementary`, `analogous`, `triadic`, `monochromatic` and
  `colour blind` appeared zero times in the whole skill. The module covers the
  three questions that have answers, says why five of the seven classical
  harmony schemes are solving an interface's problem rather than a logo's, and
  ends with what the checks do not measure.
- **`scripts/contrast.py`.** WCAG contrast for every ink against every surface
  the brand named plus white, black and mid grey; a greyscale merge test, which
  is not the one-colour test and catches a different failure; and the three
  dichromacies, reported as the proportion of separation kept rather than
  against an absolute floor, because a pair that falls from dE 109 to 13 has
  lost everything while clearing any floor worth setting.
- **`scripts/gamut.py`.** Whether a press can reach the colour at all, which no
  other check here can see. Round-trips through a CMYK profile and reports
  CIEDE2000. `--find` holds the hue and walks the chroma to the boundary, so a
  failing colour gets located rather than desaturated. Skips with an install
  hint when `transicc` is absent.
- **A new invariant, at 2, and everything below it renumbered.** Contrast and
  gamut are the sibling of "the mark survives one colour" and belong beside it.
  The one reference to a moved number, in `examples/self/README.md`, moved with
  it.
- **`preview.py` reports contrast per card and adds a mid-grey band.** The dark
  panel now says what it is: the full-colour file on a dark plate, which is what
  a reader without the reversed variant will do, with the number that explains
  why `mono-light` exists. Mid grey is there because a mark that clears white
  and black can still fail it, and nobody previews it.
- **Outline before variants, in `SKILL.md` and in CI.** The documented order ran
  `variants.py` on the live-text master and `print.sh` last, so every delivered
  digital SVG carried live text and `check.py` failed all of them. The skill's
  own linter was rejecting the skill's own output. CI now runs the corrected
  order and lints what it produced.
- **CI installs `liblcms2-utils`, `icc-profiles-free` and `ghostscript`**, so the
  measured path runs there rather than the skip path, and gates on two controls:
  a colour known to be out of gamut has to be caught, and a luminance-matched
  red and green have to be reported as merging.

## 0.0.3 — the changelog stopped claiming a release that never happened

- The initial commit shipped a hand-written `0.1.0` and was never tagged. The
  entry that described it as `0.0.1` was describing a release that does not
  exist. This entry exists because 0.0.3 was itself missing from the file until
  0.0.4 went to write above it.

## 0.0.2 — governance, versioning and a manifest fix

- **WendtVer, derived from the commit count.** `scripts/version.sh` computes the
  version rather than anyone maintaining it, and CI checks it on both sides: a
  pull request must bump PATCH by exactly one, and a push to `main` must match
  the commit count exactly. The version in `plugin.json` is Claude Code's update
  key, so a stale one means installed users silently stop receiving anything.
- **A merge to `main` is a release.** The `release` job tags `v<version>` and
  generates notes. Nothing about a release is decided by hand.
- **`marketplace.json` no longer carries a `version` on its plugin entry.** That
  field pins the plugin, which made it a second update key to forget. Checked by
  `scripts/check-structure.sh` so it cannot come back.
- **`$schema` dropped from `marketplace.json`.** The URL inherited from another
  skill's manifest redirects and could not be verified to resolve. Claude Code
  ignores the field at load time, so shipping an unverified URL bought nothing.
- **Marketplace renamed to `durmazoguzhan-design`.** A user can register only one
  marketplace per name and `durmazoguzhan` already belongs to `turkish-humanify`,
  so the two would have collided on install.
- **`scripts/check-structure.sh`** asserts the layout the plugin loader expects,
  including the one that fails silently: the skill's invocation name comes from
  the `SKILL.md` frontmatter first and the directory second, so the two
  disagreeing renames the skill between installs.
- **Squash-only, protected `main`, maintainer-only merge.** `CONTRIBUTING.md`
  records the settings rather than the intention.
- **`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue and pull
  request templates** added.

## Before 0.0.2 — the initial commit, never released

Kept for the record rather than as a release. That commit carried `0.1.0`, a
number written by hand, and no release job existed yet to tag it. **v0.0.2 is
the first release** and contains everything below.

- **The skill**, five style modules and ten checkable invariants, written from
  scratch: the two strongest prior skills ship no licence file, so nothing could
  be copied from either. `NOTICE.md` records what could have been reused and was
  not.
- **Nine standalone scripts**, no API key anywhere, each degrading around a
  missing tool rather than blocking the run: `check.py`, `legibility.sh`,
  `outline.sh`, `variants.py`, `icon-extract.py`, `render.sh`, `ico.sh`,
  `print.sh`, `preview.py`.
- **The font-substitution audit**, which nothing else in the survey does.
  Text-to-path freezes the font fontconfig actually resolved, not the one the
  file names.
- **`docs/prior-art.md`**, five skills measured with the commands to reproduce
  every number.
- **`examples/self`**, a real run of the workflow including one iteration that
  changed nothing and is kept because that is also a result.
