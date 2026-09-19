#!/usr/bin/env python3
"""
rag_gate.py — Hard pre-answer gate for simcorp-super-agent skill.

Every SimCorp factual question, deliverable-producing task, or Nicola-related
synthesis invocation MUST run this gate BEFORE any file reads, doc writes, or
answer production. The gate:

  1. Opens the canonical AKG DuckDB facts store (akg.duckdb.cowork).
  2. Runs a keyword scan against facts.source_citations.extracted_text.
  3. Returns a JSON token with {gate_id, query, hit_count, top_5_sources,
     timestamp, session_hint}.
  4. Appends the gate call to ~/.auto-memory/rag_gate.log.jsonl for auditability.
  5. Exits non-zero if no --query is provided (forces invocation).

Output token format (paste into response verbatim before any other content):

  <rag-gate id="gate_YYYYMMDD_HHMMSS_NNN" hits="N">
    query: "<text>"
    top_sources:
      - [tier N] <source_name> (K hits)
      - ...
  </rag-gate>

If hit_count == 0, you MUST declare "RAG-EMPTY" in your response and justify
why you're proceeding to read source files anyway.

USAGE
  python3 rag_gate.py --query "FO_DECOMP_DAILY batch chain"
  python3 rag_gate.py --query "redemption policy" --limit 10
  python3 rag_gate.py --query "SAAM TAA wealth" --db /custom/path/akg.duckdb
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# --- config resolution --------------------------------------------------------

DEFAULT_DB_CANDIDATES = [
    # On Dan's Mac, AKG runs from the GitHub clone (per auto-memory
    # feedback_run_from_github): venv 3.12 is installed in that clone.
    Path.home() / "Documents" / "GitHub" / "akg" / "data" / "akg.duckdb",
    # On the Cowork VM mount, the populated DB lives under the workspace:
    Path(os.environ.get("AKG_DB_PATH", "")) if os.environ.get("AKG_DB_PATH") else None,
    # Fallback: iCloud workspace copy
    Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs"
        / "01 Work & Business" / "a. Consulting - SimCorp" / "akg" / "data"
        / "akg.duckdb.cowork",
]

LOG_PATH = Path.home() / ".auto-memory" / "rag_gate.log.jsonl"

# --- gate implementation ------------------------------------------------------

def resolve_db_path(explicit: str | None) -> Path:
    """Return the first AKG DB path that actually exists."""
    if explicit:
        p = Path(explicit).expanduser()
        if p.exists():
            return p
        raise SystemExit(f"rag_gate: --db {explicit} does not exist")
    for candidate in DEFAULT_DB_CANDIDATES:
        if candidate and candidate.exists():
            return candidate
    raise SystemExit(
        "rag_gate: No AKG DuckDB found. Checked:\n  "
        + "\n  ".join(str(c) for c in DEFAULT_DB_CANDIDATES if c)
        + "\nSet AKG_DB_PATH env var or pass --db."
    )


def run_keyword_gate(db_path: Path, query: str, limit: int = 5) -> dict:
    """Keyword-scan source_citations for query, return summary token."""
    try:
        import duckdb
    except ImportError:
        raise SystemExit(
            "rag_gate: duckdb not installed. Install with: "
            "pip install duckdb --break-system-packages"
        )

    con = duckdb.connect(str(db_path), read_only=True)
    like_pattern = f"%{query.lower()}%"

    total_hits = con.execute(
        "SELECT COUNT(*) FROM facts.source_citations "
        "WHERE lower(extracted_text) LIKE ?",
        [like_pattern],
    ).fetchone()[0]

    top_sources = con.execute(
        """
        SELECT source_uri, tier, COUNT(*) AS hits
        FROM facts.source_citations
        WHERE lower(extracted_text) LIKE ?
        GROUP BY source_uri, tier
        ORDER BY hits DESC
        LIMIT ?
        """,
        [like_pattern, limit],
    ).fetchall()

    con.close()

    gate_id = (
        "gate_"
        + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        + "_"
        + uuid.uuid4().hex[:4]
    )

    return {
        "gate_id": gate_id,
        "query": query,
        "db_path": str(db_path),
        "hit_count": total_hits,
        "top_sources": [
            {"source": Path(uri).name, "tier": tier, "hits": hits}
            for (uri, tier, hits) in top_sources
        ],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def render_token(summary: dict) -> str:
    """Render the token block the agent embeds in its response."""
    lines = [
        f'<rag-gate id="{summary["gate_id"]}" hits="{summary["hit_count"]}">',
        f'  query: "{summary["query"]}"',
        f'  db: {Path(summary["db_path"]).name}',
        "  top_sources:",
    ]
    for s in summary["top_sources"]:
        lines.append(f'    - [tier {s["tier"]}] {s["source"]} ({s["hits"]} hits)')
    if summary["hit_count"] == 0:
        lines.append("  status: RAG-EMPTY — agent must justify proceeding without RAG grounding")
    lines.append("</rag-gate>")
    return "\n".join(lines)


def log_gate(summary: dict) -> None:
    """Append gate call to audit log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(summary) + "\n")


# --- CLI ----------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hard pre-answer RAG gate for simcorp-super-agent."
    )
    parser.add_argument(
        "--query", required=True,
        help="Keyword or phrase to scan against the AKG corpus."
    )
    parser.add_argument(
        "--limit", type=int, default=5,
        help="Top-N source hits to include in the token (default 5)."
    )
    parser.add_argument(
        "--db", default=None,
        help="Path to AKG DuckDB file. Defaults to the first match from "
             "DEFAULT_DB_CANDIDATES or $AKG_DB_PATH env."
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Emit full JSON instead of the rendered token block."
    )
    args = parser.parse_args()

    db_path = resolve_db_path(args.db)
    summary = run_keyword_gate(db_path, args.query, limit=args.limit)
    log_gate(summary)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(render_token(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
