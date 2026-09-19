# 01_diagnostic_page_dump.ps1 — dump first 40 cleaned text lines of a known page.
# Use to verify parser regex patterns match the live portal version.
# If wording has changed since 2510, patch references/parser_patterns.md.

$r = Invoke-WebRequest `
    -Uri 'https://help.simcorpcloud.com/2510/en/Content/Tables/Table-1.htm' `
    -UseBasicParsing `
    -UseDefaultCredentials `
    -TimeoutSec 30

Add-Type -AssemblyName System.Web
$h = $r.Content
$h = $h -replace '(?is)<(script|style)[^>]*>.*?</\1>',''
$h = $h -replace '(?i)</(p|div|h[1-6]|tr|td|th|li|table)>',"`n"
$h = $h -replace '<[^>]+>',"`t"
$h = [System.Web.HttpUtility]::HtmlDecode($h)
$lines = @($h -split "`n" | ForEach-Object { ($_ -replace '\s+',' ').Trim() } | Where-Object { $_ })

$lines | Select-Object -First 40 | ForEach-Object { Write-Host $_ }
Write-Host ""
Write-Host "=== TOTAL LINES: $($lines.Count) ===" -ForegroundColor Cyan

# Expected on 2510:
#   Line 1:  "Database table SECURITIES"   (or similar shape with table name)
#   Line ~5: "You are here:"               (breadcrumb anchor)
#   Line ~7: "Table Group: Securities"
#   Line ~8: "Sub-Table Group: Static data and configuration"
#   Line ~9: "Main table for securities."
#   Line ~10: "Fields on SECURITIES"
#   Bottom:  "Build: <date> at <time>"
#
# Also try TableFields and EditorListProperties URLs to confirm field-page structure.
