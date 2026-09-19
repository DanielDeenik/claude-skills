# Area monitoring packs, operations side

Six areas: cash transfers, corporate actions, post trade compliance, real estate redemptions, the
STP transaction window, and Onex redemptions with their related buys. Read the shared pattern and
GAP A at the top of `area-specs-trades.md` first; both apply here unchanged.

## Cash transfers

Population signal. There is an unresolved contradiction in the client documents. The scope document
says all cash activity is handled in Archon and imported, while operating model row 18 says cash
transfers are entered in SimCorp. This was carried to the client in August 2026 and has not come
back. [MEMORY project_day1_training_sessions_2026_08_25]

Consequence for the spec. Which system is the book of record decides whether this dashboard
monitors entry exceptions or import exceptions, and those are different widgets with different
sources. Do not write the spec past this point without an answer.

Data sources. If cash is entered in Dimension, Transaction Status over the cash transfer population
plus the Cash Management widget for forward balance. If cash arrives by import, the failure surface
is the interface and the batch job, so System Operation Batch Job Group History and the message
queue view matter more than any transaction widget. [MANUAL 4, 8]

Lens notes. Cash Management is the one widget family here with a documented statement shape:
Group Matrix, column groups on reference dates, row groups on a condition, giving opening balance,
the day's movements and closing balance across a forward term structure. Amounts follow the
Amount in PC check box on the underlying Cash Management setup, not the widget. [MANUAL 8.3.1,
8.3.2] Each Cash Management setup needs its own batch job, task Cash Management Execute Save
Results, before the widget updates. [MANUAL 8.1]

GAP. The Archon question above. Whether cash buckets or bank accounts are the grouping the desk
thinks in.

## Corporate actions

Population signal. At this client the Communication Server carries Bloomberg data and corporate
actions only, through BDL Convert, and nothing else on the trading path touches it.
[MEMORY project_comm_server_skill_2026_08_18]

Data sources. Corporate Actions is a category in this install's Add menu and the Dashboards manual
documents no widget in it, so no widget name may be written yet. [ENV 25-Aug-2026] [GAP,
widget-catalogue gap 5]

What can be specified today without guessing. The inbound side is a Communication Server question,
where a message type that is not enabled and a missing default handler both discard silently, so
the monitoring that actually protects this area may belong in the port and message queue view
rather than in a corporate actions widget. [MEMORY project_comm_server_skill_2026_08_18] Hand the
inbound half to `simcorp-comm-server` and keep the dashboard spec to the event population once the
submenu is captured.

GAP. The Corporate Actions submenu. Whether the desk monitors announcements, elections, or the
resulting entitlements and payments, which are three different populations.

## Post trade compliance

Population signal. Two documented homes. The Asset Manager dashboard states that it shows portfolio
post trade compliance so corrective action can be taken promptly. [MANUAL 11.1] Compliance Manager
has its own configurable dashboard whose widgets are added from the Compliance submenu and are
filtered by user profile authorisation, with statistics refreshed inside Compliance Manager rather
than from the dashboard. [MANUAL 12]

Data sources. Compliance category, widget names not documented. [GAP, widget-catalogue gap 2]
Asset Manager widgets where the audience is the portfolio manager rather than the compliance desk.
[MANUAL 11.1]

Lens notes. This is the one area where the audience choice changes the whole design. A compliance
desk wants every breach by rule with an ageing axis. A portfolio manager wants only their own
book's breaches beside their positions, which is why the manual puts it on the Asset Manager
dashboard.

Client caution. A performance test in August 2026 ran with compliance rules at zero, so any
assumption that a breach population exists in a test environment needs checking before a widget is
demonstrated there. [MEMORY project_order_perf_test_2026_08_19]

GAP. The Compliance submenu. Whether the desk works from breaches or from rule pass rates.

## Real estate redemptions

Population signal. Explicitly flagged in configuration. Order free code 10 value 2 is RE_RED_QUE,
Real Estate Waitlist NWM500 and NWM505. Contingency type 2 is Waitlist. Order free code 20 is the
waitlist called marker CALLED_EXE. Security free code 28 holds the redemption restriction, 1M
mapping to 30 days and 6M to 180 days. The waitlist machinery is batch job groups ALL_WAITLIST,
WAITLIST_ORDER_SEL and WAITLIST_ORDER_UP, order auxiliary jobs WAITLIST, WL_ORD_UPB and
WL_ORD_UPS which must run after order free codes are created or updated, and message queue
WAITLISTS number 42. [MEMORY reference_nwm_order_free_code_catalogue]

Data sources. Transaction Status or the order population filtered on the process flag, plus System
Operation Batch Job Group History over the waitlist batch job groups, because a queue that stops
being processed looks identical to a quiet day in a transaction widget. [MANUAL 4]

Lens notes. Ageing here is the whole point, and the natural axis is days since the redemption was
queued rather than days to a settlement date. Note the known trap that the waitlist push to trade
date plus 99 makes waitlisted orders invisible in the Cash Viewer, so confirm the same push does
not hide them from the widget's setup before promising the desk a complete queue.
[MEMORY project_day1_training_sessions_2026_08_25]

GAP. Whether the desk wants the queue, the called items, or both. Whether NWM500 and NWM505 are the
complete portfolio scope.

## STP transaction window

Population signal. This is the straight through processing monitor, not a file transfer view. The
STP Transaction Monitor shows the progress and status of transactions through STP and the
underlying auxiliary status jobs, and its primary use is the condition of the individual
transaction. [MANUAL 5.7] It is confirmed present in this install. [ENV 25-Aug-2026] SFTP appears
exactly once in the manual corpus, as a Mediator port attribute, and is a different subject.
[MEMORY project_day1_training_sessions_2026_08_25]

Data sources. STP Transaction Monitor, fed by the Trade processing dashboard STP service.
[MANUAL 5.2] Fund and portfolio workflow STP is a separate family with its own service and its own
widgets, STP Jobs and STP Queues, and must not be confused with this one. [MANUAL 9.5, 9.6]

Lens notes. This is the natural cross area canvas: one STP widget carries every area's transactions
at once, which makes it the overview tile for an operations lead rather than a desk widget. The
install already runs something close to this, a stacked bar titled Fund Accounting Transaction STP
Errors over message queue TP_STP. [ENV 25-Aug-2026]

GAP. The message queues in scope beyond TP_STP. Whether auxiliary status job failures should raise
alerts rather than sit in a widget.

## Onex redemptions and the related buys

Population signal. None. Onex does not appear in project memory, in the manual corpus read so far,
or in any capture from this install.

Nothing may be written for this area. What is needed to start: what Onex is in this book, whether
it is an issuer, a fund, a manager or a portfolio; what makes its redemptions different from real
estate redemptions, which already have their own queue and flag; and what related buys means, most
likely a reinvestment or a switch, which would change the population from one transaction to a
linked pair. A linked pair is the hard case, because a widget counts transactions and a pair that
half completed reads as one clean transaction and one missing one.

GAP. The whole area. One paragraph from the desk closes it.
