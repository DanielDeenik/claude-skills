# === BLOCK 2 of 3: parsers ===================================================
# Paste this DIRECTLY BELOW Block 1 in ISE Script Pane. Do NOT F5 yet.
# Then paste Block 3, then F5 to run everything.

function Parse-Tier2 ($lines, $r) {
    $sec = $null; $d = @(); $v = @()
    foreach ($c in $lines) {
        if (-not $r['column'] -and $c -match '(?i)Database field\s+([A-Z0-9_]+)\s+in\s+table\s+([A-Z0-9_]+)') {
            $r['column'] = $matches[1]
            $r['table']  = $matches[2]
            continue
        }
        if ($c -like 'Technical Information*') { $sec = 'tech'; continue }
        if ($c -like 'Found in view*')         { $sec = 'views'; continue }
        if ($c -eq  'Description')             { $sec = 'desc'; continue }
        if ($c -like 'See also*')              { $sec = 'see_also'; continue }
        if ($c -like 'Give feedback*')         { $sec = $null; continue }
        $bd = Get-BuildDate $c
        if ($bd) { $r['build_date'] = $bd; break }
        if ($sec -eq 'tech') {
            if ($c -match '(?i)always mandatory')        { $r['nullable'] = 'NOT NULL (always)' }
            elseif ($c -match '(?i)partly mandatory')    { $r['nullable'] = 'NOT NULL (partly)' }
            if ($c -match 'Database type:\s*([A-Z0-9(),\s]+?)(?:\t|Internal max|$)') {
                $r['dbtype'] = $matches[1].Trim()
            }
            if ($c -match 'Internal max\.?\s*width.*?:\s*(\d+)') {
                $r['internal_width'] = $matches[1]
            }
            if ($c -match 'internal key reference to\s+([A-Z0-9_]+)') {
                $r['fk_to'] = $matches[1]
                $r['is_key'] = 'YES'
            }
            if ($c -match 'of domain\s+([A-Za-z0-9_]+)') {
                $r['domain'] = $matches[1]
            }
        }
        elseif ($sec -eq 'views') {
            if ($c -match '^[A-Z0-9_]+(\.[A-Z0-9_]+)+$') { $v += $c }
        }
        elseif ($sec -eq 'desc') {
            if ($c) { $d += $c }
        }
        elseif ($sec -eq 'see_also') {
            if ($c -match 'General help for the Table\s+([A-Z0-9_]+)') {
                $tbl = $matches[1]
                $r['help_topic_raw'] = "Table:$tbl"
            }
            if ($c -match 'Help for the referenced field\s+([A-Z0-9_]+)\.([A-Z0-9_]+)') {
                if (-not $r['fk_to']) { $r['fk_to'] = $matches[1] }
            }
        }
    }
    if ($d) { $r['description'] = ($d -join ' ') }
    if ($v) { $r['dwh_views']   = ($v -join '; ') }
}

function Parse-TableSummary ($lines, $r) {
    $started = $false
    $sec = $null
    $d = @()
    foreach ($c in $lines) {
        if (-not $started) {
            if ($c -like 'You are here*') { $started = $true }
            continue
        }
        if (-not $r['table'] -and $c -match '(?i)Database table\s+([A-Z0-9_]+)') {
            $r['table'] = $matches[1]
            $sec = 'preface'
            continue
        }
        if ($c -match '(?i)^Table Group:\s*(.+)$') {
            $r['domain'] = $matches[1].Trim()
            continue
        }
        if ($c -match '(?i)^Sub-Table Group:\s*(.+)$') {
            $r['category'] = $matches[1].Trim()
            $sec = 'desc'
            continue
        }
        if ($c -like 'Fields on*' -or $c -like 'List of fields*') { $sec = $null; continue }
        if ($c -like 'See also*'  -or $c -like 'Give feedback*')  { $sec = $null; continue }
        $bd = Get-BuildDate $c
        if ($bd) { $r['build_date'] = $bd; break }
        if ($sec -eq 'desc' -and $c -and $c.Length -gt 5 -and $c -notmatch '^[A-Z0-9_]{3,}$') {
            $d += $c
        }
    }
    if ($d) { $r['description'] = ($d -join ' ') }
}

function Parse-Generic ($lines, $r) {
    $started = $false
    $textStarted = $false
    $d = @()
    foreach ($c in $lines) {
        if (-not $started) {
            if ($c -like 'You are here*') { $started = $true }
            continue
        }
        $bd = Get-BuildDate $c
        if ($bd) { $r['build_date'] = $bd; break }
        if ($c -like 'Give feedback*') { break }
        if ($c -like 'See also*')      { break }
        if ($textStarted -and $c.Length -gt 20) {
            $d += $c
            if ($d.Count -ge 10) { break }
        }
        if ($c -match '^\w' -and $c.Length -gt 10) { $textStarted = $true }
    }
    if ($d) { $r['description'] = ($d -join ' ') }
}
