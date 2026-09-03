#!/usr/bin/env bash
# Two measurements a preview grid cannot give you.
#
#   legibility.sh logo.svg [size ...]        (default 16 32 48)
#
# 1. COLOUR DEPENDENCE — how much of the logo's structure is geometry and how
#    much is hue. Count the internal edges in the full-colour render, count
#    them again in the one-colour render, and divide. A mark whose parts are
#    held apart by colour alone loses those edges and the ratio collapses.
#    That matters because single-plate print, embossing, engraving, fax,
#    watermarks and a 16px favicon are all one colour.
#
# 2. DETAIL RETENTION — render at 512, shrink to N, blow it back up to 512 and
#    compare against the real 512, inside the mark's bounding box. The
#    difference is the detail that does not survive size N. Cropping to the
#    bounding box matters: measured over the whole canvas, a small mark on a
#    big empty field scores well for being mostly empty.
#
# Read both comparatively: run them over several concepts and prefer the one
# that loses least. The thresholds below are orientation, not a pass mark, and
# a low colour-dependence score is a fact about the design, not a verdict on
# it. An app icon on a coloured plate is *supposed* to score low; a wordmark
# that scores low is in trouble.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

[ $# -ge 1 ] || { echo "usage: legibility.sh <logo.svg> [size ...]" >&2; exit 64; }
src=$1; shift
sizes=("$@"); [ ${#sizes[@]} -gt 0 ] || sizes=(16 32 48)

detect_tools
require_rasteriser || exit 69
if [ "$HAS_ICO" -eq 0 ]; then
  echo "legibility.sh needs ImageMagick for the measurements." >&2
  echo "  apt install imagemagick  |  brew install imagemagick" >&2
  exit 69
fi

tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
here=$(dirname "${BASH_SOURCE[0]}")
stem=$(basename "$src"); stem=${stem%.svg}

echo "=== $src ==="

# --- 1. colour dependence ---------------------------------------------------
# Edges are counted on a white-flattened greyscale copy, so transparency does
# not register as an edge and inflate the count.
edge_density() {
  im "$1" -background white -alpha remove -colorspace Gray -edge 1 \
     -format '%[fx:mean]' info:
}

python3 "$here/variants.py" "$src" "$tmp/v" >/dev/null
mono="$tmp/v/$stem-mono-dark.svg"
if [ -f "$mono" ] \
   && svg_render "$src" "$tmp/full.png" 512 \
   && svg_render "$mono" "$tmp/mono.png" 512; then
  ef=$(edge_density "$tmp/full.png")
  em=$(edge_density "$tmp/mono.png")
  ratio=$(awk -v a="$em" -v b="$ef" 'BEGIN{printf "%.2f", (b>0)? a/b : 0}')
  # A mark drawn in a single ink scores 1.00 by construction, which is true and
  # says nothing. Name that case rather than letting it read as a good result.
  inks=$(grep -oiE '#[0-9a-f]{3,8}' "$src" | tr 'A-Z' 'a-z' | sort -u | wc -l)
  printf 'colour dependence  structure kept in one colour: %s  ' "$ratio"
  if [ "$inks" -le 1 ]; then
    echo "-- already one colour, so this number is trivially 1.00"
  else
    awk -v r="$ratio" 'BEGIN{
      if (r < 0.25) print "-- colour is doing the work; the one-colour version is a different mark";
      else if (r < 0.50) print "-- weakened in one colour; look at the mono variant before signing off";
      else print "-- geometry carries it; the one-colour version still reads";
    }'
  fi
else
  echo "colour dependence  (could not render both variants)"
fi

# --- 2. detail retention ----------------------------------------------------
# Measure inside the mark's own bounding box. Over the whole canvas a small
# mark on a large empty field scores well for being mostly empty.
geo=$(im "$tmp/full.png" -background white -alpha remove -format '%@' info:)
im "$tmp/full.png" -crop "$geo" +repage "$tmp/refc.png"

for s in "${sizes[@]}"; do
  im "$tmp/full.png" -filter Lanczos -resize "${s}x${s}" \
     -filter Point -resize 512x512 "$tmp/rt.png"
  im "$tmp/rt.png" -crop "$geo" +repage "$tmp/rtc.png"
  # `compare` exits non-zero whenever the images differ, which is always
  rmse=$( { im_compare -metric RMSE "$tmp/refc.png" "$tmp/rtc.png" null: 2>&1 || true; } \
          | sed -E 's/.*\(([0-9.]+)\).*/\1/')
  printf 'detail loss @%-5s %.4f  ' "${s}px" "$rmse"
  awk -v r="$rmse" 'BEGIN{
    if (r > 0.17) print "-- heavy: simplify before using it at this size";
    else if (r > 0.10) print "-- noticeable";
    else print "-- survives";
  }'
done
