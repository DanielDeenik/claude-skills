# SimCorp Citrix Scraper — Full Runbook

Top-to-bottom workflow for extracting `help.simcorpcloud.com` from a Citrix
PowerShell session into a structured CSV ready for AKG/LightRAG ingestion.

## Step 0 — Open PowerShell ISE in Citrix

1. Start menu → type **"ISE"** → open **Windows PowerShell ISE**.
2. View menu → tick **"Show Script Pane Top"** (or Ctrl+R) if the top white area is missing.
3. You'll work in two panes: **Script Pane** (top, where scripts get pasted) and **Console Pane** (bottom, where output appears).

**Never use Notepad** — Citrix's clipboard truncates large pastes silently, saves 0-byte files.

## Step 1 — Preflight: confirm portal is reachable

Paste into the **Console Pane** and Enter:

```powershell
try {
    $r = Invoke-WebRequest -Uri 'https://help.simcorpcloud.com/2510/en/Content/Tables/Table-1.htm' `
        -UseBasicParsing -UseDefaultCredentials -TimeoutSec 30
    [pscustomobject]@{ Status=$r.StatusCode; Length=$r.Content.Length; HasContent=($r.Content -match 'Database table') }
} catch { Write-Host "FAIL: $($_.Exception.Message)" -ForegroundColor Red }
```

**Expected:** `Status: 200`, `Length: ~140000`, `HasContent: True`.

If you get 401/403 → cookie capture needed (see `references/cookie_capture.md` in the skill folder).
If you get timeout → Citrix firewall blocks the host; escalate to NW IT.

## Step 2 — Diagnostic: dump 40 lines of a known page

Confirms parser regex still matches the live portal version. Paste in Console:

```powershell
$r = Invoke-WebRequest -Uri 'https://help.simcorpcloud.com/2510/en/Content/TableFields/Table-1%20Field-190.htm' -UseBasicParsing -UseDefaultCredentials -TimeoutSec 30
Add-Type -AssemblyName System.Web
$h = $r.Content
$h = $h -replace '(?is)<(script|style)[^>]*>.*?</\1>',''
$h = $h -replace '(?i)</(p|div|h[1-6]|tr|td|th|li|table)>',"`n"
$h = $h -replace '<[^>]+>',"`t"
$h = [System.Web.HttpUtility]::HtmlDecode($h)
$lines = @($h -split "`n" | ForEach-Object { ($_ -replace '\s+',' ').Trim() } | Where-Object { $_ })
$lines | Select-Object -First 40
```

**Expected content includes:**
- `Database field EXCIK in table SECURITIES`
- `Technical Information`
- `Database type: NUMBER(5) Internal max. width...`
- `Found in view(s):`
- `Description`
- `Build: ... at ...`

If wording has drifted, patch parser regexes per `references/parser_patterns.md` BEFORE the next step.

## Step 3 — PoC: validate one page end-to-end

Clear Script Pane (**Ctrl+A → Delete**) and paste the contents of `scripts/02_poc_single_page.ps1` (~90 lines, ~3 KB). Press **F5**.

**Success criterion:** STEP 4 of the output shows ~13 populated fields:
- `column = EXCIK`, `table = SECURITIES`, `dbtype = NUMBER(5)`, `internal_width = 5`
- `nullable = NOT NULL (partly)`, `fk_to = EXCHANGES`, `is_key = YES`
- `dwh_views` with 4 views joined by `; `
- `description` with the field's prose
- `build_date = 01/05/2026 11:59`

If any of those are empty → parser broken; do NOT proceed. Fix per `references/parser_patterns.md`.

## Step 4 — Pick your extraction strategy

| Strategy | When to use | Pros | Cons |
|----------|-------------|------|------|
| **A. All-at-once** | Stable Citrix session, can leave running 1-2 hrs | Single run, simple | If Citrix disconnects you lose progress (recoverable via `-Resume` logic in checkpoint) |
| **B. Batched** (Recommended) | Long-running, hit-and-run Citrix usage | Run any time, pick up where left off, predictable batches | Need to F5 multiple times |

Strategy B is safer for Citrix and matches your actual workflow.

## Step 5A — All-at-once production (if you chose A)

Clear Script Pane, then paste three blocks **without F5 between them**:

1. `scripts/03_block1_config_helpers.ps1` (~3 KB)
2. `scripts/04_block2_parsers.ps1` (~4 KB)
3. `scripts/05_block3_main.ps1` (~3 KB)

Then verify parse-clean (Step 6) and F5.

## Step 5B — Batched production (recommended)

Clear Script Pane, paste `scripts/09_batch_scraper.ps1` (~5 KB, self-contained), F5.

**Tune at the top of the script:**

```powershell
$Mode              = 'TableFields'   # focuses on Phase 2 (missing from previous runs)
$BatchSize         = 500              # URLs per F5 — adjust to fit your session length
$StartTableId      = 1                # first Table-N to enumerate from
$EndTableId        = 8000             # stop at this Table-N
$MaxFieldsPerTable = 1500             # cap Field-F per table
$MissesToSkipTable = 75               # consecutive 404s → next table
```

Each F5 processes 500 URLs (~2-5 min depending on hit rate), saves state to `_batch_state.txt`, then exits. **Re-F5 to continue from where it left off.**

Run 50-100 batches across multiple Citrix sessions to complete the TableFields corpus.

## Step 6 — Verify parse-clean before every F5

Always run this in the Console Pane BEFORE F5:

```powershell
$tokens = $errors = $null
[System.Management.Automation.Language.Parser]::ParseInput($psISE.CurrentFile.Editor.Text, [ref]$tokens, [ref]$errors) | Out-Null
if ($errors) {
    $errors | ForEach-Object { Write-Host ("ERROR line {0}: {1}" -f $_.Extent.StartLineNumber, $_.Message) -ForegroundColor Red }
} else {
    Write-Host "Script parses clean. Ready to F5." -ForegroundColor Green
}
```

Catches Citrix clipboard truncation + `$var:` syntax traps before you waste time on a failed run.

## Step 7 — Monitor live progress

In a second console tab (PowerShell 2 or 3 within ISE) — doesn't interfere with the running script:

```powershell
$dir = "$env:USERPROFILE\Documents\SimCorp_Help_Structured"
@{
    Rows      = (Get-Content "$dir\SimCorp_Help_Structured.csv").Count - 1
    RawCount  = (Get-ChildItem "$dir\raw" -Filter *.htm -ErrorAction SilentlyContinue).Count
    Checkpoint = (Get-Content "$dir\_checkpoint.txt" -ErrorAction SilentlyContinue).Count
    Errors    = (Get-Content "$dir\_errors.log" -ErrorAction SilentlyContinue).Count
    State     = Get-Content "$dir\_batch_state.txt" -ErrorAction SilentlyContinue
}
```

Run every 10-15 min. `Rows` should climb between batches.

## Step 8 — Zip and transfer

When you've extracted as much as you need (or finished Phase 2), package for transfer back to Mac:

```powershell
$dir = "$env:USERPROFILE\Documents\SimCorp_Help_Structured"
$zip = "$env:USERPROFILE\Downloads\SimCorp_Help_Structured_{0}.zip" -f (Get-Date -Format 'yyyyMMdd_HHmm')
Compress-Archive -Path "$dir\*" -DestinationPath $zip -Force
Get-Item $zip | Select Name, @{N='SizeMB';E={[math]::Round($_.Length/1MB,1)}}, LastWriteTime
```

Transfer options:
- Citrix Workspace → Devices panel → File Transfer (drag-drop)
- Outlook email-to-self with attachment (<25 MB)
- Corporate OneDrive / SharePoint upload

## Step 9 — Mac-side AKG ingest (final step)

On your Mac, after zip arrives:

```bash
cd ~/Documents/GitHub/akg
RUN_TAG="simcorp_help_2510_$(date +%Y%m%d)"
mkdir -p data/lightrag-active/$RUN_TAG
unzip ~/Downloads/SimCorp_Help_Structured_*.zip -d data/lightrag-active/$RUN_TAG/
source .venv/bin/activate
bin/akg ingest --source $RUN_TAG --workspace simcorp_help
```

Or wait for the daily 02:00 `akg-rag-daily-ingest` cron (per memory `feedback_reuse_existing_tasks` — that slot already runs).

## Troubleshooting flow chart

```
Did Step 1 preflight return 200?
├── No → cookie capture (references/cookie_capture.md)
└── Yes ↓

Did Step 2 diagnostic show expected page structure?
├── No → patch parser regexes (references/parser_patterns.md)
└── Yes ↓

Did Step 3 PoC populate 13 fields?
├── No → parser still broken; do not proceed
└── Yes ↓

Did Step 6 parse-clean return green?
├── No → paste truncated; re-paste or fix line per error
└── Yes ↓

F5 → success → Step 7 monitor → Step 8 transfer → Step 9 ingest
```

## Files in this skill folder

| Path | Purpose |
|------|---------|
| `SKILL.md` | Skill metadata + trigger keywords + summary |
| `RUNBOOK.md` | This file — top-to-bottom workflow |
| `scripts/00_preflight.ps1` | Step 1 |
| `scripts/01_diagnostic_page_dump.ps1` | Step 2 |
| `scripts/02_poc_single_page.ps1` | Step 3 (single-page PoC) |
| `scripts/03_block1_config_helpers.ps1` | Step 5A part 1 |
| `scripts/04_block2_parsers.ps1` | Step 5A part 2 |
| `scripts/05_block3_main.ps1` | Step 5A part 3 |
| `scripts/06_verify_paste.ps1` | Step 6 |
| `scripts/07_monitor.ps1` | Step 7 |
| `scripts/08_zip_and_transfer.ps1` | Step 8 |
| `scripts/09_batch_scraper.ps1` | Step 5B (recommended) |
| `references/citrix_constraints.md` | 10 hard-won lessons |
| `references/csv_schema.md` | 23-column output schema |
| `references/parser_patterns.md` | Regex catalog + diagnosis |
| `references/poc_success_signature.md` | Expected PoC output |
| `references/cookie_capture.md` | SSO cookie workflow |
| `references/akg_ingest_handoff.md` | Mac-side ingest |
