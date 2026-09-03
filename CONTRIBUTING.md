# Contributing

Contributions are welcome. This file is short on ceremony and long on the two
things that are unusual here: what a claim in this repository has to be backed
by, and how the version works.

## The one rule that matters

**Do not add a design rule without saying how it is checked.**

Every entry in `references/00-invariants.md` names either a script that decides
it or a test a person can run and get the same answer twice. That is deliberate:
a design rule nobody can check is a preference, and a document full of
preferences is what every other logo skill already is.

If your rule cannot be checked yet, one of two things is true. Either it belongs
in a style module, where taste is the point and the module says so; or the
checking script is the actual contribution and the rule comes with it.

## The second rule

**Do not add a measurement without saying what it does not measure.**

Both metrics in `legibility.sh` were wrong on the first attempt and both were
caught by running them on this repository's own logo:

- *Colour dependence* scored 1.00 on a mark drawn in a single ink. True, and
  worthless. The script now names that case instead of letting it read as a
  good score.
- *Detail loss* was computed over the whole canvas, which rewards a small mark
  on a big empty field for being mostly empty. It now crops to the mark's own
  bounding box first.

A number that is right for the wrong reason is worse than no number, because it
gets quoted. If you add a metric, add the degenerate input that breaks it and
say what the script does about it.

## No paid services, ever

A pull request that introduces a dependency on an API key will be declined, and
this is the project's whole reason to exist. Three of the five skills surveyed
in `docs/prior-art.md` need one.

New tools are fine if they are free, installable and optional. Follow the
pattern in `scripts/lib.sh`: detect, degrade, and say what the missing tool
costs. A tool that stops the run when it is absent needs a good argument.

## Testing a script

Run it against real logos, including the ones in `docs/prior-art.md`. Every
claim in that document is reproducible with the commands at the bottom of it,
and a change that alters those numbers should update them in the same pull
request.

`examples/self` is the end-to-end fixture. If your change breaks it, that is CI
working.

## How a change lands

**Squash is the only merge method, and merging is the maintainer's alone.**
Reviewing is not: anyone can review a pull request here and anyone can approve
one. The repository is public and approving needs only read access. What is
restricted is the button, and only that.

The settings that hold this up, so a future disagreement is with a
configuration rather than with a paragraph:

| setting | state |
|---|---|
| merge commit / rebase merge | **disabled** on the repository |
| squash merge | the only option |
| `main` | protected: pull request required, linear history, no force push, no deletion |
| required status check | `check`, strict |
| required approving reviews | **0**, deliberately — requiring one would block the sole maintainer from merging their own work, since GitHub does not allow self-approval |
| required conversation resolution | on |
| `enforce_admins` | on; the maintainer goes through a pull request too |
| write access | the maintainer only. On a personal repository GitHub offers no "restrict who can push" list, so this is a matter of not granting `write` rather than a switch |

Branches are deleted automatically once merged.

### One pull request is one commit is one PATCH

This follows from squash-only and it is not a convention, it is arithmetic.
[WendtVer](https://wendtver.org) makes the version the commit count, and a
squash merge adds exactly one commit to `main` however many the branch carries.
So **a pull request bumps PATCH by exactly one no matter how much work is in
it.**

`scripts/version.sh --write` computes the version from the base branch rather
than from your own HEAD, which is the part that is easy to get wrong: a
four-commit branch whose version came from its own HEAD carries a bump of four,
and a gate that only asks "did the version move forward" passes it. CI checks
for equality.

## Versioning

[WendtVer](https://wendtver.org): start at 0.0.0, every commit increments PATCH,
PATCH rolls to 0 at ten and increments MINOR, MINOR rolls to 0 at ten and
increments MAJOR. The version is the commit count written one digit at a time.

SemVer is not used because a skill has no contract to break. There is no API
whose removal is a MAJOR event and no addition that is a MINOR one, so a scheme
claiming to encode severity would be encoding a guess.

The version in `.claude-plugin/plugin.json` is not decoration. Claude Code uses
it as the update key and **skips the update when it matches what the user
already has**, so a stale version means installed users silently never receive
anything.

`marketplace.json` deliberately carries no `version` on its plugin entry. That
field pins the plugin, which would make it a second place to forget. One update
key, in one file, derived from the commit count.

Before you commit:

```bash
scripts/version.sh --write
```

## Checks

```bash
./scripts/check-structure.sh                      # layout the plugin loader expects
./scripts/version.sh --check                      # version against the commit count
python3 skills/svg-logo-maker/scripts/check.py examples/self/logos/final-icon.svg
```

All of them run in CI, plus an end-to-end run of the delivery pipeline on a
clean runner. That last one exists because every script here degrades around
missing tools, and the degradation paths are exactly what a developer machine
with everything installed never exercises.

## Scope

This produces vector logos. Pull requests that add image generation,
auto-tracing or an illustration pipeline will be declined; `README.md` says why
in "What it will not do", and forking is the better outcome if you disagree.
