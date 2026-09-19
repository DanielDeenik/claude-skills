# 08_zip_and_transfer.ps1 — package extraction output for transfer back to Mac.
# Run after the main script prints "===== DONE =====".

$dir = "$env:USERPROFILE\Documents\SimCorp_Help_Structured"
$zip = "$env:USERPROFILE\Downloads\SimCorp_Help_Structured_{0}.zip" -f (Get-Date -Format 'yyyyMMdd_HHmm')

Compress-Archive -Path "$dir\*" -DestinationPath $zip -Force

Write-Host ""
Write-Host ("Zipped to: {0}" -f $zip) -ForegroundColor Green
$info = Get-Item $zip
Write-Host ("Size: {0:N1} MB" -f ($info.Length / 1MB))
Write-Host ""
Write-Host "Transfer options (pick one):" -ForegroundColor Yellow
Write-Host "  1. Citrix Workspace → Devices → File Transfer → upload zip"
Write-Host "  2. Email to yourself as attachment (Outlook in Citrix)"
Write-Host "  3. Upload to corporate OneDrive / SharePoint"
Write-Host ""
Write-Host "On Mac, after the zip arrives:"
Write-Host "  unzip ~/Downloads/SimCorp_Help_Structured_*.zip -d ~/Documents/GitHub/akg/data/lightrag-active/simcorp_help_2510/"
Write-Host "  cd ~/Documents/GitHub/akg && source .venv/bin/activate && bin/akg ingest --source simcorp_help_2510"
