# 09_batch_scraper.ps1 — batched extractor with state-file resume.
# Processes $BatchSize URLs per run; re-run to continue.
# Self-contained. Reuses _checkpoint.txt + _errors.log to skip.
# Paste into ISE Script Pane → F5. Lines kept short to dodge Citrix clipboard truncation.

# --- Tune these ---
$Mode              = 'TableFields'   # TableFields | (extend later for other shapes)
$BatchSize         = 60000            # single unattended run (was 500)
$StartTableId      = 1                # first Table-N to enumerate
$EndTableId        = 8000             # stop after this Table-N
$MaxFieldsPerTable = 1500             # cap Field-F per table
$MissesToSkipTable = 75               # consecutive 404s before moving on
$DelayMs           = 60
$TimeoutSec        = 30

$Version    = '2604'   # 26.04 release. If first fetches return 0, change to '2510' (known-good) — one number.
$BaseUrl    = "https://help.simcorpcloud.com/$Version/en/"
$OutDir     = "$env:USERPROFILE\Documents\SimCorp_Help_Structured"
$OutCsv     = Join-Path $OutDir 'SimCorp_Help_Structured.csv'
$RawDir     = Join-Path $OutDir 'raw'
$Checkpoint = Join-Path $OutDir '_checkpoint.txt'
$ErrorsLog  = Join-Path $OutDir '_errors.log'
$BatchState = Join-Path $OutDir '_batch_state.txt'

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Web
New-Item -ItemType Directory -Force -Path $OutDir,$RawDir | Out-Null

$cols = @('namespace','url_path','title','kind','table','column','dbtype','internal_width',
          'nullable','fk_to','domain','dwh_views','editor_list_identifier','editor_list_name',
          'am_field_tooltip','category','is_key','access','formatter','help_topic_raw',
          'description','build_date','source_file')
if (-not (Test-Path $OutCsv)) { ($cols -join ',') | Set-Content $OutCsv -Encoding UTF8 }

$done = @{}
if (Test-Path $Checkpoint) {
    Get-Content $Checkpoint | ForEach-Object { if ($_) { $done[$_] = $true } }
}
$bad = @{}
if (Test-Path $ErrorsLog) {
    Get-Content $ErrorsLog | ForEach-Object {
        if ($_ -match '(https?://[^\s:]+\.htm)') { $bad[$matches[1]] = $true }
    }
}
$state = @{ t = $StartTableId; f = 1 }
if (Test-Path $BatchState) {
    Get-Content $BatchState | ForEach-Object {
        if ($_ -match '^(t|f)=(\d+)$') { $state[$matches[1]] = [int]$matches[2] }
    }
}

Write-Host ("Mode={0} BatchSize={1} Resume T={2} F={3}" -f $Mode,$BatchSize,$state.t,$state.f) -ForegroundColor Cyan
Write-Host ("Already done: {0}  Known 404s: {1}" -f $done.Count,$bad.Count) -ForegroundColor DarkGray

function Esc ([string]$v) {
    if ($null -eq $v) { return '' }
    if ($v -match '[",\r\n]') { return '"'+($v -replace '"','""')+'"' }
    return $v
}
function Get-BuildDate ($c) {
    if ($c -like 'Build:*' -and $c -match 'Build:\s*(.+?)\s+at\s+(.+)') {
        $d1 = $matches[1].Trim()
        $d2 = $matches[2].Trim()
        return "$d1 $d2"
    }
    return $null
}
function H2Lines ($html) {
    $h = $html
    $h = $h -replace '(?is)<(script|style)[^>]*>.*?</\1>',''
    $h = $h -replace '(?i)<(br|hr)\b[^>]*/?>',"`n"
    $h = $h -replace '(?i)</(p|div|h[1-6]|tr|td|th|li|table)>',"`n"
    $h = $h -replace '<[^>]+>',"`t"
    $h = [System.Web.HttpUtility]::HtmlDecode($h)
    @($h -split "`n" | ForEach-Object { ($_ -replace '\s+',' ').Trim() } | Where-Object { $_ })
}
function Parse-Tier2 ($lines, $r) {
    $sec = $null; $d = @(); $v = @()
    foreach ($c in $lines) {
        if (-not $r['column'] -and $c -match '(?i)Database field\s+([A-Z0-9_]+)\s+in\s+table\s+([A-Z0-9_]+)') {
            $r['column'] = $matches[1]
            $r['table']  = $matches[2]
            continue
        }
        if ($c -like 'Technical Information*') { $sec = 'tech'; continue }
        if ($c -like 'Found in view*')         { $sec = 'views'; continue }
        if ($c -eq  'Description')             { $sec = 'desc'; continue }
        if ($c -like 'See also*')              { $sec = 'see_also'; continue }
        if ($c -like 'Give feedback*')         { $sec = $null; continue }
        $bd = Get-BuildDate $c
        if ($bd) { $r['build_date'] = $bd; break }
        if ($sec -eq 'tech') {
            if ($c -match '(?i)always mandatory')     { $r['nullable'] = 'NOT NULL (always)' }
            elseif ($c -match '(?i)partly mandatory') { $r['nullable'] = 'NOT NULL (partly)' }
            if ($c -match 'Database type:\s*([A-Z0-9(),\s]+?)(?:\t|Internal max|$)') {
                $r['dbtype'] = $matches[1].Trim()
            }
            if ($c -match 'Internal max\.?\s*width.*?:\s*(\d+)') {
                $r['internal_width'] = $matches[1]
            }
            if ($c -match 'internal key reference to\s+([A-Z0-9_]+)') {
                $r['fk_to'] = $matches[1]
                $r['is_key'] = 'YES'
            }
            if ($c -match 'of domain\s+([A-Za-z0-9_]+)') {
                $r['domain'] = $matches[1]
            }
        }
        elseif ($sec -eq 'views' -and $c -match '^[A-Z0-9_]+(\.[A-Z0-9_]+)+$') { $v += $c }
        elseif ($sec -eq 'desc' -and $c) { $d += $c }
    }
    if ($d) { $r['description'] = ($d -join ' ') }
    if ($v) { $r['dwh_views']   = ($v -join '; ') }
}

$processed = 0; $ok = 0; $skipped = 0; $startTime = Get-Date

:outer for ($t = [int]$state.t; $t -le $EndTableId; $t++) {
    $tableMisses = 0
    $startF = if ($t -eq [int]$state.t) { [int]$state.f } else { 1 }
    for ($f = $startF; $f -le $MaxFieldsPerTable; $f++) {
        if ($processed -ge $BatchSize) {
            "t=$t`nf=$f" | Set-Content $BatchState -Encoding UTF8
            break outer
        }
        $url = "$BaseUrl`Content/TableFields/Table-$t%20Field-$f.htm"
        if ($done.ContainsKey($url) -or $bad.ContainsKey($url)) { $skipped++; continue }
        try {
            $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -UseDefaultCredentials `
                                       -TimeoutSec $TimeoutSec -UserAgent 'SimCorpBatch/1.0'
            if ($resp.StatusCode -eq 200 -and $resp.Content.Length -gt 500) {
                $html = $resp.Content
                $slug = "Table-$t-Field-$f"
                $rawPath = Join-Path $RawDir "$slug.htm"
                [System.IO.File]::WriteAllText($rawPath, $html, [System.Text.UTF8Encoding]::new($false))
                $row = @{}
                foreach ($c in $cols) { $row[$c] = '' }
                $row['namespace']   = 'TableFields'
                $row['url_path']    = $url
                $row['kind']        = 'Tier2_TableField'
                $row['source_file'] = "raw/$slug.htm"
                if ($html -match '(?is)<title[^>]*>(.*?)</title>') {
                    $row['title'] = ([regex]::Replace($matches[1],'<[^>]+>','')).Trim()
                }
                Parse-Tier2 (H2Lines $html) $row
                $csvLine = ($cols | ForEach-Object { Esc ([string]$row[$_]) }) -join ','
                Add-Content $OutCsv -Value $csvLine -Encoding UTF8
                Add-Content $Checkpoint -Value $url -Encoding UTF8
                $done[$url] = $true
                $ok++
                $tableMisses = 0
                if ($ok % 25 -eq 0) {
                    Write-Host ("  T={0} F={1} ok={2} done_total={3}" -f $t,$f,$ok,$done.Count) -ForegroundColor DarkGreen
                }
            } else {
                $tableMisses++
            }
        } catch {
            $msg = $_.Exception.Message
            Add-Content $ErrorsLog -Value ("[$(Get-Date -Format s)] $url : $msg")
            $bad[$url] = $true
            $tableMisses++
        }
        $processed++
        Start-Sleep -Milliseconds $DelayMs
        if ($tableMisses -ge $MissesToSkipTable) {
            Write-Host ("  Table-{0}: skip (>= {1} misses at F={2})" -f $t, $MissesToSkipTable, $f) -ForegroundColor DarkGray
            break
        }
    }
    "t=$($t+1)`nf=1" | Set-Content $BatchState -Encoding UTF8
}

$elapsed = (Get-Date) - $startTime
Write-Host ""
Write-Host "===== BATCH DONE =====" -ForegroundColor Green
Write-Host ("  Fetched ok      : {0}" -f $ok)
Write-Host ("  Processed       : {0}" -f $processed)
Write-Host ("  Already-skipped : {0}" -f $skipped)
Write-Host ("  Elapsed         : {0:N1} min" -f $elapsed.TotalMinutes)
Write-Host ("  CSV rows total  : {0:N0}" -f ((Get-Content $OutCsv).Count - 1))
Write-Host ""
Write-Host "Re-run (F5 again) to continue from next batch — state saved." -ForegroundColor Yellow
