# 10_formulas_scraper.ps1 — BFS crawler over Formula function pages.
# Discovers + scrapes ALL formula functions by breadth-first traversal of
# sidebar links. Multi-seed kickoff guarantees alphabetical coverage.
# Self-contained. Resumable via _checkpoint.txt.
# Paste into ISE Script Pane → F5.

# Multi-seed: 8 well-distributed letters guarantee fast BFS convergence.
$Seeds = @(
    'Content/Formulas/FormulaFunction-execrefdate.htm',
    'Content/Formulas/FormulaFunction-day.htm',
    'Content/Formulas/FormulaFunction-substring.htm',
    'Content/Formulas/FormulaFunction-year.htm',
    'Content/Formulas/FormulaFunction-min.htm',
    'Content/Formulas/FormulaFunction-not.htm',
    'Content/Formulas/FormulaFunction-round.htm',
    'Content/Formulas/FormulaFunction-abs.htm'
)

$BaseUrl    = 'https://help.simcorpcloud.com/2510/en/'
$OutDir     = "$env:USERPROFILE\Documents\SimCorp_Help_Structured"
$OutCsv     = Join-Path $OutDir 'SimCorp_Help_Structured.csv'
$RawDir     = Join-Path $OutDir 'raw'
$Checkpoint = Join-Path $OutDir '_checkpoint.txt'
$ErrorsLog  = Join-Path $OutDir '_errors.log'
$DelayMs    = 50
$TimeoutSec = 30

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
    $d = @()
    $argLines = @()
    foreach ($c in $lines) {
        if (-not $started) {
            if ($c -like 'You are here*') { $started = $true }
            continue
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
function To-AbsUrl ($href, $referer) {
    if ($href -match '^https?://') { return $href }
    if ($href.StartsWith('/'))      { return 'https://help.simcorpcloud.com' + $href }
    try { return [Uri]::new([Uri]$referer, $href).AbsoluteUri } catch { return $null }
}

$discovered = @{}
$queue = New-Object System.Collections.Queue
foreach ($s in $Seeds) {
    $u = $BaseUrl + $s
    if (-not $discovered.ContainsKey($u)) {
        $discovered[$u] = $true
        $queue.Enqueue($u)
    }
}
Write-Host ("BFS seeded with {0} starting URLs" -f $queue.Count) -ForegroundColor Cyan

$ok = 0; $skip = 0; $err = 0; $startTime = Get-Date
$processed = 0
while ($queue.Count -gt 0) {
    $url = $queue.Dequeue()
    $processed++
    try {
        $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -UseDefaultCredentials `
                                   -TimeoutSec $TimeoutSec -UserAgent 'SimCorpFormulasBFS/1.0'
        if ($resp.StatusCode -ne 200) { $err++; continue }
        $html = $resp.Content

        $hits = [regex]::Matches($html, '(?i)href="([^"]*FormulaFunction-[^"]+\.htm)"')
        $newCount = 0
        foreach ($m in $hits) {
            $abs = To-AbsUrl $m.Groups[1].Value $url
            if ($abs -and -not $discovered.ContainsKey($abs)) {
                $discovered[$abs] = $true
                $queue.Enqueue($abs)
                $newCount++
            }
        }

        if ($done.ContainsKey($url)) { $skip++ }
        else {
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
            $done[$url] = $true
            $ok++
        }

        if ($processed % 20 -eq 0) {
            Write-Host ("  processed={0} discovered={1} queue={2} ok={3} new_in_last_page={4}" `
                -f $processed, $discovered.Count, $queue.Count, $ok, $newCount) -ForegroundColor DarkGreen
        }
    } catch {
        $err++
        Add-Content $ErrorsLog -Value ("[$(Get-Date -Format s)] $url : $($_.Exception.Message)")
    }
    Start-Sleep -Milliseconds $DelayMs
}

$elapsed = (Get-Date) - $startTime
Write-Host ""
Write-Host "===== FORMULAS BFS DONE =====" -ForegroundColor Green
Write-Host ("  Total discovered : {0}" -f $discovered.Count)
Write-Host ("  Fetched ok       : {0}" -f $ok)
Write-Host ("  Already-skipped  : {0}" -f $skip)
Write-Host ("  Errors           : {0}" -f $err)
Write-Host ("  Elapsed          : {0:N1} min" -f $elapsed.TotalMinutes)
Write-Host ("  CSV rows total   : {0:N0}" -f ((Get-Content $OutCsv).Count - 1))
