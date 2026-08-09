"""
Renders assets/spider.jpeg into spider-ascii.svg — an animated ASCII hero panel.

Three acts:

  act 1  0.0 - 1.6s   the web spins itself: 12 radial anchor strands shoot out
                      from centre, then 7 spiral rings chase them around
  act 2  1.5 - 3.4s   the spider materialises: rows unzip outward from the
                      panel's spine, innermost first, flickering before settling
  act 3  3.4s - loop  idle: crimson threat-pulse sweeps down every 6s, web
                      strands breathe, a handful of cells jitter characters

Animation is CSS @keyframes, not SMIL: GitHub embeds README art through <img>,
and Chrome does not run SMIL in that context (it does run CSS). Every element's
static state is its *finished* state, so if animation is unavailable — reduced
motion, an odd renderer — the panel still shows the settled spider rather than
an empty box.

Density ramp and aspect compensation follow ascii_render.py.

Usage:
    python3 scripts/make_spider_svg.py
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "spider.jpeg"
DST = ROOT / "spider-ascii.svg"

CHARS = "@%#*+=-:. "[::-1]  # dark -> light density ramp
COLS = 140
CELL_ASPECT = 2.05  # character cells are taller than wide
GAMMA = 0.68
INK = 0.24  # below this a cell is background, not part of the spider

FONT_SIZE = 9.0
CHAR_W = FONT_SIZE * 0.6
LINE_H = 9.4
PAD = 20.0
BAR_H = 30.0

BONE = "#EDEDED"
CRIMSON = "#E62429"
DEEP = "#8E1519"
WEB = "#3A3F44"
BORDER = "#2A2A2A"
MUTED = "#6E7681"

FONT_STACK = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

random.seed(1962)  # Amazing Fantasy #15 — keeps regenerated output stable


def ascii_grid(path, cols=COLS):
    """(grid of chars, grid of 0..1 brightness) for the source image."""
    img = ImageOps.autocontrast(Image.open(path).convert("L"), cutoff=1)
    w, h = img.size
    cell_w = w / cols
    rows = int(h / (cell_w * CELL_ASPECT))
    img = img.resize((cols, rows), Image.LANCZOS)
    px = img.tobytes()  # mode "L" -> one byte per pixel, row-major

    chars, vals = [], []
    for y in range(rows):
        crow, vrow = [], []
        for x in range(cols):
            v = (px[y * cols + x] / 255.0) ** GAMMA
            crow.append(CHARS[int(v * (len(CHARS) - 1))])
            vrow.append(v)
        chars.append(crow)
        vals.append(vrow)
    return trim(chars, vals)


def trim(chars, vals, ink=INK):
    """Drop fully-empty border rows/columns so the spider fills the panel
    instead of floating in dead space."""
    keep_r = [y for y, row in enumerate(vals) if max(row) >= ink]
    keep_c = [x for x in range(len(vals[0])) if max(r[x] for r in vals) >= ink]
    y0, y1 = keep_r[0], keep_r[-1] + 1
    x0, x1 = keep_c[0], keep_c[-1] + 1
    return ([r[x0:x1] for r in chars[y0:y1]], [r[x0:x1] for r in vals[y0:y1]])


def bucket(v):
    """Brightness -> fill. Bright core is bone white, the antialiased halo
    around it bleeds crimson, which is what gives the symbiote glow."""
    if v >= 0.42:
        return BONE
    if v >= 0.29:
        return CRIMSON
    return DEEP


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def web_paths(cx, cy, radius, radials=12, rings=7):
    """Radial anchor strands + sagging spiral rings, as SVG path 'd' strings."""
    out = []

    for i in range(radials):
        a = (2 * math.pi * i / radials) - math.pi / 2
        mx = cx + math.cos(a) * radius * 0.5
        my = cy + math.sin(a) * radius * 0.5
        out.append(("radial",
                    f"M{cx:.1f},{cy:.1f} Q{mx + 5:.1f},{my + 6:.1f} "
                    f"{cx + math.cos(a) * radius:.1f},"
                    f"{cy + math.sin(a) * radius:.1f}"))

    for r in range(1, rings + 1):
        rr = radius * (0.20 + 0.80 * (r / rings) ** 1.25)
        d = ""
        for i in range(radials + 1):
            a = (2 * math.pi * i / radials) - math.pi / 2
            x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
            if i == 0:
                d = f"M{x:.1f},{y:.1f}"
                continue
            prev = (2 * math.pi * (i - 1) / radials) - math.pi / 2
            amid = (prev + a) / 2
            # each thread between two anchors dips inward: real webs sag
            mx = cx + math.cos(amid) * rr * 0.88
            my = cy + math.sin(amid) * rr * 0.88
            d += f" Q{mx:.1f},{my:.1f} {x:.1f},{y:.1f}"
        out.append(("ring", d))

    return out


def row_delay(y, rows):
    """Innermost rows land first, so the spider grows out of the web centre."""
    mid = (rows - 1) / 2
    return 1.50 + (abs(y - mid) / mid) * 1.55


def build():
    chars, vals = ascii_grid(SRC)
    rows, cols = len(chars), len(chars[0])

    content_w = cols * CHAR_W
    ascii_top = BAR_H + 22.0
    ascii_h = rows * LINE_H
    footer_y = ascii_top + ascii_h + 24.0
    W = PAD * 2 + content_w
    H = footer_y + 26.0

    cx = PAD + content_w / 2
    cy = ascii_top + ascii_h / 2 - 6
    radius = min(content_w / 2, ascii_h / 2) * 1.06
    sweep_to = footer_y - 30 - BAR_H

    s = []
    a = s.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
      f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="{FONT_STACK}">')

    # ---- style / animation ------------------------------------------------
    a("<style><![CDATA[")
    a("@keyframes weave  { from { stroke-dashoffset: 100 } to { stroke-dashoffset: 0 } }\n"
      "@keyframes unzip  { 0%   { opacity: 0;   transform: scaleX(0.18) }\n"
      "                    30%  { opacity: 0.4; transform: scaleX(0.55) }\n"
      "                    62%  { opacity: 1;   transform: scaleX(1) }\n"
      "                    74%  { opacity: 0.45 }\n"
      "                    100% { opacity: 1;   transform: scaleX(1) } }\n"
      "@keyframes fade   { from { opacity: 0 } to { opacity: 1 } }\n"
      "@keyframes blink  { 0%, 100% { opacity: 0 } 50% { opacity: 0.9 } }\n"
      "@keyframes breathe{ 0%, 100% { opacity: 0.42 } 50% { opacity: 0.24 } }\n"
      "@keyframes throb  { 0%, 100% { opacity: 1 } 50% { opacity: 0.12 } }")
    a(f"@keyframes drop   {{ from {{ transform: translateY(0) }}\n"
      f"                    to   {{ transform: translateY({sweep_to:.0f}px) }} }}")
    a(".strand { stroke-dashoffset: 0;\n"
      "          animation: weave 0.7s cubic-bezier(.2,.8,.2,1) both }\n"
      ".mesh   { opacity: .42; animation: breathe 4.5s ease-in-out 3.4s infinite }\n"
      ".row    { animation: unzip .5s cubic-bezier(.2,.8,.2,1) both }\n"
      ".jit    { opacity: 0; animation: blink .22s steps(2,end) infinite }\n"
      ".late   { animation: fade .5s ease-out 3.2s both }\n"
      ".dot    { animation: throb 1.8s ease-in-out infinite }\n"
      ".sweep  { opacity: 0; animation: fade .4s ease-out 3.4s forwards,\n"
      "                                 drop 6s linear 3.4s infinite }")
    a("/* animation is decoration; the settled panel is the real content */\n"
      "@media (prefers-reduced-motion: reduce) {\n"
      "  .strand, .mesh, .row, .late, .dot { animation: none }\n"
      "  .jit, .sweep { animation: none; opacity: 0 }\n"
      "}")
    a("]]></style>")

    a("<defs>"
      '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#141013"/>'
      '<stop offset="0.55" stop-color="#0a0a0a"/>'
      '<stop offset="1" stop-color="#0d0709"/></linearGradient>'
      '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
      f'<stop offset="0" stop-color="{CRIMSON}" stop-opacity="0.16"/>'
      f'<stop offset="1" stop-color="{CRIMSON}" stop-opacity="0"/></radialGradient>'
      '<linearGradient id="pulse" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="{CRIMSON}" stop-opacity="0"/>'
      f'<stop offset="0.5" stop-color="{CRIMSON}" stop-opacity="0.22"/>'
      f'<stop offset="1" stop-color="{CRIMSON}" stop-opacity="0"/></linearGradient>'
      "</defs>")

    # ---- terminal chrome --------------------------------------------------
    a(f'<rect width="{W:.0f}" height="{H:.0f}" rx="12" fill="url(#bg)"/>')
    a(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{content_w * 0.46:.0f}" '
      f'ry="{ascii_h * 0.48:.0f}" fill="url(#glow)"/>')
    a(f'<rect x="0.5" y="0.5" width="{W - 1:.0f}" height="{H - 1:.0f}" rx="12" '
      f'fill="none" stroke="{BORDER}"/>')
    a(f'<line x1="0" y1="{BAR_H:.0f}" x2="{W:.0f}" y2="{BAR_H:.0f}" '
      f'stroke="{BORDER}"/>')
    for i, col in enumerate((CRIMSON, DEEP, "#4a1114")):
        a(f'<circle cx="{20 + i * 16}" cy="15" r="5" fill="{col}"/>')
    a(f'<text x="{W / 2:.0f}" y="19" fill="{MUTED}" font-size="12" '
      'text-anchor="middle">hari@web ~$ ./trace --spider</text>')

    # ---- act 1: the web spins itself -------------------------------------
    a(f'<g class="mesh" fill="none" stroke="{WEB}" stroke-width="0.9" '
      'stroke-linecap="round">')
    for i, (kind, d) in enumerate(web_paths(cx, cy, radius)):
        # radials fire first, spirals chase them outward
        delay = 0.10 + i * 0.045 if kind == "radial" else 0.62 + (i - 12) * 0.13
        dur = 0.55 if kind == "radial" else 0.85
        stroke = CRIMSON if kind == "radial" and i % 3 == 0 else WEB
        op = 0.55 if kind == "radial" else 0.85
        a(f'<path class="strand" d="{d}" pathLength="100" stroke-dasharray="100" '
          f'stroke="{stroke}" stroke-opacity="{op}" '
          f'style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s"/>')
    a("</g>")

    # ---- act 2: the spider materialises ----------------------------------
    # Every run of inked cells is its own <text> pinned to the grid with an
    # explicit x and textLength. Whitespace in SVG text is unreliable across
    # renderers — positioning each run keeps the grid exact everywhere.
    a(f'<g font-size="{FONT_SIZE:.1f}">')
    for y in range(rows):
        runs, x = [], 0
        while x < cols:
            if vals[y][x] < INK:
                x += 1
                continue
            start = x
            while x < cols and vals[y][x] >= INK:
                x += 1
            runs.append((start, x))
        if not runs:
            continue

        row_y = ascii_top + y * LINE_H
        a(f'<g class="row" style="transform-origin:{cx:.1f}px {row_y:.1f}px;'
          f'animation-delay:{row_delay(y, rows):.2f}s">')
        for start, end in runs:
            n = end - start
            a(f'<text x="{PAD + start * CHAR_W:.1f}" y="{row_y:.1f}" '
              f'textLength="{n * CHAR_W:.2f}" lengthAdjust="spacingAndGlyphs">')
            buf, buf_fill = [], None
            for i in range(start, end):
                fill = bucket(vals[y][i])
                if fill != buf_fill and buf:
                    a(f'<tspan fill="{buf_fill}">{esc("".join(buf))}</tspan>')
                    buf = []
                buf_fill = fill
                buf.append(chars[y][i])
            a(f'<tspan fill="{buf_fill}">{esc("".join(buf))}</tspan>')
            a("</text>")
        a("</g>")
    a("</g>")

    # ---- act 3: idle jitter + threat pulse -------------------------------
    a(f'<g font-size="{FONT_SIZE:.1f}" fill="{CRIMSON}">')
    for _ in range(16):
        # jitter only where there is ink, so it reads as the suit twitching
        # rather than as random noise in the void
        for _try in range(80):
            jy, jx = random.randrange(rows), random.randrange(cols)
            if vals[jy][jx] >= 0.35:
                break
        else:
            continue
        a(f'<text class="jit" x="{PAD + jx * CHAR_W:.1f}" '
          f'y="{ascii_top + jy * LINE_H:.1f}" '
          f'style="animation-delay:{3.6 + random.uniform(0, 5.5):.2f}s">'
          f'{esc(random.choice("#%*+=@"))}</text>')
    a("</g>")

    a(f'<rect class="sweep" x="1" y="{BAR_H + 1:.0f}" width="{W - 2:.0f}" '
      'height="34" fill="url(#pulse)"/>')

    # ---- footer status line ----------------------------------------------
    a(f'<line x1="{PAD:.0f}" y1="{footer_y - 14:.1f}" x2="{W - PAD:.0f}" '
      f'y2="{footer_y - 14:.1f}" stroke="{BORDER}"/>')
    a('<g class="late">'
      f'<text x="{PAD:.0f}" y="{footer_y:.1f}" font-size="10.5">'
      f'<tspan fill="{CRIMSON}">spider-sense</tspan>'
      f'<tspan fill="{MUTED}"> :: </tspan>'
      f'<tspan fill="{BONE}">ACTIVE</tspan>'
      f'<tspan fill="{MUTED}">   threads </tspan><tspan fill="{BONE}">8</tspan>'
      f'<tspan fill="{MUTED}">   signal </tspan><tspan fill="{BONE}">nominal</tspan>'
      "</text>"
      f'<circle class="dot" cx="{W - PAD - 6:.0f}" cy="{footer_y - 4:.1f}" '
      f'r="3.5" fill="{CRIMSON}"/></g>')

    a("</svg>")

    DST.write_text("\n".join(s), encoding="utf-8")
    print(f"wrote {DST.relative_to(ROOT)} — {DST.stat().st_size // 1024}KB, "
          f"grid {rows}x{cols}, canvas {W:.0f}x{H:.0f}")


if __name__ == "__main__":
    build()
