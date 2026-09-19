# 00 — Intake Form Specification

The intake is a 16-field contract. All 16 fields must be present (validator presence check) AND substantive (validator LLM review). Thin fields like "Audience: someone" fail the LLM review.

## The 16 fields

| # | Field | What it is | Example (Nicola v11.1) |
|---|---|---|---|
| 1 | `engagement` | Client + scope label | NWM Privates Data Dictionary |
| 2 | `profile` | `simcorp` or `generic` | `simcorp` |
| 3 | `deliverable_name` | File name pattern | `Nicola_Privates_Data_Dictionary_v{N}_{YYYY_MM_DD}.xlsx` |
| 4 | `version` | Semver or sequential | `v11.1` |
| 5 | `audience` | Named people + roles | Erhan Yildirim (Migration), Diana Schinkel (AttrConfig), Chris Wong (PELP) |
| 6 | `output_formats` | Required deliverables | XLSX + DOCX + Notion §18.32 + Mermaid + build script |
| 7 | `inputs` | Every source file as `{path, role, description}` | See sub-spec below |
| 8 | `scope_in` | What is in scope | PE, VC, PD, Infra, Mortgages — Mar 31 2026 extracts only |
| 9 | `scope_out` | What is explicitly out | NW2 / Wealth-only portfolios (NWM510 partial only) |
| 10 | `source_truth_map_stub` | At least 3 columns pre-mapped | AM Field Name → v22-ENRICHED col A; Description → SimCorp Help Structured |
| 11 | `proposed_schema` | Columns + atomic Y/N flags | 26 cols: AM Field Name / Description / Imported Y/N / Calculated Y/N / ... |
| 12 | `slicing_rule` | How to split data into sub-tabs | Per-vertical = column union across portfolios containing that vertical |
| 13 | `sme_questions` | Inline Q&A items | Pamela MTG (4 items) + Sebastian Infra (6 items); banner panel at top of tab |
| 14 | `citation_format` | How sources are cited per cell | `Verbatim quote (file path, §section)`; `[GAP: no source]` for missing |
| 15 | `verification_criteria` | What counts as "done" | (a) all rows trace to source (b) atomic cols only (c) 0 invented descriptions (d) SME Q&A coverage = 100% |
| 16 | `notion_target` | Notion §x.y where deliverable lands | §18.32 Nicola Ultimate Data Dictionary (existing page) |

## inputs sub-spec (field 7)

Each input is `{path, role, description}`:

- **path** — absolute, full path on Dan's Mac. Validator checks file exists.
- **role** — `canonical` (single source of truth for some fields) | `supplementary` (cross-check or enrichment) | `extract` (per-vertical raw export) | `template` (S-template, intake template) | `documentation` (Help, PDF, manual).
- **description** — one line, what it gives us.

A 5-input INTAKE is suspicious; the Nicola v11.1 build had 17 inputs across 4 roles.

## Open-questions field (optional 17th)

If Dan has open questions that need to halt the run, list them. Validator surfaces these to chat before STAGE 1.

## Why 16 not 6

Every field maps to a specific failure mode from the Nicola loop:

- Missing fields 7, 12 → v1 Cartesian explosion + v3 wrong scope
- Missing field 10 → v1-v7 invented descriptions
- Missing field 11 → v1-v5 long descriptions
- Missing field 13 → v1-v10 buried SME answers
- Missing field 14 → v1-v10 source-trace gaps
- Missing field 15 → "is this done?" ambiguity

Cutting fields makes the skill cheaper to invoke and more expensive to use.
