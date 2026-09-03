## What this changes

<!-- One or two sentences. If it changes what the skill produces, say which
     phase and which file. -->

## How it is checked

<!-- Required if this adds or changes a rule in
     skills/svg-logo-maker/references/ or a metric in legibility.sh.

     Rules here name their check: a script that decides them, or a test two
     people would answer the same way. See CONTRIBUTING.md.

     If you are adding a metric, say what it does NOT measure, and add the
     degenerate input that breaks it. Both existing metrics were wrong on the
     first attempt in exactly that way. -->

-

## Checklist

- [ ] `scripts/version.sh --write` run, version bumped by one
- [ ] `./scripts/check-structure.sh` passes
- [ ] Scripts run against a real logo, not only against a synthetic one
- [ ] No new dependency on a paid service or an API key
- [ ] If a new tool is used: detection and graceful degradation added to
      `scripts/lib.sh`, and the README tool table updated
- [ ] If a number in `docs/prior-art.md` or `README.md` moved, it is updated here
