# Area monitoring packs, trade side

Six areas: FX trades, options, futures, mutual fund trades, security transfers, swaps and
crystallizations. The operations side is in `area-specs-ops.md`.

## The pattern these six share

A Transaction Status widget shows the transactions inside one setup, where a setup is a named
selection of fields and transaction data in a transaction window. [MANUAL 5.9, 14] So the design
question for each area is not which widget, it is which setup defines the population, and the
answer is a client configuration fact, not a manual fact.

**GAP A, applies to every area in this file and in `area-specs-ops.md`.** No Transaction Status
setup names, transaction codes, transaction business codes or instrument types have been read from
this install. Until a setup list or a screenshot of the Transaction Status window is supplied, a
spec names the population in business language and leaves the setup line as TO BE NAMED. The
manual's own example of a business code is WdrMoney, which is an illustration and not a Nicola
value. [MANUAL 5.9]

Standard build for one of these areas, once the setup exists:

1. Transaction Status widget, Group Matrix, status on the vertical axis, a time dependency field on
   the horizontal axis. That single widget answers what is stuck and how long it has been stuck.
2. A Table widget over the same setup filtered to the exception condition, for the working list.
3. A Chart widget over the same setup for volume and trend, where the desk reports upward.
4. An alert generation rule only where an item must chase somebody. [MANUAL 6.1.1]

Keep each widget under 2,000 records and filter in the setup, not in the widget. [MANUAL 5.1, 5.9]

## FX trades

Population signal. FX is the exception to the direct order route at this client: Order Settlement
Defaults send Funds to destination SimCorp Dimension while FX goes to Order Manager, and the FIX
path to EMSX and FXGO runs through Order Manager and never the Communication Server.
[MEMORY project_day1_training_sessions_2026_08_25] Recurring FX carries order free code 10 value 1
RECUR_FX. [MEMORY reference_nwm_order_free_code_catalogue]

Data sources. Two layers. Order side, the Trading widgets on the Order Manager dashboard, Broker
Routing and Strategy Routing, which drill to the dealer window through Open Transaction.
[MANUAL 13.1, 13.3] Settlement side, Transaction Status and Match over the FX population.

Lens notes. Ageing on FX belongs on cut off time rather than settlement date, so use minutes to
custodian cut off time on the horizontal axis. [MANUAL 3.6.7]

GAP. Whether Recurring FX should be a separate widget or a group inside the FX widget. The FX
setup name. Whether FXGO status is visible in Dimension at all, since no FXGO association is
documented anywhere in the corpus. [MEMORY project_day1_training_sessions_2026_08_25]

## Options

Population signal. Nothing client specific is grounded. The only documented option handling in the
dashboard layer is commission: Commission Tracking covers equities and exchange traded futures and
options, including step outs and commission sharing agreements. [MANUAL 13.2]

Data sources. Transaction Status for lifecycle and exceptions. Commission Tracking where the
question is broker cost rather than settlement.

GAP. Whether the population is exchange traded only or includes over the counter options, which
decides whether Commission Tracking is relevant at all. Instrument types in scope. Whether options
sit inside the instrument type override that reroutes an order to Portfolio order and destination
Order Manager, since the two overridden instrument types in domain 15, values 24 and 14, are not
identified anywhere. [MEMORY reference_nwm_order_free_code_catalogue]

## Futures

Population signal. As for options, futures appear in the dashboard layer only through Commission
Tracking. [MANUAL 13.2] Exchange traded derivative custodians are in scope of reconciliation at
this client, which implies a settled population exists to monitor.
[SKILL simcorp-recon-breaks, recon domain list]

Data sources. Transaction Status for lifecycle. Commission Tracking for broker cost. Where variation
margin cash is the real concern, the Cash Management widget answers it better than a transaction
widget, because it forecasts bank account and cash bucket balances forward. [MANUAL 8]

GAP. Whether the desk wants position and margin monitoring or trade lifecycle monitoring. These are
different widgets and the question has not been asked.

## Mutual fund trades

Population signal. The documented Wealth pipeline is the NBIN extract, batch job group
DM_NW_O_NBIN_MF_FILE, gated on Line of Business WEALTH plus custodian NBIN. No Aviso trade file,
inbound or outbound, is documented anywhere in the manual corpus.
[MEMORY project_day1_training_sessions_2026_08_25] Wealth orders are direct orders with destination
SimCorp Dimension, so there is no Order Manager leg and no Capture Trade step on this path.
[MEMORY project_new_issue_wealth_vs_fi_2026_08_24]

Data sources. Transaction Status for the trade population. System Operation Batch Job Group History
for the extract itself, which is the part that actually fails. [MANUAL 4] STP Transaction Monitor
where the transactions run through STP. [MANUAL 5.7]

Lens notes. This area needs two widgets rather than one, because a clean transaction queue with a
failed extract job still means the trades did not leave the building.

GAP. Whether an inbound confirmation file exists to match against, which decides whether the Match
widget belongs here. The waitlist push to trade date plus 99 makes waitlisted orders invisible to
the Cash Viewer, and whether that also hides them from a Transaction Status setup is unknown.
[MEMORY project_day1_training_sessions_2026_08_25]

## Security transfers

Population signal. The Security Transfers window moves a security between a customer portfolio and
a portfolio in an external custody, in both directions. Direction codes are confirmed on both
sides: in, Add-C., Add-C-Cdy and reinvestment C-Reinv.; out, Remove-C and Rem-C-Cdy. Bulk entry is
Multi Security Transfer In and Out. Booking runs Request, then save, then Actual, up the status
ladder Entry, Position or Free deal, Fin calc, Trade GL and Settle GL, with client specific
intermediate levels possible. The holding key locks when the transaction is saved at Position
status or higher, and that is the moment quantity starts aggregating into the real position.
[MEMORY project_security_transfers_process_2026_08_12]

Data sources. Transaction Status grouped on requested status against actual status. This is the one
area where the two status fields disagreeing is itself the exception, because Actual can go out of
sync with Request when the transaction is not authorised or not valid.

Lens notes. Ageing by days since trade date rather than to settlement date, since a transfer parked
at Entry has no settlement pressure but is still wrong. [MANUAL 3.6.7]

GAP. The exact holding key field set for this window, still open from August 2026. Whether
transfers in and out belong on one widget split by direction code or on two.

## Swaps and crystallizations

Population signal. Both are stamped, not inferred. Transaction free code 45 is Swap trades, yes or
no. Order free code 14 is Crystallization, yes or no. Contingency type 3 is Crystallization and 5
is Swap Trades. Both have their own Assign Values button, which is an operator action rather than
an automatic rule. [MEMORY reference_nwm_order_free_code_catalogue]

Data sources. Transaction Status filtered on the free code, which is the cleanest population
definition of any area in this pack, since the flag is explicit.

Lens notes. These are event driven and low volume next to daily trading, so a Group widget with one
group per stage reads better than a matrix, and volume over time matters more than ageing.

GAP. Whether the desk monitors the order stage, the transaction stage or both. Whether free code 45
is visible as a selectable field in the Transaction Status widget, which is not guaranteed: widget
field names differ from window field names and a few window fields are unavailable in the widget.
[MANUAL 5.5]
