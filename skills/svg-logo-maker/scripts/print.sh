#!/usr/bin/env bash
# Produce the files a printer can actually open, and say what is still missing.
#
#   print.sh logo.svg out/
#
# Emits an outlined SVG, a PDF and an EPS. Everything here is RGB, because SVG
# has no CMYK and neither does any tool in this chain. The colour separation is
# the one step that stays manual, and pretending otherwise is how a logo ends
# up printed in the wrong ink.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

[ $# -ge 2 ] || { echo "usage: print.sh <logo.svg> <outdir>" >&2; exit 64; }
src=$1; outdir=$2
mkdir -p "$outdir"
here=$(dirname "${BASH_SOURCE[0]}")
stem=$(basename "$src"); stem=${stem%.svg}

detect_tools

outlined="$outdir/$stem-outlined.svg"
bash "$here/outline.sh" "$src" "$outlined" || {
  echo >&2
  echo "print.sh: stopping. A print handoff with live text is not a handoff." >&2
  exit 69
}

if [ "$HAS_OUTLINE" -eq 0 ]; then
  echo "Inkscape missing, so no PDF or EPS was written." >&2
  exit 69
fi

echo
for fmt in pdf eps; do
  target="$outdir/$stem.$fmt"
  inkscape -T --export-type="$fmt" --export-filename="$target" "$src" >/dev/null 2>&1
  [ -s "$target" ] && printf '  %-32s %s bytes\n' "$(basename "$target")" "$(wc -c <"$target" | tr -d ' ')"
done

cat <<'MSG'

Still on you, and no script in this repository can do it:

  Colour separation. These files are RGB. Ask the printer whether the job is
  CMYK process or a spot colour, then convert in a vector editor and check the
  result on their proof, not on your screen.

  Spot colours. If the brand has Pantone numbers, name them in the handoff
  document. A hex value converted to CMYK is an approximation and it drifts
  between presses.

  Rich black vs 100K. Small text and thin rules print as 100% K only. A
  four-plate rich black on a hairline registers badly and looks fuzzy.

  Minimum size and clear space. Both belong in the guideline document, in
  millimetres for print and pixels for screen.
MSG
