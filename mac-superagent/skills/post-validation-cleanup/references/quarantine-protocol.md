# Quarantine protocol

Stage 1 of the post-validation-cleanup skill stages candidates in a date-stamped
folder rather than deleting. Stage 2 (scheduled daily) hard-deletes after the
7-day grace period.

## Folder layout

```
~/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/
└── _pending_delete_YYYY-MM-DD/
    ├── manifest.md
    ├── outputs/
    │   ├── build_v2_workbook.py
    │   └── source_dump.json
    └── workspace/
        └── NWM_PE_Mapping_v1.xlsx
```

One folder per cleanup run, dated. Original relative paths preserved inside.

## manifest.md format

```markdown
# Cleanup manifest — 2026-05-14

**Triggered by:** Dan validating `NWM_SimCorp_Pricing_Documentation_v2.xlsx`
**Conversation:** <session_id>
**Quarantine expires:** 2026-05-21 (Stage 2 hard-delete will run if untouched)

## Items staged

| # | Original path | Size | Category | Reason | SHA256 |
|---|---------------|------|----------|--------|--------|
| 1 | /outputs/build_v2_workbook.py | 18 KB | B | Build script; deliverable validated; reproducible from XLSX + memory | abc123... |
| 2 | /outputs/source_dump.json | 6.1 MB | B | Intermediate JSON dump from v1 read | def456... |
| 3 | /outputs/NWM_SimCorp_Pricing_Documentation_v2.xlsx | 115 KB | A | SHA-match to workspace canonical | hash789... |

## Notion items archived

| # | Page | URL | Reason |
|---|------|-----|--------|
| 4 | NWM v1 draft | https://notion.so/... | Superseded by v3 |

## Restore commands

If you need to rescue anything:
```bash
# Restore item #1
mv "/path/to/_pending_delete_2026-05-14/outputs/build_v2_workbook.py" \
   "/sessions/.../outputs/build_v2_workbook.py"
```

For Notion items: open the URL, un-archive via the Notion UI menu.
```

## Stage 2 purge logic

Run daily at 02:00 by scheduled task `post-validation-cleanup-purge`.

For each `_pending_delete_YYYY-MM-DD/` folder under the workspace root:

1. Parse `YYYY-MM-DD` from folder name
2. If `YYYY-MM-DD + 7 days > today` → skip (still in grace period)
3. Compute the most-recent `mtime` across all files in the folder (recursive)
4. If `most_recent_mtime > quarantine_date` → skip (someone touched it; assume
   a rescue is in progress)
5. Otherwise `rm -rf` the folder
6. Append to `cleanup_log.md`:
   ```
   2026-05-21 02:00:13 — Purged _pending_delete_2026-05-14/ (3 files, 6.2 MB)
   ```

## cleanup_log.md location

`~/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/cleanup_log.md`

Append-only audit trail of every Stage 1 stage and Stage 2 purge.

## Safety

- Quarantine folder must be inside workspace, NEVER `~/Trash` or `/tmp`
  (sandbox tmp is wiped between sessions; system Trash auto-empties)
- iCloud sync preserves the quarantine folder across devices — if Dan moves
  files out via Finder on another device, the next Stage 2 sweep will see
  the `mtime` change and skip
- `rm -rf` is the final action — confirm the folder name matches the expected
  pattern before issuing
- If the user is mid-conversation when Stage 2 fires (scheduled task runs in
  background), do NOT interrupt — log silently and let them see it in the
  morning briefing
