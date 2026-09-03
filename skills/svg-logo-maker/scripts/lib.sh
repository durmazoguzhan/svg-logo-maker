#!/usr/bin/env bash
# Shared tool detection. Source this; do not run it.
#
# Every capability here is optional. A missing tool degrades one feature and
# leaves the rest working, because the alternative — refusing to start until
# Inkscape is installed — stops people who only wanted an SVG icon.

set -uo pipefail

RASTERISER=""      # resvg | inkscape | rsvg-convert | magick
HAS_OUTLINE=0      # text-to-path and PDF/EPS need Inkscape specifically
HAS_ICO=0          # multi-resolution .ico needs ImageMagick
HAS_FC=0           # font auditing needs fontconfig

_have() { command -v "$1" >/dev/null 2>&1; }

detect_tools() {
  if   _have resvg;         then RASTERISER=resvg
  elif _have inkscape;      then RASTERISER=inkscape
  elif _have rsvg-convert;  then RASTERISER=rsvg-convert
  elif _have magick;        then RASTERISER=magick
  elif _have convert;       then RASTERISER=convert
  fi
  _have inkscape && HAS_OUTLINE=1
  { _have magick || _have convert; } && HAS_ICO=1
  _have fc-match && HAS_FC=1
}

# magick vs the older convert, whichever exists
im() { if _have magick; then magick "$@"; else convert "$@"; fi; }

# `compare` is its own binary in ImageMagick 6 and a subcommand in 7. It also
# exits non-zero whenever the images differ, which is the normal case here, so
# callers must not let `set -e` see that.
im_compare() { if _have magick; then magick compare "$@"; else compare "$@"; fi; }

# Same split for `identify`.
im_identify() { if _have magick; then magick identify "$@"; else identify "$@"; fi; }

# svg_render <in.svg> <out.png> <width_px>
svg_render() {
  local src=$1 out=$2 w=$3
  case "$RASTERISER" in
    resvg)        resvg "$src" "$out" --width "$w" >/dev/null 2>&1 ;;
    inkscape)     inkscape --export-type=png --export-filename="$out" -w "$w" "$src" >/dev/null 2>&1 ;;
    rsvg-convert) rsvg-convert -w "$w" "$src" -o "$out" ;;
    magick|convert) im -background none -density 384 "$src" -resize "${w}x" "$out" ;;
    *) echo "svg-logo-maker: no SVG rasteriser found." >&2; return 1 ;;
  esac
}

require_rasteriser() {
  [ -n "$RASTERISER" ] && return 0
  cat >&2 <<'MSG'
svg-logo-maker: no SVG rasteriser found. Install any one of these:

  resvg          curl -sL https://github.com/linebender/resvg/releases/latest/download/resvg-linux-x86_64.tar.gz | tar xz
                 then move the `resvg` binary onto your PATH
  inkscape       apt install inkscape   |  brew install inkscape
  librsvg        apt install librsvg2-bin  |  brew install librsvg
  imagemagick    apt install imagemagick   |  brew install imagemagick

resvg is the smallest (one 4.6 MB binary, no dependencies). Inkscape is the
only one that can also do text-to-path and PDF/EPS, so install it too if this
logo is going to print.
MSG
  return 1
}

warn_no_outline() {
  cat >&2 <<'MSG'
svg-logo-maker: Inkscape not found, so text was NOT converted to paths.

An SVG whose wordmark is still a <text> element renders with whatever font the
opening machine happens to resolve. Do not send this file to a printer. Install
Inkscape and rerun, or outline the text in your vector editor before handoff.
MSG
}
