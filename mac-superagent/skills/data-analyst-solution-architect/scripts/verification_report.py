#!/usr/bin/env python3
"""
verification_report.py — generate the checkpoint-7 verification report.

Runs against a deliverable XLSX and emits a markdown report covering:
  A. Count audit
  B. Source-trace audit (delegates to source_trace_audit.py)
  C. Gap audit
  D. Citation spot-check sampling (10 random non-blank descriptions)
  E. SME Q&A coverage

Usage:
    python verification_report.py <xlsx> [--intake <intake.md>] [--out <report.md>]
"""
import argparse
import random
import re
import sys
from pathlib import Path
from openpyxl import load_workbook


GAP_RE = re.compile(r"^\[GAP:.*\]$")


def count_audit(wb) -> dict:
    return {
        ws.title: {
            "rows": ws.max_row,
            "cols": ws.max_column,
        }
        for ws in wb.worksheets
    }


def gap_audit(wb) -> dict:
    gaps_per_tab: dict[str, dict[str, int]] = {}
    for ws in wb.worksheets:
        tab: dict[str, int] = {}
        for row in ws.iter_rows(values_only=True):
            for v in row:
                if v is None:
                    continue
                s = str(v).strip()
                if GAP_RE.match(s):
                    # extract the reason after "GAP:"
                    reason = s[5:-1].strip()  # strip [GAP: and ]
                    tab[reason] = tab.get(reason, 0) + 1
        gaps_per_tab[ws.title] = tab
    return gaps_per_tab


def citation_spot_check(wb, n: int = 10) -> list[dict]:
    """Sample N random non-blank description cells. Return their value + source."""
    candidates: list[dict] = []
    for ws in wb.worksheets:
        headers = {ws.cell(row=1, column=c).value: c for c in range(1, ws.max_column + 1)}
        desc_cols = {h: c for h, c in headers.items() if h and "Description" in str(h)}
        src_cols = {h: c for h, c in headers.items() if h and (str(h).startswith("Source") or "Locator" in str(h))}
        if not desc_cols or not src_cols:
            continue
        first_src_col = min(src_cols.values())
        for desc_h, desc_c in desc_cols.items():
            for row in range(2, ws.max_row + 1):
                desc = ws.cell(row=row, column=desc_c).value
                if not desc:
                    continue
                s = str(desc).strip()
                if not s or GAP_RE.match(s):
                    continue
                src = ws.cell(row=row, column=first_src_col).value
                candidates.append({
                    "tab": ws.title,
                    "row": row,
                    "column": str(desc_h),
                    "value": s[:120],
                    "source": str(src or "")[:120],
                })
    if len(candidates) <= n:
        return candidates
    return random.sample(candidates, n)


def sme_qa_coverage(wb, expected_count: int | None) -> dict:
    target_tabs = ["SME_QA_Full", "SME_QA"]
    found = 0
    found_in = None
    for ws in wb.worksheets:
        if ws.title in target_tabs:
            # count rows excluding header
            for row in range(2, ws.max_row + 1):
                v = ws.cell(row=row, column=1).value
                if v and str(v).strip():
                    found += 1
            found_in = ws.title
            break
    return {
        "found": found,
        "found_in": found_in,
        "expected": expected_count,
        "match": (expected_count is None) or (found == expected_count),
    }


def render_report(xlsx: Path, counts, gaps, samples, sme) -> str:
    lines: list[str] = []
    lines.append(f"# Verification Report — {xlsx.name}")
    lines.append("")
    lines.append("## A. Count audit")
    lines.append("")
    lines.append("| Tab | Rows | Cols |")
    lines.append("|---|---|---|")
    for tab, c in counts.items():
        lines.append(f"| {tab} | {c['rows']} | {c['cols']} |")
    lines.append("")

    lines.append("## B. Source-trace audit (Rule 7)")
    lines.append("")
    lines.append("Run `python source_trace_audit.py <xlsx>` for the full pairwise check.")
    lines.append("")

    lines.append("## C. Gap audit")
    lines.append("")
    total_gaps = sum(sum(v.values()) for v in gaps.values())
    lines.append(f"Total `[GAP:]` markers across all tabs: **{total_gaps}**")
    lines.append("")
    for tab, reasons in gaps.items():
        if not reasons:
            continue
        lines.append(f"### {tab}")
        for r, n in sorted(reasons.items(), key=lambda x: -x[1]):
            lines.append(f"  - {n} × `{r}`")
        lines.append("")

    lines.append("## D. Citation spot-check")
    lines.append("")
    lines.append(f"Sampled {len(samples)} non-blank descriptions. Review each citation manually.")
    lines.append("")
    lines.append("| Tab | Row | Column | Value (≤120 chars) | Source (≤120 chars) |")
    lines.append("|---|---|---|---|---|")
    for s in samples:
        lines.append(f"| {s['tab']} | {s['row']} | {s['column']} | {s['value']} | {s['source']} |")
    lines.append("")

    lines.append("## E. SME Q&A coverage")
    lines.append("")
    if sme["found_in"]:
        lines.append(
            f"SME Q&A tab `{sme['found_in']}` has {sme['found']} items "
            f"(expected: {sme['expected']}). "
            f"Match: {'YES' if sme['match'] else 'NO'}"
        )
    else:
        lines.append("No SME_QA / SME_QA_Full tab found — skip if INTAKE field 13 = 'none'.")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"Generated for {xlsx} by verification_report.py")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx", help="path to deliverable XLSX")
    ap.add_argument("--intake", help="optional INTAKE.md (used to derive expected counts)")
    ap.add_argument("--out", help="output report path (default: _verification_report.md next to xlsx)")
    ap.add_argument("--sample", type=int, default=10)
    args = ap.parse_args()

    xlsx = Path(args.xlsx)
    if not xlsx.exists():
        print(f"FAIL — {xlsx} not found", file=sys.stderr)
        return 4

    wb = load_workbook(xlsx, data_only=True)
    counts = count_audit(wb)
    gaps = gap_audit(wb)
    samples = citation_spot_check(wb, args.sample)

    expected_sme = None
    if args.intake:
        text = Path(args.intake).read_text(encoding="utf-8")
        m = re.search(r"## 13\. sme_questions\s*\n+(.+?)(?=^## )", text, re.MULTILINE | re.DOTALL)
        if m:
            body = m.group(1)
            # count pipe-rows or bullet items as a rough heuristic
            expected_sme = sum(1 for line in body.splitlines() if line.strip().startswith("|") and "|" in line and "---" not in line and "From" not in line and "ID" not in line)

    sme = sme_qa_coverage(wb, expected_sme)

    out = Path(args.out) if args.out else xlsx.parent / "_verification_report.md"
    out.write_text(render_report(xlsx, counts, gaps, samples, sme), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
