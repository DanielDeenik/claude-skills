# Widget catalogue by Add menu category

Source tags: `[MANUAL]` is the SimCorp Dashboards user manual, September 2025, cited by section.
`[ENV]` is a screenshot of the client install. `[GAP]` means nothing authoritative has been read.

House style note: the manual separates a category from a widget name with a long dash, for example
in the System Operation widget names. Names are written here with a plain hyphen. Keep the manual
spelling when typing a name into the product.

## Environment capture log

| Capture | Date | Environment | Version | What it proves |
| --- | --- | --- | --- | --- |
| Dashboard ribbon and Add menu, Trade Processing submenu open | 25 August 2026 | NOT TAGGED, ask before reuse | NOT TAGGED | the twelve Add categories and the five Trade Processing entries in this install |

Every later capture gets a row. A catalogue line without a capture behind it is a gap, not a fact.

## The Add menu categories

Twelve categories in this install, in menu order. [ENV 25-Aug-2026]

Common, Asset Manager, General Reconciliation, Trading, Compliance, Middle Office, Trade
Processing, Corporate Actions, Cash Management, Fund/Portfolio STP, Data Warehouse, System
Operation.

The manual documents seven widget families and never lists the Add menu. Five categories in this
install therefore have no documented widget list at all: Common, General Reconciliation, Corporate
Actions, Data Warehouse, and the widget names inside Compliance.

## Trade Processing

Confirmed in this install, verbatim from the open submenu: Transaction Status, STP Transaction
Monitor, Central Trade Manager, Match, Trade Control. [ENV 25-Aug-2026]

Documented data sources in the manual: Transaction Status, STP Transaction Monitor, Match, Central
Trade Manager, SWIFT Status, Netting Manager. [MANUAL 5]

Two differences that matter and must never be smoothed over. Trade Control appears in the install
and in no section of the manual. SWIFT Status and Netting Manager are documented but do not appear
in this install's submenu. Treat the install as the authority on availability and the manual as the
authority on behaviour.

| Data source | What it monitors | Service required |
| --- | --- | --- |
| Transaction Status | transaction status across a chosen setup, groupable by any selected field such as transaction business code [MANUAL 5.9] | Trade processing dashboard Transactions service [MANUAL 5.2] |
| STP Transaction Monitor | progress and condition of transactions through STP and the underlying auxiliary status jobs [MANUAL 5.7] | Trade processing dashboard STP service |
| Match | match status of transactions against incoming confirmations, manual match from the widget [MANUAL 5.6] | Trade processing dashboard Match service |
| Central Trade Manager | matched, unmatched and cancelled trade status against the broker or dealer, messages carried by the communication server [MANUAL 5.10] | Trade processing dashboard CTM service |
| SWIFT Status | SWIFT ACK and NAK status by message type [MANUAL 5.11] | Trade processing dashboard SWIFT service |
| Netting Manager | netting status of payments and securities, for example Ready for netting [MANUAL 5.8] | Trade processing dashboard Netting service |
| Trade Control | GAP, purpose and fields unknown | GAP |

Field naming inside these widgets is deliberately not identical to the underlying window, a few
window fields are unavailable, a few widget fields have no window behind them and so cannot drill
down, and a missing date shows as 01-01-0001. Amount fields sum only within one currency.
[MANUAL 5.5]

## System Operation

Documented widgets: System Operation Central Selection window, System Operation SRM which is
System Runtime Measurements, System Operation Batch Job Group History, System Operation Queues,
System Operation Calculation Queues. [MANUAL 4]

Calculation Queues needs no configuration, runs on server time, aggregates workload in five minute
sequences with live input every minute on a rolling 24 hour scale, job chunks on the left and
services on the right. [MANUAL 4.1]

Not yet confirmed against the install. [GAP 1]

## Fund/Portfolio STP

Documented widgets: Average Execution Time, Figures, Holidays, Open Alerts, STP Jobs, STP Queues.
[MANUAL 9]

Average Execution Time reads the Avg. exec. time field of the Fund/Portfolio STP Average Execution
Times window and needs execution time alerts configured first. Figures aggregates the Fund Figure
Viewer and can show any fund figure line, for example subscription and redemption amounts or total
net asset value. Holidays counts funds that cannot calculate a NAV because of a bank holiday and
is meaningless on a portfolio dashboard. Open Alerts breaks open alert tasks down by alert type,
assigned user and acknowledgement status and opens the Alerts Inbox applet. STP Jobs shows
workflow progress by calculation event type with drill down to individual events. STP Queues shows
finished against unfinished jobs per fund or portfolio setup and can open the Process Monitor or
Queue Details applets. [MANUAL 9.1 to 9.6]

Particularly relevant in Fund Administration Manager, Portfolio Administration Manager, Portfolio
Group Administration Manager and Calculation Segment Administration Manager. [MANUAL 9]

## Cash Management

One documented widget, Cash Management, presenting cash forecast data for bank accounts and cash
buckets with drill down through View in Cash Management or View in New Cash Management.
[MANUAL 8, 8.3.2]

Two documented shapes. A statement style view for opening balance, movements and closing balance
across a term structure of future dates, built as a Group Matrix with column groups on reference
dates and row groups on a condition such as instrument type. A pivot for currency exposure, with
Bank account ID as row fields and Booking date as column fields. [MANUAL 8.3.1, 8.3.2]

Whether amounts show in portfolio or reporting currency is decided by the Amount in PC check box
on the underlying Settings Cash Management window, not in the widget. [MANUAL 8.3.1]

## Middle Office

Documented widgets, each fed by a Middle Office data source over a Risk Measurement or a
Performance Report: tree node simple single date, tree node single date, tree node top and bottom
single date, tree node chart single date, tree node chart time series, tree node table time
series, tree node chart scenarios distribution, tree node table scenarios distribution.
[MANUAL 10, 10.3 to 10.10]

Configuration parameters and which of them apply per widget type are tabulated in the manual.
Maximum drill down depth applies only to the tree node widget and defaults to 1. Show top or
bottom, number of tops and bottoms and analytics for top and bottom apply only to the top and
bottom widget. Data frequency applies only to time series and only over a Risk Measurement.
[MANUAL 10.2]

## Trading

Documented widgets on the Order Manager dashboard: Broker Routing, Commission Tracking, Strategy
Routing. [MANUAL 13]

Broker Routing shows orders routed per broker as group, pivot or chart, opens the dealer window
through Open Transaction on a row, and shows routing pattern over time when the number of periods
is configured. Commission Tracking covers equities and exchange traded futures and options,
accounts for step outs and commission sharing agreements, and can be restricted with Show
commissions with targets only. Strategy Routing shows orders carrying a given strategy with drill
down to the individual transactions. [MANUAL 13.1 to 13.3]

The install has a tab named Commission Tracking 1 beside Dashboard1, so at least this widget family
is in use here. [ENV 25-Aug-2026]

## Asset Manager

Documented widgets: Asset Manager Exposure, Asset Manager Top N Holdings, Asset Manager
Outstanding Orders, and Browser host for permitted web content such as a Qlik report. The Asset
Manager dashboard is also stated to carry portfolio post trade compliance and to accept widgets
from other dashboards. [MANUAL 11, 11.1, 11.2]

Browser host is restricted by the Browser Host Widget Trusted and Denied Off-Sites window and only
trusted URLs render. URLs accept variables including Security ID, ISIN, CUSIP and security group
codes prefixed SGC. Show in AM browser from the Portfolio Sheet needs both Browser host and Central
Selection widgets on the same dashboard. [MANUAL 11.2]

## Compliance

The category exists in the install and the manual confirms Compliance Manager has a configurable
dashboard whose widgets are added from the Compliance submenu and are filtered by user profile
authorisation, but it lists no widget names. Refresh of dashboard statistics is described in the
Compliance Manager user manual, not here. [MANUAL 12] [ENV 25-Aug-2026]

Widget names: [GAP 2].

## Common, General Reconciliation, Corporate Actions, Data Warehouse

Present in the install Add menu and absent from the manual. Nothing may be written about their
widgets until a screenshot of each submenu exists. [ENV 25-Aug-2026] [GAP 3, 4, 5, 6]

Alerts Inbox Summary is worth noting here because it is not a category but a value in the Type
field of the widget configuration window. [MANUAL 7]

## Open gaps

1. System Operation submenu not confirmed against the install.
2. Compliance submenu widget names.
3. Common submenu widget names.
4. General Reconciliation submenu widget names.
5. Corporate Actions submenu widget names.
6. Data Warehouse submenu widget names.
7. Trade Control widget purpose, fields and service, undocumented in the manual.
8. Environment and version of the 25 August 2026 capture.

Each closes with one screenshot of the open submenu, or for gap 7 the window behind the widget.
