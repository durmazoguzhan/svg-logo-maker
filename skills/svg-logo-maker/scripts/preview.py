#!/usr/bin/env python3
"""Build a review page for a folder of SVG logos.

Three things are on it, and the second and third are the ones people skip:

  the concepts, side by side, on light and on dark
  the same marks in one colour, because that is where a design held together
      by hue falls apart
  a favicon strip at 64, 32 and 16px, because that is where thin strokes go

Every cell is the live SVG, so the page reflects the files as they are on disk.
Refresh after an iteration; nothing needs regenerating except this page.

Usage:
    python3 preview.py logos/concepts/
    python3 preview.py logos/iterations/ --title "Iterations" --out logos/preview.html
"""

import argparse
import html
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{ --bg:#f4f4f5; --fg:#18181b; --card:#fff; --line:#d4d4d8; --muted:#71717a; }}
  body.dark {{ --bg:#0b0b0d; --fg:#e4e4e7; --card:#18181b; --line:#3f3f46; --muted:#a1a1aa; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--fg); font:15px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
         padding:2rem; transition:background .2s,color .2s; }}
  header {{ display:flex; justify-content:space-between; align-items:baseline; margin-bottom:.5rem; }}
  h1 {{ font-size:1.35rem; font-weight:650; }}
  h2 {{ font-size:.95rem; font-weight:600; margin:2.5rem 0 .35rem; }}
  p.note {{ color:var(--muted); font-size:.85rem; margin-bottom:1rem; max-width:60ch; }}
  button {{ background:transparent; color:inherit; border:1px solid var(--line); border-radius:6px;
            padding:.4rem .8rem; cursor:pointer; font:inherit; font-size:.85rem; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:1.1rem; }}
  .card {{ border:1px solid var(--line); border-radius:10px; overflow:hidden; background:var(--card); }}
  .art {{ display:flex; align-items:center; justify-content:center; padding:1.6rem; min-height:190px; }}
  .art img {{ max-width:100%; max-height:150px; }}
  .art.light {{ background:#fff; }}
  .art.dark {{ background:#101820; }}
  .label {{ padding:.5rem .75rem; font-size:.8rem; color:var(--muted); border-top:1px solid var(--line);
            font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}
  .strip {{ display:flex; flex-wrap:wrap; gap:2rem; align-items:flex-end;
            border:1px solid var(--line); border-radius:10px; padding:1.2rem; background:#fff; }}
  .strip .set {{ display:flex; flex-direction:column; align-items:center; gap:.5rem; }}
  .strip .row {{ display:flex; gap:1rem; align-items:flex-end; }}
  .strip figcaption {{ font-size:.7rem; color:#71717a; text-align:center; }}
  .strip .name {{ font-size:.75rem; font-family:ui-monospace,monospace; color:#71717a; }}
</style></head>
<body class="light">
<header>
  <h1>{title}</h1>
  <button onclick="document.body.classList.toggle('dark');this.textContent=document.body.classList.contains('dark')?'Light':'Dark'">Dark</button>
</header>
{sections}
</body></html>
"""


def cards(files, base, klass):
    out = []
    for path, label in files:
        rel = os.path.relpath(path, base)
        out.append(
            f'<div class="card"><div class="art {klass}">'
            f'<img src="{html.escape(rel)}" alt="{html.escape(label)}"></div>'
            f'<div class="label">{html.escape(label)}</div></div>')
    return '<div class="grid">' + "".join(out) + "</div>"


def strip(files, base):
    sets = []
    for path, label in files:
        rel = os.path.relpath(path, base)
        cells = "".join(
            f'<figure><img src="{html.escape(rel)}" width="{s}" height="{s}">'
            f"<figcaption>{s}px</figcaption></figure>" for s in (64, 32, 16))
        sets.append(f'<div class="set"><div class="row">{cells}</div>'
                    f'<div class="name">{html.escape(label)}</div></div>')
    return '<div class="strip">' + "".join(sets) + "</div>"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--out", default=None, help="default: <dir>/../preview.html")
    ap.add_argument("--title", default="Logo review")
    args = ap.parse_args()

    src_dir = os.path.abspath(args.dir)
    svgs = sorted(f for f in os.listdir(src_dir)
                  if f.endswith(".svg") and not f.startswith("_"))
    if not svgs:
        sys.exit(f"no .svg files in {src_dir}")

    out_path = os.path.abspath(
        args.out or os.path.join(os.path.dirname(src_dir), "preview.html"))
    base = os.path.dirname(out_path)

    originals = [(os.path.join(src_dir, f), os.path.splitext(f)[0]) for f in svgs]

    # One-colour versions live in a sibling folder so the concept folder stays
    # exactly what the designer iterates on.
    mono_dir = os.path.join(src_dir, "_mono")
    os.makedirs(mono_dir, exist_ok=True)
    mono_dark, mono_light = [], []
    for path, label in originals:
        subprocess.run([sys.executable, os.path.join(HERE, "variants.py"),
                        path, mono_dir],
                       capture_output=True, check=False)
        for suffix, bucket in (("mono-dark", mono_dark), ("mono-light", mono_light)):
            p = os.path.join(mono_dir, f"{label}-{suffix}.svg")
            if os.path.exists(p):
                bucket.append((p, f"{label} · {suffix}"))

    sections = [
        "<h2>Concepts on light</h2>", cards(originals, base, "light"),
        "<h2>Concepts on dark</h2>", cards(originals, base, "dark"),
        "<h2>One colour, dark ink on white</h2>",
        '<p class="note">This is what a single-plate print, an engraving and a '
        "favicon at 16px all get. A mark that only works in colour fails here "
        "first.</p>", cards(mono_dark, base, "light"),
        "<h2>One colour, reversed on dark</h2>",
        '<p class="note">Invisible on white is correct for this variant. Check '
        "it against the darkest surface the brand actually uses.</p>",
        cards(mono_light, base, "dark"),
        "<h2>Favicon strip</h2>",
        '<p class="note">If a detail disappears at 32px it is not a detail, it '
        "is noise. For a combination mark, run icon-extract.py first and strip "
        "the square icon, not the horizontal lockup.</p>", strip(originals, base),
    ]

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(PAGE.format(title=html.escape(args.title),
                             sections="\n".join(sections)))
    print(f"wrote {out_path}  ({len(originals)} concepts)")
    print("Open it in a browser; refresh after each iteration.")


if __name__ == "__main__":
    main()
