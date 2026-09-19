# Publishing to SharePoint / ClickUp / Notion

How the deliverable and its images reach each target. The key constraint: on the
NWM tenant the **Graph API is blocked** and no SharePoint connector is assumed, so
images are prepared for a **one-time human upload**, not pushed programmatically.

## Image transport (all targets)

1. Run `scripts/extract_doc_images.py <doc.docx>` → named PNGs in
   `<doc>_assets/` + an image→step map + a placement manifest.
2. Keep the `[[IMAGE: <file>]]` markers in the body so the human knows where each
   screenshot goes.
3. CID/email-embedded images (Bloomberg emails pasted into the doc) are references,
   not files — list them under "re-capture", never fabricate.

## SharePoint page

- SharePoint modern pages do **not** render Markdown or mermaid. Convert to the
  target: use the page editor's Text web part for prose, and insert diagrams as
  **images** (render mermaid to PNG/SVG first — see parse-check below, then export).
- Upload screenshots via the page editor (Insert → Image → Upload), or drop them in
  the site's **Site Assets / a document library** first and insert by reference so
  they have stable URLs.
- Paste the FAQ text, then at each `[[IMAGE: ...]]` marker insert the matching file
  from the manifest.

## ClickUp

- ClickUp Docs/descriptions accept a subset of Markdown (headings, bold, tables,
  numbered lists) but **not mermaid**. Paste the prose SOP; drag screenshots inline
  at each marker.

## Notion Wiki (§18.35)

- Notion renders Markdown and has native mermaid code blocks, so the diagrams travel
  as-is. Images upload via drag-drop or the API if a connector is authorized.
- Promote only Validated, High-Cited content; extend an existing Wiki page rather
  than creating a duplicate.

## Mermaid parse-check (before exporting to image)

Every diagram must parse before it ships. Quick headless check:

```bash
npm install mermaid jsdom >/dev/null 2>&1
node --input-type=module -e '
import { JSDOM } from "jsdom";
const dom = new JSDOM("<!DOCTYPE html><body></body>",{pretendToBeVisual:true});
global.window=dom.window; global.document=dom.window.document;
const m=(await import("mermaid")).default;
m.initialize({startOnLoad:false,securityLevel:"loose"});
import fs from "fs";
await m.parse(fs.readFileSync(process.argv[1],"utf8")); console.log("OK");
' diagram.mmd
```

To render to image for SharePoint/ClickUp, use `@mermaid-js/mermaid-cli` (`mmdc -i
diagram.mmd -o diagram.png`) where a headless browser is available, or paste into a
mermaid live editor and export.
