# 05 — Full Build

## Goal

Scale the v0.1 slice pattern across every section. The build is a single `.py` script — re-runnable, idempotent, no hardcoded paths (Dan's project rule).

## Output

1. `build_{deliverable}_{version}.py` — the build script (re-runnable).
2. `{deliverable_name}.xlsx` — the primary workbook.
3. `_build_log_{date}.txt` — what loaded, what was skipped, what wrote.

## Build script structure

```python
"""Build {deliverable} v{N}."""
from pathlib import Path
import pandas as pd
from openpyxl import Workbook

# --- CONFIG (from INTAKE, never hardcoded) ----------------------------------
INTAKE = Path("INTAKE.md")  # parse upfront
INPUTS = parse_intake_inputs(INTAKE)        # list of {path, role, description}
SOURCE_TRUTH = pd.read_csv("_source_truth_map_*.csv")
SCHEMA = parse_schema("_schema_design_*.md")
SCOPE = parse_intake_scope(INTAKE)

# --- LOAD -------------------------------------------------------------------
data = {}
for inp in INPUTS:
    df = load_with_encoding_fallback(inp["path"])   # utf-8 → utf-16 → utf-16-le → cp1252
    print(f"loaded {inp['path']} → {len(df)} × {len(df.columns)}")
    data[inp["path"]] = df

# --- BUILD PER TAB ----------------------------------------------------------
wb = Workbook()
for tab in SCHEMA["tabs"]:
    ws = wb.create_sheet(tab["name"])
    write_header(ws, tab["columns"])
    if tab.get("banner_panel"):
        write_banner(ws, tab["banner_panel"])
    for row in iter_rows(tab, data, SOURCE_TRUTH, SCOPE):
        write_row(ws, row)
    print(f"tab {tab['name']}: {ws.max_row} × {ws.max_column}")

# --- SAVE -------------------------------------------------------------------
out = Path(INTAKE.parent) / f"{SCHEMA['deliverable_name']}.xlsx"
wb.save(out)
print(f"saved {out}")
```

## Rules the build script must enforce

| At write time | Enforced by |
|---|---|
| Atomic Y/N values (Y, N, or blank) | `assert v in ("Y", "N", "")` |
| Description → Source pair | `assert (desc == "") or (source != "")` |
| Cell length ≤ 150 chars | warn if exceeded; reroute to atomic columns |
| `[GAP: <reason>]` for missing descriptions | substitute when source-search empty |
| Column names match v22 convention | template loaded from INTAKE field 16 |

## Re-runnable

Re-running the script must produce a byte-identical output (modulo timestamps in cell metadata). Test by running twice and diffing.

## No hardcoded values (Dan's project rule)

Every input path, every constant, every column name comes from INTAKE, source-truth map, or schema. If you find yourself typing a path or a column name in the script, stop — move it to a config file.

## Anti-pattern: "I'll write per-tab logic inline"

The build script iterates over SCHEMA. If a tab needs special handling (banner panel, sort order, color coding), the SCHEMA spec carries that, not the script. Adding a new tab is a schema change, not a code change.

## Anti-pattern: "Loading errors are recoverable"

If a file in INPUTS fails to load, the build halts. Do not silently skip. The Nicola UTF-16 BOM failure took a session to diagnose because the loader silently fell back to empty DataFrame.
