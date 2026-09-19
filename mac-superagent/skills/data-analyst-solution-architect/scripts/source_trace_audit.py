#!/usr/bin/env python3
"""
source_trace_audit.py — verify every non-blank description cell has a non-blank
Source column adjacent. This is the Rule 7 enforcement at checkpoint 7.

Pairs every column matching the pattern `* Description` with the column
following it (expected to be `* Source` or `Source Locator` etc.). Any cell
where Description is non-blank and Source is blank is a RULE_7_VIOLATION.

Also counts `[GAP: ...]` markers per tab — these are honest gaps, not failures.

Usage:
    python source_trace_audit.py /path/to/deliverable.xlsx
"""
import re
import sys
from pathlib import Path
from openpyxl import load_workbook


GAP_RE = re.compile(r"^\[GAP:.*\]$")


def audit_workbook(xlsx_path: Path) -> int:
    wb = load_workbook(xlsx_path, data_only=True)
    total_violations = 0
    total_gaps = 0

    print(f"source_trace_audit — {xlsx_path}")
    print()

    for ws in wb.worksheets:
        # Find Description columns. Pattern: any header containing 'Description'.
        headers = [
            (col, ws.cell(row=1, column=col).value)
            for col in range(1, ws.max_column + 1)
        ]
        desc_cols: list[tuple[int, str, int, str]] = []
        # For each Description column, find the corresponding Source column.
        # Convention: the Source column is the next column to the right, OR a
        # column whose header starts with "Source" closest to the right.
        for col, header in headers:
            if header and "Description" in str(header):
                source_col = None
                source_header = None
                for c2, h2 in headers:
                    if c2 > col and h2 and (
                        str(h2).startswith("Source")
                        or "Locator" in str(h2)
                        or "Citation" in str(h2)
                    ):
                        source_col = c2
                        source_header = str(h2)
                        break
                if source_col is None and col < ws.max_column:
                    # fallback: column immediately to the right
                    source_col = col + 1
                    source_header = str(ws.cell(row=1, column=source_col).value or "")
                desc_cols.append((col, str(header), source_col or -1, source_header or ""))

        if not desc_cols:
            print(f"[{ws.title}] no Description columns — skipped")
            continue

        tab_violations = 0
        tab_gaps = 0
        for desc_col, desc_header, src_col, src_header in desc_cols:
            for row in range(2, ws.max_row + 1):
                desc_val = ws.cell(row=row, column=desc_col).value
                src_val = ws.cell(row=row, column=src_col).value if src_col > 0 else None
                if desc_val is None or str(desc_val).strip() == "":
                    continue
                desc_s = str(desc_val).strip()
                if GAP_RE.match(desc_s):
                    tab_gaps += 1
                    continue
                src_s = "" if src_val is None else str(src_val).strip()
                if not src_s:
                    tab_violations += 1
                    if tab_violations <= 5:  # show first 5 per tab
                        print(
                            f"  ✗ [{ws.title}] row {row}, col {desc_header!r}: "
                            f"description set, source ({src_header!r}) blank"
                        )

        print(
            f"[{ws.title}] description-source check: "
            f"{tab_violations} violations · {tab_gaps} GAP markers"
        )
        total_violations += tab_violations
        total_gaps += tab_gaps

    print()
    print(f"TOTAL: {total_violations} Rule-7 violations · {total_gaps} GAP markers")
    if total_violations:
        print("\nHALT — Rule 7 violations must be fixed before delivery.")
        return 1
    print("\n✓ Rule 7 passes — every non-blank description has a non-blank source.")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-deliverable.xlsx>", file=sys.stderr)
        return 4
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"FAIL — file not found: {p}", file=sys.stderr)
        return 4
    return audit_workbook(p)


if __name__ == "__main__":
    sys.exit(main())
