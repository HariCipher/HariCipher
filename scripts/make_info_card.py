"""
Generates info-card.svg — the neofetch-style panel beside the spider in the
README hero. Content comes from the resume.

Animation is CSS, not SMIL, for the reason explained in make_spider_svg.py:
GitHub renders README art through <img>, where Chrome runs CSS keyframes but
not SMIL. Static state is the settled state, so the card never renders empty.

Usage:
    python3 scripts/make_info_card.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "info-card.svg"

W, H = 480, 376
BAR_H = 30
PAD = 20
LABEL_X = PAD + 88

BONE = "#EDEDED"
CRIMSON = "#E62429"
FIRE = "#FF3B30"
DIM = "#8E1519"
BORDER = "#2A2A2A"
MUTED = "#6E7681"

FONT_STACK = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

ROWS = [
    ("Role", "SOC Analyst Intern — Gardiyan"),
    ("Term", "Sep 2025 – Jan 2026 · Turkey (remote)"),
    ("SIEM", "Splunk · Wazuh"),
    ("Forensics", "Wireshark · tshark · PCAP · C2 ident"),
    ("OS", "Kali Linux · Windows 10"),
    ("Lang", "Python · Bash"),
    ("Focus", "Detection Eng · DFIR · Threat Hunting"),
    ("Edu", "B.Tech CSE · Poornima Univ · '28"),
    ("Loc", "Palakkad, Kerala, IN"),
]

SWATCHES = [CRIMSON, FIRE, DIM, "#4a1114", BONE, MUTED, "#3A3F44", "#1a1a1a"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    s = []
    a = s.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
      f'viewBox="0 0 {W} {H}" font-family="{FONT_STACK}">')

    a("<style><![CDATA[")
    a("@keyframes rise { from { opacity: 0; transform: translateY(6px) }\n"
      "                  to   { opacity: 1; transform: none } }\n"
      "@keyframes fade { from { opacity: 0 } to { opacity: 1 } }\n"
      "@keyframes throb{ 0%, 100% { opacity: 1 } 50% { opacity: 0.1 } }\n"
      ".r  { animation: rise .4s ease-out both }\n"
      ".sw { animation: fade .3s ease-out both }\n"
      ".dot{ animation: throb 1.6s ease-in-out infinite }\n"
      "@media (prefers-reduced-motion: reduce) {\n"
      "  .r, .sw, .dot { animation: none }\n"
      "}")
    a("]]></style>")

    a("<defs>"
      '<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#141013"/>'
      '<stop offset="1" stop-color="#0a0a0a"/></linearGradient>'
      '<radialGradient id="iglow" cx="0.85" cy="0.1" r="0.75">'
      f'<stop offset="0" stop-color="{CRIMSON}" stop-opacity="0.14"/>'
      f'<stop offset="1" stop-color="{CRIMSON}" stop-opacity="0"/></radialGradient>'
      "</defs>")

    a(f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>')
    a(f'<rect width="{W}" height="{H}" rx="12" fill="url(#iglow)"/>')
    a(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" '
      f'fill="none" stroke="{BORDER}"/>')
    a(f'<line x1="0" y1="{BAR_H}" x2="{W}" y2="{BAR_H}" stroke="{BORDER}"/>')
    for i, col in enumerate((CRIMSON, DIM, "#4a1114")):
        a(f'<circle cx="{20 + i * 16}" cy="15" r="5" fill="{col}"/>')
    a(f'<text x="{W // 2}" y="19" fill="{MUTED}" font-size="12" '
      'text-anchor="middle">hari@web ~$ neofetch --spider</text>')

    def row(delay, body):
        a(f'<g class="r" style="animation-delay:{delay:.2f}s">{body}</g>')

    row(0.15,
        f'<text x="{PAD}" y="60" font-size="14" font-weight="700">'
        f'<tspan fill="{CRIMSON}">hari</tspan>'
        f'<tspan fill="{MUTED}">@</tspan>'
        f'<tspan fill="{BONE}">HariCipher</tspan></text>'
        f'<line x1="152" y1="56" x2="{W - PAD}" y2="56" stroke="{BORDER}"/>')

    y = 84
    for i, (label, value) in enumerate(ROWS):
        row(0.30 + i * 0.10,
            f'<text x="{PAD}" y="{y}" font-size="11.5" fill="{CRIMSON}" '
            f'font-weight="700">{esc(label)}</text>'
            f'<text x="{LABEL_X}" y="{y}" font-size="11.5" fill="{BONE}">'
            f'{esc(value)}</text>')
        y += 22

    a(f'<line x1="{PAD}" y1="{y - 6}" x2="{W - PAD}" y2="{y - 6}" stroke="{BORDER}"/>')
    row(1.30,
        f'<text x="{PAD}" y="{y + 16}" font-size="11.5" fill="{CRIMSON}" '
        f'font-weight="700">Spider-Sense</text>'
        f'<text x="{LABEL_X}" y="{y + 16}" font-size="11.5" fill="{BONE}">'
        f'online — watching the logs</text>'
        f'<circle class="dot" cx="{PAD + 300}" cy="{y + 12}" r="4" fill="{FIRE}"/>')

    sw_y = y + 32
    for i, col in enumerate(SWATCHES):
        a(f'<rect class="sw" x="{PAD + i * 22}" y="{sw_y}" width="18" height="10" '
          f'rx="2" fill="{col}" style="animation-delay:{1.45 + i * 0.05:.2f}s"/>')

    a("</svg>")
    DST.write_text("\n".join(s), encoding="utf-8")
    print(f"wrote {DST.relative_to(ROOT)} — {DST.stat().st_size // 1024}KB")


if __name__ == "__main__":
    build()
