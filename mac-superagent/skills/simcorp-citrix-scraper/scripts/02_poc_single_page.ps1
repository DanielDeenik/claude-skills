# 02_poc_single_page.ps1 — PoC: fetch + parse + CSV write on ONE page.
# Run in ISE Script Pane → F5.
# Success criterion: STEP 4 prints 13 populated fields for EXCIK.

$Url    = 'https://help.simcorpcloud.com/2510/en/Content/TableFields/Table-1%20Field-190.htm'
$OutDir = "$env:USERPROFILE\Documents\SimCorp_Help_Structured"
$OutCsv = Join-Path $OutDir 'PoC_single_row.csv'

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Web
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

Write-Host "=== STEP 1: Fetch ===" -ForegroundColor Cyan
$resp = Invoke-WebRequest -Uri $Url -UseBasicParsing -UseDefaultCredentials `
                          -TimeoutSec 30 -UserAgent 'SimCorpPoC/1.0'
Write-Host ("  HTTP {0}, {1} bytes" -f $resp.StatusCode, $resp.Content.Length) -ForegroundColor Green

Write-Host ""
Write-Host "=== STEP 2: Tokenize ===" -ForegroundColor Cyan
$h = $resp.Content
$h = $h -replace '(?is)<(script|style)[^>]*>.*?</\1>',''
$h = $h -replace '(?s)<!--.*?-->',''
$h = $h -replace '(?i)<(br|hr)\b[^>]*/?>',"`n"
$h = $h -replace '(?i)</(p|div|h[1-6]|tr|td|th|li|table)>',"`n"
$h = $h -replace '<[^>]+>',"`t"
$h = [System.Web.HttpUtility]::HtmlDecode($h)
$lines = @($h -split "`n" | ForEach-Object { ($_ -replace '\s+',' ').Trim() } | Where-Object { $_ })
Write-Host ("  Cleaned to {0} lines" -f $lines.Count) -ForegroundColor Green

Write-Host ""
Write-Host "=== STEP 3: Parse Tier-2 ===" -ForegroundColor Cyan
$cols = @('namespace','url_path','title','kind','table','column','dbtype','internal_width',
          'nullable','fk_to','domain','dwh_views','editor_list_identifier','editor_list_name',
          'am_field_tooltip','category','is_key','access','formatter','help_topic_raw',
          'description','build_date','source_file')
$row = @{}; foreach ($c in $cols){ $row[$c]='' }
$row['namespace'] = 'TableFields'
$row['url_path']  = $Url
$row['kind']      = 'Tier2_TableField'
if ($resp.Content -match '(?is)<title[^>]*>(.*?)</title>') {
    $row['title'] = ([regex]::Replace($matches[1],'<[^>]+>','')).Trim()
}

$sec=$null; $d=@(); $v=@()
foreach ($c in $lines) {
    if (-not $row['column'] -and $c -match '(?i)Database field\s+([A-Z0-9_]+)\s+in\s+table\s+([A-Z0-9_]+)') {
        $row['column']=$matches[1]; $row['table']=$matches[2]; continue
    }
    if ($c -like 'Technical Information*'){ $sec='tech'; continue }
    if ($c -like 'Found in view*')        { $sec='views'; continue }
    if ($c -eq 'Description')             { $sec='desc'; continue }
    if ($c -like 'See also*')             { $sec=$null; continue }
    if ($c -like 'Give feedback*')        { $sec=$null; continue }
    if ($c -like 'Build:*' -and $c -match 'Build:\s*(.+?)\s+at\s+(.+)') {
        $row['build_date']="$($matches[1].Trim()) $($matches[2].Trim())"; break
    }
    switch ($sec) {
        'tech' {
            if ($c -match '(?i)always mandatory'){ $row['nullable']='NOT NULL (always)' }
            elseif ($c -match '(?i)partly mandatory'){ $row['nullable']='NOT NULL (partly)' }
            if ($c -match 'Database type:\s*([A-Z0-9(),\s]+?)(?:\t|Internal max|$)') { $row['dbtype']=$matches[1].Trim() }
            if ($c -match 'Internal max\.?\s*width.*?:\s*(\d+)') { $row['internal_width']=$matches[1] }
            if ($c -match 'internal key reference to\s+([A-Z0-9_]+)') { $row['fk_to']=$matches[1]; $row['is_key']='YES' }
        }
        'views' { if ($c -match '^[A-Z0-9_]+(\.[A-Z0-9_]+)+$'){ $v += $c } }
        'desc'  { if ($c){ $d += $c } }
    }
}
if ($d){ $row['description']=($d -join ' ') }
if ($v){ $row['dwh_views']=($v -join '; ') }
Write-Host "  Done" -ForegroundColor Green

Write-Host ""
Write-Host "=== STEP 4: Structured row (only populated fields) ===" -ForegroundColor Cyan
$row.GetEnumerator() | Where-Object { $_.Value -ne '' } | Sort-Object Name | ForEach-Object {
    Write-Host ("  {0,-20} {1}" -f $_.Name, $_.Value)
}

Write-Host ""
Write-Host "=== STEP 5: Write CSV ===" -ForegroundColor Cyan
function Esc ([string]$v) {
    if ($null -eq $v) { return '' }
    if ($v -match '[",\r\n]') { return '"'+($v -replace '"','""')+'"' }
    return $v
}
($cols -join ',') | Set-Content -Path $OutCsv -Encoding UTF8
($cols | ForEach-Object { Esc ([string]$row[$_]) }) -join ',' | Add-Content -Path $OutCsv -Encoding UTF8
Write-Host ("  Wrote {0}" -f $OutCsv) -ForegroundColor Green

Write-Host ""
Write-Host "=== PoC complete ===" -ForegroundColor Yellow
Write-Host "Success = STEP 4 showed dbtype/nullable/fk_to/dwh_views/description/build_date populated." -ForegroundColor Yellow
