# 09 — Post-Validation Cleanup

## Goal

After Dan validates the deliverable, archive prior versions and intermediate artifacts so the workspace stays clean. Per Dan's feedback rule `feedback_post_validation_cleanup.md`: 2-stage quarantine — stage to `_pending_delete_YYYY_MM_DD/` with per-item confirm, hard-delete after 7d untouched via daily 02:00 scheduled task.

## Trigger

Dan says "approved", "ship it", "looks good", or marks the engagement Status=Approved in Notion. NOT before.

## Output

1. `_pending_delete_{YYYY_MM_DD}/` folder in the engagement directory.
2. Per-item move log `_cleanup_log_{date}.md`.
3. Scheduled task `cleanup-engagement-{date}` registered for 02:00 next day (idempotent — skip if exists).

## What to move

- Prior versions of the deliverable XLSX/DOCX (keep latest only at top level).
- Intermediate build scripts that were superseded (`build_v10.py`, `add_qa_panels_v11_1.py` etc.).
- Working CSVs (`_lens_*.csv`, `_source_truth_map_v*.csv`, etc.) — keep latest only.
- Cache directories (`_desc_cache/`, `__pycache__/`).
- Lockfiles (`~$*.docx`, `~$*.xlsx`).

## What to NEVER move (REQUIRED — per memory `project_workspace_cleanup_2026_05_18`)

- The 14 REQUIRED dictionary source files (PELP, AGM_SSC, v22-ENRICHED, etc.).
- The current deliverable's XLSX, DOCX, build script.
- INTAKE.md and source-truth-map.csv (engagement contract — keep for re-runs).
- Notion-linked files (anything referenced by computer:// in the Notion page).

## Invocation

This checkpoint delegates to the `post-validation-cleanup` sister skill — do not reimplement the cleanup logic here. Pass the engagement directory and the manifest of "keep" files.

## Anti-pattern: "Delete is fine, we have iCloud"

Two-stage quarantine is the rule. iCloud sync delay + Dan's "let me check that one more thing" pattern means deletes get recovered. Stage first, delete after 7d untouched, log every move.

## Anti-pattern: "Skip cleanup if the engagement is small"

Cleanup is mandatory regardless of size. Small engagements still leave 3–4 intermediate files; multiplied across 20 engagements that's 80 files of working state in the workspace root.
