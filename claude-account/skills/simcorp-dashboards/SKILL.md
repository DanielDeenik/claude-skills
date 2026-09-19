---
name: simcorp-dashboards
description: >
  Design SimCorp Dimension dashboards that monitor an operations area, and write the spec sheet a
  desk builds from. Covers the dashboard object chain (layout, page collection, canvas, tile, widget,
  widget configuration), the five display types, filters, conditional formatting, time dependency
  fields for ageing, record permissions, the services and batch jobs each widget family needs before
  it shows anything, the widget catalogue per Add menu category, and the alert path through Business
  Rules Manager and the Alerts Inbox. Carries a monitoring pack per area for cash transfers, FX
  trades, options, futures, security transfers, mutual fund trades, corporate actions, post trade
  compliance, real estate redemptions, swaps and crystallizations, the STP transaction window, and
  Onex redemptions. Use when asked to build, spec, review or troubleshoot a SimCorp dashboard, a
  canvas, a widget, a monitoring view, an STP monitor, an alerts inbox rule, or when a widget shows
  no data.
---

# SimCorp Dashboards

This skill produces one deliverable: a dashboard spec sheet for one desk and one monitoring area,
grounded in sources and honest about what is not yet known. It does not click through the build for
the user and it never invents a widget, a field or a setup name.

## Rule 1. The grounding contract

Every line of a spec carries one of three source tags, and nothing may be written without one.

1. `[MANUAL]` for the SimCorp Dashboards user manual, September 2025, local at
   `ii. Manuals & Documentation/PDFs/dashb.pdf`, cited by section number. This is the only
   authority on how dashboards behave.
2. `[ENV]` for a screenshot or config export from the client install, cited by date and
   environment. Widget availability differs from the manual, so the install always wins on the
   question of what exists.
3. `[MEMORY]` for a settled client fact already recorded in project memory, cited by memory file.

Anything else goes into the GAP block at the end of the spec, numbered, each line naming the exact
evidence that would close it. Never fill a gap by reasoning from plausibility. The Add menu carries
categories the manual does not document at all, so a plausible widget name is very often wrong.

## Rule 2. The object chain, and permissions only narrow

Layout holds dashboards. A dashboard shows one canvas at a time, or a page collection when several
canvases act as pages. A canvas is a grid of tiles. One widget sits on one tile and can be resized
across several. A widget is a widget data source plus a widget configuration plus a UI type.
[MANUAL 2.1, 3.3, 3.4, 14]

Record permissions exist on layout, page collection, canvas and widget. A lower element can never
carry wider rights than the element around it, so canvas rights of view only make widget update
rights inert. Data authorisation sits underneath all of it: an unauthorised portfolio is simply not
in the widget, and where a service supplies the data the service user needs the read access too.
[MANUAL 2.1, 3.7.1, 3.7.2]

Consequence for a spec: name the owning authorisation profile for every canvas and widget, and say
which profile is owner. A canvas that nobody owns cannot be permissioned later.

## Rule 3. Data source sets the population, display type sets the lens

The four monitoring lenses map onto display types as follows.

| Lens | Display type | Mechanism |
| --- | --- | --- |
| Exceptions only | Table, or Group with one group per exception | filter in the widget, `The rest` column shows what fell outside every group [MANUAL 3.6.3.4] |
| Lifecycle status | Group, or Group Matrix with status on one axis | Insert Group with Filter Properties per status [MANUAL 3.6.3.5] |
| Ageing and SLA | Group Matrix with a time dependency field on the horizontal axis | Time to deadline, days to settlement date or minutes to custodian cut off time; Time from, minutes since creation or days since trade date [MANUAL 3.6.7] |
| Volumes and trend | Chart, with the number of periods configured | Chart Editor, Add view for the chart type, Drill Down from the chart [MANUAL 3.6.3.1] |

Two traps live here. First, a filter applies only to the main section of a widget, never to the
drill down data underneath it. [MANUAL 3.6.5] Second, grouping by a reference date is only
meaningful when every instrument in scope shares a calendar convention, otherwise items land in
`The rest` and read as clean. [MANUAL 3.6.7]

Conditional formatting is set per field, on the Conditional Format tab of Field Properties, and is
what turns a status column into something a desk can scan. [MANUAL 3.6.6]

## Rule 4. A widget with no service behind it is an empty widget

Before specifying a widget, name what must be running. This is the first thing to check when a
desk reports a blank tile.

| Widget family | What must run first |
| --- | --- |
| Trade Processing | one job per data source in the Trade Processing Dashboard Service Configuration window, Transactions, STP, Match, CTM, SWIFT or Netting, polling around five seconds [MANUAL 5.2] |
| Trade Processing alerts | the trade processing alert service plus the alert email service, with rules enabled in Business Rules Manager [MANUAL 5.3, 6.1] |
| Cash Management | one batch job per setup, batch task Cash Management Execute Save Results with the setup in the CM setup field [MANUAL 8.1] |
| Fund and Portfolio STP | the fund or portfolio STP service, and execution time alerts configured before the Average Execution Time widget means anything [MANUAL 9, 9.1] |
| Middle Office | a Middle Office data source pointing at a Risk Measurement or a Performance Report, and for a performance report the Top down calculation only check box [MANUAL 10.1] |
| Compliance | dashboard statistics refreshed in Compliance Manager [MANUAL 12] |

The server does not prepare data for a canvas that was never saved, so the canvas must be saved
before the service can populate it. [MANUAL 5.2]

## Rule 5. Size the widget or it will be slow

Keep most widgets under 2,000 records and let at most one reach 10,000. [MANUAL 5.9] Do the
filtering in the underlying transaction status setup rather than in the widget, because the widget
still carries every record it was given. [MANUAL 5.1] On the Trade Processing Dashboard and Alerts
tab of Interface Options, set Disregard data older than a low number of days, seven in production,
and understand that Minutes between verification of data defaults to 60 and treats anything lower
as 60: volatile changes such as a status change appear at once, static changes such as a renamed
counterparty only at the next verification or reload. [MANUAL 5.4]

## Rule 6. Exceptions that must chase someone belong in the alert path

A widget shows a queue. It does not chase anybody. When the area needs escalation, specify an
alert generation rule in Business Rules Manager against the same setup, with Create after and
Create per, in Simulation first so the volume is known before it is enabled, then the alert rules
for automatic email, due date or assignment, and the Alerts Inbox filter folder the desk works
from. An alert runs Not Started with sub status New, then In Progress with sub status Resolved for
24 hours, then Finished with sub status Closed by System if the cause does not return, or In
Progress with sub status Recurring if it does. A rule cannot be disabled while its alerts are
open. [MANUAL 6, 6.1.1, 6.1.2, 6.2] The Alerts Inbox Summary widget reports on the alerts
themselves and drills back into the inbox. [MANUAL 7]

## How to produce a spec

1. Read project memory for the area and for the client, and read `references/area-specs.md`.
2. Confirm the desk that owns the area and the environment the dashboard is for. Roles only, never
   individual names on a deliverable.
3. Pick the widget data source from `references/widget-catalogue.md`. If the area has no confirmed
   data source in that install, stop and ask for a screenshot of the Add submenu rather than
   guessing a name.
4. Choose one lens per widget from Rule 3 and keep the canvas to the fewest widgets that answer the
   desk's first question of the day.
5. Write the spec on the template in `references/spec-template.md`.
6. State the services, batch jobs and setups from Rule 4 as prerequisites, in build order.
7. State the record permissions and the owning authorisation profile per element.
8. Close with the numbered GAP block. Then validate against `references/widget-mechanics.md` before
   handing it over.

## Scope boundary

This skill owns the dashboard layer only. Reconciliation break handling belongs to
`simcorp-recon-breaks`, front office flow architecture to `simcorp-fo-flow-architect`, message and
port behaviour to `simcorp-comm-server`, extraction and reporting to `simcorp-extraction`. When an
area's underlying process is in question rather than its monitoring view, hand off to the sister
skill and use its answer as the population definition.
