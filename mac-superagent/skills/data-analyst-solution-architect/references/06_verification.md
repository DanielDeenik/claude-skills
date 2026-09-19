# 06 — Verification

## Goal

Prove the deliverable meets the verification criteria declared in INTAKE field 15.

## Output

`_verification_report_{date}.md` covering five audit dimensions:

### A. Count audit

| Metric | Expected (from INTAKE) | Actual (from XLSX) | Match |
|---|---|---|---|
| Total tabs | | | |
| Master tab rows | | | |
| Per-vertical tab rows (each) | | | |
| SME Q&A items (each tab) | | | |
| Total columns per tab | | | |

Mismatches halt the engagement and route back to checkpoint 3 or 6.

### B. Source-trace audit

For every row in every tab, every non-blank description cell, verify there is a non-blank source cell adjacent. Run `scripts/source_trace_audit.py`. Output:

| tab | row | column | value | source | status |
|---|---|---|---|---|---|

`status` is `OK` (both filled) | `RULE_7_VIOLATION` (value filled, source blank) | `GAP` (value is `[GAP: ...]` marker).

Zero `RULE_7_VIOLATION` to pass.

### C. Gap audit

Count `[GAP: ...]` markers per tab. Group by reason. This is information, not failure. Surface to Dan:

> "There are 47 GAP markers in the Infrastructure tab — 32 'no source in Pricing Doc', 15 'AICOMPONENTS table not on Mac (Portal-gated)'. Want to escalate the 15 Portal-gated to Diana, or keep them as gaps?"

### D. Citation spot-check

Pick 10 random non-blank description cells. Open each citation. Read the actual locator. Verify the cell value is a verbatim quote. Any mismatch is a Rule 1 violation — halt.

### E. SME Q&A coverage

If INTAKE field 13 declared N SME questions, verify N appear in the SME_QA_Full tab AND in the banner panel of the relevant vertical tab. Missing items halt.

## Anti-pattern: "Verification = open the file and squint"

Verification is a script, not a vibe check. Every check is reproducible and re-runnable. The output is a markdown report Dan reviews, not a "looks good" from Claude.

## Anti-pattern: "GAP markers are bugs"

Every deliverable has gaps. The Portal-gated SimCorp DDL files aren't on Dan's Mac — those gaps are real and honest. Hiding them with plausible-sounding text is the bug (Rule 10). The verification report counts and categorizes them so Dan can decide which to escalate.
