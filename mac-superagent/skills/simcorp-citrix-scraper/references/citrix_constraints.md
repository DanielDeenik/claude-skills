# Citrix + PowerShell Constraints — Empirical Findings (2026-05-15)

These are NOT theoretical limitations — every entry below was observed during
the validation run with Dan in his NW Citrix session. Read this BEFORE
recommending any approach.

## C1 — Citrix clipboard truncates pastes silently above ~8-12 KB

**Observed:** A 12 KB PowerShell script pasted into Notepad saved as a 0-byte
file. Same script pasted into ISE Script Pane partially loaded — broke
mid-function (`if ($b) {` with no closing brace), producing parser error
`Missing closing '}' in statement block`.

**Rule:** Any individual paste operation must be `< 4 KB` to be safe.

**Mitigation:** Split scripts into multiple paste-blocks. Verify each block's
length with:
```powershell
$psISE.CurrentFile.Editor.Text.Length
```

## C2 — Notepad creates 0-byte files when paste fails

**Observed:** `Test-Path Scrape.ps1` → `True`, but `Get-Item ... | Select Length`
→ `0`. Notepad's Save operation succeeds even with empty content.

**Rule:** Never use Notepad as the script-paste channel in Citrix.

**Mitigation:** Use ISE Script Pane (Ctrl+R if hidden). Paste lands as one
atomic unit; F5 runs immediately without needing a `.ps1` file at all.

## C3 — PowerShell `$var:` is parsed as a scope prefix

**Observed:** `Write-Host "  #$n: $hits hits so far"` failed with
`Variable reference is not valid. ':' was not followed by a valid variable
name character.` Same script with `${n}` or `-f` formatting works.

**Rule:** Avoid `$singleletter:` patterns in any string interpolation.

**Mitigation:**
```powershell
# BAD
Write-Host "#$n: $hits hits"

# GOOD
Write-Host ("#{0}: {1} hits" -f $n, $hits)
```

## C4 — `Invoke-WebRequest -UseDefaultCredentials` works for server-rendered SimCorp pages

**Observed:** First successful fetch of `Content/Tables/Table-1.htm` returned
HTTP 200 with 144,997 bytes of full HTML — all body content present, parseable
by our regex patterns.

**Rule:** For Tables / TableFields / Forms / Views / Commands / Formulas, use
`-UseDefaultCredentials` to pass Windows / Kerberos auth. No cookie capture
needed.

```powershell
Invoke-WebRequest -Uri $url -UseBasicParsing -UseDefaultCredentials -TimeoutSec 30
```

## C5 — EditorListProperties (Tier-1) pages are JS-rendered

**Observed:** `view-source:` for an EditorListProperties URL showed only
`<link>` tags for CSS and a few `.button.*` CSS classes — zero field content.
Content is rendered client-side from `?cshid=...` parameter after page load.

**Rule:** `Invoke-WebRequest` returns the empty shell. Skipping this namespace
in the first-pass extraction is acceptable.

**Mitigation (deferred):** Drive IE COM (`New-Object -ComObject
InternetExplorer.Application`) to render and extract `document.documentElement.outerHTML`.
Slower (~1-2 s per page) but works.

## C6 — TOC discovery fails on 2510

**Observed:** All TOC URL probes returned 404:
- `Data/Tocs/Default.xml`
- `Data/Toc.xml`
- `Data/SearchResources/Cloud/0_Cloud_Chunk0.js`
- `Data/Search/SearchData/Chunks/0_Cloud_Chunk0.js`

**Rule:** Don't rely on MadCap search index for URL discovery on this portal
version. Path layout varies by Flare version.

**Mitigation:** Use numeric URL enumeration with miss-counter early-stop:
```powershell
for ($n = 1; $n -le $MaxId; $n++) {
    $url = "$BaseUrl Content/Tables/Table-$n.htm"
    if (FETCH OK) { hits++; misses = 0 }
    else { misses++ }
    if ($misses -ge 200) { break }   # ID space exhausted
}
```

## C7 — ID space has gaps; 404s are expected and benign

**Observed:** Tables 487, 488, 489, 499, 509 returned 404 — non-existent IDs
between valid ones. 5,743 total 404s logged across the run. All correctly
handled by the miss-counter.

**Rule:** Log 404s but don't surface them as errors. Continue iterating.

## C8 — Run output goes to Documents, NOT Downloads

**Observed:** User looked for output in Downloads, found none. Output was in
`$env:USERPROFILE\Documents\SimCorp_Help_Structured\` — Explorer view was
sorted by date or filter, so subfolder wasn't visible.

**Rule:** Always confirm output location via PowerShell `Get-ChildItem`, not
Explorer view. Explorer can mislead.

**Output canonical path:**
```
C:\Users\<user>\Documents\SimCorp_Help_Structured\
├── SimCorp_Help_Structured.csv     (live-growing)
├── raw\<slug>.htm                  (one file per fetched page)
├── _checkpoint.txt                 (one URL per line)
└── _errors.log                     (HTTP failures incl. 404s)
```

## C9 — Citrix execution-policy warnings are benign

**Observed:** `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
returned warning: "setting is overridden by a policy defined at a more
specific scope ... your shell will retain its current effective execution
policy of Unrestricted."

**Rule:** Unrestricted is MORE permissive than Bypass. Ignore the warning.

## C10 — Citrix's BITS dialog hangs on 404 URLs

**Observed:** When `Invoke-WebRequest` failed and the script fell back to
`Start-BitsTransfer`, BITS popped up a "Connecting…" dialog that hung
indefinitely on 404 URLs.

**Rule:** Don't include BITS fallback for high-volume URL probing. Use plain
IWR and let 404s be 404s.

## Summary cheat-sheet for the next person

1. **Don't** use Notepad. **Do** use ISE Script Pane.
2. **Don't** paste 12 KB at once. **Do** split into 3-4 KB blocks.
3. **Don't** use `$var:` interpolation. **Do** use `-f` format strings.
4. **Don't** scrape EditorListProperties via plain IWR. **Do** defer them.
5. **Don't** discover URLs via TOC. **Do** enumerate numeric IDs.
6. **Don't** use BITS as fallback. **Do** let IWR fail cleanly.
7. **Don't** look in Downloads for live output. **Do** look in Documents.
8. **Don't** run full corpus before PoC validates parsers. **Do** validate
   one page end-to-end first.
