# 00_preflight.ps1 — verify Citrix can reach help.simcorpcloud.com from PowerShell.
# Run in ISE console pane. Expects HTTP 200 with ~140 KB body.
# 10-second test before any extraction work.

try {
    $r = Invoke-WebRequest `
        -Uri 'https://help.simcorpcloud.com/2510/en/Content/Tables/Table-1.htm' `
        -UseBasicParsing `
        -UseDefaultCredentials `
        -TimeoutSec 30
    [pscustomobject]@{
        Status        = $r.StatusCode
        Length        = $r.Content.Length
        HasTableHdr   = ($r.Content -match 'Database table')
        ServerHeader  = $r.Headers['Server']
    } | Format-List
}
catch {
    Write-Host "PREFLIGHT FAILED: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Diagnosis:" -ForegroundColor Yellow
    Write-Host "  HTTP 401/403  → SSO cookie capture needed (see references/cookie_capture.md)"
    Write-Host "  Timeout       → Citrix firewall blocks; escalate to NW IT"
    Write-Host "  DNS failure   → confirm host resolves: nslookup help.simcorpcloud.com"
}
