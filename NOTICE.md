# Prior art and attribution

This skill was written after reading five existing Claude Code logo skills. No
text was copied from any of them. What was taken is the shape of the problem:
which steps a logo workflow needs, and which ones each of those five left out.

The survey that produced this skill is in [`docs/prior-art.md`](docs/prior-art.md),
including the measurements behind each claim.

## Licence status of the skills surveyed

| Skill | Licence | What we could have reused |
|---|---|---|
| [neonwatty/logo-designer-skill](https://github.com/neonwatty/logo-designer-skill) | MIT | Reusable with attribution. We reimplemented instead, but the favicon size-check idea and the converter-fallback idea both come from here. |
| [ReScienceLab/opc-skills](https://github.com/ReScienceLab/opc-skills) (`logo-creator`) | Apache-2.0 | Reusable with attribution. Not reused: its pipeline is image-generation first and needs three paid API keys. |
| [op7418/logo-generator-skill](https://github.com/op7418/logo-generator-skill) | **none declared** | Nothing. With no licence file the default is all rights reserved, so its `design_patterns.md` could not be copied into an MIT repository. The design doctrine here was written from scratch. |
| [rknall/claude-skills](https://github.com/rknall/claude-skills) (`svg-logo-designer`) | **none declared** | Nothing, same reason. Its print vocabulary (clear space, spot colour, reversed variants) is standard brand-identity practice and is documented independently here. |
| [sennabruno/claude-skills](https://github.com/sennabruno/claude-skills) (`community/svg-logo-designer`) | none declared | Nothing. It is an abridged copy of the rknall skill. |

If you are one of these authors and you think something here crosses a line,
open an issue and it comes out.
