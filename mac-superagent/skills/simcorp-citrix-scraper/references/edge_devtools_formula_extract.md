# Edge DevTools — Extract Formula URL List

The MadCap sidebar is JavaScript-rendered. `Invoke-WebRequest` can't see it,
neither can IE COM (the tree builder fails to populate). Edge DevTools IS the
working path because Edge renders the page fully.

This produces `$env:USERPROFILE\Downloads\formulas.txt` containing one URL per
line, which `scripts/11_formulas_from_file.ps1` then consumes.

## Step 1 — open a formula page in Edge

```
https://help.simcorpcloud.com/2510/en/Content/Formulas/FormulaFunction-execrefdate.htm
```

Any formula URL works — the sidebar is the same.

## Step 2 — wait for sidebar to render

Look at the left side of the Edge window. You should see an alphabetical list
of formula names: `abs`, `add`, `addbusinessdays`, ... If you don't see them,
wait 5-10 seconds or scroll the sidebar once to force render.

## Step 3 — unlock DevTools paste

Press **F12** to open DevTools, click **Console** tab. The first time per
session, Edge blocks pasting code as anti-XSS protection. **Type these two
words literally** (do not paste them):

```
allow pasting
```

Press Enter. The yellow warning disappears.

## Step 4 — run the URL extractor

Paste this snippet:

```javascript
(()=>{
  let u = [...document.querySelectorAll('a[href*="FormulaFunction"]')]
    .map(a => a.href.replace(/[?#].*$/,''))
    .filter((v,i,a) => a.indexOf(v) === i)
    .sort();
  console.log("Found " + u.length + " formula URLs");
  if (u.length === 0) { console.warn("Zero URLs — sidebar not loaded. Wait, scroll sidebar, re-run."); return; }
  let blob = new Blob([u.join('\n')], {type:'text/plain'});
  let a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'formulas.txt';
  document.body.appendChild(a);
  a.click();
  a.remove();
  console.log("Saved formulas.txt to Downloads");
})();
```

Expected console output:

```
Found 435 formula URLs
Saved formulas.txt to Downloads
```

The exact count varies by SimCorp Dimension version. 2510 had 435.

## Step 5 — confirm file exists

In Citrix Explorer or File menu, navigate to:

```
C:\Users\<yourname>\Downloads\formulas.txt
```

Should be 30-50 KB depending on URL count.

## Step 6 — run the PowerShell scraper

`scripts/11_formulas_from_file.ps1` reads that file and scrapes each URL.
Paste into ISE Script Pane → F5.

## Why this works when other approaches fail

| Approach | Result | Why |
|---|---|---|
| BFS crawl via `Invoke-WebRequest` | 0 URLs found | Sidebar entirely JS-rendered, not in HTML source |
| IE COM with `Document.documentElement.outerHTML` | 0 URLs found | MadCap's tree builder uses AJAX after readyState=4; outerHTML captures pre-AJAX state |
| Brute-force alphabetic URL probing | Slow + missing names | 26-letter × probable-name combinations is millions of probes; misses hard-to-guess names like `sdcloggetvalue` |
| Edge DevTools `document.querySelectorAll` | All URLs found ✓ | Edge has already rendered the full DOM by the time we run this; we just read the result |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Found 0 formula URLs` | Wait longer; scroll the sidebar to force render; re-run snippet |
| DevTools blocks paste | Type `allow pasting` + Enter |
| `formulas.txt` doesn't appear in Downloads | Edge may have prompted "Save As" — accept; or check default download location |
| PS script says "URL file not found" | Verify `$env:USERPROFILE\Downloads\formulas.txt` exists; default Edge download dir might differ |
