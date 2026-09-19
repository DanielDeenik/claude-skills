#!/usr/bin/env python3
"""
build_skeleton.py — generates a re-runnable build script skeleton for a new
engagement. Pass it the INTAKE.md path and it emits a `build_{deliverable}.py`
in the current directory with all paths, schema, and source-truth references
wired in. No hardcoded values — everything sourced from INTAKE.

Usage:
    python build_skeleton.py /path/to/INTAKE.md
"""
import re
import sys
from pathlib import Path
from datetime import date


SKELETON = '''"""Build {deliverable_name} v{version}.

Generated from INTAKE at: {intake_path}
Generated on: {today}

Re-running this script must produce a byte-identical XLSX (modulo cell
metadata timestamps). Edit only the CONFIG block to change behaviour —
column lists, paths, and rules come from INTAKE, source-truth map, and
schema spec files. NO HARDCODED VALUES.
"""
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

# --- CONFIG (auto-wired from INTAKE) -----------------------------------------
INTAKE_PATH = Path(r"{intake_path}")
SOURCE_TRUTH_MAP = Path(r"{intake_dir}/_source_truth_map.csv")
SCHEMA_SPEC = Path(r"{intake_dir}/_schema_design.md")
OUTPUT_DIR = Path(r"{intake_dir}")
DELIVERABLE = OUTPUT_DIR / "{deliverable_name}"

ENCODING_CHAIN = ["utf-8", "utf-16", "utf-16-le", "cp1252", "latin-1"]

# --- LOAD HELPERS ------------------------------------------------------------
def load_with_encoding_fallback(path):
    """Try each encoding in the chain. Print which one worked."""
    p = Path(path)
    if p.suffix.lower() in (".xlsx", ".xls", ".xlsm"):
        df = pd.read_excel(p)
        print(f"  loaded {{p.name}} (xlsx) → {{len(df)}} × {{len(df.columns)}}")
        return df
    for enc in ENCODING_CHAIN:
        try:
            df = pd.read_csv(p, encoding=enc, sep=None, engine="python")
            print(f"  loaded {{p.name}} ({{enc}}) → {{len(df)}} × {{len(df.columns)}}")
            return df
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise RuntimeError(f"could not decode {{p}} with any of {{ENCODING_CHAIN}}")

def parse_intake_inputs(intake_path):
    """Extract the inputs table from the INTAKE.md inputs section."""
    text = intake_path.read_text(encoding="utf-8")
    inputs = []
    m = re.search(r"## 7\\. inputs\\s*\\n(.*?)(?=^## )",
                  text, re.MULTILINE | re.DOTALL)
    if not m:
        raise RuntimeError("could not find INTAKE inputs section")
    for line in m.group(1).splitlines():
        if "|" not in line or line.startswith("|---") or "path" in line.lower():
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4 and parts[1] and parts[1] != "":
            inputs.append({{
                "path": parts[1],
                "role": parts[2],
                "description": parts[3],
            }})
    return inputs

# --- ANTI-SHORTCUT RULES ENFORCEMENT -----------------------------------------
def assert_atomic_yn(value):
    """Rule 2: Y/N values must be exactly Y, N, or blank."""
    if value not in ("Y", "N", "", None):
        raise ValueError(f"Y/N value must be Y, N, or blank — got {{value!r}}")
    return value

def assert_desc_source_pair(description, source):
    """Rule 7: non-blank description requires non-blank source."""
    desc_set = description and str(description).strip()
    src_set = source and str(source).strip()
    if desc_set and not src_set:
        raise ValueError(
            f"Rule 7 violation: description set ({{description[:50]!r}}) but source blank"
        )

def assert_cell_length(value, max_chars=150):
    """Rule 9: cells over 150 chars should be split into atomic columns."""
    if value and len(str(value)) > max_chars:
        print(f"  WARN — cell length {{len(str(value))}} > {{max_chars}}: {{str(value)[:60]}}...")

# --- BUILD -------------------------------------------------------------------
import re  # for parse_intake_inputs

def main():
    print(f"build {{DELIVERABLE.name}}")
    print(f"  INTAKE: {{INTAKE_PATH}}")
    inputs = parse_intake_inputs(INTAKE_PATH)
    print(f"  inputs: {{len(inputs)}}")

    data = {{}}
    for inp in inputs:
        path = Path(inp["path"])
        if not path.exists():
            raise FileNotFoundError(f"INTAKE references missing file: {{path}}")
        data[path.name] = load_with_encoding_fallback(path)

    wb = Workbook()
    wb.remove(wb.active)

    # TODO: build tabs per schema spec
    # for tab in schema['tabs']:
    #     ws = wb.create_sheet(tab['name'])
    #     write_header(ws, tab['columns'])
    #     for row in iter_rows(tab, data, source_truth):
    #         write_row(ws, row)
    #         assert_atomic_yn(row['Imported Y/N'])
    #         assert_desc_source_pair(row['Description'], row['Source'])

    wb.save(DELIVERABLE)
    print(f"saved {{DELIVERABLE}}")


if __name__ == "__main__":
    main()
'''


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-INTAKE.md>", file=sys.stderr)
        return 4

    intake = Path(sys.argv[1])
    if not intake.exists():
        print(f"FAIL — INTAKE not found: {intake}", file=sys.stderr)
        return 4

    text = intake.read_text(encoding="utf-8")
    m1 = re.search(r"## 3\. deliverable_name\s*\n+([^\n]+)", text)
    m2 = re.search(r"## 4\. version\s*\n+([^\n]+)", text)
    deliverable = (m1.group(1).strip() if m1 else "deliverable.xlsx").replace("{N}", "1").replace("{YYYY_MM_DD}", date.today().strftime("%Y_%m_%d"))
    version = m2.group(1).strip() if m2 else "v1"

    out = Path.cwd() / f"build_{Path(deliverable).stem}.py"
    out.write_text(
        SKELETON.format(
            deliverable_name=deliverable,
            version=version,
            intake_path=str(intake),
            intake_dir=str(intake.parent),
            today=date.today().isoformat(),
        ),
        encoding="utf-8",
    )
    print(f"wrote {out}")
    print("Next: open the file and fill in the TODO sections — schema parsing + iter_rows logic.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
