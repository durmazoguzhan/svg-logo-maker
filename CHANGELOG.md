# Changelog

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

## 0.0.1 — initial release

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
