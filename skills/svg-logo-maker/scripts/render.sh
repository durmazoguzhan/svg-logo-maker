#!/usr/bin/env bash
# Rasterise an SVG at several widths.
#
#   render.sh logo.svg out/ 16 32 48 180 192 512 1024
#
# Defaults to the set that covers favicons, PWA icons, app icons and social
# avatars. Output is named after the source: logo-32.png and so on.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

[ $# -ge 2 ] || { echo "usage: render.sh <in.svg> <outdir> [size ...]" >&2; exit 64; }
src=$1; outdir=$2; shift 2
sizes=("$@")
[ ${#sizes[@]} -gt 0 ] || sizes=(16 32 48 180 192 512 1024 2048)

detect_tools
require_rasteriser || exit 69
mkdir -p "$outdir"
stem=$(basename "$src"); stem=${stem%.svg}

for s in "${sizes[@]}"; do
  out="$outdir/$stem-$s.png"
  if svg_render "$src" "$out" "$s"; then
    printf '  %-28s %s\n' "$(basename "$out")" "$(wc -c <"$out" | tr -d ' ') bytes"
  else
    echo "  FAILED at ${s}px" >&2
  fi
done
echo "rendered with: $RASTERISER"
