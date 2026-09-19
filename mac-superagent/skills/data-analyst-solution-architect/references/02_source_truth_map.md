# 02 — Source-of-Truth Map

## Goal

For every output column, declare exactly which source file (and which locator within it) is the canonical truth. This is the contract that prevents "I'll figure out where this comes from when I write the cell."

## Output

A CSV `_source_truth_map_{date}.csv` with one row per output column:

| output_column | source_file | source_locator | role | fallback_files | notes |
|---|---|---|---|---|---|
| AM Field Name | NWM_AM_Field_Summary_ENRICHED_v22.xlsx | sheet "Master", col A | canonical | — | |
| AM Field Description | SimCorp_Help_Structured.csv | description matching field_name | canonical | Field-{NNN}.htm; db2.sql COMMENT ON COLUMN | Search corpus chain: Help_Structured → Field-htm → Table-htm → Command-htm → PDFs → db2.sql |
| Calculated Y/N | derived | from "Calculation Description" non-blank | derived | — | Y if Calculation Description is non-blank |
| Calculation Description | Pricing_Documentation.pdf | §3.1–§3.4 + §7.1–§7.4 | canonical | SimCorp_Help_Structured Forms | Verbatim quote required |
| AttrConfig Name | NWM_AttrConfig.xlsx | sheet "AttrConfig", col "Free Code Name" | canonical | — | |
| Source | derived | concatenation of source_file + source_locator | derived | — | One per non-blank description |

## Rules

1. **Every output column has exactly one canonical source.** If two files could give the same value, name the priority order in `fallback_files`.
2. **`derived` rows must explain the derivation rule.** Y/N flags from non-blank text, computed FX from {funded × historical + unfunded × current}, etc.
3. **A column with no source can't ship.** Either find a source, drop the column, or escalate to Dan in checkpoint 3.

## Anti-pattern: vague locators

"Pricing Doc" is not a locator. "Pricing Doc §3.1 formula F-001" is. The verification audit (checkpoint 7) opens each citation and confirms the value at that locator matches the cell.

## Worked example

The Nicola v11.1 build had 27 output columns. Its source-of-truth map had 27 rows. The build script iterates over the map, never over a hardcoded column list — so adding a column is a one-line change, not a code rewrite.
