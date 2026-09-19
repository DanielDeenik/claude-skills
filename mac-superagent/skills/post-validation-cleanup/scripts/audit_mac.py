#!/usr/bin/env python3
"""
Audit Mac filesystem for cleanup candidates per the post-validation-cleanup
skill ruleset. Produces JSON list of candidates; never deletes.

Usage:
  python3 audit_mac.py \
    --workspace "/Users/<user>/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp" \
    --outputs   "/Users/<user>/Library/Application Support/Claude/local-agent-mode-sessions/.../outputs" \
    [--include-hash-dupes] \
    > candidates.json

The workspace and outputs paths come from the conversation's <env> block —
NEVER hardcode session UUIDs or user paths.
"""
import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

EXCLUDE_DIRS = {".git", ".claude", ".cursor", ".vscode", "memory",
                "_pending_delete_", "node_modules", "__pycache__", ".venv"}
EXCLUDE_FILE_PATTERNS = [r"^\.DS_Store$", r"^\.gitkeep$",
                         r"^__init__\.py$", r"^LICENSE$"]
SAFE_DUPES = {"__init__.py", ".gitkeep", "LICENSE", "README.md"}

VERSION_SUFFIX_RE = re.compile(r"(.+?)_v(\d+)(\.[^.]+)$", re.IGNORECASE)
DRAFT_SUFFIXES = ("_draft", "_old", "_backup", "_wip", "_temp")
BUILD_SCRIPT_PATTERNS = [
    r"^build_.*\.py$", r"^append_.*\.py$", r"^rename_.*\.py$",
    r"^.*_dump\.json$", r"^source_.*\.json$"
]


def excluded(p: Path) -> bool:
    for part in p.parts:
        if any(part.startswith(d.rstrip("_")) for d in EXCLUDE_DIRS):
            return True
    for pat in EXCLUDE_FILE_PATTERNS:
        if re.search(pat, p.name):
            return True
    return False


def sha256_file(p: Path, max_bytes=200 * 1024 * 1024) -> str:
    if p.stat().st_size > max_bytes:
        return ""  # skip very large files
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def category_A(outputs_root: Path, workspace_root: Path):
    """Sandbox /outputs/ files that are SHA-identical to a workspace file."""
    if not outputs_root.exists():
        return []
    workspace_hashes = {}
    for f in workspace_root.rglob("*"):
        if f.is_file() and not excluded(f.relative_to(workspace_root)):
            h = sha256_file(f)
            if h:
                workspace_hashes.setdefault(h, []).append(str(f))
    candidates = []
    for f in outputs_root.rglob("*"):
        if not f.is_file() or excluded(f.relative_to(outputs_root)):
            continue
        h = sha256_file(f)
        if not h:
            continue
        if h in workspace_hashes:
            candidates.append({
                "path": str(f),
                "size_bytes": f.stat().st_size,
                "sha256": h,
                "category": "A",
                "reason": f"SHA-match to workspace canonical: {workspace_hashes[h][0]}",
                "canonical_counterpart": workspace_hashes[h][0],
            })
    return candidates


def category_B(outputs_root: Path):
    """Build artefacts: build_*.py, append_*.py, *_dump.json in /outputs/."""
    if not outputs_root.exists():
        return []
    candidates = []
    for f in outputs_root.rglob("*"):
        if not f.is_file() or excluded(f.relative_to(outputs_root)):
            continue
        if any(re.search(pat, f.name) for pat in BUILD_SCRIPT_PATTERNS):
            candidates.append({
                "path": str(f),
                "size_bytes": f.stat().st_size,
                "category": "B",
                "reason": "Build artefact / intermediate dump; deliverable likely validated",
            })
    return candidates


def category_C(workspace_root: Path):
    """Superseded versions: foo_v1.xlsx when foo_v2.xlsx exists in same folder."""
    candidates = []
    versioned = {}
    for f in workspace_root.rglob("*"):
        if not f.is_file() or excluded(f.relative_to(workspace_root)):
            continue
        m = VERSION_SUFFIX_RE.match(f.name)
        if m:
            base, version, ext = m.group(1), int(m.group(2)), m.group(3)
            key = (str(f.parent), base.lower(), ext.lower())
            versioned.setdefault(key, []).append((version, f))
    for key, items in versioned.items():
        items.sort(key=lambda x: x[0], reverse=True)
        latest_v = items[0][0]
        for v, f in items:
            if v < latest_v:
                candidates.append({
                    "path": str(f),
                    "size_bytes": f.stat().st_size,
                    "category": "C",
                    "reason": f"Older version (v{v}); v{latest_v} exists in same folder",
                })
    # Draft / old / backup suffixes
    for f in workspace_root.rglob("*"):
        if not f.is_file() or excluded(f.relative_to(workspace_root)):
            continue
        stem = f.stem.lower()
        for suf in DRAFT_SUFFIXES:
            if stem.endswith(suf):
                base_name = stem[:-len(suf)] + f.suffix
                if (f.parent / base_name).exists():
                    candidates.append({
                        "path": str(f),
                        "size_bytes": f.stat().st_size,
                        "category": "C",
                        "reason": f"{suf} suffix; non-suffix version exists in same folder",
                    })
                break
    return candidates


def category_E(outputs_root: Path, days=7):
    """Stale /outputs/ files older than N days."""
    if not outputs_root.exists():
        return []
    cutoff = datetime.now() - timedelta(days=days)
    candidates = []
    for f in outputs_root.rglob("*"):
        if not f.is_file() or excluded(f.relative_to(outputs_root)):
            continue
        if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
            candidates.append({
                "path": str(f),
                "size_bytes": f.stat().st_size,
                "category": "E",
                "reason": f"Stale: not modified in {days}+ days",
            })
    return candidates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--include-hash-dupes", action="store_true",
                    help="Also run Category D (cross-tree hash dupes)")
    args = ap.parse_args()

    workspace = Path(args.workspace)
    outputs = Path(args.outputs)

    if not workspace.exists():
        print(json.dumps({"error": f"workspace not found: {workspace}"}))
        return 1

    candidates = []
    candidates += category_A(outputs, workspace)
    candidates += category_B(outputs)
    candidates += category_C(workspace)
    candidates += category_E(outputs)

    # De-duplicate by path (a file might match multiple categories)
    seen = {}
    for c in candidates:
        if c["path"] in seen:
            seen[c["path"]]["category"] += f"+{c['category']}"
            seen[c["path"]]["reason"] += f"; ALSO: {c['reason']}"
        else:
            seen[c["path"]] = c

    out = {
        "audit_timestamp": datetime.now().isoformat(timespec="seconds"),
        "workspace": str(workspace),
        "outputs": str(outputs),
        "candidate_count": len(seen),
        "total_size_bytes": sum(c["size_bytes"] for c in seen.values()),
        "candidates": list(seen.values()),
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
