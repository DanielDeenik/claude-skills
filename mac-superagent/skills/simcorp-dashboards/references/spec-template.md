# Dashboard spec sheet template

One spec covers one desk and one monitoring area. Fill every field or mark it TO BE NAMED and add
it to the gap block. Roles and teams only, never individual names.

---

## 1. Header

| Field | Value |
| --- | --- |
| Area | |
| Owning desk | |
| Manager application | the application the dashboard applet lives in |
| Environment | install and version this spec is written against |
| Author and date | |
| Sources used | manual sections, captures by date, memory files |

## 2. What the desk asks first thing in the morning

One or two sentences in the desk's own words. If this cannot be written, the spec is premature and
the answer is an interview, not a canvas. Every widget below has to earn its tile against this
sentence.

## 3. Population

| Field | Value |
| --- | --- |
| Business definition | what counts as an item in this area |
| Underlying window | |
| Setup name | the named selection of fields and transaction data, or TO BE NAMED |
| Filter applied inside the setup | keeps the widget small, since the widget carries every record it is given |
| Expected record count | target under 2,000 |
| Exclusions | what deliberately does not appear, and why |

## 4. Canvas layout

Tile grid size, and one row per widget.

| Tile | Widget title | Data source | UI type | Lens | Records |
| --- | --- | --- | --- | --- | --- |
| | | | | exceptions, lifecycle, ageing or trend | |

Keep the widget count low. Start up time degrades with many tabs and many widgets per canvas, and
several manager installations open at once with heavy canvases can fail on memory.

## 5. Per widget detail

Repeat this block for each widget.

**Title.** As it appears in the widget header.

**Data source and UI type.** From the catalogue, with the source tag that proves the widget exists
in this install.

**Fields shown.** Main section fields in display order. Note any field whose widget name differs
from the underlying window name, and any field that cannot drill down because it has no window
behind it.

**Grouping.** For Group, the groups in order and the Filter Properties behind each. For Group
Matrix, both axes. State whether The rest is always shown, whether the All row or column is shown,
and whether Count unique on transaction number is set.

**Filter.** The widget filter, in words and as the field, operator and value list. State plainly
that it does not reach the drill down data.

**Conditional formatting.** Field, condition, colour, and what the colour means to the desk.

**Time dependency.** Which of the four measures is used: days to settlement date, minutes to
custodian cut off time, minutes since creation, days since trade date. Confirm the calendar
convention is uniform across the population, or record the risk that items land in The rest and
read as clean.

**Refresh.** Minutes before becoming obsolete for a group or matrix widget, and how that sits
against the service polling interval and the verification interval.

**Drill path.** What a right click gives the desk, and which window it lands in.

## 6. Prerequisites, in build order

| Step | Object | Where | Done |
| --- | --- | --- | --- |
| 1 | setup in the underlying window | | |
| 2 | service or batch job for this data source | | |
| 3 | interface options for trade processing widgets | | |
| 4 | canvas created and saved, because the server does not prepare data for an unsaved canvas | | |
| 5 | widgets added and configured | | |
| 6 | permissions | | |

## 7. Permissions

| Element | Owner profile | Profiles with view | Profiles with update | Profiles with delete |
| --- | --- | --- | --- | --- |
| layout | | | | |
| page collection | | | | |
| canvas | | | | |
| each widget | | | | |

Rights never widen going inward, so check that the canvas rights do not make the widget rights
inert. Add the data authorisation note: the service user needs read access to everything the
widget is supposed to show, or the tile is quietly incomplete rather than empty.

## 8. Alerts, only where an item must chase somebody

| Field | Value |
| --- | --- |
| Alert generation rule name | |
| Rule type and setup | |
| Condition | |
| Create after, Create per | |
| Workflow task | must match the alert generation type |
| Simulation first | yes, always, with the simulated count recorded here |
| Alert rules | automatic email, due date or assign, with recipients as groups |
| Inbox folder and filter | the folder the desk actually works from |
| Closure expectation | resolved for 24 hours, then closed by system if the cause does not recur |

## 9. How this is proved before handover

State the evidence, not the intention. Record counts against the underlying window for the same
setup and date. One known exception traced from the widget through the drill path to the window.
One item aged past the threshold appearing in the right column. A screenshot of the built canvas.
Whoever signs it off is named by role.

## 10. Gap block

Numbered, each line naming the exact evidence that closes it and who holds it. A spec ships with
gaps. It does not ship with guesses.

---

# Worked fragment, from the install capture of 25 August 2026

This is not a full spec. It is what a capture yields before any interview, and it shows the level
of grounding the header table expects.

Observed on the canvas named Dashboard1, with a second tab named Commission Tracking 1.
[ENV 25-Aug-2026]

| Widget title as shown | What the capture proves | What it does not prove |
| --- | --- | --- |
| FUND ACCOUNTING - TRANSACTION STP ERRORS | a stacked bar, x axis message queue with TP_STP, series by transaction type showing ABS, ALM and FX forward, y axis transaction number, with a Stacked Bar Default and a Stacked Bar view button | the data source, the setup, the filter, the refresh interval |
| CONTROL BY PAYMENT DATE | a pivot with Grand Total and empty Drop Column Fields and Drop Data Items zones | everything else, the widget was mid configuration |
| ACTIVE TRANSACTIONS - PAYMENT RECONCILIED NOT SETTLED | a table whose columns are Transaction no., Portfolio, Security ID, Nominal, Quotation currency, Price, Payment amount QC, Trade date, Payment date, with a header filter icon present | the setup behind it, and whether the exception is expressed in the setup or in the widget filter |

Two facts worth carrying forward from the same capture. The ribbon in this install groups as EDIT,
CANVAS, PRINT, DATA, CANVAS SIZE, WIDGET PLACEMENT, WIDGET DETAILS and EXTRA WIDGET DETAILS, which
does not match the manual's ribbon wording, so click paths are written from the install and not
from the manual. The status bar shows a layout named My Layout and a state named Initial, which is
the layout layer of the object chain and belongs in the header table of any spec written for this
environment.
