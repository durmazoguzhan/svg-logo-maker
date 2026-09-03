#!/usr/bin/env python3
"""Generate the colour variants a brand handoff is expected to contain.

Every identity guideline asks for the same four, and none of the logo skills
surveyed produced them: full colour, one-colour dark, one-colour light
(reversed, for dark backgrounds), and locked-background versions.

One-colour is not a nicety. It is what a single-plate print run, an embossed
surface, a fax, and a favicon at 16px all need, and it is the variant that
exposes a logo relying on colour to hold its shapes together.

Usage:
    python3 variants.py logo.svg out/
    python3 variants.py logo.svg out/ --dark '#101820' --light '#FFFFFF' --bg
"""

import argparse
import copy
import os
import re
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
PAINT_ATTRS = ("fill", "stroke", "stop-color", "flood-color", "lighting-color")


def local(tag):
    return tag.split("}", 1)[-1]


def repaint_attr(value, ink):
    """A paint value becomes `ink`, unless it is deliberately absent."""
    if value is None:
        return None
    v = value.strip().lower()
    if v in ("none", "transparent", "inherit", "currentcolor"):
        return None          # leave it alone
    return ink               # covers hex, named colours and url(#gradient)


def repaint_style(style, ink):
    def sub(m):
        prop, val = m.group(1), m.group(2)
        new = repaint_attr(val, ink)
        return f"{prop}:{val}" if new is None else f"{prop}:{new}"
    return re.sub(r"\b(fill|stroke|stop-color|flood-color|lighting-color)\s*:\s*([^;]+)",
                  sub, style)


def monochrome(root, ink):
    out = copy.deepcopy(root)
    for el in out.iter():
        for attr in PAINT_ATTRS:
            new = repaint_attr(el.get(attr), ink)
            if new is not None:
                el.set(attr, new)
        style = el.get("style")
        if style:
            el.set("style", repaint_style(style, ink))
    return out


def viewbox(root):
    vb = root.get("viewBox")
    if not vb:
        return None
    parts = re.split(r"[,\s]+", vb.strip())
    return [float(p) for p in parts] if len(parts) == 4 else None


def with_background(root, colour):
    """Put an opaque plate behind the mark, sized to the viewBox."""
    vb = viewbox(root)
    if vb is None:
        return None
    out = copy.deepcopy(root)
    rect = ET.Element(f"{{{SVG}}}rect", {
        "x": f"{vb[0]:g}", "y": f"{vb[1]:g}",
        "width": f"{vb[2]:g}", "height": f"{vb[3]:g}",
        "fill": colour, "id": "background",
    })
    out.insert(0, rect)
    return out


def write(root, path):
    ET.register_namespace("", SVG)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    print(f"  {os.path.basename(path)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg")
    ap.add_argument("outdir")
    ap.add_argument("--dark", default="#000000",
                    help="the one ink for light backgrounds (default #000000)")
    ap.add_argument("--light", default="#FFFFFF",
                    help="the one ink for dark backgrounds (default #FFFFFF)")
    ap.add_argument("--bg", action="store_true",
                    help="also write versions with an opaque plate behind the mark")
    ap.add_argument("--bg-dark", default="#101820",
                    help="plate colour for the reversed version (default #101820)")
    args = ap.parse_args()

    ET.register_namespace("", SVG)
    root = ET.parse(args.svg).getroot()
    os.makedirs(args.outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(args.svg))[0]
    j = lambda suffix: os.path.join(args.outdir, f"{stem}-{suffix}.svg")

    print(f"variants of {args.svg}:")
    write(copy.deepcopy(root), j("full"))
    write(monochrome(root, args.dark), j("mono-dark"))
    write(monochrome(root, args.light), j("mono-light"))

    if args.bg:
        plated = with_background(monochrome(root, args.light), args.bg_dark)
        if plated is None:
            print("  (skipped plated versions: no viewBox to size the plate to)")
        else:
            write(plated, j("on-dark"))
            write(with_background(copy.deepcopy(root), "#FFFFFF"), j("on-light"))

    print("\nmono-light is the reversed version: it is invisible on white, which")
    print("is correct. Check it on the darkest background the brand actually uses.")


if __name__ == "__main__":
    main()
