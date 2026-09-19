#!/usr/bin/env python3
"""Turn a SimCorp Service Manager log export into a timeline and a finding sheet.

Input: the xlsx or csv exported from the Service Manager Log window. Expected
columns, in any order, matched by header text: Date, Message, Message type.
A first row holding a single URL (a support case link) is kept as context.

Output, to stdout or to the file given with --out:
  1. Header block: file, row count, time span, message type counts, case URL.
  2. Collapsed timeline: every line whose pattern occurs at most --keep times,
     in time order, then one summary row per repeated pattern with its count,
     first and last time.
  3. Flagged lines: every row whose type is not Information, plus every row that
     matches a watch pattern (DEAD, Unknown, ConnectionReset, exception, error,
     fail, denied, not found, could not load, out of date).
  4. Membership block for Data Store logs: the node this instance runs on, the
     other hosts, and the DEAD nodes, so the quorum arithmetic is explicit.

The script never names a cause. It reports counts, order and matches.

Usage:
  python3 read_service_log.py export.xlsx
  python3 read_service_log.py export.csv --keep 2 --out timeline.md
"""
import argparse
import csv
import re
import sys
from collections import Counter, OrderedDict
from datetime import datetime

WATCH = re.compile(
    r"DEAD|Unknown|ConnectionReset|exception|error|fail|denied|not found|"
    r"could not load|out of date|refused|timeout",
    re.IGNORECASE,
)
DATE_FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f", "%d/%m/%Y %H:%M:%S",
                "%m/%d/%Y %H:%M:%S", "%Y-%m-%dT%H:%M:%S")


def parse_date(value):
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def load_rows(path):
    rows = []
    case_url = None
    if path.lower().endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
        ws = wb.worksheets[0]
        raw = [list(r) for r in ws.iter_rows(values_only=True)]
    else:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            raw = [r for r in csv.reader(fh)]
    header_idx = None
    for i, r in enumerate(raw):
        cells = [str(c).strip().lower() if c is not None else "" for c in r]
        if "message" in cells and any(c.startswith("date") for c in cells):
            header_idx = i
            break
        joined = " ".join(c for c in cells if c)
        if joined.startswith("http"):
            case_url = joined
    if header_idx is None:
        sys.exit("No header row with Date and Message columns found.")
    header = [str(c).strip().lower() if c is not None else "" for c in raw[header_idx]]
    col = {}
    for i, h in enumerate(header):
        if h.startswith("date"):
            col["date"] = i
        elif h == "message":
            col["message"] = i
        elif "type" in h:
            col["type"] = i
    for r in raw[header_idx + 1:]:
        if r is None or all(c is None or str(c).strip() == "" for c in r):
            continue
        msg = r[col["message"]] if col.get("message") is not None and col["message"] < len(r) else None
        if msg is None:
            continue
        date = r[col["date"]] if col.get("date") is not None and col["date"] < len(r) else None
        typ = r[col["type"]] if col.get("type") is not None and col["type"] < len(r) else ""
        rows.append({"time": parse_date(date), "raw_time": str(date), "msg": str(msg).strip(),
                     "type": str(typ).strip() if typ is not None else ""})
    return rows, case_url


def pattern(msg):
    p = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "#guid", msg, flags=re.I)
    p = re.sub(r"\d+(\.\d+)*", "#", p)
    return p[:110]


def fmt(row):
    t = row["time"].strftime("%Y-%m-%d %H:%M:%S") if row["time"] else row["raw_time"]
    return f"{t} | {row['type']} | {row['msg']}"


def membership(rows):
    me, others, dead, ports = None, [], [], None
    for r in rows:
        m = r["msg"]
        hit = re.search(r"Starting EventStore at (\S+) i\.e\. (\S+)", m)
        if hit:
            me = f"{hit.group(2)} ({hit.group(1)})"
        hit = re.search(r"Other host: (\S+)", m)
        if hit:
            others.append(hit.group(1))
        hit = re.search(r"node \[([\d.]+):(\d+)\] is DEAD", m)
        if hit and hit.group(1) not in dead:
            dead.append(hit.group(1))
        hit = re.search(r"Service Starting on Tcp : (\d+) Http : (\d+)", m)
        if hit:
            ports = f"TCP {hit.group(1)}, HTTP {hit.group(2)}"
    return me, others, dead, ports


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--keep", type=int, default=2, help="max occurrences kept per pattern")
    ap.add_argument("--out")
    args = ap.parse_args()
    rows, case_url = load_rows(args.path)
    rows.sort(key=lambda r: (r["time"] is None, r["time"] or datetime.min))
    out = []
    times = [r["time"] for r in rows if r["time"]]
    out.append(f"# Service log timeline: {args.path}")
    out.append(f"Rows: {len(rows)}. Span: {min(times) if times else 'n/a'} to {max(times) if times else 'n/a'}.")
    out.append("Message types: " + ", ".join(f"{k} {v}" for k, v in Counter(r["type"] for r in rows).most_common()))
    if case_url:
        out.append(f"Case link in export: {case_url}")
    me, others, dead, ports = membership(rows)
    if me or others or dead:
        out.append("")
        out.append("## Data Store membership from the log")
        out.append(f"This node: {me or 'not stated'}")
        out.append(f"Other hosts configured: {', '.join(others) if others else 'none stated'}")
        out.append(f"Configured node count: {len(others) + 1 if me else 'unknown'}")
        out.append(f"Nodes reported DEAD: {', '.join(dead) if dead else 'none'}")
        out.append(f"Ports: {ports or 'not stated'}")
        if me and others:
            up = len(others) + 1 - len(dead)
            out.append(f"Nodes not reported DEAD: {up} of {len(others) + 1}. Write availability needs at least half (Front Office Configuration 16.4).")
    counts = Counter(pattern(r["msg"]) for r in rows)
    seen = Counter()
    first_last = OrderedDict()
    out.append("")
    out.append("## Collapsed timeline")
    for r in rows:
        p = pattern(r["msg"])
        seen[p] += 1
        first_last.setdefault(p, [r, r])
        first_last[p][1] = r
        if counts[p] <= args.keep or seen[p] <= args.keep:
            out.append(fmt(r) + (f"   [pattern repeats {counts[p]} times]" if counts[p] > args.keep and seen[p] == 1 else ""))
    repeated = [(p, c) for p, c in counts.items() if c > args.keep]
    if repeated:
        out.append("")
        out.append("## Repeated patterns")
        for p, c in sorted(repeated, key=lambda x: -x[1]):
            f, l = first_last[p]
            ft = f["time"].strftime("%H:%M:%S") if f["time"] else f["raw_time"]
            lt = l["time"].strftime("%H:%M:%S") if l["time"] else l["raw_time"]
            out.append(f"{c} times, {ft} to {lt}: {p}")
    flagged = [r for r in rows if r["type"].lower() != "information" or WATCH.search(r["msg"])]
    out.append("")
    out.append(f"## Flagged lines ({len(flagged)})")
    shown = Counter()
    for r in flagged:
        p = pattern(r["msg"])
        shown[p] += 1
        if shown[p] <= args.keep:
            out.append(fmt(r))
    text = "\n".join(out)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"Written {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
