#!/usr/bin/env python3
"""
Render a UML-style sequence diagram to SVG (+ PNG via cairosvg) without a browser
or mermaid-cli. Participants across the top with lifelines; messages as arrows
(solid=call, dashed=return, self=loop); notes as full-width bands. Colour by mark
(ok=green, err=red). Content supplied by caller — nothing hardcoded.
"""
import cairosvg, html

MARGIN, GAP, TOPH, ROWH = 140, 340, 172, 60
PBOXW, PBOXH, PBOXY = 210, 46, 70
COLORS = {"call": "#475569", "ok": "#16a34a", "err": "#dc2626"}


def esc(s): return html.escape(s, quote=True)


def wrap(t, n):
    out, cur = [], ""
    for w in t.split():
        if len(cur) + len(w) + 1 <= n: cur = (cur + " " + w).strip()
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out or [""]


def render(title, participants, rows, out_svg, out_png=None):
    n = len(participants)
    W = 2 * MARGIN + (n - 1) * GAP + 40
    x = [MARGIN + i * GAP for i in range(n)]
    # pre-measure height
    y = TOPH + 40
    ys = []
    for r in rows:
        if r["t"] == "note":
            h = len(wrap(r["text"], 60)) * 18 + 22
        else:
            h = ROWH
        ys.append((y, h)); y += h
    H = y + 40
    e = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI,Arial">',
         '<defs>'
         '<marker id="c" markerWidth="11" markerHeight="11" refX="9" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#475569"/></marker>'
         '<marker id="ok" markerWidth="11" markerHeight="11" refX="9" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#16a34a"/></marker>'
         '<marker id="er" markerWidth="11" markerHeight="11" refX="9" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#dc2626"/></marker>'
         '</defs>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="30" y="34" font-size="19" font-weight="bold" fill="#0f172a">{esc(title)}</text>']
    # lifelines + headers (box | actor stick-figure | store dotted-box)
    for i, part in enumerate(participants):
        pname, col = part[0], part[1]
        kind = part[2] if len(part) > 2 else "box"
        cx = x[i]
        e.append(f'<line x1="{cx}" y1="{TOPH}" x2="{cx}" y2="{H-30}" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 4"/>')
        if kind == "actor":
            ty = 56
            e.append(f'<circle cx="{cx}" cy="{ty+8}" r="9" fill="none" stroke="{col}" stroke-width="2.5"/>')
            e.append(f'<line x1="{cx}" y1="{ty+17}" x2="{cx}" y2="{ty+38}" stroke="{col}" stroke-width="2.5"/>')
            e.append(f'<line x1="{cx-14}" y1="{ty+25}" x2="{cx+14}" y2="{ty+25}" stroke="{col}" stroke-width="2.5"/>')
            e.append(f'<line x1="{cx}" y1="{ty+38}" x2="{cx-12}" y2="{ty+53}" stroke="{col}" stroke-width="2.5"/>')
            e.append(f'<line x1="{cx}" y1="{ty+38}" x2="{cx+12}" y2="{ty+53}" stroke="{col}" stroke-width="2.5"/>')
            for j, ln in enumerate(wrap(pname, 22)):
                e.append(f'<text x="{cx}" y="{ty+70+j*15}" font-size="13" font-weight="bold" text-anchor="middle" fill="{col}">{esc(ln)}</text>')
        elif kind == "store":
            lines = wrap(pname, 18)
            bh = max(PBOXH, len(lines) * 16 + 18)
            by = 40
            e.append(f'<rect x="{cx-PBOXW/2}" y="{by}" width="{PBOXW}" height="{bh}" rx="8" fill="#fff7ed" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 4"/>')
            for j, ln in enumerate(lines):
                e.append(f'<text x="{cx}" y="{by+bh/2+5-(len(lines)-1)*8+j*15}" font-size="13" font-weight="bold" text-anchor="middle" fill="{col}">{esc(ln)}</text>')
        else:
            e.append(f'<rect x="{cx-PBOXW/2}" y="{PBOXY}" width="{PBOXW}" height="{PBOXH}" rx="8" fill="{col}"/>')
            for j, ln in enumerate(wrap(pname, 22)):
                e.append(f'<text x="{cx}" y="{PBOXY+PBOXH/2+5-(len(wrap(pname,22))-1)*8+j*15}" font-size="13" font-weight="bold" text-anchor="middle" fill="#ffffff">{esc(ln)}</text>')
    # rows
    for r, (ry, rh) in zip(rows, ys):
        if r["t"] == "note":
            col = {"fix": ("#e7f9ed", "#16a34a"), "warn": ("#fef2f2", "#dc2626")}.get(r.get("style"), ("#f1f5f9", "#94a3b8"))
            bx0, bx1 = MARGIN - 70, W - (MARGIN - 70)
            e.append(f'<rect x="{bx0}" y="{ry}" width="{bx1-bx0}" height="{rh-8}" rx="8" fill="{col[0]}" stroke="{col[1]}" stroke-width="1.5"/>')
            ty = ry + 20
            for ln in wrap(r["text"], 60):
                e.append(f'<text x="{(bx0+bx1)/2}" y="{ty}" font-size="12.5" text-anchor="middle" fill="#0f172a">{esc(ln)}</text>')
                ty += 18
            continue
        a, b = r["frm"], r["to"]
        mark = r.get("mark", "call")
        col = COLORS.get(mark, COLORS["call"])
        mid = {"call": "url(#c)", "ok": "url(#ok)", "err": "url(#er)"}.get(mark, "url(#c)")
        dash = ' stroke-dasharray="6 4"' if r.get("ret") else ''
        yy = ry + rh - 14
        if a == b:  # self loop
            x0 = x[a]
            if a == len(participants) - 1:  # rightmost participant → draw loop + label to the LEFT
                e.append(f'<path d="M{x0},{yy-14} h-44 v14 h44" fill="none" stroke="{col}" stroke-width="2"{dash} marker-end="{mid}"/>')
                e.append(f'<text x="{x0-52}" y="{yy-16}" font-size="12" text-anchor="end" fill="#0f172a">{esc(r["text"])}</text>')
                if r.get("tag"):
                    e.append(f'<text x="{x0-52}" y="{yy+4}" font-size="11" text-anchor="end" fill="{col}" font-style="italic">{esc(r["tag"])}</text>')
            else:
                e.append(f'<path d="M{x0},{yy-14} h44 v14 h-44" fill="none" stroke="{col}" stroke-width="2"{dash} marker-end="{mid}"/>')
                e.append(f'<text x="{x0+52}" y="{yy-16}" font-size="12" fill="#0f172a">{esc(r["text"])}</text>')
                if r.get("tag"):
                    e.append(f'<text x="{x0+52}" y="{yy+4}" font-size="11" fill="{col}" font-style="italic">{esc(r["tag"])}</text>')
        else:
            x0, x1 = x[a], x[b]
            e.append(f'<line x1="{x0}" y1="{yy}" x2="{x1}" y2="{yy}" stroke="{col}" stroke-width="2"{dash} marker-end="{mid}"/>')
            anchor = "middle"; tx = (x0 + x1) / 2
            lbl = r["text"]
            e.append(f'<text x="{tx}" y="{yy-6}" font-size="12" text-anchor="{anchor}" fill="#0f172a">{esc(lbl)}</text>')
            if r.get("tag"):
                e.append(f'<text x="{tx}" y="{yy+15}" font-size="11" text-anchor="{anchor}" fill="{col}" font-style="italic">{esc(r["tag"])}</text>')
    e.append("</svg>")
    open(out_svg, "w").write("\n".join(e))
    if out_png:
        cairosvg.svg2png(url=out_svg, write_to=out_png, scale=2.0, background_color="white")
    return out_svg
