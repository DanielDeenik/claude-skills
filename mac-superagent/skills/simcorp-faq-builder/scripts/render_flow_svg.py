#!/usr/bin/env python3
"""
Render a simple vertical flowchart to SVG (and PNG via cairosvg) WITHOUT a browser
or mermaid-cli. SharePoint/ClickUp cannot render mermaid, so this produces real
image files you upload like any screenshot.

Define diagrams as Python dicts (steps + optional side notes) and call render().
No hardcoded content here — the caller supplies the steps.
"""
import html

BOX_W, NOTE_W = 380, 300
X_BOX, X_NOTE = 40, 450
PAD_X, LH, FS = 16, 20, 14
GAP = 34
COLORS = {
    "step": ("#e8f4ff", "#3b82f6"),
    "gate": ("#fff4e5", "#f59e0b"),
    "done": ("#e7f9ed", "#22a565"),
    "head": ("#1f2937", "#111827"),
}


def wrap(text, maxchars=44):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= maxchars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def esc(s):
    return html.escape(s, quote=True)


def render(title, steps, out_svg):
    """steps: list of dicts {text, kind(step/gate/done/head), note(optional)}"""
    y = 60
    elems, centers = [], []
    for s in steps:
        lines = wrap(s["text"])
        h = len(lines) * LH + 20
        fill, stroke = COLORS.get(s.get("kind", "step"), COLORS["step"])
        tcol = "#ffffff" if s.get("kind") == "head" else "#0f172a"
        cy = y + h / 2
        centers.append(cy)
        elems.append(
            f'<rect x="{X_BOX}" y="{y}" width="{BOX_W}" height="{h}" rx="10" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )
        ty = y + 24
        for ln in lines:
            elems.append(
                f'<text x="{X_BOX + PAD_X}" y="{ty}" font-family="Segoe UI,Arial" '
                f'font-size="{FS}" fill="{tcol}">{esc(ln)}</text>'
            )
            ty += LH
        if s.get("note"):
            nlines = wrap(s["note"], 40)
            nh = len(nlines) * (LH - 2) + 16
            ny = cy - nh / 2
            elems.append(
                f'<rect x="{X_NOTE}" y="{ny}" width="{NOTE_W}" height="{nh}" rx="8" '
                f'fill="#f3e8ff" stroke="#8b5cf6" stroke-width="1.5" stroke-dasharray="5 3"/>'
            )
            elems.append(
                f'<line x1="{X_BOX + BOX_W}" y1="{cy}" x2="{X_NOTE}" y2="{cy}" '
                f'stroke="#8b5cf6" stroke-width="1.3" stroke-dasharray="4 3"/>'
            )
            nty = ny + 18
            for ln in nlines:
                elems.append(
                    f'<text x="{X_NOTE + 12}" y="{nty}" font-family="Segoe UI,Arial" '
                    f'font-size="12" fill="#4c1d95">{esc(ln)}</text>'
                )
                nty += LH - 2
        y += h + GAP

    arrows = []
    for i in range(len(centers) - 1):
        y1 = centers[i] + (wrap(steps[i]["text"]).__len__() * LH + 20) / 2
        y2 = centers[i + 1] - (wrap(steps[i + 1]["text"]).__len__() * LH + 20) / 2
        cx = X_BOX + BOX_W / 2
        arrows.append(
            f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" stroke="#64748b" '
            f'stroke-width="2" marker-end="url(#ar)"/>'
        )

    W, H = X_NOTE + NOTE_W + 40, y + 10
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="Segoe UI,Arial">',
        '<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" '
        'orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#64748b"/></marker></defs>',
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>',
        f'<text x="{X_BOX}" y="34" font-size="18" font-weight="bold" '
        f'fill="#0f172a">{esc(title)}</text>',
    ] + arrows + elems + ["</svg>"]
    open(out_svg, "w").write("\n".join(svg))
    return out_svg
