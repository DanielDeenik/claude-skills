# 07_monitor.ps1 — live progress monitoring while production script runs.
# Run in a SECOND console pane (PowerShell 2 / 3 tab) while main script runs in PowerShell 1.
# Repeat every 10-15 minutes.

$dir = "$env:USERPROFILE\Documents\SimCorp_Help_Structured"

Write-Host ""
Write-Host "=== Folder contents ===" -ForegroundColor Cyan
Get-ChildItem $dir -ErrorAction SilentlyContinue | Format-Table Name, Length, LastWriteTime -AutoSize

Write-Host ""
Write-Host "=== CSV row count (data rows, excluding header) ===" -ForegroundColor Cyan
$csv = Join-Path $dir 'SimCorp_Help_Structured.csv'
if (Test-Path $csv) {
    $rows = (Get-Content $csv).Count - 1
    Write-Host ("  {0} rows" -f $rows) -ForegroundColor Green
} else {
    Write-Host "  CSV not yet created" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Raw .htm files captured ===" -ForegroundColor Cyan
$raw = Join-Path $dir 'raw'
if (Test-Path $raw) {
    $rawCount = (Get-ChildItem $raw -Filter *.htm).Count
    Write-Host ("  {0} files" -f $rawCount) -ForegroundColor Green
} else {
    Write-Host "  raw/ not yet created" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Latest 5 raw pages ===" -ForegroundColor Cyan
if (Test-Path $raw) {
    Get-ChildItem $raw -Filter *.htm |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 5 Name, Length, LastWriteTime |
        Format-Table -AutoSize
}

Write-Host ""
Write-Host "=== Latest 3 CSV rows (truncated) ===" -ForegroundColor Cyan
if (Test-Path $csv) {
    Get-Content $csv -Tail 3 | ForEach-Object { Write-Host ("  {0}" -f $_.Substring(0, [Math]::Min(200, $_.Length))) }
}

Write-Host ""
Write-Host "=== Error log (last 5 errors) ===" -ForegroundColor Cyan
$errs = Join-Path $dir '_errors.log'
if (Test-Path $errs) {
    $errCount = (Get-Content $errs).Count
    Write-Host ("  Total errors logged: {0}" -f $errCount) -ForegroundColor $(if ($errCount -gt 1000) { 'Yellow' } else { 'DarkGray' })
    Get-Content $errs -Tail 5 | ForEach-Object { Write-Host ("  {0}" -f $_) -ForegroundColor DarkGray }
}
