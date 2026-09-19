# Anti-Shortcut Rules

Ten rules learned from the Nicola Privates Data Dictionary v1 → v11.1 iteration loop (2026-05-17 → 2026-05-18). Each rule cites the version(s) that triggered it.

> **CRITICAL UPDATE 2026-05-18 (post v11.1).** Dan corrected the "verbatim only" rule. Rules 1, 7, and 9 below are SUPERSEDED by `feedback_descriptions_for_reader_not_verbatim.md`:
>
> - **Descriptions are written for the READER, not for validation.** Plain English. Useful. Not pasted text from a manual section.
> - **Mapping must be evidence-based, not similarity-based.** The v11.1 search-lookup matched fields by keyword similarity — many to the WRONG field. Mapping requires evidence: the field name in DB COMMENT, the table it lives in, the AM display label, the import file column.
> - **Citation is for traceability, not for the cell content.** The Source column stays (audit trail); the Description column is rewritten in plain English.
> - **The right architecture is AKG + DuckDB.** Build the SimCorp Help + DB comments + S-template mapping + Help corpus into a queryable store. Descriptions are derived with field-identity confidence, not search similarity.

Paste these as 10 TodoWrite items at every invocation. They stay pending throughout the engagement as a visible track.

## Rule 1 — Descriptions are written for the reader, not for validation (REVISED 2026-05-18)

**Rule.** Descriptions in the deliverable are plain-English explanations of what the field IS, what it represents, when it's used. Useful to the reader. NOT verbatim text pasted from a SimCorp manual to prove the source to Dan.

**Original v1–v7 rule was the over-correction.** Claude invented descriptions from training knowledge in v1–v7; Dan corrected that with "use SimCorp source"; the team then over-rotated to "verbatim only" through v11; Dan corrected AGAIN at v11.1 with: "never add in verbatim, follow simple guidelines that it needs to make sense to the person reading it not validation for me".

**How to apply.**
1. Find the EVIDENCE for what the field means: DB COMMENT, Help table description, Field-NNN.htm, manual section.
2. SYNTHESIZE a clear, brief description for the reader. Plain English. Useful. 1–3 sentences typically.
3. The Source column remains — it's the audit trail. The Description column is your synthesis, not a quote.
4. If no evidence exists, the cell is `[GAP: no evidence found for this field]` — better an honest gap than an invented description.

**Critical: mapping must be evidence-based.** Search-similarity (keyword match) is NOT evidence. The Nicola v11.1 build matched many fields to wrong descriptions because keyword overlap was treated as identity. Require: matching field name in DB COMMENT, matching table, matching AM display label.

## Rule 2 — Atomic Y/N columns

**Rule.** Boolean facts live in their own columns. "Imported Y/N", "Calculated Y/N", "Derived Y/N", "AttrConfig Y/N". The corresponding description lives in a separate column ("Calculation Description", "AttrConfig Name", "AttrConfig Description").

**Triggered by.** v1–v5. Long mixed descriptions like "This is calculated as funded × historical FX, configured via AttrConfig PFC2, imported from S2 column 18". Dan: "use multiple columns rather than long descriptions, i.e. calculated Yes / No and a description of the calculation".

**How to apply.** Every boolean characteristic becomes a column. The column name says what it is; the value is exactly `Y` or `N` or blank. A separate column carries the prose. If you find yourself writing a comma-separated list of facts in one cell, stop — split into atomic columns.

## Rule 3 — Strict NAME / DESCRIPTION column split

**Rule.** A concept's name and its description are two columns. "Import File" + "Import File Description". "AttrConfig Name" + "AttrConfig Description". "AM Field" + "AM Field Description". Never merge.

**Triggered by.** v1–v9. Repeated mixing where one column carried both. Dan: "strict NAME/DESCRIPTION separation per concept".

**How to apply.** Schema design (checkpoint 3) lists every concept and verifies it has exactly two columns. If a concept needs more (e.g. AttrConfig Name + Free Code Number + Description = 3 columns), make all three explicit.

## Rule 4 — Per-vertical = only fields in extracts

**Rule.** A per-vertical tab contains exactly the columns present in extracts for that vertical. If PE extracts have 19 columns, PE tab has 19 rows. Not 154.

**Triggered by.** v1–v8. Claude built per-vertical tabs from a "theoretical full field set". Dan: "Per vertical I only need the fields that were part of the extractions".

**How to apply.** Checkpoint 1 (inventory) records the column union per vertical. Checkpoint 5 (full build) loops over that column union — not the master list. Wealth portfolios (e.g. NWM510 mixed) get added to multiple verticals only if they actually populate fields for that vertical.

## Rule 5 — Read every source file before writing any output cell

**Rule.** No "draft now, fix later". Every source file in INTAKE field 7 (`inputs`) must be Read before any output cell is written.

**Triggered by.** Constant root cause. v22 NameError, str→astype error, UTF-16 BOM, NWM510 generic asset class — all from "I'll just check the file later".

**How to apply.** Checkpoint 1 explicitly lists "Read all N inputs" as the first sub-step. The build script imports each file with its discovered encoding (utf-8 / utf-16 / utf-16-le fallback chain) and prints `loaded {path} → {rows} × {cols}` before any transform.

## Rule 6 — SME Q&A inline in relevant tabs

**Rule.** When the engagement has SME questions (Pamela's mortgage queries, Sebastian's infra queries, etc.), they live in three places: dedicated SME_QA_Full tab, banner panel at top of the relevant vertical tab, and full narrative in the companion DOCX. Never just one of those.

**Triggered by.** v1–v10. Dan: "have you answered the questions posed to infrastructure and mortgages in the output?" Resolutions had been put only in a separate DOCX, invisible to a reviewer in the XLSX.

**How to apply.** Checkpoint 3 (schema) declares whether SME Q&A is in scope. If yes, the per-vertical tab layout includes a "banner panel" row block at the top (10–15 rows), each Q&A as one row with columns: ID, From, Date, Question, SimCorp Answer, Status, Open Action, Owner.

## Rule 7 — Every description carries traceable citation (REVISED 2026-05-18)

**Rule.** Every non-blank description has an adjacent Source column locating the EVIDENCE for the field's meaning — DB COMMENT line, Help table id, Field-NNN.htm, manual page. The description text itself is the reader-focused synthesis (Rule 1), not the verbatim quote.

**Triggered by.** v1–v10 source attribution gaps. Dan: "use the simcorp field descriptions" needed proof of evidence.

**How to apply.** Schema (checkpoint 3) mandates a Source column adjacent to every Description column. The Description is plain-English (Rule 1); the Source is the locator for the evidence behind it. Verification (checkpoint 7) asserts: for every non-blank description, the source column is also non-blank AND opening the source locator confirms the field-identity (not just keyword similarity).

## Rule 8 — Match existing column naming convention

**Rule.** If a backbone file (v22-ENRICHED, PE_Mapping, AGM_SSC, etc.) exists with established column names, the new deliverable uses those names verbatim. Do not invent variants.

**Triggered by.** v3, v5. Claude proposed "AM_Display_Label" when v22 used "AM Field Name". Dan corrected.

**How to apply.** Checkpoint 1 identifies the backbone file. Checkpoint 3 lists every new column with a Source: which existing column it inherits from, or "NEW — needs sign-off". NEW columns require Dan's approval in checkpoint 3, not assumed.

## Rule 9 — Descriptions are 1–3 sentences of plain English (REVISED 2026-05-18)

**Rule.** Descriptions are 1–3 sentences of plain English that help the reader. Not a one-line keyword (too thin) and not three paragraphs of verbatim manual text (too thick). Other factual attributes (Y/N flags, codes, calc rules) go in separate atomic columns per Rule 2.

**Triggered by.** v1–v5 long descriptions; v8–v11 verbatim citation chunks. Dan 2026-05-18: descriptions must "make sense to the person reading it not validation for me".

**How to apply.** Verification (checkpoint 7) flags descriptions under 20 chars (thin) or over 300 chars (likely pasted citation block). Build script warns at both extremes. Author writes for the reader — clear English, no jargon-without-context, no manual section numbers inside the prose (those live in the Source column).

## Rule 10 — Show gaps honestly

**Rule.** When a search returns empty or a field has no source, mark `[GAP: <reason>]`. Never extrapolate. Empty SQL result proves only "empty for this query", not "the data doesn't exist" or "we're in TEST DB not PROD".

**Triggered by.** v2 wrong "53 of 99 orphans" number. v8 PROD-vs-TEST DB misdiagnosis where empty Prepare-result was extrapolated to "Prepare never ran". Dan: "Empty SQL results prove only 'empty for this query.'"

**How to apply.** Every empty-result branch in build code either logs `[GAP: <reason>]` to the cell, or raises. Never silently substitutes a plausible value. Verification (checkpoint 7) counts `[GAP:` markers and presents them to Dan — the count IS information.

---

## How violation gets caught

Three layers:

1. **At write time.** Build script asserts atomic Y/N values, asserts non-blank source-when-description-non-blank, asserts cell length ≤150.
2. **At verification.** Checkpoint 7 reads the finished XLSX and runs `source_trace_audit.py` which lists every row × column with: value, source, citation, gap-marker. Any "value non-blank, source blank" is a rule-7 violation.
3. **At Dan review.** Checkpoint 3 (schema approval) and checkpoint 5 (v0.1 review) are blocking. Dan eyeballs and rejects if any rule is breached at the design stage, before scale.
