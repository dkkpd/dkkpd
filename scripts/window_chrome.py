"""Shared macOS-style window chrome for profile SVG panels."""

# README display widths — each About Me panel; together they match the heatmap (860px).
PORTRAIT_DISPLAY_W = 430
INFO_DISPLAY_W = 430
ABOUT_ROW_W = PORTRAIT_DISPLAY_W + INFO_DISPLAY_W

# Target on-screen sizes (px) when rendered at the widths above.
VISUAL_TITLEBAR_H = 28
VISUAL_TITLE_FONT = 12
VISUAL_DOT_R = 5.5
VISUAL_DOT_STEP = 17


def intrinsic_px(visual_px, intrinsic_w, display_w):
    return visual_px * intrinsic_w / display_w


def intrinsic_titlebar_h(intrinsic_w, display_w, visual_h=VISUAL_TITLEBAR_H):
    return intrinsic_px(visual_h, intrinsic_w, display_w)


def display_height(intrinsic_w, intrinsic_h, display_w):
    return round(intrinsic_h * display_w / intrinsic_w)


def append_titlebar(parts, canvas_w, title, *, display_w, intrinsic_w, pad, frame, title_color):
    bar_h = intrinsic_titlebar_h(intrinsic_w, display_w)
    dot_r = intrinsic_px(VISUAL_DOT_R, intrinsic_w, display_w)
    dot_step = intrinsic_px(VISUAL_DOT_STEP, intrinsic_w, display_w)
    font_size = intrinsic_px(VISUAL_TITLE_FONT, intrinsic_w, display_w)
    cy = bar_h / 2
    ty = cy + font_size * 0.18

    parts.append(f'<line x1="0" y1="{bar_h}" x2="{canvas_w}" y2="{bar_h}" stroke="{frame}"/>')
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(
            f'<circle cx="{pad + i * dot_step}" cy="{cy:.1f}" r="{dot_r:.2f}" fill="{dotcol}"/>'
        )
    parts.append(
        f'<text x="{canvas_w/2}" y="{ty:.1f}" fill="{title_color}" font-size="{font_size:.1f}" '
        f'text-anchor="middle" font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif">'
        f"{title}</text>"
    )
    return bar_h
