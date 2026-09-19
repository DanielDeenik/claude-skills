# === BLOCK 1 of 3: config + helpers ==========================================
# Paste into ISE Script Pane (after Ctrl+A → Delete). Do NOT F5 yet.
# Then paste BLOCK 2 directly below this, then BLOCK 3.
# Final F5 runs the full extraction.

$BaseUrl    = 'https://help.simcorpcloud.com/2510/en/'
$OutDir     = "$env:USERPROFILE\Documents\SimCorp_Help_Structured"
$OutCsv     = Join-Path $OutDir 'SimCorp_Help_Structured.csv'
$RawDir     = Join-Path $OutDir 'raw'
$Checkpoint = Join-Path $OutDir '_checkpoint.txt'
$ErrorsLog  = Join-Path $OutDir '_errors.log'
$DelayMs    = 80
$TimeoutSec = 30

$Shapes = @(
    @{ Name='Tables';   Pattern='Content/Tables/Table-{0}.htm';     MaxId=8000; StopAfterMisses=200 },
    @{ Name='Forms';    Pattern='Content/Forms/Form-{0}.htm';        MaxId=8000; StopAfterMisses=200 },
    @{ Name='Views';    Pattern='Content/Views/View-{0}.htm';        MaxId=3000; StopAfterMisses=200 },
    @{ Name='Commands'; Pattern='Content/Commands/Command-{0}.htm'; MaxId=15000; StopAfterMisses=300 }
)

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
    Write-Host ("Resume: {0} URLs already done" -f $done.Count) -ForegroundColor Cyan
}

function Esc ([string]$v) {
    if ($null -eq $v) { return '' }
    if ($v -match '[",\r\n]') { return '"' + ($v -replace '"','""') + '"' }
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
    $h = $h -replace '(?s)<!--.*?-->',''
    $h = $h -replace '(?i)<(br|hr)\b[^>]*/?>',"`n"
    $h = $h -replace '(?i)</(p|div|h[1-6]|tr|td|th|li|table)>',"`n"
    $h = $h -replace '<[^>]+>',"`t"
    $h = [System.Web.HttpUtility]::HtmlDecode($h)
    @($h -split "`n" | ForEach-Object { ($_ -replace '\s+',' ').Trim() } | Where-Object { $_ })
}

function Get-Title ($html) {
    if ($html -match '(?is)<title[^>]*>(.*?)</title>') {
        return ([regex]::Replace($matches[1],'<[^>]+>','')).Trim()
    }
    return ''
}

function Get-Page ($url) {
    Invoke-WebRequest -Uri $url -UseBasicParsing -UseDefaultCredentials -TimeoutSec $TimeoutSec -UserAgent 'SimCorpExtract/1.0'
}

function Extract-FieldLinks ($html) {
    $hits = [regex]::Matches($html,'(?i)href="([^"]*Content/TableFields/[^"]+\.htm)"')
    $hits | ForEach-Object {
        $h = $_.Groups[1].Value
        if ($h -match '^https?://') { $h }
        elseif ($h.StartsWith('/')) { 'https://help.simcorpcloud.com' + $h }
        else {
            try { [Uri]::new([Uri]"$BaseUrl`Content/Tables/dummy.htm",$h).AbsoluteUri } catch { $null }
        }
    } | Where-Object { $_ } | Select-Object -Unique
}

function Get-Kind ($url) {
    if ($url -match '/Content/TableFields/')           { return 'Tier2_TableField' }
    if ($url -match '/Content/EditorListProperties/')  { return 'Tier1_Field' }
    if ($url -match '/Content/Tables/')                { return 'Table_Summary' }
    if ($url -match '/Content/Forms/')                 { return 'Form' }
    if ($url -match '/Content/Views/')                 { return 'View' }
    if ($url -match '/Content/Formulas/')              { return 'Formula' }
    if ($url -match '/Content/Commands/')              { return 'Command' }
    if ($url -match '/Content/ReleaseNotes/')          { return 'ReleaseNote' }
    return 'Main_Narrative'
}
