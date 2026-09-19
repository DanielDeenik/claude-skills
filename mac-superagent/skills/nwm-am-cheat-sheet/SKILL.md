---
name: nwm-am-cheat-sheet
description: >
  Build NWM Asset Manager Front-Office cheat sheets (one DOCX per private team:
  Private Equity, Private Debt, Venture Capital, Infrastructure, Mortgages).
  Reads per-team YAML config from teams/<team>.yaml, embeds screenshots from a
  workspace `_screenshots/` folder, and renders a 2-3 page DOCX cheat sheet
  matching Dan's approved format (CHEAT SHEET title, plain-numbered sections
  1-6, no [Screenshot] label boxes, 4-row §5 config table with bulleted
  attribute columns, no notes/sources footer). Trigger on: NWM cheat sheet,
  AM cheat sheet, Asset Manager cheat sheet, front office cheat sheet,
  rebuild cheat sheet, generate cheat sheet for <team>, update <team> cheat
  sheet, NWM AM tear sheet (legacy term), private team cheat sheet.
  Pairs with: simcorp-super-agent (Q&A), simcorp-extraction (.dat / DEX work).
---

# NWM AM Front-Office Cheat Sheet Builder

Produces a single-team DOCX cheat sheet for the Asset Manager front-office
workflow. One file per team. The format is fixed (Dan's approval 2026-05-26);
only the per-team CONFIG VALUES and screenshots change.

---

## When to use

- Dan asks for a cheat sheet for one of the 5 private teams (PE / PD / VC /
  Infra / MTG).
- Dan updates a team's config values (Analysis Properties name, Layout name,
  Data Selector, attribute columns) and wants the doc re-rendered.
- Dan adds or replaces screenshots in `_screenshots/` and wants the doc rebuilt.

Do NOT use for: cheat sheets for other domains (not AM), or for the older
"tear sheet" format (the longer §5 with [Unverified] tags, §7 notes, sources
footer). That format is deprecated — every regeneration produces the new
cheat-sheet format.

---

## Inputs

1. **Per-team YAML** in `teams/<team_key>.yaml` — required. Schema below.
2. **Screenshots** in `<workspace>/_AM_FO_TearSheets_2026_05_26/_screenshots/`
   — referenced by filename in the YAML. Supported extensions: `.png`, `.jpg`,
   `.jpeg`. Optional: any screenshot missing from disk renders as a placeholder
   box; the doc still builds.

### YAML schema

```yaml
team:
  key: PrivateDebt          # used in output filename + as fallback prefix
  name: Private Debt        # what appears in the big title

config:
  analysis_properties: Private Debt                     # short value for §5
  default_layout: NWM Private Debt – Portfolio Mgt. 1   # short value for §5
  data_selector: Private Debt All                       # short value for §5
  attribute_columns:                                    # bulleted in §5
    - Investment link
    - Borrower
    - Spread
    # ... etc

screenshots:
  am_overview: privatedebt_am_overview.jpg          # §2 + §4 (same image both)
  portfolio_sheet: privatedebt_layout.jpg           # §3
  cash_viewer: privatedebt_cash_viewer.jpg          # §6
  cash_viewer_options: null                         # §6 supplementary; null to skip
```

---

## Output

`<workspace>/_AM_FO_TearSheets_2026_05_26/NWM_AM_FO_CheatSheet_<team_key>.docx`

Filename uses `CheatSheet` (not `TearSheet`) to disambiguate from the legacy
format. The older `NWM_AM_FO_TearSheet_*.docx` files are NOT touched by this
skill — Dan should archive them manually once the new files are accepted.

---

## How to run

```bash
cd "<workspace>/ix. SimCorp SuperAgent/skills/nwm-am-cheat-sheet"

# Build one team
python3 scripts/build_cheat_sheet.py --team teams/private_debt.yaml

# Build all teams that have a YAML
python3 scripts/build_cheat_sheet.py --all
```

Defaults:
- Output dir: `<workspace>/_AM_FO_TearSheets_2026_05_26/`
- Screenshots dir: `<workspace>/_AM_FO_TearSheets_2026_05_26/_screenshots/`

Override with `--output-dir` and `--screenshots-dir`.

---

## Format spec (fixed — do not modify without Dan's approval)

See `references/format_spec.md` for the exact rules. Summary:

1. Title band: `ASSET MANAGER — FRONT OFFICE CHEAT SHEET` (10pt muted bold),
   then team name (20pt navy bold). **No audience line, no subtitle.**
2. Section headings: plain numbers, e.g. `1 WORKFLOW (GENERIC ACROSS ALL
   PRIVATE TEAMS)`, `2 ANALYSIS PROPERTIES WINDOW`, `3 PORTFOLIO SHEET VIEW
   (Labelled as Positions)`. **No § symbol, no em-dash.**
3. Each screenshot section: bold subhead → image → italic caption.
   **No light-blue `[Screenshot]` label band.**
4. §5 config table: exactly 4 rows — `Analysis Properties`, `Default Layout`,
   `Data Selector`, `Key attribute columns` (bulleted list in the value cell).
   **No `[Unverified]` amber tags, no Free Codes / Pricing / Call Money rows.**
5. **No §7 Notes for this team. No Sources footer.**

---

## Sister skills

- `simcorp-super-agent` — for Q&A about SimCorp config (NAV, lookthrough, etc.)
- `simcorp-extraction` — for designing .dat / DEX / DFS extracts
- `simcorp-notebooklm-bridge` — for NotebookLM ↔ Claude hand-off via Notion

---

## Approval history

- **2026-05-26** — format approved by Dan after editing
  `NWM_AM_FO_TearSheet_Mortgages.docx` down from the original tear-sheet format.
  See `references/format_spec.md` for the diff.
