# Parser Regex Patterns — Validated Against 2510 Portal

Every regex below was traced through actual page content from
`help.simcorpcloud.com/2510/en/` on 2026-05-15 and confirmed working in the
PoC (EXCIK in SECURITIES) and production run (656 Tables + 2,210 Forms).

If the user reports parser misses on a future portal version, **first run
`01_diagnostic_page_dump.ps1`** to inspect the new line content, then patch
the relevant regex below.

## Tier-2 TableField parser (`Parse-Tier2`)

Sample page: `Content/TableFields/Table-1 Field-190.htm` (EXCIK in SECURITIES)

Page structure on 2510:
```
[nav chrome — skip]
Database field EXCIK in table SECURITIES
Technical Information
The field is partly mandatory (NOT NULL) with zero for values not specified.
Database type: NUMBER(5) Internal max. width in SimCorp Dimension: 5
The field is internally an internal key reference to EXCHANGES
Found in view(s):
A_EQUITIES.EXCHANGE
A_SECS.EXCHANGE
A_SECS.EXCHANGE_REF
DR_SD_SECURITIES.EXCHANGE_ID
See also
General help for the Table SECURITIES
Help for the referenced field EXCHANGES.EXCIK
Description
This field contains a reference to an exchange.
Some securities can be quoted on several exchanges, ...
Give feedback
Build: 01/05/2026 at 11:59
```

| Field | Regex | Notes |
|-------|-------|-------|
| `column`, `table` | `(?i)Database field\s+([A-Z0-9_]+)\s+in\s+table\s+([A-Z0-9_]+)` | H1 capture; both in one match |
| Section: tech | `-like 'Technical Information*'` | Wildcard tolerates `(Reference)` etc. |
| Section: views | `-like 'Found in view*'` | Tolerates `Found in view(s):` |
| Section: desc | `-eq 'Description'` | Exact match |
| Section: see_also | `-like 'See also*'` | |
| Terminator | `-like 'Give feedback*'` | Stops body accumulation |
| Build date | `Build:\s*(.+?)\s+at\s+(.+)` | Captures date + time separately, then concatenated |
| `nullable` (always) | `(?i)always mandatory` | |
| `nullable` (partly) | `(?i)partly mandatory` | |
| `dbtype` | `Database type:\s*([A-Z0-9(),\s]+?)(?:\t\|Internal max\|$)` | Non-greedy; lookahead stops before "Internal max" |
| `internal_width` | `Internal max\.?\s*width.*?:\s*(\d+)` | Tolerates period after "max" |
| `fk_to`, `is_key` | `internal key reference to\s+([A-Z0-9_]+)` | Sets both fields |
| `domain` | `of domain\s+([A-Za-z0-9_]+)` | Mixed-case domain names allowed |
| DWH view line | `^[A-Z0-9_]+(\.[A-Z0-9_]+)+$` | Dotted-uppercase shape |
| `help_topic_raw` (see_also) | `General help for the Table\s+([A-Z0-9_]+)` | |

## Table_Summary parser (`Parse-TableSummary`)

Sample page: `Content/Tables/Table-1.htm` (SECURITIES)

Page structure on 2510:
```
[nav chrome]
You are here:
Database table SECURITIES
Securities
Table Group: Securities
Sub-Table Group: Static data and configuration
Main table for securities.
Fields on SECURITIES
ASSLIATYPE
Asset/ Liability
BLKDATE
...
[Build: ...]
```

Key difference from 2019 samples: new metadata fields (`Table Group:`,
`Sub-Table Group:`) replace the old `Technical Information` block.

| Field | Regex | Notes |
|-------|-------|-------|
| Skip nav chrome | `-like 'You are here*'` | Anchor; ignore lines before this |
| `table` | `(?i)Database table\s+([A-Z0-9_]+)` | H1 capture |
| `domain` | `(?i)^Table Group:\s*(.+)$` | Trimmed |
| `category` | `(?i)^Sub-Table Group:\s*(.+)$` | Trimmed |
| Fields-list start | `-like 'Fields on*'` OR `-like 'List of fields*'` | Stops description accumulation |
| Body filter | `-notmatch '^[A-Z0-9_]{3,}$'` | Excludes bare column-name lines from description |

## Generic parser (`Parse-Generic`) — Forms, Views, Formulas, Commands, ReleaseNotes, Main

| Field | Regex | Notes |
|-------|-------|-------|
| Skip nav chrome | `-like 'You are here*'` | |
| Text start | `-match '^\w'` AND `.Length -gt 10` | First substantive prose line |
| Body line filter | `.Length -gt 20` | Excludes short menu-link text |
| Max lines | `$d.Count -ge 10` | Caps description at 10 lines |
| Terminator | `-like 'Give feedback*'` OR `-like 'See also*'` | |

## When patterns break

If a regex fails on a future portal version:

1. Run `scripts/01_diagnostic_page_dump.ps1` against a representative URL of
   the kind that's failing
2. Compare the first 40 cleaned lines to the "Page structure" block above
3. Identify the diverging element (H1 wording, section label, terminator)
4. Patch the corresponding regex above + the parser function
5. Re-run `02_poc_single_page.ps1` to validate before re-running full corpus

Common failure modes:

| Symptom | Cause | Fix |
|---------|-------|-----|
| `table` empty for Table_Summary | H1 wording changed | Update `Database table` regex |
| `dbtype` empty for Tier-2 | Layout collapsed | Adjust `Database type:` lookahead alternation |
| `description` polluted with `Give feedback` text | Terminator missing | Ensure `Give feedback` break is BEFORE description switch |
| `build_date` empty | Build line moved or removed | Run diagnostic, check footer area |
