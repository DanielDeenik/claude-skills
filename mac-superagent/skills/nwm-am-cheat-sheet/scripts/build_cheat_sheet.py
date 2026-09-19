"""
Build an NWM AM Front-Office cheat sheet (single DOCX per team).

Reads per-team config from teams/<team>.yaml, embeds screenshots from the
workspace _screenshots/ folder, and renders a 2-3 page DOCX in the approved
cheat-sheet format. See ../references/format_spec.md for the spec.

Usage
-----

    cd "<workspace>/ix. SimCorp SuperAgent/skills/nwm-am-cheat-sheet"

    # Build one team
    python3 scripts/build_cheat_sheet.py --team teams/private_debt.yaml

    # Build all teams that have a YAML
    python3 scripts/build_cheat_sheet.py --all

    # Custom paths
    python3 scripts/build_cheat_sheet.py \\
        --team teams/private_debt.yaml \\
        --output-dir "/custom/output" \\
        --screenshots-dir "/custom/screenshots"

Exits non-zero on YAML load failure or unwritable output path. Missing
screenshots are NOT a failure — the slot renders a placeholder box and the
build continues.

No hardcoded values: all team-specific data lives in YAML, all paths
resolve from --output-dir / --screenshots-dir CLI flags.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# =========================================================================
# Defaults — resolve workspace root by walking up from this script's location
# =========================================================================

SCRIPT_DIR = Path(__file__).resolve().parent           # .../scripts
SKILL_DIR = SCRIPT_DIR.parent                          # .../nwm-am-cheat-sheet
# Walk up to "a. Consulting - SimCorp" workspace root
# Skill path: <ws>/ix. SimCorp SuperAgent/skills/nwm-am-cheat-sheet/scripts/
WORKSPACE = SKILL_DIR.parent.parent.parent             # .../a. Consulting - SimCorp

DEFAULT_OUTPUT_DIR = WORKSPACE / "_AM_FO_TearSheets_2026_05_26"
DEFAULT_SCREENSHOTS_DIR = DEFAULT_OUTPUT_DIR / "_screenshots"
TEAMS_DIR = SKILL_DIR / "teams"

# Content width = 8.5" - 0.6" left - 0.6" right = 7.3" = 10512 DXA
CONTENT_WIDTH_DXA = 10512
IMAGE_WIDTH_IN = 7.0


# =========================================================================
# Style constants
# =========================================================================

NAVY = RGBColor(0x1E, 0x27, 0x61)
NAVY_HEX = "1E2761"
GOLD_HEX = "C9A961"
MUTED = RGBColor(0x5A, 0x64, 0x78)
TEXT = RGBColor(0x21, 0x29, 0x3C)


# =========================================================================
# Workflow content — constant across teams (see format_spec.md §1)
# =========================================================================

WORKFLOW_ROWS = [
    ("1", "Login", "Asset Manager",
     "Opens user session."),
    ("2", "Select Analysis Properties", "Analysis Properties",
     "Defines analytics scope, incl. term structure consumed by Cash Viewer."),
    ("3", "Apply Layout", "Layout (team-shared default; user can save own)",
     "Sheet configuration: columns, charts, filters, and panel arrangement."),
    ("4", "Load data", "Data Selector",
     "Pulls portfolios + positions into the session. Three modes: Selection Editor, My Portfolios, Quick Selection."),
    ("5", "Slice + visualise", "Portfolio Sheet",
     "Filter, dependency cascades to charts; add attribute columns (security data, analytics, accounting data)."),
    ("6", "Manage cash", "Cash Viewer",
     "Term structure from Analysis Properties; Options → Actual Dates surfaces forecast + actuals (ALMs, interest, dividends, coupons)."),
]


# =========================================================================
# Captions — constant across teams (see format_spec.md §2, §3, §4, §6)
# =========================================================================

CAPTION_AP = (
    "Analysis Properties lives in the AM ribbon → ANALYSIS group. Open the "
    "picker to confirm the team-linked profile is selected before loading data."
)
CAPTION_PORTFOLIO_SHEET = (
    "Portfolio Sheet (Labelled as Positions) visible attribute columns, "
    "groupings, filter row, and the chart panel underneath. Right-click any "
    "field → Select Fields to surface column choices."
)
CAPTION_DATA_SELECTOR = (
    "Data Selector panel (left side of the AM workspace). Selection Editor "
    "with the team's portfolios selected, or load a saved selection. F5 lists "
    "all saved setups; the Layout indicator at the bottom right confirms "
    "which Layout is currently applied."
)
CAPTION_CASH_VIEWER = (
    "Present + future cash by portfolio with the Details panel expanded. "
    "Forecast and actuals visible (ALMs, interest, dividends, coupons). "
    "Historical Mode can look back up to 10 business days; configure default "
    "in Settings Template → Cash Viewer tab."
)
CAPTION_CASH_VIEWER_OPTIONS = (
    "Toggle between Actual Dates and the defined Term Structure "
    "(e.g. Daily for 2 Weeks)."
)


# =========================================================================
# DOCX helpers
# =========================================================================

def setup_page(doc):
    sec = doc.sections[0]
    sec.page_height = Inches(11)
    sec.page_width = Inches(8.5)
    sec.left_margin = Inches(0.6)
    sec.right_margin = Inches(0.6)
    sec.top_margin = Inches(0.5)
    sec.bottom_margin = Inches(0.5)
    s = doc.styles["Normal"]
    s.font.name = "Calibri"
    s.font.size = Pt(10)


def shade(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def cell_pad(cell, top=60, bottom=60, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in (("top", str(top)), ("bottom", str(bottom)),
                      ("left", str(left)), ("right", str(right))):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:w"), val)
        e.set(qn("w:type"), "dxa")
        tcMar.append(e)
    tcPr.append(tcMar)


def set_cell(cell, text, *, bold=False, size=9.5, color=TEXT, align=None,
             italic=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    if align:
        p.alignment = align
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    r.font.color.rgb = color
    cell_pad(cell)
    return p


def _set_table_width(tbl, total_dxa):
    """Replace (not append) the tblW element on a table — avoids schema duplicates."""
    tblPr = tbl._element.find(qn("w:tblPr"))
    existing = tblPr.find(qn("w:tblW"))
    if existing is not None:
        tblPr.remove(existing)
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:w"), str(total_dxa))
    tblW.set(qn("w:type"), "dxa")
    tblPr.append(tblW)


# =========================================================================
# Page-level rendering (format_spec.md sections in order)
# =========================================================================

def title_band(doc, team_name):
    """Title band — format_spec.md §Title band."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("ASSET MANAGER — FRONT OFFICE CHEAT SHEET")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = MUTED

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(8)
    r2 = p2.add_run(team_name)
    r2.bold = True
    r2.font.size = Pt(20)
    r2.font.color.rgb = NAVY


def section_heading(doc, text):
    """Plain-numbered section heading (no §, no em-dash)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = NAVY
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), GOLD_HEX)
    pBdr.append(bottom)
    pPr.append(pBdr)


def section_subhead(doc, text):
    """Bold sub-heading inside a section — used above each screenshot."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = NAVY


def screenshot_image(doc, image_path, caption_text):
    """Embed image OR placeholder, then italic caption underneath.

    No light-blue [Screenshot] label band (format_spec.md — that band is REMOVED
    in the cheat sheet format).
    """
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_after = Pt(2)

    if image_path is not None and Path(image_path).exists():
        r = p_img.add_run()
        r.add_picture(str(image_path), width=Inches(IMAGE_WIDTH_IN))
    else:
        r = p_img.add_run("[ paste screenshot here ]")
        r.italic = True
        r.font.size = Pt(11)
        r.font.color.rgb = MUTED

    # Italic caption
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(caption_text)
    r_cap.italic = True
    r_cap.font.size = Pt(8.5)
    r_cap.font.color.rgb = MUTED


def workflow_table(doc):
    """§1 workflow table — constant content."""
    headers = ["#", "Step", "Component", "What it does"]
    widths_dxa = [480, 1800, 2900, 5332]  # sum = 10512 = full content width

    tbl = doc.add_table(rows=len(WORKFLOW_ROWS) + 1, cols=len(headers))
    tbl.autofit = False
    _set_table_width(tbl, CONTENT_WIDTH_DXA)

    for i, h in enumerate(headers):
        c = tbl.rows[0].cells[i]
        c.width = Inches(widths_dxa[i] / 1440)
        shade(c, NAVY_HEX)
        set_cell(c, h, bold=True, size=9.5,
                 color=RGBColor(0xFF, 0xFF, 0xFF),
                 align=WD_ALIGN_PARAGRAPH.LEFT)

    for ridx, row in enumerate(WORKFLOW_ROWS, start=1):
        for i, val in enumerate(row):
            c = tbl.rows[ridx].cells[i]
            c.width = Inches(widths_dxa[i] / 1440)
            bold = (i == 0) or (i == 1)
            set_cell(c, val, bold=bold, size=9.5)


def config_table(doc, config):
    """§5 per-team configuration — 4 rows only.

    Schema (from YAML):
      config.analysis_properties: str
      config.default_layout: str
      config.data_selector: str
      config.attribute_columns: list[str]
    """
    headers = ["Configuration item", "Value for this team"]
    widths_dxa = [3200, 7312]  # sum = 10512

    rows = [
        ("Analysis Properties", config["analysis_properties"], None),
        ("Default Layout",      config["default_layout"],      None),
        ("Data Selector",       config["data_selector"],       None),
        ("Key attribute columns", None, config["attribute_columns"]),
    ]

    tbl = doc.add_table(rows=len(rows) + 1, cols=2)
    tbl.autofit = False
    _set_table_width(tbl, CONTENT_WIDTH_DXA)

    # Header
    for i, h in enumerate(headers):
        c = tbl.rows[0].cells[i]
        c.width = Inches(widths_dxa[i] / 1440)
        shade(c, NAVY_HEX)
        set_cell(c, h, bold=True, size=9.5,
                 color=RGBColor(0xFF, 0xFF, 0xFF),
                 align=WD_ALIGN_PARAGRAPH.LEFT)

    # Body
    for ridx, (item, value, bullets) in enumerate(rows, start=1):
        c_item = tbl.rows[ridx].cells[0]
        c_item.width = Inches(widths_dxa[0] / 1440)
        set_cell(c_item, item, bold=True, size=9.5)

        c_val = tbl.rows[ridx].cells[1]
        c_val.width = Inches(widths_dxa[1] / 1440)
        c_val.text = ""
        cell_pad(c_val)

        if bullets is not None:
            # Bulleted list in the value cell
            for idx, b in enumerate(bullets):
                if idx == 0:
                    p = c_val.paragraphs[0]
                else:
                    p = c_val.add_paragraph()
                p.style = doc.styles["List Bullet"]
                p.paragraph_format.left_indent = Inches(0.2)
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                r = p.add_run(b)
                r.font.size = Pt(9.5)
                r.font.color.rgb = TEXT
        else:
            p = c_val.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(value)
            r.font.size = Pt(9.5)
            r.font.color.rgb = TEXT


# =========================================================================
# Main per-team build
# =========================================================================

def resolve_screenshot(screenshots_dir, filename):
    """Return absolute Path if file exists, else None."""
    if filename is None:
        return None
    p = Path(screenshots_dir) / filename
    return p if p.exists() else None


def build_cheat_sheet(team_yaml_path, output_dir, screenshots_dir):
    """Build one cheat sheet from a YAML config. Returns the output Path."""
    with open(team_yaml_path) as f:
        cfg = yaml.safe_load(f)

    team_key = cfg["team"]["key"]
    team_name = cfg["team"]["name"]
    config = cfg["config"]
    screenshots = cfg.get("screenshots", {})

    # Resolve screenshot paths (None if file missing — placeholder will render)
    ss_am = resolve_screenshot(screenshots_dir, screenshots.get("am_overview"))
    ss_ps = resolve_screenshot(screenshots_dir, screenshots.get("portfolio_sheet"))
    ss_cv = resolve_screenshot(screenshots_dir, screenshots.get("cash_viewer"))
    ss_cv_opts = resolve_screenshot(screenshots_dir, screenshots.get("cash_viewer_options"))

    doc = Document()
    setup_page(doc)

    # Title band
    title_band(doc, team_name)

    # §1 — Workflow
    section_heading(doc, "1 WORKFLOW (GENERIC ACROSS ALL PRIVATE TEAMS)")
    workflow_table(doc)

    # §2 — Analysis Properties Window
    section_heading(doc, "2 ANALYSIS PROPERTIES WINDOW")
    section_subhead(doc, "Analysis Properties (AM ribbon)")
    screenshot_image(doc, ss_am, CAPTION_AP)

    # §3 — Portfolio Sheet View
    section_heading(doc, "3 PORTFOLIO SHEET VIEW  (Labelled as Positions)")
    screenshot_image(doc, ss_ps, CAPTION_PORTFOLIO_SHEET)

    # §4 — Data Selector
    section_heading(doc, "4 DATA SELECTOR")
    section_subhead(doc, "Data Selector loaded with the team's book")
    screenshot_image(doc, ss_am, CAPTION_DATA_SELECTOR)

    # §5 — Per-Team Configuration
    section_heading(doc, "5 PER-TEAM CONFIGURATION")
    config_table(doc, config)

    # §6 — Cash Viewer
    section_heading(doc, "6 CASH VIEWER (WITH ACTUAL DATES)")
    section_subhead(doc, "Cash Viewer with the Details panel expanded")
    screenshot_image(doc, ss_cv, CAPTION_CASH_VIEWER)

    # §6 supplementary (only if file exists)
    if ss_cv_opts is not None:
        section_subhead(doc, "Options → Show Movement → Actual Dates / All toggle")
        screenshot_image(doc, ss_cv_opts, CAPTION_CASH_VIEWER_OPTIONS)

    # Save
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"NWM_AM_FO_CheatSheet_{team_key}.docx"
    doc.save(str(out_path))
    return out_path


# =========================================================================
# CLI
# =========================================================================

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--team", type=Path,
                   help="Path to a single team YAML (e.g. teams/private_debt.yaml)")
    g.add_argument("--all", action="store_true",
                   help="Build every team in teams/ directory")
    ap.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
                    help=f"Default: {DEFAULT_OUTPUT_DIR}")
    ap.add_argument("--screenshots-dir", type=Path, default=DEFAULT_SCREENSHOTS_DIR,
                    help=f"Default: {DEFAULT_SCREENSHOTS_DIR}")
    args = ap.parse_args()

    if args.all:
        yamls = sorted(TEAMS_DIR.glob("*.yaml"))
        if not yamls:
            sys.exit(f"No YAML files in {TEAMS_DIR}")
        targets = yamls
    else:
        if not args.team.exists():
            sys.exit(f"Team YAML not found: {args.team}")
        targets = [args.team]

    for yaml_path in targets:
        out_path = build_cheat_sheet(
            team_yaml_path=yaml_path,
            output_dir=args.output_dir,
            screenshots_dir=args.screenshots_dir,
        )
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
