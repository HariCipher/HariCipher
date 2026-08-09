"""
Generates web-divider.svg — the sagging web strand used as a section rule
between every README block.

Animation is CSS, not SMIL: GitHub renders README art through <img>, where
Chrome runs CSS keyframes but not SMIL. Static state is the settled state, so
the divider never renders blank.

Usage:
    python3 scripts/make_divider.py
"""

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "web-divider.svg"

W, H = 860, 46
CRIMSON = "#E62429"
WEB = "#3A3F44"
BONE = "#EDEDED"

random.seed(1962)  # Amazing Fantasy #15 — keeps regenerated output stable

# (sag, colour, opacity, stroke width)
THREADS = [(12, WEB, 0.75, 1.0), (20, CRIMSON, 0.45, 0.9)]

MID = H / 2
SPIDER_X = W / 2 + 120


def sag_y(x, sag):
    """Height of a quadratic sag at x, matching the drawn curve."""
    t = x / W
    return MID + sag * 4 * t * (1 - t)


def build():
    s = []
    a = s.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
      f'viewBox="0 0 {W} {H}">')

    a("<style><![CDATA[")
    a("@keyframes weave { from { stroke-dashoffset: 100 } to { stroke-dashoffset: 0 } }\n"
      "@keyframes fade  { from { opacity: 0 } to { opacity: 1 } }\n"
      "@keyframes sway  { 0%, 100% { transform: translateX(0) }\n"
      "                   50%      { transform: translateX(5px) } }\n"
      ".t { stroke-dashoffset: 0; animation: weave 1.1s cubic-bezier(.2,.8,.2,1) both }\n"
      ".x { stroke-dashoffset: 0; animation: weave .3s ease-out both }\n"
      ".s { animation: fade .5s ease-out 1.2s both, sway 5s ease-in-out 1.7s infinite }\n"
      "@media (prefers-reduced-motion: reduce) {\n"
      "  .t, .x, .s { animation: none }\n"
      "}")
    a("]]></style>")

    # main sagging threads, drawn left-to-right
    for i, (sag, col, op, sw) in enumerate(THREADS):
        a(f'<path class="t" d="M0 {MID:.1f} Q{W / 2:.1f} {MID + sag * 2:.1f} '
          f'{W} {MID:.1f}" fill="none" stroke="{col}" stroke-width="{sw}" '
          f'stroke-opacity="{op}" pathLength="100" stroke-dasharray="100" '
          f'style="animation-delay:{i * 0.18:.2f}s"/>')

    # cross-stitches between the two threads
    n = 23
    for i in range(n):
        x = (i + 0.5) * (W / n) + random.uniform(-6, 6)
        y1 = sag_y(x, THREADS[0][0] * 2)
        y2 = sag_y(x, THREADS[1][0] * 2)
        a(f'<line class="x" x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}" '
          f'stroke="{WEB}" stroke-width="0.7" stroke-opacity="0.55" '
          f'pathLength="100" stroke-dasharray="100" '
          f'style="animation-delay:{0.45 + i * 0.025:.2f}s"/>')

    # small spider rappelling off the lower thread
    sy = sag_y(SPIDER_X, THREADS[1][0] * 2)
    body_y = sy + 9
    a(f'<g class="s">')
    a(f'<line x1="{SPIDER_X:.1f}" y1="{sy:.1f}" x2="{SPIDER_X:.1f}" '
      f'y2="{body_y - 3:.1f}" stroke="{WEB}" stroke-width="0.7"/>')
    for dx, dy in ((-5, -3), (-5, 2), (5, -3), (5, 2)):
        a(f'<path d="M{SPIDER_X:.1f} {body_y:.1f} q{dx / 2:.1f} {dy:.1f} '
          f'{dx} {dy + 2:.1f}" fill="none" stroke="{BONE}" stroke-width="0.7" '
          f'stroke-opacity="0.85"/>')
    a(f'<ellipse cx="{SPIDER_X:.1f}" cy="{body_y:.1f}" rx="2.4" ry="3" fill="{BONE}"/>')
    a(f'<circle cx="{SPIDER_X:.1f}" cy="{body_y - 3.4:.1f}" r="1.4" fill="{BONE}"/>')
    a("</g>")

    a("</svg>")
    DST.write_text("\n".join(s), encoding="utf-8")
    print(f"wrote {DST.relative_to(ROOT)} — {DST.stat().st_size} bytes")


if __name__ == "__main__":
    build()
