# Cookie Capture (only if preflight returns 401/403)

The validation run on 2510 worked with `-UseDefaultCredentials` (Windows /
Kerberos auth passed through). But if the user's tenant gates the help portal
behind a different SSO scheme (Okta / Azure AD with cookie-based session),
they may need to capture cookies from Edge.

## Step 1 — confirm Edge has a live session

In the Citrix Edge tab, navigate to `https://help.simcorpcloud.com/2510/en/`.
The page should load fully. If it redirects to a login screen, complete SSO
first.

## Step 2 — capture cookies via F12 DevTools

1. Press **F12** in Edge
2. **Application** tab → **Cookies** → `https://help.simcorpcloud.com`
3. Copy the **Name** and **Value** of every cookie. Especially anything ending
   in `Auth`, `Session`, `JSESSIONID`, `AAD`, `MSAL`, `OKTA`.

## Step 3 — inject cookies into PowerShell session

In the ISE console pane:

```powershell
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

# Repeat this block for each cookie copied from DevTools
$c = New-Object System.Net.Cookie
$c.Name   = 'PASTE_COOKIE_NAME_HERE'
$c.Value  = 'PASTE_COOKIE_VALUE_HERE'
$c.Path   = '/'
$c.Domain = 'help.simcorpcloud.com'
$session.Cookies.Add($c)
```

## Step 4 — patch the production script

In Block 1, modify `Get-Page` to include the WebSession:

```powershell
function Get-Page ($url) {
    Invoke-WebRequest -Uri $url `
        -UseBasicParsing `
        -UseDefaultCredentials `
        -WebSession $script:helpSession `
        -TimeoutSec $TimeoutSec `
        -UserAgent 'SimCorpExtract/1.0'
}
```

And before Phase 1 starts:

```powershell
$script:helpSession = $session   # use the $session captured above
```

## Step 5 — re-verify with preflight

Re-run `scripts/00_preflight.ps1` after injecting cookies. Should return
HTTP 200 with body length > 100 KB.

## Cookies expire — capture again as needed

SSO cookies typically live 8-24 hours. If the script starts returning 401s
mid-run, re-capture and re-inject.
