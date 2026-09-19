# 06_verify_paste.ps1 — confirm Script Pane contents parse cleanly BEFORE F5.
# Run in ISE console pane. Green message → ready to F5. Red errors → patch.

$tokens = $errors = $null
[System.Management.Automation.Language.Parser]::ParseInput(
    $psISE.CurrentFile.Editor.Text,
    [ref]$tokens,
    [ref]$errors
) | Out-Null

if ($errors) {
    $errors | ForEach-Object {
        Write-Host ("ERROR line {0}: {1}" -f $_.Extent.StartLineNumber, $_.Message) -ForegroundColor Red
    }
}
else {
    Write-Host "Script parses clean. Ready to F5." -ForegroundColor Green
}
