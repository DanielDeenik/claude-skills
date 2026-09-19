---
name: post-validation-cleanup
description: Two-stage cleanup of redundant Mac files and Notion duplicate/orphan pages, triggered when Dan validates a deliverable. Stage 1 quarantines candidates into _pending_delete_YYYY-MM-DD/ with per-item confirmation; Stage 2 hard-deletes after 7 days untouched (daily 02:00 scheduled sweep). Trigger on phrases like "validated", "approved", "looks good", "done with this", "ship it", "ready", "final" said about a just-produced deliverable.
---

# Post-Validation Cleanup

Mandatory workspace hygiene skill. Locked design 2026-05-14: Dan chose
**post-validation trigger** + **two-stage quarantine**. See
`feedback_post_validation_cleanup.md` for the binding rule.

## When to invoke

Invoke immediately, without asking, when Dan uses any of these phrases about
a deliverable Claude just produced in this conversation:

- "validated" / "validation done"
- "approved"
- "looks good" / "this looks good"
- "done with this" / "we're done"
- "ship it" / "shipped"
- "ready" / "ready to go"
- "ok this is final" / "final version"
- "perfect, clean up" or any explicit cleanup ask

If unsure whether Dan's message constitutes validation, do not invoke — ask.
False positives are worse than a missed cleanup.

## Workflow

### 1. Identify the validated deliverable
The most recent file Claude saved to the workspace folder
`~/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/`
(or wherever the user's selected workspace resolves to). If multiple deliverables
were produced this session, treat the most recently saved as primary; ask Dan
if any of the others are NOT yet validated.

### 2. Audit Mac filesystem
Read `references/mac-cleanup-rules.md` for the full ruleset. Quick version:

- **/outputs/ duplicates** — files in `/outputs/` that also exist in workspace
  are redundant; workspace is canonical
- **Build scripts** — `build_*.py`, `append_*.py`, `*_dump.json`, `rename_*.py`
  that produced the validated deliverable; reproducible from the workspace XLSX
  + memory notes if ever needed again
- **Older versions** — `*_v1.xlsx`, `*_v2.xlsx`, `*_draft.*` in workspace where
  a newer version exists in the same folder
- **Hash duplicates** — same content, different filenames or paths

Use `scripts/audit_mac.py` to produce the candidate list (path, size, reason,
sha256 of duplicate-target if applicable). Never auto-delete; the script only
audits.

### 3. Audit Notion structure
Read `references/notion-cleanup-rules.md`. Apply the 6-cluster IA from
`feedback_kb_routing_rules.md` (REF / ARCH / FLOW / TRAIN / IMPL / GOV /
ARCHIVE):

- Orphan root-level pages outside the IA → flag for re-home or archive
- Pages with duplicate titles → flag for merge (keep latest, archive losers)
- Stale Q&A Log entries whose Wiki promotion already happened → archive

Use Notion MCP tools: `notion-search`, `notion-fetch`,
`notion-query-database-view`. For archive, use `notion-update-page` with
`archived: true`. Never `notion-delete` at Stage 1.

### 4. Present candidates to Dan
Markdown table per surface (Mac files, Notion pages). For every row:
`#`, `path/page`, `size or word count`, `reason flagged`, `proposed action`.
End with: *"Reply with 'y' (all), 'n' (none), or a comma list of row #s to
quarantine. Anything not listed stays put."*

### 5. Stage 1: Quarantine
After Dan's per-item confirmation:

- Create `~/Library/Mobile Documents/.../a. Consulting - SimCorp/_pending_delete_YYYY-MM-DD/`
  if not already present for today
- For each confirmed Mac file: `mv` into the quarantine folder, preserving
  relative path structure inside (so a file from `/outputs/foo.py` lands at
  `_pending_delete_2026-05-14/outputs/foo.py`)
- For each confirmed Notion page: `notion-update-page archived=true` and record
  the page ID + URL in `manifest.md`
- Write `_pending_delete_YYYY-MM-DD/manifest.md` with: validated deliverable
  that triggered the cleanup, list of every moved item with original path and
  reason, restoration commands

### 6. Stage 2: Hard-delete (scheduled)
A daily 02:00 scheduled task runs `scripts/quarantine_purge.py`:

- For each `_pending_delete_YYYY-MM-DD/` folder where YYYY-MM-DD + 7 ≤ today,
  AND the folder's recursive `mtime` shows no human touches in 7 days,
  `rm -rf` the folder
- Append a summary entry to `~/Library/Mobile Documents/.../a. Consulting - SimCorp/cleanup_log.md`
- For Notion archived pages older than 7 days untouched, run Notion-side hard
  delete (or escalate to Dan if Notion MCP can't permanently delete)

If a quarantine folder has been touched (any file inside modified since
quarantine timestamp), skip the purge and re-page Dan — assume he rescued
something.

## Output template

```
## Post-validation cleanup — <validated deliverable>

**Mac files flagged (N)**
| # | Path                                          | Size  | Reason          | Action     |
|---|-----------------------------------------------|-------|-----------------|------------|
| 1 | /outputs/build_v2_workbook.py                 | 18 KB | Build script... | Quarantine |
| 2 | /outputs/source_dump.json                     |  6 MB | Intermediate... | Quarantine |
| 3 | /outputs/NWM_SimCorp_..._v2.xlsx              | 115KB | Dup of workspace| Quarantine |

**Notion pages flagged (M)**
| # | Page                                  | Status      | Reason       | Action  |
|---|---------------------------------------|-------------|--------------|---------|
| 4 | NWM v1 draft (3467772fa7ae812a...)    | superseded  | v3 published | Archive |

Quarantine folder will be: `/workspace/_pending_delete_2026-05-14/`

Reply 'y' to stage all, 'n' to skip, or comma list (e.g. "1,2,4") for selective.
```

## Safety invariants

Never touch:
- `memory/` directories (auto-memory store)
- `.claude/`, `.cursor/`, `.vscode/`, `~/.config/` and similar
- Files in skill directories (this skill, sister skills)
- The validated deliverable itself
- Any file Dan marked "keep" in a prior turn this session
- Any file with unique content (no hash duplicate anywhere on Mac)

Never act without per-item confirmation at Stage 1. The scheduled Stage 2
purge is the ONLY auto-delete path, and it requires 7 days of untouched
mtime to fire.

## References

- `references/mac-cleanup-rules.md` — full Mac filesystem ruleset
- `references/notion-cleanup-rules.md` — full Notion ruleset and 6-cluster IA
- `references/quarantine-protocol.md` — quarantine folder spec, manifest
  format, restore commands
- `scripts/audit_mac.py` — find candidates on Mac
- `scripts/quarantine_purge.py` — Stage 2 daily sweep

## Memory pointers

- `feedback_post_validation_cleanup.md` — the binding rule
- `feedback_kb_routing_rules.md` — Notion 6-cluster IA
- `reference_mac_filesystem.md` — canonical Mac paths
- `feedback_reuse_existing_tasks.md` — scheduled-task reuse rule
