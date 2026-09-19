#!/usr/bin/env python3
"""
Annotate a real SimCorp (or any) screenshot for an FAQ/SOP: wrap it with a titled
header band and a grounded caption strip, and drop numbered badges on the actual
controls. This keeps annotations GROUNDED in the real UI — we never invent SimCorp
screens, we mark up the screenshots the client provided.

API:
    annotate(src_png, out_png, step, title, badges, caption)
      badges  = [{"n":1, "x":0.55, "y":0.19}, ...]  # x,y are fractions of the image
      caption = "footer text (include manual § and the badge legend)"
Coordinates are fractional so they survive rescaling. No hardcoded content here.
"""
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
HEADER_BG, HEADER_FG = (31, 41, 55), (255, 255, 255)
CAP_BG, CAP_FG, CAP_BORDER = (248, 250, 252), (15, 23, 42), (203, 213, 225)
BADGE_BG, BADGE_FG = (220, 38, 38), (255, 255, 255)
PAD = 18


def _wrap(draw, text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            out.append(cur); cur = w
    if cur:
        out.append(cur)
    return out or [""]


def annotate(src_png, out_png, step, title, badges, caption):
    im = Image.open(src_png).convert("RGB")
    W, H = im.size
    fh = max(20, W // 45)
    hb = ImageFont.truetype(FONTB, fh)
    cf = ImageFont.truetype(FONT, max(15, W // 60))
    d0 = ImageDraw.Draw(im)

    header_h = fh + 2 * PAD
    cap_lines = _wrap(d0, caption, cf, W - 2 * PAD)
    cap_h = len(cap_lines) * (cf.size + 6) + 2 * PAD

    canvas = Image.new("RGB", (W, header_h + H + cap_h), "white")
    d = ImageDraw.Draw(canvas)
    # header
    d.rectangle([0, 0, W, header_h], fill=HEADER_BG)
    d.text((PAD, PAD), f"STEP {step} · {title}", font=hb, fill=HEADER_FG)
    # screenshot
    canvas.paste(im, (0, header_h))
    # caption
    cy0 = header_h + H
    d.rectangle([0, cy0, W, cy0 + cap_h], fill=CAP_BG)
    d.line([0, cy0, W, cy0], fill=CAP_BORDER, width=2)
    ty = cy0 + PAD
    for ln in cap_lines:
        d.text((PAD, ty), ln, font=cf, fill=CAP_FG)
        ty += cf.size + 6
    # badges on the screenshot (offset by header height)
    r = max(12, W // 55)
    bf = ImageFont.truetype(FONTB, int(r * 1.2))
    for b in badges:
        cx = int(b["x"] * W)
        cy = header_h + int(b["y"] * H)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BADGE_BG, outline="white", width=3)
        num = str(b["n"])
        tw = d.textlength(num, font=bf)
        d.text((cx - tw / 2, cy - bf.size / 2 - 1), num, font=bf, fill=BADGE_FG)
    canvas.save(out_png)
    return out_png


if __name__ == "__main__":
    import json, sys
    spec = json.load(open(sys.argv[1]))
    for s in spec:
        annotate(s["src"], s["out"], s["step"], s["title"], s["badges"], s["caption"])
        print("annotated", s["out"])
