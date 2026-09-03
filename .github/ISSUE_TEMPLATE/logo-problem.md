---
name: The skill produced a bad logo
about: A design or delivery problem, with the SVG attached
labels: quality
---

## What you asked for

<!-- The brief, and which style module the skill used. -->

## What came out

<!-- Attach or paste the SVG. The file is the report; a screenshot alone makes
     this hard to diagnose because most of what goes wrong is in the markup. -->

```xml

```

## What the scripts say

<!-- Both of these, if you can run them. They are often enough to locate the
     problem, and if they say the logo is fine while it plainly is not, that
     is itself the more interesting bug. -->

```
$ python3 skills/svg-logo-maker/scripts/check.py your-logo.svg

$ skills/svg-logo-maker/scripts/legibility.sh your-logo.svg

```

## Environment

- OS:
- Which of resvg / Inkscape / ImageMagick / fontconfig are installed:
