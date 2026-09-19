# Worked Example — NWM Privates Data Dictionary v11.1

## Files

- `INTAKE_FILLED.md` — the INTAKE that *should* have been filled at the start of the engagement on 2026-05-17. Filled retroactively from the v11.1 deliverable.

## What the deliverable looked like

After 11 iterations over 2 days, the v11.1 deliverable was:

- `Nicola_Privates_Data_Dictionary_v11_1_2026_05_18.xlsx` (84 KB, 7 tabs, 158 master rows)
  - Full_Data_Dictionary (158 rows × 27 cols)
  - SME_QA_Full (10 items × 8 cols)
  - Private_Equity (19 rows)
  - Venture_Capital (29 rows)
  - Private_Debt (55 rows)
  - Mortgages (22 rows, banner panel for 4 PQ-* items)
  - Infrastructure (29 rows, banner panel for 6 SQ-* items)

- `Nicola_SimCorp_SME_QA_Resolutions_v11_1_2026_05_18.docx` (19 KB, ~16 pages narrative companion)

## How many iterations this skill would have saved

- v1 (Cartesian explosion 884 rows): prevented by checkpoint 2 source-truth map + checkpoint 4 v0.1 slice.
- v2 (wrong "53 of 99 orphans"): prevented by Rule 10 (show gaps honestly) + checkpoint 7 verification.
- v3–v5 (inferred descriptions, long descriptions, wrong column names): prevented by checkpoint 3 schema design + Rules 1, 2, 3, 7, 8, 9.
- v6–v8 (wrong per-vertical scope): prevented by Rule 4 + slicing rule in INTAKE field 12.
- v9–v10 (SME Q&A buried in separate DOCX): prevented by Rule 6 + INTAKE field 13.
- v11 (post-hoc switch to verbatim SimCorp sources): would have been v1 if INTAKE field 14 had locked citation format up front.

Expected engagement under this skill: 2–3 iterations (intake → schema review → v0.1 slice → full build), not 11.

## How to use this example

When invoking the skill for a new SimCorp data-dictionary engagement, copy `INTAKE_FILLED.md` to your engagement folder, edit fields 1, 3, 4, 5, 7 (paths), 8, 9, and the audience-specific bits in 13–15. The structure and rules are identical across SimCorp-profile engagements.
