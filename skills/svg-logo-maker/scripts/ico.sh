#!/usr/bin/env bash
# Build a real multi-resolution .ico.
#
#   ico.sh icon.svg favicon.ico
#
# Windows, older browsers and desktop shortcuts still want .ico, and a proper
# one carries several bitmaps so the OS picks the right pixel grid instead of
# scaling a 256px image down to 16 and turning it to mush. None of the logo
# skills surveyed emitted one.
#
# Feed this the SQUARE icon, never a horizontal combination mark. A wordmark
# squeezed into a 16x16 cell is a grey smudge.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

[ $# -ge 1 ] || { echo "usage: ico.sh <icon.svg> [out.ico]" >&2; exit 64; }
src=$1
out=${2:-${src%.svg}.ico}
sizes=(16 24 32 48 64 128 256)

detect_tools
require_rasteriser || exit 69
if [ "$HAS_ICO" -eq 0 ]; then
  echo "ico.sh needs ImageMagick to assemble the .ico container." >&2
  echo "  apt install imagemagick  |  brew install imagemagick" >&2
  exit 69
fi

vb=$(grep -oE 'viewBox="[^"]*"' "$src" | head -1 | sed -E 's/viewBox="([^"]*)"/\1/')
if [ -n "$vb" ]; then
  read -r _ _ w h <<<"$vb"
  ratio=$(awk -v w="$w" -v h="$h" 'BEGIN{printf "%.2f", (h>0)? w/h : 0}')
  if awk -v r="$ratio" 'BEGIN{exit !(r < 0.9 || r > 1.1)}'; then
    echo "warning: viewBox is ${w}x${h} (ratio $ratio), not square." >&2
    echo "         Extract the icon group into a square file first, or every" >&2
    echo "         bitmap in this .ico will be letterboxed." >&2
  fi
fi

tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
pngs=()
for s in "${sizes[@]}"; do
  svg_render "$src" "$tmp/$s.png" "$s" || { echo "failed at ${s}px" >&2; exit 70; }
  pngs+=("$tmp/$s.png")
done

im "${pngs[@]}" -colors 256 "$out"
echo "wrote $out"
im_identify "$out" | sed 's/^/  /'
