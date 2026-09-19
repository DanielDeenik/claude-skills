#!/usr/bin/env python3
"""
Extract embedded images from a .docx client workflow doc, name each by the step
text that precedes it, and flag images that are CID/email references (not real
files, e.g. pasted Bloomberg emails) and therefore cannot be recovered.

Usage:
    python extract_doc_images.py <doc.docx> [--out <assets_dir>]

Writes:
    <assets_dir>/NN_<slug>.png       one per embedded raster image, in doc order
    prints an image -> step map and a list of CID-only images to stderr/stdout

No hardcoded paths or counts — everything is derived from the document.
"""
import argparse
import os
import re
import sys
import zipfile

# Images are referenced two ways: r:embed (stored in the doc) and r:link (external /
# CID pointers, e.g. Bloomberg email images pasted in). We must scan BOTH — r:link
# images are unrecoverable and MUST be reported for re-capture, not silently dropped.
NS_REF = re.compile(r'r:(?:embed|link)="([^"]+)"')
NS_TEXT = re.compile(r"<w:t[^>]*>(.*?)</w:t>", re.S)
PARA = re.compile(r"<w:p\b.*?</w:p>", re.S)
REL = re.compile(r'Id="([^"]+)"[^>]*?Type="[^"]*image[^"]*"[^>]*?Target="([^"]+)"')


def slugify(text, maxlen=48):
    text = re.sub(r"&lt;|&gt;|&amp;", " ", text)
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return (text[:maxlen] or "image").rstrip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    doc = args.doc
    if not doc.lower().endswith(".docx"):
        sys.exit("This script handles .docx. For PDF, extract images with the pdf skill.")
    base = os.path.splitext(os.path.basename(doc))[0]
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(doc)), base + "_assets")
    os.makedirs(out, exist_ok=True)

    with zipfile.ZipFile(doc) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
        rels = z.read("word/_rels/document.xml.rels").decode("utf-8", "ignore")
        rid2target = {m.group(1): m.group(2) for m in REL.finditer(rels)}

        # Walk paragraphs in reading order; remember the last non-empty text so each
        # image can be captioned by the step it illustrates.
        seq = []  # (rid, target, step_text)
        last_text = ""
        for p in PARA.findall(xml):
            txt = "".join(NS_TEXT.findall(p)).strip()
            if txt:
                last_text = txt
            for rid in NS_REF.findall(p):
                seq.append((rid, rid2target.get(rid, ""), last_text))

        real, cid = [], []
        n = 0
        for rid, target, step in seq:
            # Unrecoverable: CID/email pointers, external links, or anything not stored
            # under word/media/. Report these for re-capture rather than dropping them.
            if not target or target.startswith("cid:") or "media/" not in target:
                cid.append((rid, target, step))
                continue
            n += 1
            member = "word/" + target
            ext = os.path.splitext(target)[1] or ".png"
            fname = f"{n:02d}_{slugify(step)}{ext}"
            with z.open(member) as src, open(os.path.join(out, fname), "wb") as dst:
                dst.write(src.read())
            real.append((fname, step))

    print(f"Assets folder: {out}\n")
    print("IMAGE -> STEP MAP")
    for fname, step in real:
        print(f"  {fname}  <-  {step[:80]!r}")
    if cid:
        print("\nCID / EMAIL-EMBEDDED IMAGES (cannot be recovered, re-capture needed):")
        for rid, target, step in cid:
            print(f"  {rid} ({target[:40]}...)  <-  {step[:80]!r}")

    print("\nPLACEMENT MANIFEST (markdown)")
    print("| Step | Image file |")
    print("|---|---|")
    for fname, step in real:
        print(f"| {step[:70]} | {fname} |")


if __name__ == "__main__":
    main()
