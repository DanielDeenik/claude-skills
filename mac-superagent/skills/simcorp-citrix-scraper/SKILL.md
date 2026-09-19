---
name: simcorp-citrix-scraper
description: |
  PowerShell extractor for SimCorp Dimension help portal (help.simcorpcloud.com)
  run from a locked-down Citrix session. Produces a structured 23-column CSV
  matching CITRIX_RUNBOOK_full_corpus.md schema, ready for AKG / LightRAG
  ingestion. Validated against the live 2510 portal on 2026-05-15 (2,866 rows
  extracted across Tables + Forms namespaces; PoC + production scripts proven).

  Trigger on: "scrape SimCorp help", "extract help documentation", "citrix
  scraper", "SimCorp Cloud help portal", "MadCap Flare extraction", "SCDAT
  field dictionary", "TableFields parse", "EditorListProperties scrape",
  "Tier-1 / Tier-2 field docs", "structured CSV from help.simcorpcloud.com",
  "rebuild URL inventory", "AKG ingest from help portal", "help corpus".
type: extraction
version: 1.0.0
created: 2026-05-15
validated_on:
  portal: help.simcorpcloud.com/2510/en/
  poc_record: PoC_single_row.csv (EXCIK in SECURITIES, 13 fields populated)
  production_run: 2,866 rows (656 Tables + 2,210 Forms), 5,743 expected 404s
---

# SimCorp Help — Citrix PowerShell Scraper

## Why this skill exists

Extracting the SimCorp Dimension help portal into a structured corpus from a
Citrix session is HARDER than it looks. Across one engineering session we hit
every possible constraint and learned the working path. This skill encodes
that path so the next person doesn't relive the debug journey.

The output is a 23-column CSV that joins cleanly to `db2.sql` column comments
(49,198 rows in `SimCorp_DB_Field_Dictionary.csv`) on `(table, column)` —
yielding the full SCDAT data dictionary with business descriptions, FK paths,
and DWH view bindings for AKG / LightRAG retrieval.

## When to use this skill

Use this skill whenever the user wants to:

- Scrape SimCorp Dimension help from `help.simcorpcloud.com` in a Citrix session
- Rebuild the URL inventory (`_SimCorp_Help_Extraction/SimCorp_Help_URL_Inventory.csv` equivalent)
- Re-extract TableFields / EditorListProperties / Forms / Views / Formulas / Commands
- Merge help docs with `SimCorp_DB_Field_Dictionary.csv` for AKG ingestion
- Refresh the AKG `simcorp_help` corpus from a fresher portal version

## When NOT to use this skill

- For `docs.simcorpdimension.com` (Portal user manuals — DOCX/PDF) — different toolchain
- For F1 contextual help bundled with the desktop client install — different toolchain
- For NotebookLM / Wiki / Solution Architecture work — defer to `simcorp-super-agent`

## The 5 hard-won constraints (read before writing any code)

| # | Constraint | Implication |
|---|------------|-------------|
| 1 | **Citrix clipboard truncates pastes over ~8-12 KB silently** | Split any large script into multiple paste-blocks each &lt; 4 KB. Verify with `Get-Item ... \| Select Length` before F5. |
| 2 | **Notepad save creates 0-byte files when clipboard truncates** | Never use Notepad as the script-paste channel. Use **ISE Script Pane** instead — paste lands as one unit, F5 runs it. |
| 3 | **PowerShell `$var:` is parsed as a scoped variable** | Avoid `$name:` patterns in string interpolation. Use `-f` format strings: `("...{0}..." -f $var)`. |
| 4 | **`Invoke-WebRequest -UseDefaultCredentials` works for Tier-2 / Tables / Forms** | Server-rendered pages return full HTML to PS with Windows / Kerberos auth. No cookie capture needed for these. |
| 5 | **EditorListProperties (Tier-1) is JS-rendered — `Invoke-WebRequest` returns empty shell** | Defer Tier-1 to a later pass via IE COM or Edge "Save As". Don't block Tier-2 extraction on this. |

## The 4 wrong turns to skip

1. **Don't try to fetch MadCap chunk files** (`Data/SearchResources/Cloud/0_Cloud_Chunk*.js`)
   — the 2510 portal returns 404. Chunk paths vary by Flare version. **Use URL
   enumeration instead** (numeric IDs).

2. **Don't try to discover URLs via TOC** (`Data/Tocs/Default.xml` etc.)
   — returns no results on 2510. Use numeric enumeration.

3. **Don't paste 12 KB scripts into Notepad and "Save As"**
   — clipboard truncates, file saves 0 bytes, script never runs. Use ISE Script Pane.

4. **Don't waste cycles on full corpus runs until PoC validates parsers**
   — every regex change blocks a 60-90 min run. Always validate fetch + parse +
   CSV write on ONE page first.

## How to use this skill

### Step 1 — verify portal reachability (10 seconds)

Have the user run [scripts/00_preflight.ps1](scripts/00_preflight.ps1)
in their Citrix ISE console pane. Expects `200, ~140 KB` response. If
401/403 → cookie capture needed; if timeout → Citrix firewall (escalate to
NW IT).

### Step 2 — diagnostic page dump (30 seconds)

Have the user run [scripts/01_diagnostic_page_dump.ps1](scripts/01_diagnostic_page_dump.ps1)
in console. Returns the first 40 cleaned text lines of `Table-1.htm` so you can
verify the parser patterns in [references/parser_patterns.md](references/parser_patterns.md)
match the current portal version's H1 / section labels. If wording has
changed since 2510, patch parsers BEFORE running PoC.

### Step 3 — PoC validation (60 seconds)

[scripts/02_poc_single_page.ps1](scripts/02_poc_single_page.ps1) fetches a
known Tier-2 page (EXCIK in SECURITIES) and writes a single-row CSV.
Success = STEP 4 of the script's own output shows 13 populated fields
(see [references/poc_success_signature.md](references/poc_success_signature.md)).
Failure = parser regex needs adjustment per [references/parser_patterns.md](references/parser_patterns.md).

### Step 4 — paste production script in 3 blocks

Have the user **Ctrl+A → Delete** their Script Pane first, then paste:

- [scripts/03_block1_config_helpers.ps1](scripts/03_block1_config_helpers.ps1) (config + helpers, ~3 KB)
- [scripts/04_block2_parsers.ps1](scripts/04_block2_parsers.ps1) (all 3 parsers, ~4 KB)
- [scripts/05_block3_main.ps1](scripts/05_block3_main.ps1) (main loop, ~3 KB)

Each block fits well under Citrix clipboard limits.

### Step 5 — verify parse integrity, then F5

Before F5, run the parse-clean check from [scripts/06_verify_paste.ps1](scripts/06_verify_paste.ps1).
If `$errors` is empty → F5. If errors → patch line numbers reported.

### Step 6 — monitor live progress

While the production script runs (60-120 min), the user can monitor via
[scripts/07_monitor.ps1](scripts/07_monitor.ps1) in a second console pane.

### Step 7 — transfer back

When done, run [scripts/08_zip_and_transfer.ps1](scripts/08_zip_and_transfer.ps1)
to create the Downloads zip. User transfers to Mac via email / Citrix
Workspace file redirection / OneDrive.

### Step 8 — Mac-side merge into AKG

After zip arrives on Mac:
```bash
cd ~/Documents/GitHub/akg
unzip ~/Downloads/SimCorp_Help_Structured.zip -d data/lightrag-active/simcorp_help_2510/
source .venv/bin/activate
bin/akg ingest --source simcorp_help_2510
```

Or wait for the daily `akg-rag-daily-ingest` cron at 02:00.

## Output schema (23 columns)

See [references/csv_schema.md](references/csv_schema.md).

## Production-run benchmark (2026-05-15)

| Metric | Value |
|---|---|
| Rows extracted | 2,866 (Tables + Forms only — Phase 2 didn't complete) |
| Expected 404s logged | 5,743 (ID gaps) |
| With `table` populated | 656 (every Table_Summary row) |
| With `description` populated | 1,275 (45%) |
| Total runtime | ~60 min for Phase 1 |
| Per-page avg | ~250 ms (fetch + parse + write + delay) |

## Known follow-ups

- **Tier-1 EditorListProperties** — JS-rendered, needs IE COM render pass. Defer.
- **Phase 2 TableFields** — `Extract-FieldLinks` may not capture the 2510 portal's link format. To verify: dump one Table-1.htm raw, check link patterns, patch `Extract-FieldLinks` regex.
- **Views / Formulas / Commands** — Phase 1 didn't reach them in the validation run. Likely work as-is with the Generic parser.
- **Build date footer** — Some pages may put `Build:` line in a different location post-2510. The current parser handles either side of `Give feedback` cleanly.

## Cross-references

- [`simcorp-extraction`](../simcorp-extraction/SKILL.md) — sister skill for .dat / DEX / DFS design
- [`simcorp-super-agent`](../simcorp-super-agent/SKILL.md) — Q&A core that consumes the output corpus
- Mac-side artifacts:
  - `_pd_iter1/powershell/Get-SimCorpHelpFullCorpus.ps1` (original Markdown variant, 676 lines)
  - `_SimCorp_Help_Extraction/SimCorp_DB_Field_Dictionary.csv` (49,198 db2.sql columns for merge)
  - `_SimCorp_Help_Extraction/CITRIX_RUNBOOK_full_corpus.md` (older runbook — schema definition still authoritative)

## Provenance

Validated against `help.simcorpcloud.com/2510/en/` on 2026-05-15 with Dan in
his NW Citrix session. PoC produced fully-populated 13-field row for
EXCIK in SECURITIES. Production run produced 2,866 rows before being stopped
to debug the TableFields link-extraction issue. Every regex pattern traced
back to verbatim page content from the live portal.
