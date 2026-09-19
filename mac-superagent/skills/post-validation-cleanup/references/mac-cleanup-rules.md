# Mac filesystem cleanup ruleset

Canonical workspace per `reference_mac_filesystem.md`:
`~/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/`
(legacy iCloud path, NOT CloudStorage).

Sandbox outputs:
`/Users/<user>/Library/Application Support/Claude/local-agent-mode-sessions/.../local_*/outputs/`
(or whatever path the current Cowork session resolves to — read from
`<env>` block; never hardcode the session UUID).

## Categories — what counts as redundant

### Category A — Sandbox /outputs/ duplicates of workspace files
**Rule:** if a file exists in both the sandbox `/outputs/` AND the workspace
folder, and SHA256 matches, the `/outputs/` copy is redundant. The workspace
is canonical because the user can see it; the sandbox is invisible to them.

**Examples:** `/outputs/NWM_SimCorp_Pricing_Documentation_v2.xlsx` after
`cp` to workspace; `/outputs/anything.docx` after copy.

**Why redundant:** the sandbox is per-session, regenerable from build scripts
in memory. Workspace persists.

### Category B — Build artefacts whose deliverable is validated
**Rule:** Python build scripts (`build_*.py`, `append_*.py`,
`rename_*.py`) and intermediate data dumps (`*_dump.json`,
`*_extract.csv`, `source_*.json`) that produced a now-validated deliverable
are redundant. The deliverable itself supersedes them.

**Exception:** if the build script encodes non-trivial logic the user might
want to re-run (e.g. a re-buildable specification), Dan should explicitly
say "keep build scripts" — by default they go.

### Category C — Superseded versions in workspace
**Rule:** files matching `<base>_v[0-9]+.<ext>`, `<base>_draft.<ext>`,
`<base>_old.<ext>`, `<base>_backup.<ext>` are redundant when a newer
version (higher v-number, or no suffix) exists in the same folder.

**Examples:** `NWM_PE_Mapping_v1.xlsx` when `v2` or `v3` exists; anything
ending `_draft.docx` when the non-draft version exists.

**Never** consolidate version history unilaterally — flag for confirmation
only.

### Category D — Hash duplicates anywhere on Mac
**Rule:** for any file with SHA256 matching another file under workspace OR
under known consulting paths (`~/Documents/GitHub/akg/`,
`~/Documents/GitHub/Superagent_Consulting/`), keep the one in workspace, flag
the others.

**Exception:** `__init__.py`, `.gitkeep`, `LICENSE`, `README.md` are expected
duplicates — never flag.

### Category E — Stale sandbox files
**Rule:** files in `/outputs/` older than 7 days with no workspace
counterpart are likely orphaned intermediates. Flag for cleanup.

## NEVER auto-flag

- `memory/` directories (auto-memory store)
- `.claude/`, `.cursor/`, `.vscode/`, `~/.config/`, `~/.local/`
- Any file under `~/Documents/GitHub/<repo>/.git/`
- Plugin / skill source files under the canonical SimCorp SuperAgent path
- Files in the validated deliverable's own folder that are NOT version-stamped
  duplicates
- Anything Dan tagged "keep" earlier in the session

## Reporting format

Per candidate:
```
{
  "path": "/outputs/foo.json",
  "size_bytes": 6291456,
  "sha256": "abc123...",
  "category": "A | B | C | D | E",
  "reason": "human-readable why",
  "canonical_counterpart": "/workspace/.../foo.json"  // for A/D only
}
```

## Restore path

Quarantine moves preserve relative path under the quarantine folder. To
restore: `mv /workspace/_pending_delete_YYYY-MM-DD/outputs/foo.py /sessions/.../outputs/foo.py`
(or wherever the original path resolves on Mac).

## Edge cases

- **Symlinks** — `ls -l` to detect; never delete a symlink target via the link.
  Treat the symlink itself as a flag candidate only if the target is unreachable.
- **Open files** — `lsof` check before move; if open, skip and re-flag next run.
- **Mac aliases** (`.alias` extension or Finder-aliases) — leave alone; they're
  not regular files.
- **iCloud sync state** — files with `.icloud` extension are not yet downloaded.
  Skip; can't compute hash.
