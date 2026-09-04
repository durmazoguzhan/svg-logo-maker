#!/usr/bin/env python3
"""Ask whether a brand colour survives being printed in process CMYK.

A hex picked on a monitor is a promise the press may not be able to keep, and
the failure is silent: the separation quietly moves the colour, and the first
anyone sees of it is a proof that looks wrong for reasons nobody can name.

The question is answerable. Convert the colour into the press's space, convert
it back, and measure how far it travelled. A colour that returns where it
started is inside the gamut and prints as itself. One that shifts was altered
by the separation before a single sheet was run.

This is not the same question as contrast, and `contrast.py` cannot see it. A
colour can clear 4.5:1 against paper, hold under every dichromacy, and still be
unreachable by a four-colour press.

**When a colour fails, do not desaturate until it passes.** Hold the hue, walk
the chroma down, and stop at the boundary — `--find` does exactly that. The
difference between the two is the difference between losing the brand colour
and locating it.

Profiles: this uses whatever CMYK ICC profile it finds, and Ghostscript's
"Artifex CMYK SWOP" is the usual one on Linux. That profile represents coated
process printing; it is not FOGRA39 and it is emphatically not your printer's
profile. Treat the numbers as a ranking and re-run with theirs when there is a
job. Pass `--cmyk-profile` to do that.

Needs `transicc` from liblcms2-utils. Without it this script reports what is
missing and exits 0, because a missing colour-management tool should cost one
feature rather than a run.

Usage:
    gamut.py '#C8442A' '#14171A'
    gamut.py --find '#C8442A'                 # the same hue, inside the gamut
    gamut.py --cmyk-profile ISOcoated_v2.icc '#C8442A'
"""

import argparse
import math
import os
import shutil
import subprocess
import sys

# Ubuntu, Debian and Fedora all put Ghostscript's profiles in one of these.
CMYK_CANDIDATES = [
    "/usr/share/color/icc/ghostscript/default_cmyk.icc",
    "/usr/share/ghostscript/iccprofiles/default_cmyk.icc",
    "/usr/share/color/icc/colord/ISOcoated_v2.icc",
]
SRGB_CANDIDATES = [
    "/usr/share/color/icc/sRGB.icc",
    "/usr/share/color/icc/ghostscript/srgb.icc",
    "/usr/share/color/icc/colord/sRGB.icc",
]
LAB_CANDIDATES = [
    "/usr/share/color/icc/ghostscript/lab.icc",
    "/usr/share/color/icc/LCMSLABI.ICM",
]

# CIEDE2000 bands, as a print buyer would read them.
BAND = [
    (1.0, "prints as itself"),
    (2.0, "shift invisible side by side"),
    (3.5, "shift visible on a proof"),
]
REACHABLE = 2.0     # what --find will accept


def first_existing(paths):
    return next((p for p in paths if os.path.exists(p)), None)


def transicc(lines, src, dst, intent=1):
    """Run one conversion for a whole batch; transicc reads many lines."""
    out = subprocess.run(["transicc", "-i", src, "-o", dst, "-t", str(intent)],
                         input="\n".join(lines) + "\n",
                         capture_output=True, text=True).stdout
    rows = []
    for line in out.splitlines():
        if "=" not in line:
            continue
        nums = []
        for tok in line.replace("=", " ").split():
            try:
                nums.append(float(tok))
            except ValueError:
                pass
        if len(nums) in (3, 4):
            rows.append(nums)
    return rows


def de2000(p, q):
    """CIEDE2000. Worth the arithmetic here because CIE76 overstates the error
    in saturated reds, and reds are where brand colours get chosen."""
    L1, a1, b1 = p
    L2, a2, b2 = q
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7))) if Cb else 0.0
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0

    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    else:
        dhp = h2p - h1p - 360 if h2p > h1p else h2p - h1p + 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)

    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hbp = (h1p + h2p + 360) / 2
    else:
        hbp = (h1p + h2p - 360) / 2

    T = (1 - 0.17 * math.cos(math.radians(hbp - 30))
         + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6))
         - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dTh = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) if Cbp else 0.0
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc, Sh = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dTh)) * Rc

    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                     + Rt * (dCp / Sc) * (dHp / Sh))


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def verdict(de):
    for limit, text in BAND:
        if de < limit:
            return text
    return "SHIFTS — the press cannot reach this"


def roundtrip(hexes, srgb, cmyk, lab):
    """Lab as asked for, Lab as returned, and the separation in between."""
    rgbs = [hex_rgb(h) for h in hexes]
    lines = [" ".join(str(v) for v in c) for c in rgbs]
    targets = transicc(lines, srgb, lab)
    seps = transicc(lines, srgb, cmyk)
    actuals = transicc([" ".join(f"{v:.4f}" for v in s) for s in seps], cmyk, lab)
    return targets, seps, actuals


def report(hexes, srgb, cmyk, lab):
    targets, seps, actuals = roundtrip(hexes, srgb, cmyk, lab)
    if not (len(targets) == len(seps) == len(actuals) == len(hexes)):
        print("  WARN  the profile chain returned an unexpected shape; "
              "check that transicc and the profiles agree")
        return 0
    worst = 0.0
    print(f"  {'hex':<10}{'CMYK':<26}{'dE2000':>8}   verdict")
    for h, t, s, a in zip(hexes, targets, seps, actuals):
        de = de2000(t, a)
        worst = max(worst, de)
        clipped = any(v >= 99.995 for v in s)
        sep = " ".join(f"{v:5.1f}" for v in s)
        print(f"  {h.upper():<10}{sep:<26}{de:>8.2f}   {verdict(de)}"
              + ("   [plate clipped]" if clipped else ""))
    return worst


def find_reachable(hexstr, srgb, cmyk, lab):
    """Hold the hue, walk the chroma down, stop at the boundary.

    Reported as the highest chroma that still round-trips, because the point is
    to keep as much of the colour as the press allows and not to arrive at a
    safe grey."""
    target = transicc([" ".join(str(v) for v in hex_rgb(hexstr))], srgb, lab)
    if not target:
        return None
    L0, a0, b0 = target[0]
    C0 = math.hypot(a0, b0)
    H0 = math.degrees(math.atan2(b0, a0)) % 360
    print(f"  holding hue {H0:.1f}deg, walking chroma down from {C0:.1f} "
          f"at L* {L0:.1f}")

    steps = [C0 - i for i in range(0, int(C0) - 4)]
    labs = [f"{L0} {C * math.cos(math.radians(H0))} {C * math.sin(math.radians(H0))}"
            for C in steps]
    rgbs = transicc(labs, lab, srgb)

    cands = []
    for C, rgb in zip(steps, rgbs):
        if all(0.4 <= v <= 254.6 for v in rgb):       # inside sRGB, not clamped
            cands.append((C, "#%02X%02X%02X" % tuple(round(v) for v in rgb)))
    if not cands:
        return None

    targets, seps, actuals = roundtrip([h for _, h in cands], srgb, cmyk, lab)
    for (C, h), t, s, a in zip(cands, targets, seps, actuals):
        if any(v >= 99.995 for v in s):
            continue
        de = de2000(t, a)
        if de < REACHABLE:
            return h, C, C0, de
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("colours", nargs="+", help="hex colours to measure")
    ap.add_argument("--find", action="store_true",
                    help="for each colour that fails, report the highest chroma "
                         "on the same hue that the press can reach")
    ap.add_argument("--cmyk-profile", help="the printer's own profile, when you have it")
    ap.add_argument("--floor", type=float, default=REACHABLE,
                    help=f"dE2000 above which a colour counts as failing "
                         f"(default {REACHABLE})")
    args = ap.parse_args()

    if not shutil.which("transicc"):
        print("  SKIP  transicc not installed, so gamut is unmeasured here.")
        print("        apt install liblcms2-utils   (or brew install little-cms2)")
        print("        Contrast and legibility are unaffected; this costs one check.")
        return 0

    cmyk = args.cmyk_profile or first_existing(CMYK_CANDIDATES)
    srgb = first_existing(SRGB_CANDIDATES)
    lab = first_existing(LAB_CANDIDATES)
    missing = [n for n, p in (("CMYK", cmyk), ("sRGB", srgb), ("Lab", lab)) if not p]
    if missing:
        print(f"  SKIP  no {', '.join(missing)} ICC profile found.")
        print("        apt install icc-profiles-free ghostscript")
        return 0

    print(f"  profile  {os.path.basename(cmyk)}"
          + ("" if args.cmyk_profile else "  (generic; not your printer's)"))
    worst = report(args.colours, srgb, cmyk, lab)

    if args.find:
        for h in args.colours:
            t, s, a = roundtrip([h], srgb, cmyk, lab)
            if not t:
                continue
            if de2000(t[0], a[0]) < args.floor:
                continue
            print(f"\n  {h.upper()} does not print. Same hue, inside the gamut:")
            found = find_reachable(h, srgb, cmyk, lab)
            if found:
                new, C, C0, de = found
                print(f"  -> {new}  chroma {C:.0f} of {C0:.0f} kept, dE {de:.2f}")
                print("     Lightness is unchanged, so the mark's balance is unchanged.")
            else:
                print("  -> nothing on this hue round-trips; the hue itself is "
                      "outside what this profile reaches")

    # A colour the press cannot reach is a finding, not a failure of the run:
    # a screen-only brand is a legitimate choice as long as it was chosen.
    if worst >= args.floor:
        print(f"\n  At least one colour shifts by dE {worst:.2f}. That is fine if "
              f"the brand never prints.\n  If it does, run --find.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
