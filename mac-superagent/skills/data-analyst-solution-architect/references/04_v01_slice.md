# 04 — v0.1 Slice (BLOCKING — Dan reviews before full build)

## Goal

Build the deliverable for ONE representative section first. Dan eyeballs it. Confirms the schema, the citations, the gap markers, and the SME Q&A panel render correctly. Only then do we build the rest.

## What "one section" means

- For a data dictionary: ONE vertical (the smallest one), ALL columns, 5 representative fields with full citations.
- For a mapping workbook: ONE source-system table, ALL columns, 5 fields mapped.
- For an audit cross-reference: ONE audit finding, ALL fields, with full source-trace.

Pick the smallest non-trivial slice. The Nicola v11.1 slice would have been Mortgages (22 rows, 4 SME questions inline) — smallest vertical, every kind of column exercised.

## Output

A real `.xlsx` file `_v0_1_slice_{date}.xlsx` written to the working directory. NOT a markdown preview. Dan needs to open it in Excel and see exactly what the final will look like at scale.

## What the slice exercises

- Every column from the locked schema (Rule 8 verbatim names).
- The Y/N atomic convention (Rule 2).
- The Name / Description column split (Rule 3).
- At least 3 cells with verbatim citations + Source column (Rule 7).
- At least 1 `[GAP: no source]` marker (Rule 10) — every deliverable has gaps; surface them at v0.1.
- The SME Q&A banner panel at the top, if applicable (Rule 6).
- The source-trace report (counts non-blank vs gap markers).

## Approval gate

After writing the v0.1 slice file, emit `AskUserQuestion` with three options:

1. **Approve v0.1 — proceed to full build** — Claude advances to checkpoint 6 and applies the same pattern across all sections.
2. **Request changes** — Dan specifies what's wrong (column order, missing citation column, Y/N values wrong, etc.); Claude rebuilds the slice; re-emit gate.
3. **Abandon** — engagement halted.

Do not move on without "approve". And do not skip this checkpoint thinking "the schema was approved so the slice is just mechanical" — the schema approves the COLUMNS; the slice approves the CONTENT.

## Why not skip straight to full build

The Nicola loop's pattern was: build everything → Dan reviews → 8 things wrong → rebuild → 6 things wrong → rebuild → 4 things wrong. Each rebuild was hours. A v0.1 slice would have caught 6 of the 11 iterations in one round-trip.

## Anti-pattern: "v0.1 slice = a screenshot"

The slice is a real XLSX file. Dan opens it in Excel. Reviews it as the user, not as the reviewer of a markdown preview. The screenshot version of v0.1 hid the column-order bugs that came out in v3.

## Anti-pattern: "I'll just pick PE for the slice because it has the most data"

Pick the smallest non-trivial slice. More data means more things to review means slower iteration on the slice itself. Smallest vertical that exercises all schema features wins.
