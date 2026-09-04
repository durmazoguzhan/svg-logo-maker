#!/usr/bin/env python3
"""Measure whether a logo's colours are doing a job the geometry cannot.

The rest of this skill treats colour as a risk to be removed: do not let hue
carry structure, do not rescue a weak silhouette with a gradient. That is the
right instinct and it is only half the subject. Colour also has to be *chosen*,
and three of those choices are measurable rather than tasteful:

  contrast    a logo is a graphic, so WCAG 1.4.11 asks 3:1 against every
              surface it is approved for. A wordmark that functions as the
              product name is held to 4.5:1, because people read it.
  greyscale   two inks of the same luminance merge in a fax, a laser engraving
              and most colour vision deficiency. This is not the one-colour
              test: that one collapses every ink into one, this one keeps the
              luminance difference and asks whether it was ever there.
  deficiency  simulate the three dichromacies and ask whether two inks that
              were distinct converge. If they do, the pair was a hue pair.

Usage:
    contrast.py logo.svg
    contrast.py logo.svg --bg '#FAF7F2,#101820' --floor 3.0
    contrast.py logo.svg --text-floor 4.5      # treat every ink as read text
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET

# Surfaces a mark meets whether or not the brand chose them. Mid grey is here
# because a logo that clears white and black can still die on #808080, and that
# is the one nobody previews.
DEFAULT_BACKGROUNDS = ["#FFFFFF", "#000000", "#808080"]

NON_TEXT_FLOOR = 3.0      # WCAG 1.4.11, graphical objects
DELTA_E_FLOOR = 20.0      # below this two inks read as one at a glance
DELTA_E_KEPT = 0.35       # a pair that keeps less than this fraction of its
                          # separation has lost the distinction even when the
                          # remainder clears the absolute floor

# Machado, Oliveira and Fernandes (2009), severity 1.0, applied in linear RGB.
DICHROMACY = {
    "protanopia":  ((0.152286,  1.052583, -0.204868),
                    (0.114503,  0.786281,  0.099216),
                    (-0.003882, -0.048116, 1.051998)),
    "deuteranopia": ((0.367322,  0.860646, -0.227968),
                     (0.280085,  0.672501,  0.047413),
                     (-0.011820, 0.042940,  0.968881)),
    "tritanopia":  ((1.255528, -0.076749, -0.178779),
                    (-0.078411, 0.930809,  0.147602),
                    (0.004733,  0.691367,  0.303900)),
}

NAMED = {"black": "#000000", "white": "#FFFFFF", "red": "#FF0000",
         "green": "#008000", "blue": "#0000FF", "grey": "#808080",
         "gray": "#808080", "silver": "#C0C0C0", "navy": "#000080"}

PAINT_ATTRS = ("fill", "stroke", "stop-color")
SKIP = {"none", "transparent", "inherit", "currentcolor"}


def parse_colour(value):
    """Return (r, g, b) 0-255, or None when the value is not a literal colour."""
    if not value:
        return None
    v = value.strip().lower()
    if v in SKIP or v.startswith("url("):
        return None
    v = NAMED.get(v, v)
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) in (6, 8) and re.fullmatch(r"[0-9a-f]+", h):
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        return None
    m = re.fullmatch(r"rgba?\(([^)]+)\)", v)
    if m:
        parts = [p.strip() for p in re.split(r"[,\s/]+", m.group(1)) if p.strip()]
        try:
            return tuple(int(round(float(p[:-1]) * 2.55 if p.endswith("%") else float(p)))
                         for p in parts[:3])
        except ValueError:
            return None
    return None


def to_linear(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_rgb(rgb):
    return tuple(to_linear(c) for c in rgb)


def luminance(rgb):
    r, g, b = linear_rgb(rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def lab(rgb):
    """CIE L*a*b* under D65, for the one question contrast cannot answer:
    whether two inks of similar lightness are still different colours."""
    r, g, b = linear_rgb(rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.00000
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29

    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(a, b):
    """CIE76. Coarser than DE2000 and honest about it: it is used here only to
    separate 'these are two colours' from 'these are one colour', a call it
    makes reliably at the magnitudes a logo palette works in."""
    la, lb = lab(a), lab(b)
    return sum((x - y) ** 2 for x, y in zip(la, lb)) ** 0.5


def simulate(rgb, kind):
    m = DICHROMACY[kind]
    lin = linear_rgb(rgb)
    out = []
    for row in m:
        v = sum(row[i] * lin[i] for i in range(3))
        v = max(0.0, min(1.0, v))
        v = 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
        out.append(int(round(v * 255)))
    return tuple(out)


def hexof(rgb):
    return "#%02X%02X%02X" % rgb


def viewbox(root):
    vb = root.get("viewBox")
    if not vb:
        return None
    parts = re.split(r"[,\s]+", vb.strip())
    return [float(p) for p in parts] if len(parts) == 4 else None


def plate_colour(root):
    """The fill of a rect that covers the whole viewBox, if there is one.

    A file carrying its own opaque plate is answerable only for the marks on
    that plate; asking how it behaves on white is asking about a surface it
    will never meet."""
    vb = viewbox(root)
    if vb is None:
        return None
    for el in root.iter():
        if el.tag.split("}")[-1] != "rect":
            continue
        try:
            x, y = float(el.get("x", 0)), float(el.get("y", 0))
            w, h = float(el.get("width", 0)), float(el.get("height", 0))
        except (TypeError, ValueError):
            continue
        if (abs(x - vb[0]) < 1 and abs(y - vb[1]) < 1
                and w >= vb[2] - 1 and h >= vb[3] - 1):
            rgb = parse_colour(el.get("fill"))
            if rgb:
                return rgb
    return None


def collect_inks(path):
    """Every literal paint in the file, in document order, deduplicated."""
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        print(f"  ERROR malformed        {e}")
        return None
    inks, seen = [], set()
    for el in root.iter():
        values = [el.get(a) for a in PAINT_ATTRS]
        style = el.get("style")
        if style:
            values += re.findall(r"\b(?:fill|stroke|stop-color)\s*:\s*([^;]+)", style)
        for v in values:
            rgb = parse_colour(v)
            if rgb and rgb not in seen:
                seen.add(rgb)
                inks.append(rgb)
    return inks, plate_colour(root)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", nargs="+")
    ap.add_argument("--bg", default="",
                    help="comma separated backgrounds the brand actually uses; "
                         "white, black and mid grey are always added")
    ap.add_argument("--floor", type=float, default=NON_TEXT_FLOOR,
                    help=f"contrast floor for a graphic (default {NON_TEXT_FLOOR})")
    ap.add_argument("--text-floor", type=float, default=None,
                    help="apply a text floor (4.5) instead; use when the mark "
                         "is a wordmark and the name is being read")
    args = ap.parse_args()

    floor = args.text_floor if args.text_floor is not None else args.floor
    brand = [b.strip() for b in args.bg.split(",") if b.strip()]
    backgrounds = brand + [b for b in DEFAULT_BACKGROUNDS if b.upper() not in
                           {x.upper() for x in brand}]

    failed = False
    for path in args.svg:
        print(f"\n=== {path} ===")
        got = collect_inks(path)
        if got is None:
            failed = True
            continue
        inks, plate = got
        if not inks:
            print("  INFO  no literal paint found; nothing to measure")
            continue

        print(f"  INFO  inks               {', '.join(hexof(c) for c in inks)}")
        if plate is not None:
            print(f"  INFO  plate              {hexof(plate)} covers the viewBox; "
                  f"this file is opaque, so only the marks on it are in question")
            backgrounds = [hexof(plate)]

        # An ink is allowed to fail a background the brand never uses, so the
        # ones the user named are reported as errors and the rest as warnings.
        for bg in backgrounds:
            bg_rgb = parse_colour(bg)
            if bg_rgb is None:
                print(f"  WARN  bad background     {bg}")
                continue
            # Only the plate is excluded. An ink that merely happens to equal
            # the surface is a mark that vanished on it, which is the finding.
            marks = [i for i in inks if i != plate]
            if not marks:
                print(f"  INFO  on {bg:<12} nothing but the plate itself")
                continue
            worst = min(contrast(ink, bg_rgb) for ink in marks)
            named = bg in brand
            if worst < floor:
                weak = [hexof(i) for i in marks if contrast(i, bg_rgb) < floor]
                tag = "ERROR" if named else "WARN "
                print(f"  {tag} on {bg:<12} {worst:5.2f}:1 worst — "
                      f"{', '.join(weak)} under {floor}:1"
                      + ("" if named else "  (not a brand surface; reverse instead)"))
                if named:
                    failed = True
            else:
                print(f"  INFO  on {bg:<12} {worst:5.2f}:1 worst of {len(marks)} inks")

        if len(inks) < 2:
            continue

        # Adjacent inks are a separate question from ink against background:
        # two shapes that touch are told apart by the difference between them.
        print("  ---- ink against ink ----")
        for i in range(len(inks)):
            for j in range(i + 1, len(inks)):
                a, b = inks[i], inks[j]
                cr, de = contrast(a, b), delta_e(a, b)
                if cr < 1.5:
                    print(f"  WARN  {hexof(a)} / {hexof(b)}   merge in greyscale "
                          f"({cr:4.2f}:1), dE76 {de:5.1f} — one plate, an engraving "
                          f"and a fax keep luminance and drop the rest")
                else:
                    print(f"  INFO  {hexof(a)} / {hexof(b)}   {cr:4.2f}:1 apart, "
                          f"dE76 {de:5.1f}")

        print("  ---- colour vision deficiency ----")
        for kind in DICHROMACY:
            sims = [simulate(c, kind) for c in inks]
            worst_pair, worst_de = None, None
            for i in range(len(inks)):
                for j in range(i + 1, len(inks)):
                    de = delta_e(sims[i], sims[j])
                    if worst_de is None or de < worst_de:
                        worst_de, worst_pair = de, (i, j)
            i, j = worst_pair
            base = delta_e(inks[i], inks[j])
            kept = worst_de / base if base else 1.0
            if worst_de < DELTA_E_FLOOR or kept < DELTA_E_KEPT:
                why = ("under the floor" if worst_de < DELTA_E_FLOOR
                       else f"keeps only {kept:.0%} of its separation")
                print(f"  WARN  {kind:<13} {hexof(inks[i])} and {hexof(inks[j])} "
                      f"converge, dE {base:.1f} -> {worst_de:.1f}, {why}; "
                      f"that pair was hue, not structure")
            else:
                print(f"  INFO  {kind:<13} closest pair holds, dE {base:.1f} -> "
                      f"{worst_de:.1f} ({kept:.0%} kept)")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
