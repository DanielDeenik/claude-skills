# 12_viewfields_scraper.ps1 — ViewFields (per-field docs for Report Views).
# Crawls Views numerically, extracts ViewField links from each, scrapes each.
# New namespace=ViewFields, kind=ViewField. Resumable via _batch_state_views.txt.
# Paste into ISE Script Pane → F5. Re-F5 to continue from saved state.

$BatchSize         = 500
$StartViewId       = 1
$EndViewId         = 25000
$MissesToSkipView  = 100
$DelayMs           = 60
$TimeoutSec        = 30

$BaseUrl    = 'https://help.simcorpcloud.com/2510/en/'
$OutDir     = "$env:USERPROFILE\Documents\SimCorp_Help_Structured"
$OutCsv     = Join-Path $OutDir 'SimCorp_Help_Structured.csv'
$RawDir     = Join-Path $OutDir 'raw'
$Checkpoint = Join-Path $OutDir '_checkpoint.txt'
$ErrorsLog  = Join-Path $OutDir '_errors.log'
$BatchState = Join-Path $OutDir '_batch_state_views.txt'

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
$state = @{ v = $StartViewId }
if (Test-Path $BatchState) {
    Get-Content $BatchState | ForEach-Object {
        if ($_ -match '^v=(\d+)$') { $state['v'] = [int]$matches[1] }
    }
}
Write-Host ("BatchSize={0} ResumeView={1}" -f $BatchSize, $state.v) -ForegroundColor Cyan
Write-Host ("Already done: {0}  Known 404s: {1}" -f $done.Count, $bad.Count) -ForegroundColor DarkGray

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
function Parse-ViewField ($lines, $r) {
    $sec = $null; $d = @()
    foreach ($c in $lines) {
        if ($c -match '(?i)^Report view field\s+([A-Za-z0-9_]+)\s+in\s*(.+)$') {
            $r['column'] = $matches[1]
            $r['help_topic_raw'] = $matches[2].Trim()
            $sec = 'desc'
            continue
        }
        if ($c -like 'Technical Information*') { $sec = 'tech'; continue }
        if ($c -like 'Give feedback*')          { $sec = $null; continue }
        $bd = Get-BuildDate $c
        if ($bd) { $r['build_date'] = $bd; break }
        if ($sec -eq 'tech') {
            if ($c -match 'This field is based on\s+([A-Z0-9_]+)\.([A-Z0-9_]+)') {
                $r['table']  = $matches[1]
                $r['editor_list_name'] = $matches[2]
            }
            if ($c -match '([A-Z0-9_]+(?:\.[A-Z0-9_]+)+(?:->[A-Z0-9_]+(?:\.[A-Z0-9_]+)+)+)') {
                $r['fk_to'] = $matches[1]
            }
        }
        elseif ($sec -eq 'desc' -and $c) { $d += $c }
    }
    if ($d) { $r['description'] = ($d -join ' ') }
}
function Get-Page ($url) {
    Invoke-WebRequest -Uri $url -UseBasicParsing -UseDefaultCredentials `
                      -TimeoutSec $TimeoutSec -UserAgent 'SimCorpViewFields/1.0'
}
function Process-ViewField ($vfUrl) {
    if ($done.ContainsKey($vfUrl) -or $bad.ContainsKey($vfUrl)) { return $false }
    try {
        $resp = Get-Page $vfUrl
        if ($resp.StatusCode -ne 200 -or $resp.Content.Length -lt 300) { return $false }
        $html = $resp.Content
        $slugBase = [System.IO.Path]::GetFileNameWithoutExtension(([uri]$vfUrl).LocalPath)
        $slug = ($slugBase -replace '[^A-Za-z0-9_\-]+','-').Trim('-')
        if ($slug.Length -gt 200) { $slug = $slug.Substring(0,200) }
        [System.IO.File]::WriteAllText((Join-Path $RawDir "$slug.htm"), $html, [System.Text.UTF8Encoding]::new($false))
        $row = @{}
        foreach ($c in $cols) { $row[$c] = '' }
        $row['namespace']   = 'ViewFields'
        $row['url_path']    = $vfUrl
        $row['kind']        = 'ViewField'
        $row['source_file'] = "raw/$slug.htm"
        if ($html -match '(?is)<title[^>]*>(.*?)</title>') {
            $row['title'] = ([regex]::Replace($matches[1],'<[^>]+>','')).Trim()
        }
        Parse-ViewField (H2Lines $html) $row
        $csvLine = ($cols | ForEach-Object { Esc ([string]$row[$_]) }) -join ','
        Add-Content $OutCsv -Value $csvLine -Encoding UTF8
        Add-Content $Checkpoint -Value $vfUrl -Encoding UTF8
        $done[$vfUrl] = $true
        return $true
    } catch {
        $msg = $_.Exception.Message
        Add-Content $ErrorsLog -Value ("[$(Get-Date -Format s)] $vfUrl : $msg")
        $bad[$vfUrl] = $true
        return $false
    }
}

$processed = 0; $vfOk = 0; $viewMisses = 0; $startTime = Get-Date

:outer for ($v = [int]$state.v; $v -le $EndViewId; $v++) {
    if ($processed -ge $BatchSize) {
        "v=$v" | Set-Content $BatchState -Encoding UTF8
        break outer
    }
    $viewUrl = "$BaseUrl`Content/Views/View-$v.htm"
    try {
        $resp = Get-Page $viewUrl
        if ($resp.StatusCode -ne 200 -or $resp.Content.Length -lt 500) {
            $viewMisses++
            if ($viewMisses -ge $MissesToSkipView) {
                Write-Host ("  Stop after {0} consecutive missing Views at V={1}" -f $MissesToSkipView, $v) -ForegroundColor DarkGray
                "v=$($v+1)" | Set-Content $BatchState -Encoding UTF8
                break outer
            }
            continue
        }
        $viewMisses = 0
        $vHtml = $resp.Content
        $hits = [regex]::Matches($vHtml, '(?i)href="([^"]*ViewFields/[^"]+\.htm)"')
        $vfUrls = New-Object System.Collections.Generic.HashSet[string]
        foreach ($m in $hits) {
            $h = $m.Groups[1].Value
            $abs = if ($h -match '^https?://') { $h }
                   elseif ($h.StartsWith('/')) { 'https://help.simcorpcloud.com' + $h }
                   else {
                       try { [Uri]::new([Uri]$viewUrl, $h).AbsoluteUri } catch { $null }
                   }
            if ($abs) { [void]$vfUrls.Add($abs) }
        }
        foreach ($vfUrl in $vfUrls) {
            if ($processed -ge $BatchSize) { break }
            if (Process-ViewField $vfUrl) {
                $vfOk++
                if ($vfOk % 25 -eq 0) {
                    Write-Host ("  V={0} vfOk={1} done_total={2}" -f $v, $vfOk, $done.Count) -ForegroundColor DarkGreen
                }
            }
            $processed++
            Start-Sleep -Milliseconds $DelayMs
        }
    } catch {
        $msg = $_.Exception.Message
        Add-Content $ErrorsLog -Value ("[$(Get-Date -Format s)] $viewUrl : $msg")
        $viewMisses++
    }
    "v=$($v+1)" | Set-Content $BatchState -Encoding UTF8
}

$elapsed = (Get-Date) - $startTime
Write-Host ""
Write-Host "===== VIEWFIELDS BATCH DONE =====" -ForegroundColor Green
Write-Host ("  ViewFields ok   : {0}" -f $vfOk)
Write-Host ("  Processed       : {0}" -f $processed)
Write-Host ("  Elapsed         : {0:N1} min" -f $elapsed.TotalMinutes)
Write-Host ("  CSV rows total  : {0:N0}" -f ((Get-Content $OutCsv).Count - 1))
Write-Host ""
Write-Host "Re-run (F5 again) to continue from saved state." -ForegroundColor Yellow
