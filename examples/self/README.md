# Worked example: the skill's own logo

This is a real run of the workflow, kept because a skill that claims a process
should be able to show one. Every number below came out of the scripts in this
repository.

## Brief

Icon plus wordmark, geometric style, one ink, has to survive a favicon and a
one-colour print. The name is `logomaker`.

## Concepts

Three directions, not three tints of one direction:

| | Idea |
|---|---|
| `concept-1` | cascade — one mark and the two reductions it has to survive as |
| `concept-2` | aperture — a regular ring broken once, with a solid dot as the focus |
| `concept-3` | knockout — two squares whose overlap is removed rather than tinted |

All three passed the checks, so the choice was about the idea rather than the
measurements. Concept 1 won because the rationale is about what the thing does:
one drawing, several sizes. That is invariant 6 doing its job — the sentence
"three shapes descending" would have fitted twenty other companies.

## Iterations, and what each one fixed

**iteration-1** put the wordmark on the canvas centre while the icon cascade
ran past it, so the lockup sat crooked and the gaps in the cascade were 16 and
32 for no reason.

**iteration-2** rebuilt the cascade on a system: the gap is the constant (16)
and the size is the variable (192, 120, 72 — a steady 1.6 ratio), with the
corner radius held at 0.22 of the side so the three squares stay one family.
Then the wordmark overflowed the canvas, because its width had been estimated.

**iteration-3** measured instead of estimating:

```
$ inkscape --query-id=wordmark --query-x --query-width final.svg
```

At 90px with -4 tracking the ink is exactly 496 wide, which lands the frame on
icon 48-464, one 64 gap, wordmark ink 528-1024, right margin 48. The wordmark
`x` is 520 rather than 528, because `l` carries a side bearing and optical
alignment is about where the ink starts.

**One iteration that changed nothing, and that counts too.** Aligning the
wordmark to the primary square instead of the whole block was rendered and
compared side by side. It made the composition top-heavy and left the
bottom-right empty. The original alignment stayed.

## Measurements on the final

```
detail loss @16px  0.0224  -- survives
detail loss @32px  0.0124  -- survives
detail loss @48px  0.0117  -- survives
```

For scale, the same measurement on two logos from the prior-art survey lands at
0.20 and 0.22 at 16px. Solid chunky forms with real gaps survive reduction;
that is not a compliment to this mark, it is what the geometry buys.

The one-colour test reports 1.00 and says so is meaningless here, because the
mark was drawn in a single ink to begin with. The script names that case rather
than letting it read as a good score.

## A bug the linter caught

The first draft of `iteration-3.svg` had `--query-id` written inside an XML
comment. XML comments cannot contain `--`, so the file was invalid and resvg
refused it. `check.py` reported it before anything downstream did:

```
ERROR malformed   not parseable as XML: not well-formed (invalid token): line 6, column 43
```

## Delivered

```
out/digital/   full colour, mono dark, mono light, plated, square icon,
               PNG ladder 16-1024, multi-resolution favicon.ico
out/print/     outlined SVG (0 live text, 12 paths), PDF, EPS
```

Open `preview-concepts.html` and `preview-iterations.html` in a browser to see
the review pages the workflow generates.

## Reproduce it

```bash
S=../../skills/svg-logo-maker/scripts
python3 $S/check.py logos/final.svg
$S/legibility.sh logos/final-icon.svg
python3 $S/variants.py logos/final.svg out/digital --bg
$S/ico.sh out/digital/icon.svg out/digital/favicon.ico
$S/print.sh logos/final.svg out/print
```
