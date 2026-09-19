# New Issues Workflow (BOOM) — Screenshot Placement Manifest

Source: `New issues workflow BOOM.docx` (client procedure doc).
Purpose: tells you exactly which extracted screenshot goes at which step when you
build the SharePoint FAQ page.

- **Recoverable screenshots:** 8 PNGs, extracted to `New_issues_workflow_BOOM_assets/`.
- **Not recoverable:** 3 Bloomberg email-embedded (CID) images — references only, no
  file inside the doc. These must be **re-captured** by hand (see the second table).
- File naming: `NN_<slug>.png`, numbered in document reading order.

---

## Table A — Recoverable screenshots (upload these)

| # | Step in the workflow | Screenshot file to insert here |
|---|----------------------|--------------------------------|
| 1 | **Create a shell for the new issue** — Open a new simulation tab and add the additional "New Issue" columns. | `01_open-new-simulation-tab-and-make-sure-you-add-th.png` |
| 2 | Click "Save New Issue" to create the shell (after choosing a similar existing security to clone, inputting its ISIN under "New Issue – Existing Security ID", and naming the shell under "New Issue – Security ID"). | `02_click-on-save-new-issue-to-create-the-shell.png` |
| 3 | Once the simulation is created, make sure the **"Primary Market" box is ticked** before releasing the trade to Order Manager. | `03_once-the-simulation-is-created-make-sure-primary.png` |
| 4 | **Route to Order Manager** → Accept the trade → right-click the VCON → "Match". In the "Match" window, click **Request** to pull security details from Bloomberg (any identifier in the dropdown). | `04_in-the-match-window-click-on-request-to-pull-the.png` |
| 5 | Once security details are pulled from Bloomberg, click **"Validate"** (validates security parameters against compliance rules), then "Match and Allocate". | `05_once-security-details-is-pulled-from-bloomberg-c.png` |
| 6 | **Access to BOOM in UAT / BETA** — `BOOM <go>` on Bloomberg. | `06_boom-go.png` |
| 7 | Trade ticket (opened from clicking a rate / yellow field in BOOM; hit Submit). | `07_trade-ticket.png` |
| 8 | Run `BLOT <go>` to see the ticket in your blotter; click into it to see details of the trade that flows to SimCorp. | `08_run-blot-to-see-ticket-in-your-blotter-you-can-c.png` |

---

## Table B — CID / Bloomberg email-embedded images (NOT in the file — re-capture)

The doc's author pasted three images straight from a Bloomberg email. Word stored
these as `cid:` **links to the email**, not as embedded files, so there is nothing to
extract — they show as broken/blank in the .docx. They live in the last section
(the BOOM/BLOT UAT walkthrough), each sitting immediately after its recoverable
screenshot above.

| Step it belongs to | CID reference (source only) | Action |
|--------------------|-----------------------------|--------|
| `BOOM <go>` (same step as image 06) | `cid:img_68F93CE9000109860C430001_3@bloomberg.net` | Re-capture the BOOM screen |
| `Trade ticket` (same step as image 07) | `cid:img_68F93CE9000109860C430001_5@bloomberg.net` | Re-capture the trade ticket |
| `Run BLOT to see ticket in your blotter` (same step as image 08) | `cid:img_68F93CE9000109860C430001_6@bloomberg.net` | Re-capture the BLOT blotter |

Note: each CID image is a **duplicate/companion** of the recoverable screenshot at
the same step (6/7/8). The embedded PNGs (06–08) are intact, so you likely already
have a usable image for each of these steps — the CID versions can be ignored unless
you specifically want the Bloomberg-email variant.

---

## Insert markers (paste into the FAQ body)

Drop these markers into the SharePoint page text so each screenshot lands at the
right step:

- After step 1 text → `[[IMAGE: 01_open-new-simulation-tab-and-make-sure-you-add-th.png]]`
- After step 2 text → `[[IMAGE: 02_click-on-save-new-issue-to-create-the-shell.png]]`
- After step 3 text → `[[IMAGE: 03_once-the-simulation-is-created-make-sure-primary.png]]`
- After step 4 text → `[[IMAGE: 04_in-the-match-window-click-on-request-to-pull-the.png]]`
- After step 5 text → `[[IMAGE: 05_once-security-details-is-pulled-from-bloomberg-c.png]]`
- After `BOOM <go>` → `[[IMAGE: 06_boom-go.png]]`
- After `Trade ticket` → `[[IMAGE: 07_trade-ticket.png]]`
- After `Run BLOT ...` → `[[IMAGE: 08_run-blot-to-see-ticket-in-your-blotter-you-can-c.png]]`

## Open items to confirm (wording drift — do not silently "correct")

- Client says **"Primary Market" box/tick** (step 3). Confirm this against the
  live screen label before publishing — in the SimCorp Asset Manager UI this
  control is often labelled differently. Preserve the client's word until confirmed.
- `New Issue – Existing Security ID` and `New Issue – Security ID` field names are
  taken verbatim from the client doc — confirm against the actual simulation columns.
