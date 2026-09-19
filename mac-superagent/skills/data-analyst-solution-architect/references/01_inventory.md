# 01 — Source Inventory

## Goal

A complete picture of every file the deliverable depends on, before any output cell is written.

## Output

A markdown table written to `_inventory_{date}.md` in the working directory, with one row per input file:

| # | Path | Role | Rows | Cols | Encoding | First-seen | Description |

## Steps

1. **Read every path in INTAKE field 7.** Use the Read tool. Confirm the file exists. Record its size and modification date.
2. **Parse each file with the correct loader.** XLSX → openpyxl/pandas; CSV → pandas with encoding detection (utf-8 → utf-16 → utf-16-le → cp1252 → latin-1 fallback chain); DOCX → python-docx; PDF → PyPDF2 or pdfplumber; HTML → BeautifulSoup. Print `loaded {path} → {rows} × {cols} ({encoding})`.
3. **Record column union per vertical / per section.** For each per-vertical scope from INTAKE field 12, compute the union of columns across the inputs that map to that vertical.
4. **Flag any anomalies up front.** UTF-16 BOM, blank header row, merged cells, duplicate columns (auto-suffixed `.1`), zero-row sheets, files whose advertised vertical doesn't appear in the data.

## Anti-pattern: "I'll figure out the encoding when I get there"

UTF-16 .txt files hit the Nicola build twice. The fix is the encoding fallback chain, applied at load time, with a print statement. Confirmation that you loaded the file is the only thing that proves the path was right.

## Anti-pattern: "Most fields will overlap so I'll just read one"

Per-vertical = column union. You must read every file in the vertical's input set. The verticals where a column only appears in one file are exactly the verticals where skipping a file silently drops a field.
