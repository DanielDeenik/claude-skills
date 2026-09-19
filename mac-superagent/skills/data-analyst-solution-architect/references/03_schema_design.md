# 03 — Schema Design (BLOCKING — Dan approves before proceeding)

## Goal

Lock the column structure of every output tab BEFORE building anything. Schema changes after the build is the #1 source of re-iteration. Get it wrong here and you rebuild — get it right here and the build is one pass.

## Output

A markdown spec `_schema_design_{date}.md` listing every tab and every column in it. Then an `AskUserQuestion` "Approve schema to proceed?" with three options: approve / request changes / abandon. Do NOT proceed past this checkpoint without an explicit "approve".

## Per-tab schema rubric

For each tab:

1. **Tab name** + purpose (one line).
2. **Row scope** — what one row represents. "One AM field." "One field × one portfolio." "One SME question."
3. **Column list** — every column with: name (verbatim, matching existing convention per Rule 8), atomic Y/N or text or numeric, source (per source-of-truth map), example value, max length.
4. **Sort order** + group order.
5. **Banner panels** — if the tab has top-of-tab banner rows (SME Q&A, version notes, color legend), list them.

## Atomic Y/N column convention

Every boolean characteristic is a column:

- `Imported Y/N` + `Import File` + `Import File Description`
- `Calculated Y/N` + `Calculation Description` + `Calculation Source`
- `Derived Y/N` + `Derivation Rule`
- `AttrConfig Y/N` + `AttrConfig Name` + `AttrConfig Free Code Number` + `AttrConfig Description`
- `In Extract Y/N` (which extract files have a non-blank value for this field)

Y/N values are exactly `Y`, `N`, or blank. Not `Yes`/`No`, not `True`/`False`, not `1`/`0`. The user reads the workbook in Excel — Y/N stays atomic and filterable.

## Name vs Description columns

For every concept that has a name AND a description, both columns are required:

| Concept | Name column | Description column |
|---|---|---|
| AM field | `AM Field Name` | `AM Field Description` |
| Import file | `Import File` | `Import File Description` |
| AttrConfig | `AttrConfig Name` | `AttrConfig Description` |
| SimCorp source | `Source File` | `Source Locator` (file + section / page / line) |
| SME question | `SME Question` | `SimCorp Answer` |

## Approval gate

After writing the schema spec, emit `AskUserQuestion` with three options:

1. **Approve schema — proceed to v0.1 slice** — Claude advances to checkpoint 4.
2. **Request changes** — Dan specifies what to change; Claude updates schema; re-emit gate.
3. **Abandon** — engagement halted; reason logged.

Do not move on without "approve".

## Anti-pattern: "I'll figure out the columns as I go"

The Nicola v22-ENRICHED file had 16 columns. v1 of the new dictionary used 8 of them with different names. v3 had 14 different names. v5 had still-different names. By v9 the schema had been "decided" four times. Lock once, build once.

## Anti-pattern: "Adding a column is cheap"

Adding a column means re-running the source-of-truth lookup for every row, which means re-loading every source file, which means re-running the build. Cheap to add to the spec — expensive to add after the build. Capture every column you'll need in this checkpoint.
