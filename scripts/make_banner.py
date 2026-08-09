"""
Generates web-banner.svg — the README header. Replaces the generic
capsule-render waving banner with something on-theme and self-hosted.

Three layers, staged: webbing weaves in across the band, the name and tagline
resolve, then a symbiote drip bleeds off the bottom edge into the page.

Animation is CSS, not SMIL: GitHub renders README art through <img>, where
Chrome runs CSS keyframes but not SMIL. Static state is the settled state, so
the banner never renders blank.

Usage:
    python3 scripts/make_banner.py
"""

import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "web-banner.svg"

W, H = 1000, 262
MASS_Y = H - 26            # top of the symbiote mass; tendrils climb up from it

BONE = "#EDEDED"
CRIMSON = "#E62429"
FIRE = "#FF3B30"
DEEP = "#8E1519"
WEB = "#3A3F44"
MUTED = "#6E7681"

FONT_STACK = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

NAME = "HariCipher"
TAGLINE = "SOC  ·  DFIR  ·  DETECTION ENGINEERING"

random.seed(1962)  # Amazing Fantasy #15 — keeps regenerated output stable


def corner_web(cx, cy, r, radials, rings, quadrant):
    """Web anchored in a corner, spanning one quadrant. Returns path strings."""
    a0, a1 = quadrant
    out = []
    for i in range(radials):
        a = a0 + (a1 - a0) * i / (radials - 1)
        out.append(f"M{cx:.1f} {cy:.1f} L{cx + r * math.cos(a):.1f} "
                   f"{cy + r * math.sin(a):.1f}")
    for j in range(1, rings + 1):
        rr = r * j / rings
        pts = []
        for i in range(radials):
            a = a0 + (a1 - a0) * i / (radials - 1)
            sag = rr * 0.055  # strands sag between anchors
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a), a, sag))
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for k in range(1, len(pts)):
            x0, y0, aa0, _ = pts[k - 1]
            x1, y1, aa1, sag = pts[k]
            am = (aa0 + aa1) / 2
            mr = rr - sag
            d += (f" Q{cx + mr * math.cos(am):.1f} {cy + mr * math.sin(am):.1f} "
                  f"{x1:.1f} {y1:.1f}")
        out.append(d)
    return out


def drip_path(y, bumps, lo, hi, wide=(26, 60), fingers=0,
              finger_h=(26, 46), finger_w=(12, 18)):
    """
    Symbiote mass flooding the bottom of the band.

    The upper contour is a sum of Gaussian lumps sampled along the width, so it
    reads as heavy goo rather than a spiky graph: every rise is at least as wide
    as it is tall. Closes down to the bottom edge and fills as one silhouette.
    """
    lumps = []
    for _ in range(bumps):
        lumps.append((random.uniform(-40, W + 40),
                      random.uniform(lo, hi),
                      random.uniform(*wide)))
    # a few taller fingers reaching up out of the mass — still wider than
    # they are sharp, so they read as goo rather than as a spiky graph
    tips = []
    for _ in range(fingers):
        cx = random.uniform(60, W - 60)
        amp = random.uniform(*finger_h)
        lumps.append((cx, amp, random.uniform(*finger_w)))
        tips.append((cx, y - amp))

    def surface(x):
        # max, not sum — neighbouring lumps merge instead of stacking into hills
        h = 0.0
        for cx, amp, sg in lumps:
            h = max(h, amp * math.exp(-((x - cx) ** 2) / (2 * sg * sg)))
        return y - h

    step = 5
    pts = [(x, surface(x)) for x in range(0, W + step, step)]
    d = [f"M0 {H}", f"L{pts[0][0]} {pts[0][1]:.1f}"]
    for x, yy in pts[1:]:
        d.append(f"L{x} {yy:.1f}")
    d.append(f"L{W} {H} Z")
    return " ".join(d), tips


def build():
    s = []
    a = s.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
      f'viewBox="0 0 {W} {H}" font-family="{FONT_STACK}">')

    a("<style><![CDATA[")
    a("@keyframes weave { from { stroke-dashoffset: 100 } to { stroke-dashoffset: 0 } }\n"
      "@keyframes fade  { from { opacity: 0 } to { opacity: 1 } }\n"
      "@keyframes bleed { from { opacity: 0; transform: translateY(-14px) }\n"
      "                   to   { opacity: 1; transform: none } }\n"
      "@keyframes glow  { 0%, 100% { opacity: 0.30 } 50% { opacity: 0.62 } }\n"
      "@keyframes ooze  { 0%, 100% { transform: translateY(0) }\n"
      "                   50%      { transform: translateY(3px) } }\n"
      "@keyframes throb { 0%, 100% { opacity: 1 } 50% { opacity: 0.15 } }\n"
      ".s    { stroke-dashoffset: 0; animation: weave 1s cubic-bezier(.2,.8,.2,1) both }\n"
      ".name { animation: fade .7s ease-out 1.15s both }\n"
      ".halo { opacity: .30; animation: fade .7s ease-out 1.15s both,\n"
      "                                glow 4s ease-in-out 1.9s infinite }\n"
      ".rule { stroke-dashoffset: 0; animation: weave .6s ease-out 1.5s both }\n"
      ".tag  { animation: fade .6s ease-out 1.75s both }\n"
      ".goo  { animation: bleed .8s cubic-bezier(.3,.7,.2,1) 2.0s both,\n"
      "                   ooze 6s ease-in-out 2.8s infinite }\n"
      ".dot  { animation: throb 1.8s ease-in-out infinite }\n"
      "@media (prefers-reduced-motion: reduce) {\n"
      "  .s, .name, .halo, .rule, .tag, .goo, .dot { animation: none }\n"
      "  .halo { opacity: .38 }\n"
      "}")
    a("]]></style>")

    a("<defs>"
      f'<radialGradient id="bglow" cx="0.5" cy="0.46" r="0.62">'
      f'<stop offset="0" stop-color="{DEEP}" stop-opacity="0.5"/>'
      f'<stop offset="0.55" stop-color="{DEEP}" stop-opacity="0.12"/>'
      f'<stop offset="1" stop-color="{DEEP}" stop-opacity="0"/></radialGradient>'
      f'<linearGradient id="gooG" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="#3a0f14"/>'
      f'<stop offset="0.5" stop-color="#1a0507"/>'
      f'<stop offset="1" stop-color="#050101"/></linearGradient>'
      f'<linearGradient id="vig" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="#0a0a0a" stop-opacity="1"/>'
      f'<stop offset="0.18" stop-color="#0a0a0a" stop-opacity="0"/>'
      f'<stop offset="0.82" stop-color="#0a0a0a" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="#0a0a0a" stop-opacity="1"/></linearGradient>'
      "</defs>")

    a(f'<rect width="{W}" height="{H}" fill="#0a0a0a"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#bglow)"/>')

    # webbing anchored in both top corners, weaving inward
    webs = []
    webs += [(d, i) for i, d in enumerate(
        corner_web(0, 0, 340, 8, 5, (0.0, math.pi / 2)))]
    webs += [(d, i) for i, d in enumerate(
        corner_web(W, 0, 340, 8, 5, (math.pi / 2, math.pi)))]
    for d, i in webs:
        col = CRIMSON if i % 5 == 4 else WEB
        op = 0.26 if col == CRIMSON else 0.46
        a(f'<path class="s" d="{d}" fill="none" stroke="{col}" '
          f'stroke-width="0.9" stroke-opacity="{op}" pathLength="100" '
          f'stroke-dasharray="100" style="animation-delay:{0.05 + i * 0.09:.2f}s"/>')

    a(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')

    # name — crimson halo behind, bone on top
    cx = W // 2
    ny = 108
    for cls, fill, dx, dy, extra in (
            ("halo", CRIMSON, 3, 3, ""),
            ("name", BONE, 0, 0, "")):
        a(f'<text class="{cls}" x="{cx + dx}" y="{ny + dy}" '
          f'font-size="72" font-weight="700" letter-spacing="6" '
          f'text-anchor="middle" fill="{fill}"{extra}>{NAME}</text>')

    a(f'<line class="rule" x1="{cx - 210}" y1="{ny + 26}" x2="{cx + 210}" '
      f'y2="{ny + 26}" stroke="{CRIMSON}" stroke-width="1.2" '
      f'stroke-opacity="0.8" pathLength="100" stroke-dasharray="100"/>')

    a(f'<text class="tag" x="{cx}" y="{ny + 54}" font-size="15" '
      f'letter-spacing="3.5" text-anchor="middle" fill="{MUTED}">'
      f'{TAGLINE}</text>')

    # symbiote mass flooding the bottom, in two layers for depth. The front
    # layer is rim-lit in crimson so the silhouette reads against the band.
    back, _ = drip_path(MASS_Y - 7, 18, 10, 30, wide=(30, 62),
                        fingers=4, finger_h=(30, 52), finger_w=(15, 22))
    front, tips = drip_path(MASS_Y + 2, 24, 7, 24, wide=(20, 46),
                            fingers=5, finger_h=(24, 44), finger_w=(12, 19))
    a('<g class="goo">')
    a(f'<path d="{back}" fill="#180509" opacity="0.9"/>')
    a(f'<path d="{back}" fill="none" stroke="{DEEP}" stroke-width="0.9" '
      f'stroke-opacity="0.3"/>')
    a(f'<path d="{front}" fill="url(#gooG)"/>')
    a(f'<path d="{front}" fill="none" stroke="{CRIMSON}" stroke-width="1.2" '
      f'stroke-opacity="0.55"/>')
    a(f'<path d="{front}" fill="none" stroke="{FIRE}" stroke-width="4" '
      f'stroke-opacity="0.1"/>')
    spread = sorted(tips)
    for tx, ty in (spread[0], spread[len(spread) // 2], spread[-1]):
        r = random.uniform(1.8, 3.0)
        a(f'<ellipse cx="{tx + random.uniform(-5, 5):.1f}" '
          f'cy="{ty - random.uniform(8, 18):.1f}" rx="{r:.1f}" '
          f'ry="{r * 1.4:.1f}" fill="{CRIMSON}" fill-opacity="0.45"/>')
    a("</g>")

    # spider-sense tell, bottom-left
    a(f'<text class="tag" x="22" y="26" font-size="11" fill="{MUTED}" '
      f'style="animation-delay:2.3s">spider-sense :: ACTIVE</text>')
    a(f'<circle class="dot" cx="{W - 24}" cy="22" r="3.5" fill="{FIRE}"/>')

    a("</svg>")
    DST.write_text("\n".join(s), encoding="utf-8")
    print(f"wrote {DST.relative_to(ROOT)} — {DST.stat().st_size} bytes")


if __name__ == "__main__":
    build()
