# 07 — DOCX Companion

## Goal

The XLSX is the structured deliverable. The DOCX is the narrative — what's in the workbook, why it's structured this way, what the gaps are, what the SME questions are and their full answers with verbatim manual citations.

## Output

`{deliverable_name}_Companion_{date}.docx` — same base name as XLSX, `_Companion` suffix.

## Structure (sections in order)

1. **Cover** — title, version, date, audience, companion-to filename.
2. **Contents** — section index.
3. **Executive Summary** — what's in the deliverable, what's new vs prior version, what's open.
4. **Source-of-Truth Map** — table from checkpoint 2, in narrative form.
5. **Schema Walkthrough** — every tab, every column, with rationale ("why we have a separate Source column for each Description column" = Rule 7).
6. **Per-section Deep-Dives** — one section per tab, with example rows annotated.
7. **SME Q&A Long Form** — every SME item with full question / SimCorp answer / verbatim manual citation / resolution / outstanding action. This is the full narrative the XLSX banner panel summarizes.
8. **Gap Register** — every `[GAP: ...]` marker, grouped by reason, with proposed escalation owner.
9. **Sources Cited** — every file referenced, with role (canonical / supplementary / extract / documentation).
10. **How this Companion sits next to the XLSX** — explains the three-place SME Q&A pattern (Rule 6).

## Citation format inside DOCX

Every claim that came from a SimCorp manual or NWM document carries a parenthetical citation: `(FUND - Fund admin §3.3 FX)` or `(Pricing Documentation p.47)` or `(SimCorp_Help_Structured.csv row 12,403)`.

Never write "SimCorp says" without the §. Never write "per the documentation" without naming the document.

## Why this exists

The Nicola v11.1 DOCX was 16 pages. Without it, the XLSX is a wall of cells without a story. The DOCX is what a reviewer reads when they want to understand WHY a column exists, not just WHAT is in it.

## Anti-pattern: "DOCX = repeat the XLSX"

The DOCX is narrative, not data. If a section is a table that already lives in the XLSX, summarize the table in prose and reference the XLSX tab. Repeating the same table in two places means they will drift.

## Anti-pattern: "I'll write the DOCX after Dan signs off on the XLSX"

The DOCX is part of the deliverable, not an afterthought. It ships with the XLSX. Checkpoint 8 is mandatory.
