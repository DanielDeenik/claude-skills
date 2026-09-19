# NWM AM Front-Office Cheat Sheet — Format Spec

**Approved by Dan: 2026-05-26**
**Reference doc:** Dan's edited `NWM_AM_FO_TearSheet_Mortgages.docx` (uploaded
2026-05-26 14:54 PT).

This file is the **single source of truth** for the cheat-sheet layout. The
builder script (`scripts/build_cheat_sheet.py`) implements exactly this spec.
Do not change the builder behaviour without updating this doc first, and
without Dan's explicit sign-off.

---

## Page setup

| Property | Value |
|---|---|
| Paper | US Letter (8.5" × 11") |
| Margins | 0.6" left/right, 0.5" top/bottom |
| Default font | Calibri |
| Default size | 10pt body, 9.5pt table cells |

---

## Title band (top of page)

```
ASSET MANAGER — FRONT OFFICE CHEAT SHEET           ← 11pt, muted gray, bold
<Team Name>                                         ← 20pt, navy, bold
                                                    ← blank line (8pt)
```

**Team name** = `team.name` from YAML (e.g. `Mortgages`, `Private Debt`,
`Private Equity`). Plain, no parenthetical (Mortgages doc reads "Mortgages",
NOT "Mortgages (CA + US)").

**No audience line. No subtitle. No KPIs band.**

---

## Section 1 — Workflow (constant)

Heading: `1 WORKFLOW (GENERIC ACROSS ALL PRIVATE TEAMS)`

- 10pt navy bold
- Gold underline (1px, color `C9A961`)
- Plain number `1`, single space, then label. **No `§` symbol, no em-dash.**

Table (full content width, 6 data rows + header):

| # | Step | Component | What it does |
|---|---|---|---|
| 1 | Login | Asset Manager | Opens user session. |
| 2 | Select Analysis Properties | Analysis Properties | Defines analytics scope, incl. term structure consumed by Cash Viewer. |
| 3 | Apply Layout | Layout (team-shared default; user can save own) | Sheet configuration: columns, charts, filters, and panel arrangement. |
| 4 | Load data | Data Selector | Pulls portfolios + positions into the session. Three modes: Selection Editor, My Portfolios, Quick Selection. |
| 5 | Slice + visualise | Portfolio Sheet | Filter, dependency cascades to charts; add attribute columns (security data, analytics, accounting data). |
| 6 | Manage cash | Cash Viewer | Term structure from Analysis Properties; Options → Actual Dates surfaces forecast + actuals (ALMs, interest, dividends, coupons). |

Row styling:
- Header row: navy fill, white text, bold, 9.5pt
- Body rows: tight padding (60dxa top/bottom, 120dxa left/right)
- No alternating shading — rows are uniformly white
- Column widths (DXA, sum = 10512 = 7.3"): 480 / 1800 / 2900 / 5332

---

## Section 2 — Analysis Properties Window

Heading: `2 ANALYSIS PROPERTIES WINDOW`

Sub-heading (under the rule, before the image): `Analysis Properties (AM ribbon)`

- 10pt navy bold, no indent
- Single blank line above and below

Image: `screenshots.am_overview` from YAML. Width = 7.0". Centered. If file
missing, render `[ paste screenshot here ]` placeholder box (no blue label band).

Caption (italic, 8.5pt, muted, centered):

> Analysis Properties lives in the AM ribbon → ANALYSIS group. Open the
> picker to confirm the team-linked profile is selected before loading data.

---

## Section 3 — Portfolio Sheet View

Heading: `3 PORTFOLIO SHEET VIEW  (Labelled as Positions)`

**Note: TWO spaces before `(Labelled as Positions)` — this is Dan's spacing
convention, kept as-is.**

Sub-heading: (none — image goes directly under the section rule)

Image: `screenshots.portfolio_sheet` from YAML. Width = 7.0".

Caption:

> Portfolio Sheet (Labelled as Positions) visible attribute columns,
> groupings, filter row, and the chart panel underneath. Right-click any
> field → Select Fields to surface column choices.

---

## Section 4 — Data Selector

Heading: `4 DATA SELECTOR`

Sub-heading: `Data Selector loaded with the team's book`

Image: `screenshots.am_overview` from YAML (intentionally same file as §2 —
the AM overview screenshot shows both the Analysis Properties ribbon AND the
Data Selector panel, so it's reused).

Caption:

> Data Selector panel (left side of the AM workspace). Selection Editor with
> the team's portfolios selected, or load a saved selection. F5 lists all
> saved setups; the Layout indicator at the bottom right confirms which
> Layout is currently applied.

---

## Section 5 — Per-Team Configuration

Heading: `5 PER-TEAM CONFIGURATION`

Table (2 columns, 4 data rows + header):

| Configuration item | Value for this team |
|---|---|
| Analysis Properties | `config.analysis_properties` (plain text) |
| Default Layout | `config.default_layout` (plain text — fixed-width font for layout names with hyphens / dashes) |
| Data Selector | `config.data_selector` (plain text) |
| Key attribute columns | bulleted list of `config.attribute_columns` |

Row styling:
- Header row: navy fill, white text, bold, 9.5pt
- Body rows: white fill, 9.5pt body
- Column widths (DXA, sum = 10512): 3200 (item) / 7312 (value)
- Bulleted list in last row uses Word `List Bullet` style with 0.2" left indent

**CRITICAL — what is NOT in this table:**

- No `[Unverified]` / `[Recommended]` amber-italic tags
- No `Free-code columns` row
- No `Cash Viewer term structure` row
- No `Pricing pipeline` row
- No `Call Money` / `Wells Fargo PDDL` row
- No `Open Transaction Window menu` row
- No `FX method` row

The detailed config rows from the legacy tear-sheet format are intentionally
dropped — the cheat sheet is a 2-3 page quick reference, not a deep config
spec.

---

## Section 6 — Cash Viewer (with Actual Dates)

Heading: `6 CASH VIEWER (WITH ACTUAL DATES)`

Sub-heading: `Cash Viewer with the Details panel expanded`

Image: `screenshots.cash_viewer` from YAML. Width = 7.0".

Caption:

> Present + future cash by portfolio with the Details panel expanded.
> Forecast and actuals visible (ALMs, interest, dividends, coupons).
> Historical Mode can look back up to 10 business days; configure default
> in Settings Template → Cash Viewer tab.

### §6 supplementary (optional — only if `screenshots.cash_viewer_options` is set)

Sub-heading: `Options → Show Movement → Actual Dates / All toggle`

Image: `screenshots.cash_viewer_options` from YAML. Width = 7.0".

Caption:

> Toggle between Actual Dates and the defined Term Structure (e.g. Daily
> for 2 Weeks).

---

## What the cheat sheet does NOT have

These were in the original tear-sheet format and are explicitly REMOVED:

- §7 "Notes for this team" bullet list (OID treatment, Reference rate
  fixings, Two-layer structure, daily LF_* batches, etc.)
- SOURCES footer (AM Design Reference, AMGSG §1..§8, etc.)
- KPIs band (Windows to learn, AM concepts, Transaction types, Parallel
  Days)
- Audience subtitle line
- Cross-team callouts ("Sister decks: G1 PE...")
- Lifecycle event table
- NW anchor holdings table
- Parallel Day 1/2/3 readiness blocks
- Escalation map

If Dan wants any of these back, he creates a new format (e.g. "training tear
sheet" vs "cheat sheet") with its own builder — don't graft them onto this
one.

---

## Diff vs legacy tear-sheet format

| Element | Legacy tear sheet | New cheat sheet |
|---|---|---|
| Title | "TEAR SHEET" | "CHEAT SHEET" |
| Audience line | yes | no |
| Section headings | `§1 — WORKFLOW (...)` | `1 WORKFLOW (...)` |
| Screenshot label box | `[ Screenshot ] Screenshot N — <label>` blue band | bold subhead only, no band |
| §5 rows | 7-9 detailed rows with amber `[Unverified]` tags | 4 short rows, no tags |
| §5 columns row | dot-separated prose | bulleted list |
| §7 Notes | 3-4 bullets | removed |
| Sources footer | yes | removed |
| File suffix | `_TearSheet_<Team>.docx` | `_CheatSheet_<Team>.docx` |

---

## Change log

- **2026-05-26** — Initial spec, approved by Dan based on his edit of
  `NWM_AM_FO_TearSheet_Mortgages.docx`.
