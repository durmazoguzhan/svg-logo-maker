#!/usr/bin/env python3
"""Lint an SVG logo before it is delivered.

Reports three severities. ERROR means the file will misbehave somewhere it
matters (print, favicon, another machine). WARN means look at it. INFO is
measurement, not judgement.

Exit code is 1 if any ERROR was reported, so this can gate a CI job.

Usage:  python3 check.py logo.svg [logo2.svg ...]
        python3 check.py --favicon-size 16 logo.svg
"""

import argparse
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"

# Below this many device pixels a stroke stops being a line and becomes a
# grey smear. One CSS pixel is the floor; 1.5 is where it still reads.
STROKE_FLOOR_PX = 1.0


class Report:
    def __init__(self, path):
        self.path = path
        self.rows = []

    def add(self, level, code, msg):
        self.rows.append((level, code, msg))

    @property
    def errors(self):
        return sum(1 for lvl, _, _ in self.rows if lvl == "ERROR")

    def render(self):
        print(f"\n=== {self.path} ===")
        if not self.rows:
            print("  clean")
            return
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        for lvl, code, msg in sorted(self.rows, key=lambda r: order[r[0]]):
            print(f"  {lvl:<5} {code:<18} {msg}")


def local(tag):
    return tag.split("}", 1)[-1]


def parse_viewbox(root):
    vb = root.get("viewBox")
    if not vb:
        return None
    parts = re.split(r"[,\s]+", vb.strip())
    if len(parts) != 4:
        return None
    try:
        return [float(p) for p in parts]
    except ValueError:
        return None


def font_families(text):
    """Every font-family named in the file, presentation attribute or CSS."""
    found = set()
    for m in re.finditer(r'font-family\s*[:=]\s*"([^"]+)"', text):
        found.add(m.group(1))
    for m in re.finditer(r"font-family\s*:\s*([^;\"'}]+)", text):
        found.add(m.group(1).strip())
    return {f.strip() for f in found if f.strip()}


def first_family(stack):
    """The family a renderer tries first, unquoted."""
    return stack.split(",")[0].strip().strip("'\"")


def check(path, favicon_size):
    rep = Report(path)
    try:
        raw = open(path, encoding="utf-8").read()
    except OSError as exc:
        rep.add("ERROR", "unreadable", str(exc))
        return rep
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        rep.add("ERROR", "malformed", f"not parseable as XML: {exc}")
        return rep

    elements = list(root.iter())

    # --- geometry contract -------------------------------------------------
    vb = parse_viewbox(root)
    if vb is None:
        rep.add("ERROR", "no-viewbox",
                "no usable viewBox; the logo cannot scale predictably")
    else:
        rep.add("INFO", "viewbox", f"{vb[2]:g} x {vb[3]:g}")
        if root.get("width") or root.get("height"):
            rep.add("WARN", "fixed-size",
                    "width/height on the root pin the logo to one size; "
                    "keep viewBox alone and let the container decide")

    # --- text is the print killer -----------------------------------------
    texts = [e for e in elements if local(e.tag) in ("text", "tspan")]
    if texts:
        rep.add("ERROR", "live-text",
                f"{len(texts)} <text>/<tspan> element(s) still live; outline "
                "before print handoff (scripts/outline.sh)")
        fams = font_families(raw)
        for stack in sorted(fams):
            want = first_family(stack)
            got = resolve_font(want)
            if got is None:
                rep.add("INFO", "font", f'"{want}" (fontconfig not available)')
            elif got.lower() == want.lower():
                rep.add("INFO", "font", f'"{want}" resolves to itself')
            else:
                rep.add("WARN", "font-substituted",
                        f'"{want}" is not installed here; this machine renders '
                        f'"{got}" instead. Outlining now would freeze the '
                        "substitute, not the font you named")

    # --- anything the file cannot carry with it ---------------------------
    for el in elements:
        name = local(el.tag)
        href = el.get("href") or el.get(f"{{{XLINK}}}href") or ""
        if name == "image":
            if href.startswith("data:"):
                rep.add("ERROR", "embedded-raster",
                        "an embedded bitmap makes this a picture of a logo, "
                        "not a logo; it cannot be recoloured or scaled")
            else:
                rep.add("ERROR", "external-image",
                        f"external image reference: {href[:60]}")
        elif href and not href.startswith("#") and not href.startswith("data:"):
            rep.add("ERROR", "external-ref",
                    f"<{name}> points outside the file: {href[:60]}")
    if "@import" in raw or "fonts.googleapis" in raw:
        rep.add("ERROR", "external-font",
                "@import or a webfont URL; the file stops being self-contained")

    # --- will it survive a favicon ----------------------------------------
    if vb:
        scale = favicon_size / max(vb[2], vb[3])
        widths = []
        for el in elements:
            sw = el.get("stroke-width")
            if sw is None:
                style = el.get("style") or ""
                m = re.search(r"stroke-width\s*:\s*([0-9.]+)", style)
                sw = m.group(1) if m else None
            if sw is None:
                continue
            try:
                widths.append(float(re.sub(r"[a-z%]+$", "", sw.strip())))
            except ValueError:
                continue
        if widths:
            thinnest = min(widths)
            device = thinnest * scale
            msg = (f"thinnest stroke {thinnest:g} user units = "
                   f"{device:.2f} px at {favicon_size}px")
            if device < STROKE_FLOOR_PX:
                rep.add("WARN", "stroke-vanishes",
                        msg + " — it will disappear; thicken it or drop it "
                        "from the small variant")
            else:
                rep.add("INFO", "stroke-floor", msg)
        else:
            rep.add("INFO", "stroke-floor", "no strokes; solid fills survive "
                                            "small sizes best")

    # --- shape of the file itself -----------------------------------------
    paths = [e for e in elements if local(e.tag) == "path"]
    nodes = 0
    for p in paths:
        nodes += len(re.findall(r"[MmLlCcQqAaSsTtHhVv]", p.get("d") or ""))
    prims = [e for e in elements
             if local(e.tag) in ("circle", "rect", "ellipse", "polygon",
                                 "line", "polyline")]
    rep.add("INFO", "shape-count",
            f"{len(paths)} path ({nodes} nodes), {len(prims)} primitive")
    if nodes > 250:
        rep.add("WARN", "autotrace-shape",
                f"{nodes} path nodes: this is the node count of a traced "
                "bitmap, not a drawn logo. Nobody can edit it")

    if not any(local(e.tag) == "g" and e.get("id") for e in elements):
        rep.add("WARN", "no-named-group",
                'no <g id="...">; name at least the icon so "make the icon '
                'bigger" has something to grab')

    return rep


_font_cache = {}


def resolve_font(family):
    """What this machine actually renders when asked for `family`."""
    if not shutil.which("fc-match"):
        return None
    if family in _font_cache:
        return _font_cache[family]
    try:
        out = subprocess.run(["fc-match", "-f", "%{family[0]}", family],
                             capture_output=True, text=True, timeout=10)
        got = out.stdout.strip() or None
    except (subprocess.SubprocessError, OSError):
        got = None
    _font_cache[family] = got
    return got


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", nargs="+")
    ap.add_argument("--favicon-size", type=int, default=16,
                    help="smallest size the logo must survive (default 16)")
    args = ap.parse_args()

    failed = 0
    for path in args.svg:
        rep = check(path, args.favicon_size)
        rep.render()
        failed += rep.errors
    print()
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
