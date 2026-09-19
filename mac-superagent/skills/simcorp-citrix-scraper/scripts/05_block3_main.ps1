# === BLOCK 3 of 3: main loop =================================================
# Paste this DIRECTLY BELOW Block 2 in ISE Script Pane. Then F5.

function Process-Page ($url, $ns) {
    if ($done.ContainsKey($url)) { return $false }
    try {
        $resp = Get-Page $url
        if ($resp.StatusCode -ne 200 -or $resp.Content.Length -lt 500) { return $false }
        $html = $resp.Content
        $slugBase = [System.IO.Path]::GetFileNameWithoutExtension(([uri]$url).LocalPath)
        $slug = ($slugBase -replace '[^A-Za-z0-9_\-]+','-').Trim('-')
        if (-not $slug) { $slug = 'page' }
        if ($slug.Length -gt 200) { $slug = $slug.Substring(0,200) }
        $rawPath = Join-Path $RawDir "$slug.htm"
        [System.IO.File]::WriteAllText($rawPath, $html, [System.Text.UTF8Encoding]::new($false))

        $kind = Get-Kind $url
        $row = @{}
        foreach ($c in $cols) { $row[$c] = '' }
        $row['namespace']   = $ns
        $row['url_path']    = $url
        $row['kind']        = $kind
        $row['title']       = Get-Title $html
        $row['source_file'] = "raw/$slug.htm"

        $lines = H2Lines $html
        switch ($kind) {
            'Tier2_TableField' { Parse-Tier2        $lines $row }
            'Table_Summary'    { Parse-TableSummary $lines $row }
            default            { Parse-Generic      $lines $row }
        }

        $csvLine = ($cols | ForEach-Object { Esc ([string]$row[$_]) }) -join ','
        Add-Content $OutCsv -Value $csvLine -Encoding UTF8
        Add-Content $Checkpoint -Value $url -Encoding UTF8
        $done[$url] = $true
        return $true
    } catch {
        $msg = $_.Exception.Message
        Add-Content $ErrorsLog -Value ("[$(Get-Date -Format s)] $url : $msg") -Encoding UTF8
        return $false
    }
}

# === PHASE 1: enumerate shapes ===============================================
Write-Host ""
Write-Host "===== PHASE 1: Enumerate shapes =====" -ForegroundColor Cyan

$fieldUrlBacklog = New-Object System.Collections.Generic.HashSet[string]
$phase1Hits = 0

foreach ($s in $Shapes) {
    Write-Host ""
    Write-Host ("Shape: {0}" -f $s.Name) -ForegroundColor Yellow
    $hits = 0; $misses = 0
    for ($n = 1; $n -le $s.MaxId; $n++) {
        $rel = $s.Pattern -f $n
        $url = $BaseUrl + $rel
        $ok = Process-Page $url $s.Name
        if ($ok) {
            $hits++; $misses = 0
            if ($s.Name -eq 'Tables') {
                $rawPath = Join-Path $RawDir "Table-$n.htm"
                if (Test-Path $rawPath) {
                    $tHtml = Get-Content -LiteralPath $rawPath -Raw -Encoding UTF8
                    foreach ($fu in Extract-FieldLinks $tHtml) {
                        [void]$fieldUrlBacklog.Add($fu)
                    }
                }
            }
            if ($hits % 50 -eq 0) {
                Write-Host ("  {0} hits={1} idx={2}" -f $s.Name, $hits, $n) -ForegroundColor DarkGreen
            }
        } else {
            $misses++
        }
        if ($misses -ge $s.StopAfterMisses) {
            Write-Host ("  {0}: stopped at idx={1}" -f $s.Name, $n)
            break
        }
        Start-Sleep -Milliseconds $DelayMs
    }
    $phase1Hits += $hits
    Write-Host ("  {0} TOTAL: {1} pages" -f $s.Name, $hits) -ForegroundColor Green
}

# === PHASE 2: TableFields ====================================================
Write-Host ""
Write-Host "===== PHASE 2: TableFields =====" -ForegroundColor Cyan
Write-Host ("Backlog: {0} TableField URLs" -f $fieldUrlBacklog.Count)

$fhits = 0
$ftotal = $fieldUrlBacklog.Count
$fi = 0
foreach ($fu in $fieldUrlBacklog) {
    $fi++
    if (Process-Page $fu 'TableFields') {
        $fhits++
        if ($fhits % 100 -eq 0) {
            Write-Host ("  Fields hits={0} progress={1}/{2}" -f $fhits, $fi, $ftotal) -ForegroundColor DarkGreen
        }
    }
    Start-Sleep -Milliseconds $DelayMs
}

# === Summary =================================================================
Write-Host ""
Write-Host "===== DONE =====" -ForegroundColor Green
Write-Host ("  Phase 1 pages : {0}" -f $phase1Hits)
Write-Host ("  Phase 2 fields: {0}" -f $fhits)
Write-Host ("  Total rows    : {0}" -f ($phase1Hits + $fhits))
Write-Host ("  CSV           : {0}" -f $OutCsv)
Write-Host ("  Raw archive   : {0}" -f $RawDir)
Write-Host ("  Errors        : {0}" -f $ErrorsLog)
