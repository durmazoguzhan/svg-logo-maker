# Security

## What this project is

`svg-logo-maker` is a set of Markdown instruction files plus nine small scripts.
Installing it copies those files into a skills directory; using it means a model
reads the Markdown and, when you agree, runs the scripts on files in your
working directory.

That second half is the difference from a pure prose skill and it shapes the
threat model. The scripts shell out to `inkscape`, `resvg`, `rsvg-convert`,
`fc-match` and ImageMagick, and they take file paths from the conversation.

The plausible risks:

- **Prompt injection through the reference files.** A change that lands
  instructions unrelated to logo design would be executed by every user the
  next time a model reads the file. This is the one that matters most.
- **Argument injection into a rendering tool.** A crafted filename reaching a
  script's `$1` reaches a subprocess. The scripts quote their variables; a
  place where one does not is a real finding.
- **A malicious SVG.** SVG is a programmable format. The renderers here are
  the mitigation, not this project: `resvg` executes no script and loads no
  external resource, which is one reason it is first in the detection order.
  `check.py` reports external references and embedded rasters as errors partly
  for this reason.
- **Workflow injection** in `.github/workflows/`, via untrusted input such as a
  pull request title or branch name interpolated into a `run:` block.

## Reporting

Report privately through GitHub's **Report a vulnerability** button on the
Security tab of <https://github.com/durmazoguzhan/svg-logo-maker>, which opens a
private advisory.

Please do not open a public issue for anything you believe is exploitable.

Include what you found, the file and line, and what an attacker gets. A working
reproduction helps but is not required; a clear description of the mechanism is
enough.

I maintain this in my own time, so I will not promise a response window I cannot
keep. I will acknowledge what I receive and say plainly if I am not going to act
on it.

## Scope

**In scope**

- Instructions in `skills/svg-logo-maker/` that do anything other than describe
  or perform logo design.
- Any script in `skills/svg-logo-maker/scripts/` where an attacker-controlled
  path, filename or SVG attribute reaches a shell.
- Anything in `.github/workflows/` that lets untrusted input reach a shell.
- A `plugin.json` or `marketplace.json` that would cause Claude Code to fetch
  from somewhere other than this repository.

**Out of scope**

- The skill producing a logo you do not like. That is a quality issue; open a
  normal issue.
- Vulnerabilities in Inkscape, ImageMagick, librsvg or resvg. Report those
  upstream. If this project invokes one of them in a way that widens the
  exposure, that part is in scope.
- Behaviour of Claude Code itself. Report that to Anthropic.

## For users installing this

Two things worth knowing regardless of this project:

1. A skill is instructions your assistant will follow, and this one also ships
   scripts it will offer to run. Read them before installing. Everything is
   plain text and deliberately short; `SKILL.md` is about 230 lines and the
   longest script is under 200.
2. Install from this repository, not from a mirror. The marketplace name is
   `durmazoguzhan-design` and the source is
   <https://github.com/durmazoguzhan/svg-logo-maker>.
