---
name: simcorp-am-excel-export
description: "Export a SimCorp Dimension Asset Manager layout to Excel for a chosen as-at date, and turn the exported text file into a clean workbook. Use for pulling positions out of Asset Manager, an export that lands as .txt, an empty grid after Load, or trailing junk columns in the sheet."
---

# Asset Manager export to Excel

Pull the contents of an Asset Manager layout out of SimCorp Dimension for a stated as-at date and deliver it as a clean Excel workbook. Grounded in the Nicola Wealth PROD environment, Dimension 26.04, reached through the Citrix HTML5 client. Screenshots of the live environment are the source of truth for client specific layout and column names.

## Parameters, never hardcoded

Establish all five before touching the system. Ask when any is missing rather than assuming the last run's value.

| Parameter | Example | Notes |
|---|---|---|
| Layout | Private Debt | The saved Asset Manager layout, listed with its owning team in the Select layout dialog |
| Date mode | Fixed | Today follows the system date, Fixed pins the analysis to one day |
| As-at date | 31 August 2026 | The environment displays and accepts US order, so 8/31/2026 |
| Data selection | Private Debt All | The node selected in the Data Selector tree, or a Quick selection portfolio or portfolio group |
| Output name | Private Debt 31082026 | House convention is layout name then the date as ddmmyyyy |

## What the export actually produces

The Export button writes a tab delimited text file, not a workbook. The Save as type box in SimCorp's save dialog reads Text file (\*.txt) and that is correct at that step. Excel then opens the text file and shows a POSSIBLE DATA LOSS bar. Anyone who presses Save at that point keeps a text file with an xlsx sounding name. The conversion to a real workbook is a separate, deliberate step.

## Click path in Dimension

1. Launch Dimension from the PROD shortcuts folder, shortcut PRODscd - 4_GB. The splash names the version and the environment, so read it and confirm PROD before continuing.
2. From the portal home, open Asset Manager under Solutions.
3. Home ribbon, DATA group, Open with F5 for the full Select layout dialog, or Open Recent for the numbered short list. Pick the layout.
4. Home ribbon, ANALYSIS group. Set the date mode dropdown to Fixed, then set the date field to the as-at date.
5. Press Load in the same group. Every tab and the Data Selector re-title with that date, which is the confirmation that the date took effect.
6. Open the POSITIONS contextual ribbon tab. The Export button sits in the EXCEL group, next to Import. It is not on the HOME tab.
7. In Select file to save data, set the file name and press Save. Leave the type as Text file.

## The empty grid rule

A Load that returns zero rows means no positions are stored for that date, not a broken layout and not a permissions problem. Month ends carry data reliably; intermediate dates and future dates often do not. Before reporting an empty result, reload on the previous month end and compare. State the date that worked.

## Convert the file rather than editing it by hand

Deleting the trailing columns in Excel and then choosing Save As with the type switched to Excel Workbook works, but it is manual, silent about mistakes, and the deleted range moves whenever the layout changes. Prefer a scripted conversion once the file is reachable.

When the file is on the user's machine in a connected folder, convert it in place with device_bash. When it is only inside the Citrix session, it has to be brought over first with the Citrix toolbar File transfer, then Download.

Conversion rules, in order:

1. Read as tab delimited, UTF-16 or UTF-8 as the file dictates, keeping all values as text so identifiers do not become numbers or dates.
2. Drop every column that is entirely empty across all rows.
3. Drop the trailing provenance block, the columns carrying the Dimension version and module string and the Export Key.
4. Keep everything the layout displays, including columns that are legitimately all zero, unless the caller names a keep list or drop list.
5. Write xlsx with a frozen header row, an autofilter across the header, and the sheet named for the layout and date.
6. Report the row count and the columns dropped by name so the trim is auditable.

Never guess a drop range by column letter. Column letters shift with the layout.

## Verification before handing it over

Row count in the workbook matches the record count shown in the Dimension grid. The as-at date in the file name matches the date the tabs re-titled with. One known position reconciles on a value column. Say which three checks passed.

## Automation boundary

Computer use grants browsers read only access, so the Citrix session cannot be clicked by Claude. Claude guides the in session steps and captures state, and owns everything from the exported file onward. Do not attempt to drive the Citrix canvas by any other route.

## Production discipline

This is PROD. The path above is read only by nature: loading a layout and exporting a grid changes nothing. Do not save a layout, do not create shortcuts, and do not leave test exports in shared folders. Exports belong in the user's own Downloads or the folder named in the request.

## House style for any deliverable built from this

Full sentences. No dashes, arrows, middots or maths glyphs. Roles and teams rather than individual names. Screenshots decide client specific column names.