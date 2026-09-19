# 08 — Notion Push (§18.x Hub)

## Goal

The deliverable lands in Notion under the Solution Architecture §18 family. Reviewers find it via the §18 hub, not via a chat link they'll lose.

## Output

A new Notion sub-page under §18 with:

1. **Title** = `§18.{N} {Engagement} — {Deliverable Name} v{version}`
2. **Properties** — Date, Owner (Dan), Status (Draft / Review / Approved / Archived)
3. **Body** sections:
   - Executive summary (3–5 paragraphs from DOCX §3)
   - Source-of-truth map (table from checkpoint 2)
   - Schema walkthrough (one h2 per tab; column list)
   - SME Q&A summary (table from XLSX SME_QA_Full)
   - Gap register (escalations grouped by owner)
   - Files (computer:// links to XLSX + DOCX + build script)
   - Mermaid lineage diagrams (embed in `mermaid` code fence)
4. **Cross-links** — to prior §18.x pages this supersedes or relates to.

## Pre-flight: pick the §18.x number

List existing §18.x pages first via `mcp__plugin_engineering_notion__authenticate` → `notion-search` for "§18.". Pick the next unused integer. Do not guess — the Nicola family already uses §18.27 through §18.33. Confirm with Dan before reserving.

## Mermaid diagrams

For data-dictionary deliverables, embed at least:

1. **Source → tab → column lineage** — which source file feeds which tab.
2. **AM field → AttrConfig → S-template path** — for SimCorp profile only.
3. **SME Q&A flow** — asker → tab → resolution status.

Use the standard SimCorp ER diagram styling (dashed for temp/bridge tables, solid for permanent).

## Properties

Match the existing §18 page schema. Inspect §18.32 properties before creating. Keep enums consistent (Status values, Owner format, Date format).

## Anti-pattern: "Notion push = paste a screenshot"

The Notion page is the canonical artifact reviewers cite in tickets. It carries the structured information (schema, gap register, SME Q&A), not screenshots. Reviewers can subscribe to it, comment on it, link to it from Asana/Linear.

## Anti-pattern: "I'll push to Notion after the engagement"

Notion push is checkpoint 9, mandatory. It's how the deliverable becomes discoverable beyond Dan's iCloud folder. The MEMORY.md `project_*.md` entry references the Notion page ID, so future sessions find it.
