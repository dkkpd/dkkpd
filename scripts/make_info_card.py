#!/usr/bin/env python3
"""
Neofetch-style info card SVG for the profile README.
Each line fades and slides in with a short stagger.
"""
import os
import re

from window_chrome import INFO_DISPLAY_W, append_titlebar, intrinsic_titlebar_h

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
PORTRAIT_SVG = os.path.join(HERE, "..", "dkkpd-ascii.svg")

CANVAS_W = INFO_DISPLAY_W
WINDOW_TITLE = "About Me"
PAD = 20

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
TEXT = "#e6edf3"
MUTED = "#7d8590"

ROWS = [
    ("Host", "#22d3ee", "dkkpd@github"),
    ("OS", "#39d353", "University of Waterloo"),
    ("Kernel", "#f778ba", "Math / Computer Science"),
    ("Role", "#d2a8ff", "Student"),
]

STATIC = bool(os.environ.get("STATIC"))
LINE_H = 34
BODY_FONT = 16


def portrait_display_height():
    with open(PORTRAIT_SVG, encoding="utf-8") as f:
        svg = f.read()
    return int(float(re.search(r'height="([0-9.]+)"', svg).group(1)))


def render():
    canvas_h = portrait_display_height()
    content_h = (len(ROWS) - 1) * LINE_H + BODY_FONT
    start_y = (canvas_h - content_h) / 2 + BODY_FONT * 0.75

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{canvas_h}" '
        f'viewBox="0 0 {CANVAS_W} {canvas_h}" font-family="ui-monospace, SFMono-Regular, '
        f'Menlo, Consolas, monospace">',
        "<defs>"
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
        f"</linearGradient></defs>",
        f'<rect width="{CANVAS_W}" height="{canvas_h}" rx="12" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{canvas_h-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1"/>',
    ]

    append_titlebar(
        parts, CANVAS_W, WINDOW_TITLE,
        display_w=INFO_DISPLAY_W, intrinsic_w=CANVAS_W,
        pad=PAD, frame=FRAME, title_color=TITLE_TEXT,
    )

    for i, (label, color, value) in enumerate(ROWS):
        y = start_y + i * LINE_H
        delay = i * 0.12
        block = (
            f'<text x="{PAD}" y="{y:.1f}" font-size="{BODY_FONT}">'
            f'<tspan fill="{color}">{label}</tspan>'
            f'<tspan fill="{MUTED}">: </tspan>'
            f'<tspan fill="{TEXT}">{value}</tspan></text>'
        )
        if STATIC:
            parts.append(block)
            continue
        parts.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" '
            f'dur="0.35s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="-8 0" to="0 0" begin="{delay:.2f}s" dur="0.35s" fill="freeze"/>'
            f"{block}</g>"
        )

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    svg = render()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg)} bytes)")
