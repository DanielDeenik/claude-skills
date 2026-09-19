# 11_formulas_from_file.ps1 — Scrape formula function pages from URL list in
# $env:USERPROFILE\Downloads\formulas.txt (produced by Edge DevTools JavaScript
# snippet that extracts JS-rendered sidebar links).
#
# Workflow:
#   1. In Citrix Edge, open any FormulaFunction-*.htm page
#   2. F12 → Console → type "allow pasting" (one-time unlock)
#   3. Paste the JS snippet (see references/edge_devtools_formula_extract.md)
#   4. Snippet downloads formulas.txt to $env:USERPROFILE\Downloads
#   5. Paste THIS script into ISE Script Pane → F5
#
# Paste into ISE Script Pane → F5. ~10-15 min for 400+ formula functions.

$UrlFile    = "$env:USERPROFILE\Downloads\formulas.txt"
$BaseUrl    = 'https://help.simcorpcloud.com/2510/en/'
$OutDir     = "$env:USERPROFILE\Documents\SimCorp_Help_Structured"
$OutCsv     = Join-Path $OutDir 'SimCorp_Help_Structured.csv'
$RawDir     = Join-Path $OutDir 'raw'
$Checkpoint = Join-Path $OutDir '_checkpoint.txt'
$ErrorsLog  = Join-Path $OutDir '_errors.log'
$DelayMs    = 60
$TimeoutSec = 30

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Web
New-Item -ItemType Directory -Force -Path $OutDir,$RawDir | Out-Null

if (-not (Test-Path $UrlFile)) {
    throw "$UrlFile not found. Do Edge DevTools step first."
}

$urls = Get-Content $UrlFile | ForEach-Object { $_.Trim() } |
        Where-Object { $_ -match '^https?://.*FormulaFunction-' } |
        Sort-Object -Unique
Write-Host ("Loaded {0} unique formula URLs from {1}" -f $urls.Count, $UrlFile) -ForegroundColor Cyan
if ($urls.Count -eq 0) { throw "formulas.txt has no valid URLs." }

$cols = @('namespace','url_path','title','kind','table','column','dbtype','internal_width',
          'nullable','fk_to','domain','dwh_views','editor_list_identifier','editor_list_name',
          'am_field_tooltip','category','is_key','access','formatter','help_topic_raw',
          'description','build_date','source_file')
if (-not (Test-Path $OutCsv)) { ($cols -join ',') | Set-Content $OutCsv -Encoding UTF8 }

$done = @{}
if (Test-Path $Checkpoint) {
    Get-Content $Checkpoint | ForEach-Object { if ($_) { $done[$_] = $true } }
}

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
function Parse-Formula ($lines, $r) {
    $started = $false
    $sec = $null
    $d = @(); $argLines = @()
    foreach ($c in $lines) {
        if (-not $started) {
            if ($c -like 'You are here*' -or $c -match '(?i)^Formula Function\s') { $started = $true }
            else { continue }
        }
        if ($c -match '(?i)^Formula Function\s+([A-Za-z_][A-Za-z0-9_]*)') {
            $r['column'] = $matches[1]
            $r['editor_list_name'] = $matches[1]
            $sec = 'desc'
            continue
        }
        if ($c -eq 'Example')   { $sec = 'example'; continue }
        if ($c -eq 'Arguments') { $sec = 'args'; continue }
        if ($c -like 'Give feedback*') { $sec = $null; continue }
        $bd = Get-BuildDate $c
        if ($bd) { $r['build_date'] = $bd; break }
        if ($sec -eq 'desc' -and $c) { $d += $c }
        elseif ($sec -eq 'args' -and $c -match '^[a-z]') { $argLines += $c }
    }
    if ($d) {
        $body = $d -join ' '
        if ($argLines) { $body += ' | Arguments: ' + ($argLines -join '; ') }
        $r['description'] = $body
    }
}

$ok = 0; $skip = 0; $err = 0; $startTime = Get-Date
$i = 0; $total = $urls.Count
foreach ($url in $urls) {
    $i++
    if ($done.ContainsKey($url)) { $skip++; continue }
    try {
        $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -UseDefaultCredentials `
                                   -TimeoutSec $TimeoutSec -UserAgent 'SimCorpFormulas/1.0'
        if ($resp.StatusCode -ne 200 -or $resp.Content.Length -lt 500) { $err++; continue }
        $html = $resp.Content
        $slugBase = [System.IO.Path]::GetFileNameWithoutExtension(([uri]$url).LocalPath)
        $slug = ($slugBase -replace '[^A-Za-z0-9_\-]+','-').Trim('-')
        if ($slug.Length -gt 200) { $slug = $slug.Substring(0,200) }
        [System.IO.File]::WriteAllText((Join-Path $RawDir "$slug.htm"), $html, [System.Text.UTF8Encoding]::new($false))
        $row = @{}
        foreach ($c in $cols) { $row[$c] = '' }
        $row['namespace']   = 'Formulas'
        $row['url_path']    = $url
        $row['kind']        = 'Formula'
        $row['source_file'] = "raw/$slug.htm"
        if ($html -match '(?is)<title[^>]*>(.*?)</title>') {
            $row['title'] = ([regex]::Replace($matches[1],'<[^>]+>','')).Trim()
        }
        Parse-Formula (H2Lines $html) $row
        $csvLine = ($cols | ForEach-Object { Esc ([string]$row[$_]) }) -join ','
        Add-Content $OutCsv -Value $csvLine -Encoding UTF8
        Add-Content $Checkpoint -Value $url -Encoding UTF8
        $done[$url] = $true; $ok++
        if ($ok % 20 -eq 0) {
            Write-Host ("  ok={0} progress={1}/{2}" -f $ok, $i, $total) -ForegroundColor DarkGreen
        }
    } catch {
        $err++
        $msg = $_.Exception.Message
        Add-Content $ErrorsLog -Value ("[$(Get-Date -Format s)] $url : $msg")
    }
    Start-Sleep -Milliseconds $DelayMs
}

$elapsed = (Get-Date) - $startTime
Write-Host ""
Write-Host "===== FORMULAS DONE =====" -ForegroundColor Green
Write-Host ("  URLs processed : {0}" -f $total)
Write-Host ("  Fetched ok     : {0}" -f $ok)
Write-Host ("  Skipped (done) : {0}" -f $skip)
Write-Host ("  Errors         : {0}" -f $err)
Write-Host ("  Elapsed        : {0:N1} min" -f $elapsed.TotalMinutes)
Write-Host ("  CSV total rows : {0:N0}" -f ((Get-Content $OutCsv).Count - 1))
