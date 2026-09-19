#!/usr/bin/env python3
"""
Stage 2 of post-validation-cleanup. Runs daily at 02:00 via scheduled task.

For every `_pending_delete_YYYY-MM-DD/` folder under the workspace root:
  - If 7+ days have passed since YYYY-MM-DD AND nothing inside has been
    touched since the quarantine date, rm -rf the folder
  - Otherwise skip (still in grace period or files were rescued)

Append a summary line per action to `cleanup_log.md` in workspace root.

Usage:
  python3 quarantine_purge.py --workspace "/path/to/workspace"

Exits 0 on success regardless of whether anything was purged.
"""
import argparse
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

QUARANTINE_RE = re.compile(r"^_pending_delete_(\d{4}-\d{2}-\d{2})$")
GRACE_DAYS = 7


def folder_size_and_count(folder: Path):
    total = 0
    count = 0
    for p in folder.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
            count += 1
    return total, count


def most_recent_mtime(folder: Path) -> datetime:
    latest = datetime.fromtimestamp(0)
    for p in folder.rglob("*"):
        if p.is_file() or p.is_dir():
            try:
                m = datetime.fromtimestamp(p.stat().st_mtime)
                if m > latest:
                    latest = m
            except FileNotFoundError:
                pass
    return latest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    args = ap.parse_args()
    workspace = Path(args.workspace)

    if not workspace.exists():
        print(f"workspace not found: {workspace}", file=sys.stderr)
        return 1

    log = workspace / "cleanup_log.md"
    today = datetime.now().date()
    actions = []

    for folder in workspace.iterdir():
        if not folder.is_dir():
            continue
        m = QUARANTINE_RE.match(folder.name)
        if not m:
            continue
        quar_date = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        if (today - quar_date) < timedelta(days=GRACE_DAYS):
            continue  # still in grace period

        # Check if anyone touched files inside since the quarantine date
        last_touch = most_recent_mtime(folder).date()
        if last_touch > quar_date:
            actions.append((
                folder.name,
                "SKIPPED",
                f"touched on {last_touch} (after quarantine date {quar_date}) — assumed rescue in progress",
                0, 0,
            ))
            continue

        # Safe to purge
        size, count = folder_size_and_count(folder)
        try:
            shutil.rmtree(folder)
            actions.append((folder.name, "PURGED",
                            f"untouched for {(today - quar_date).days} days",
                            size, count))
        except Exception as e:
            actions.append((folder.name, "ERROR", str(e), size, count))

    # Append to log
    if actions:
        with open(log, "a") as f:
            for name, status, reason, size, count in actions:
                ts = datetime.now().isoformat(timespec="seconds")
                if status == "PURGED":
                    f.write(f"{ts} — Purged {name} ({count} files, {size:,} bytes) — {reason}\n")
                else:
                    f.write(f"{ts} — {status} {name} — {reason}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
