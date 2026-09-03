#!/usr/bin/env python3
"""Pull the icon out of a combination mark as a standalone square SVG.

A horizontal lockup cannot be a favicon or an app icon. Squeezing one into a
square cell letterboxes it into a grey smudge at 16px, which is why the icon
has to be lifted out and re-framed before it goes anywhere square.

The bounding box comes from Inkscape, because computing the visual extent of
arbitrary paths and strokes by hand is exactly the kind of arithmetic that is
wrong in the one case you do not test.

Usage:
    python3 icon-extract.py logo.svg icon.svg
    python3 icon-extract.py logo.svg icon.svg --id mark --pad 0.12
"""

import argparse
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
KEEP_ALONGSIDE = {"defs", "style", "title", "desc", "metadata"}


def local(tag):
    return tag.split("}", 1)[-1]


def query_bbox(path, group_id):
    if not shutil.which("inkscape"):
        sys.exit("icon-extract needs Inkscape to measure the group's bounding box.\n"
                 "  apt install inkscape  |  brew install inkscape\n"
                 "Without it, set the square viewBox by hand in your editor.")
    vals = []
    for flag in ("--query-x", "--query-y", "--query-width", "--query-height"):
        r = subprocess.run(["inkscape", f"--query-id={group_id}", flag, path],
                           capture_output=True, text=True)
        out = r.stdout.strip()
        if not out:
            sys.exit(f'No element with id="{group_id}" in {path}.\n'
                     "Name the icon group first: <g id=\"icon\"> ... </g>")
        vals.append(float(out))
    return vals


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg")
    ap.add_argument("out")
    ap.add_argument("--id", default="icon", help='group id to extract (default "icon")')
    ap.add_argument("--pad", type=float, default=0.08,
                    help="breathing room as a fraction of the square side (default 0.08)")
    args = ap.parse_args()

    x, y, w, h = query_bbox(args.svg, args.id)
    side = max(w, h) * (1 + 2 * args.pad)
    cx, cy = x + w / 2, y + h / 2
    vx, vy = cx - side / 2, cy - side / 2

    ET.register_namespace("", SVG)
    root = ET.parse(args.svg).getroot()

    target = None
    for el in root.iter():
        if el.get("id") == args.id:
            target = el
            break
    if target is None:
        sys.exit(f'id="{args.id}" parsed away; check the file')

    out_root = ET.Element(f"{{{SVG}}}svg", {
        "viewBox": f"{vx:.3f} {vy:.3f} {side:.3f} {side:.3f}",
    })
    for child in root:
        if local(child.tag) in KEEP_ALONGSIDE:
            out_root.append(child)
    out_root.append(target)

    ET.ElementTree(out_root).write(args.out, encoding="utf-8", xml_declaration=True)
    print(f"{args.out}")
    print(f"  source bbox   {w:.1f} x {h:.1f} at ({x:.1f}, {y:.1f})")
    print(f"  square viewBox {side:.1f} with {args.pad:.0%} padding")
    print("  Feed this to ico.sh and to the favicon sizes. Keep the full lockup")
    print("  for anywhere the name has to be readable.")


if __name__ == "__main__":
    main()
