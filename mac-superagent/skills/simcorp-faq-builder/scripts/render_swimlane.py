#!/usr/bin/env python3
"""
Render a horizontal swimlane workflow to SVG (+ PNG via cairosvg) without a browser.
Lanes = actors/systems (rows); steps placed in (lane,col) cells; sequential elbow
arrows; amber gate chips under steps; a red 'exceptions' band at the bottom with
dashed connectors. Content is supplied by the caller — nothing hardcoded here.
"""
import cairosvg, html

GUTTER, COLW, LANEH = 200, 232, 128
BOXW, BOXH = 196, 84
PAD_TOP = 54
EXC_H = 150


def esc(s): return html.escape(s, quote=True)


def wrap(text, maxchars):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 <= maxchars:
            cur = (cur + " " + w).strip()
        else:
            out.append(cur); cur = w
    if cur: out.append(cur)
    return out or [""]


def render(title, lanes, steps, ncols, exceptions, out_svg, out_png=None):
    H = PAD_TOP + len(lanes) * LANEH + EXC_H + 30
    W = GUTTER + ncols * COLW + 30
    e = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI,Arial">',
        '<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#475569"/></marker>'
        '<marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#dc2626"/></marker></defs>',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        f'<text x="20" y="34" font-size="20" font-weight="bold" fill="#0f172a">{esc(title)}</text>',
    ]
    # lane bands + labels
    for i, (lname, col) in enumerate(lanes):
        y = PAD_TOP + i * LANEH
        band = "#f8fafc" if i % 2 == 0 else "#f1f5f9"
        e.append(f'<rect x="0" y="{y}" width="{W}" height="{LANEH}" fill="{band}"/>')
        e.append(f'<rect x="0" y="{y}" width="{GUTTER}" height="{LANEH}" fill="{col}" opacity="0.16"/>')
        e.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#e2e8f0" stroke-width="1"/>')
        for j, ln in enumerate(wrap(lname, 20)):
            e.append(f'<text x="16" y="{y + LANEH/2 - 6 + j*18}" font-size="14" font-weight="bold" fill="{col}">{esc(ln)}</text>')

    def cx(c): return GUTTER + c * COLW + (COLW - BOXW) / 2
    def cy(l): return PAD_TOP + l * LANEH + (LANEH - BOXH) / 2
    centers = {}
    for s in steps:
        x, y = cx(s["col"]), cy(s["lane"])
        centers[s["id"]] = (x + BOXW/2, y + BOXH/2, x, y)
    # arrows (sequential by given order list)
    order = [s["id"] for s in steps]
    for a, b in zip(order, order[1:]):
        x1, y1, bx1, by1 = centers[a]; x2, y2, bx2, by2 = centers[b]
        sx, sy = bx1 + BOXW, y1
        ex, ey = bx2, y2
        mx = (sx + ex) / 2
        e.append(f'<path d="M{sx},{sy} H{mx} V{ey} H{ex}" fill="none" stroke="#475569" stroke-width="2" marker-end="url(#ar)"/>')
    # step boxes
    lane_col = {i: c for i, (_, c) in enumerate(lanes)}
    for s in steps:
        _, _, x, y = centers[s["id"]]
        col = lane_col[s["lane"]]
        e.append(f'<rect x="{x}" y="{y}" width="{BOXW}" height="{BOXH}" rx="9" fill="#ffffff" stroke="{col}" stroke-width="2.5"/>')
        lines = wrap(s["text"], 26)
        ty = y + BOXH/2 - (len(lines)-1)*8
        for ln in lines:
            e.append(f'<text x="{x+BOXW/2}" y="{ty}" font-size="12.5" text-anchor="middle" fill="#0f172a">{esc(ln)}</text>')
            ty += 16
        if s.get("gate"):
            gy = y + BOXH + 4
            gl = wrap(s["gate"], 30)
            gh = len(gl)*13 + 8
            e.append(f'<rect x="{x}" y="{gy}" width="{BOXW}" height="{gh}" rx="5" fill="#fff4e5" stroke="#f59e0b" stroke-width="1.2"/>')
            gyy = gy + 13
            for ln in gl:
                e.append(f'<text x="{x+BOXW/2}" y="{gyy}" font-size="10.5" text-anchor="middle" fill="#92400e">{esc(ln)}</text>')
                gyy += 13
    # exceptions band
    ey0 = PAD_TOP + len(lanes) * LANEH + 12
    e.append(f'<text x="16" y="{ey0+18}" font-size="14" font-weight="bold" fill="#dc2626">Exceptions / escalation</text>')
    for ex in exceptions:
        col = ex["col"]
        bx = GUTTER + col * COLW + (COLW - BOXW)/2
        by = ey0 + 26
        lines = wrap(ex["text"], 30)
        bh = len(lines)*14 + 12
        e.append(f'<rect x="{bx}" y="{by}" width="{BOXW}" height="{bh}" rx="7" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="5 3"/>')
        # dashed connector up to the triggering column center
        tx = GUTTER + col * COLW + COLW/2
        e.append(f'<line x1="{tx}" y1="{ey0+24}" x2="{tx}" y2="{by}" stroke="#dc2626" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#arr)"/>')
        tyy = by + 16
        for ln in lines:
            e.append(f'<text x="{bx+BOXW/2}" y="{tyy}" font-size="10.5" text-anchor="middle" fill="#991b1b">{esc(ln)}</text>')
            tyy += 14
    e.append("</svg>")
    open(out_svg, "w").write("\n".join(e))
    if out_png:
        cairosvg.svg2png(url=out_svg, write_to=out_png, scale=2.0, background_color="white")
    return out_svg
