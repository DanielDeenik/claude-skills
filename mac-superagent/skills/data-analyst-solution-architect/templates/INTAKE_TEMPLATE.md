# INTAKE — {engagement}

> Fill every field below before invoking the `data-analyst-solution-architect` skill.
> The validator runs presence + LLM review. Thin or missing fields HALT the engagement.

---

## 1. engagement
{e.g. "NWM Privates Data Dictionary"}

## 2. profile
{`simcorp` or `generic`}

## 3. deliverable_name
{e.g. "Nicola_Privates_Data_Dictionary_v{N}_{YYYY_MM_DD}.xlsx"}

## 4. version
{e.g. "v12" or "v1.0"}

## 5. audience
{Named people + roles, comma separated. NOT "the team".}

## 6. output_formats
{Multi-select: XLSX, DOCX companion, Notion §x.y, Mermaid lineage, build script}

## 7. inputs

Every source file the deliverable depends on. One row per file. Absolute paths only.

| path | role | description |
|---|---|---|
| /Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/{filename} | canonical/supplementary/extract/template/documentation | one-line purpose |
| | | |

## 8. scope_in
{What is in scope. Be specific — verticals, date range, asset class.}

## 9. scope_out
{What is explicitly out. Anti-scope is as important as scope.}

## 10. source_truth_map_stub

At least 3 output columns pre-mapped to source files.

| output_column | source_file | source_locator | role |
|---|---|---|---|
| | | | |

## 11. proposed_schema

Per tab: tab name, row scope, column list with atomic Y/N flags.

```
Tab: {name}
  Row = {what one row represents}
  Columns:
    - {Name Column}        (text, source: ...)
    - {Description Column} (text, source: ...)
    - {Imported Y/N}       (Y|N|blank)
    - {Source}             (file + section)
```

## 12. slicing_rule
{How sub-tabs are sliced from data. e.g. "per-vertical = column union across portfolios containing that vertical"}

## 13. sme_questions

Inline SME items with full attribution. If none, write "none".

| ID | From | Date | Question | Status |
|---|---|---|---|---|
| | | | | |

## 14. citation_format

{Exact format required for every citation. e.g. `{quote} ({file}, §{section})`}

## 15. verification_criteria

{What counts as "done". Concrete checks the verification report must pass.}

- All non-blank descriptions have non-blank Source column
- Per-vertical row count matches column union from inputs
- Zero invented descriptions (every cell traces to a source)
- SME Q&A coverage = 100%
- {other engagement-specific checks}

## 16. notion_target
{e.g. "§18.34 — new sub-page under SimCorp Solution Architecture"}

---

## 17. open_questions_for_dan (optional)
{If anything is undecided, list it here. Validator surfaces these to chat before the engagement starts.}
