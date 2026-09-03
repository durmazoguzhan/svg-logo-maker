#!/usr/bin/env bash
# Convert every <text> element to <path>, and say which font actually got frozen.
#
#   outline.sh logo.svg [logo-outlined.svg]
#
# Why this exists: an SVG that still contains <text> renders with whatever font
# the opening machine resolves. Outlining fixes that — but it freezes the font
# *this* machine resolved, which is not necessarily the one the file names. So
# the audit runs first and refuses to be quiet about a substitution.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

[ $# -ge 1 ] || { echo "usage: outline.sh <in.svg> [out.svg]" >&2; exit 64; }
src=$1
out=${2:-${src%.svg}-outlined.svg}

detect_tools

before=$(grep -c '<text' "$src" || true)
if [ "$before" -eq 0 ]; then
  echo "No <text> in $src; nothing to outline."
  [ "$src" != "$out" ] && cp "$src" "$out"
  exit 0
fi

# First family of every font-family stack in the file, deduplicated.
mapfile -t families < <(
  grep -oE "font-family[[:space:]]*[:=][[:space:]]*[\"'][^\"']+[\"']" "$src" \
    | sed -E "s/.*[:=][[:space:]]*[\"']//; s/[\"']\$//; s/,.*//" \
    | sed -E "s/^[[:space:]]+//; s/[[:space:]]+\$//" \
    | grep -v '^$' | sort -u
)

echo "Font audit — what this machine would freeze:"
substituted=0
if [ "$HAS_FC" -eq 0 ]; then
  echo "  fontconfig not available; cannot verify what will be frozen."
elif [ ${#families[@]} -eq 0 ]; then
  echo "  no font-family declared; the renderer picks its own default."
  substituted=1
else
  for want in "${families[@]}"; do
    got=$(fc-match -f '%{family[0]}' "$want")
    if [ "${got,,}" = "${want,,}" ]; then
      printf '  %-28s -> %s\n' "$want" "$got"
    else
      printf '  %-28s -> %s   <-- SUBSTITUTED\n' "$want" "$got"
      substituted=1
    fi
  done
fi

if [ "$substituted" -eq 1 ]; then
  echo
  echo "  A font you named is not installed here, so the outlines will carry the" >&2
  echo "  substitute's letterforms. Metrics may match; the shapes do not. Install" >&2
  echo "  the real font, or run this step on the machine that has it." >&2
fi

if [ "$HAS_OUTLINE" -eq 0 ]; then
  echo
  warn_no_outline
  exit 69
fi

inkscape -T -l --export-type=svg --export-filename="$out" "$src" >/dev/null 2>&1
after=$(grep -c '<text' "$out" || true)
echo
if [ "$after" -ne 0 ]; then
  echo "FAILED: $after <text> element(s) survived in $out" >&2
  exit 70
fi
echo "OK: $before <text> element(s) became paths -> $out"
echo "Note: -T also flattens <circle>/<rect> into <path>. Keep the input as your"
echo "editable master and treat $out as a delivery artefact."
