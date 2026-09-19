# 01 Cash Viewer mechanics (amcv September 2025, amgsg September 2025)

Quotes are verbatim except that the manual's dash separators are replaced by
colons.

## Perspective: payment date, not trade date

amcv section 2, page 6: "The Cash Viewer always shows the balances on the
bank accounts or cash buckets from the perspective of payment dates, that is,
the dates when cash payments leave the various currency bank accounts or cash
buckets. This is different from the other Asset Manager applets which
typically show values from the perspective of trade date but they can be
configured to show payment date holdings."

Consequence for the recon: the Portfolio Holdings applet cash row (Security
type CASH, Market Value PC pre-sim) is trade date based and carries the
position scope Pf+Order, so it includes every order's cash effect regardless
of its payment date. The Cash Viewer spreads the same effects over the
payment dates. The two are not expected to agree on any single date, and the
custodian's morning balance is a third perspective again (settled cash only).

## What a balance cell is made of

amcv section 2.3, page 8: "Initial balance of a bank account or cash bucket:
These are applicable only to the earliest balance displayed." "Cash payments
from transactions registered in SimCorp Dimension." "Forecasted future
payments derived from your current holdings, for example, coupon payments
that have not yet been saved as a transaction." "Unsettled trades: These are
simulations, or orders, or preliminary transactions. These can include:
Direct cash simulations. Cash effects of security simulations, or orders, or
preliminary transactions."

Which orders are inside a balance depends on the Options menu, amcv section
3.5, page 19: Include Orders None (settled cash only), Allocated, Filled
(settled plus fills recorded, for equities, FX and rights), All ("Include all
settled cash payments, all allocated orders, all fills, plus any outstanding
order amounts. Balances include the full order amount no matter how far an
order is processed."). Include Simulations and Include FX Simulations are
separate switches. Record the setting in force when you export; two exports
with different settings are not comparable.

## Fills and partial executions

amcv section 3.7, page 21: "Where fills are raised on individual orders, the
Details section and the Cash Balance Details window show one accumulated
fill value for each order as a separate row." "The order balance displayed
in the Details section and the Cash Balance Details window is updated to
show only the cash effect of the non-booked part of the fill." "A warning is
displayed where the execution amount is greater than the fill amount and the
balance is displayed as zero."

So a Details row whose Payment nominal is smaller than the order's nominal is
the unbooked remainder of that order, not the whole order.

## Warning icons

amcv section 3.3, page 16: an icon before a value marks the date cell in
which a simulation, an order or a preliminary transaction changed the value.
Three icons: simulations only, orders only, simulations and orders. Hover for
the count. "Preliminary transactions are treated as orders in this context."

## Details section and Cash Balance Details window

amcv section 3.4, page 17 to 18. Select the balance for the date, expand the
Details section, or right click the cell and choose Show cash details for the
separate window. Fields to add: "Payment source: Shows whether the
transaction is related to an Order, a Forecast, a Transaction, a Simulation,
or an FX Simulation." "Payment type: Displays the type of payment related to
Forecast, such as a Coupon payment." "Business transaction code: Displays
the type of transaction for all payments (except initial balance) such as
Buy/Sell or CloseFXBuy." "Order number: Provides a reference to specific
orders." "Payment security name: Identifies securities generating a cash
payment." Also useful and seen in the Nicola layout: Security ID (the bank
account or the bare currency), Instrument type, Payment nominal, Payment
type (Cash effect for an order, Transaction for a booked transaction),
Portfolio, Quotation Currency, Trade date, Settlement Date, Transaction No.
The Details section shows payments for the selected date only unless
"Display payment for subsequent dates" is ticked on the Cash Viewer tab of
the Settings Template (amcv section 4.2, page 27).

## Historical mode and initial balance

amcv section 3.6, page 20: up to 10 business days back, set by Historical
days on the Settings Template, and it needs Calculate forecast by server
cleared plus Local forecasting ticked in Cash Management settings (section
4.5, page 29). For the earliest balance in normal mode you see "an initial
balance on T-2 days and payments as of yesterday (T-1 day)".

## Where future balances come from

amcv section 4.4, page 29 and foconfig section 3.9, page 53: the Forecast Cash
Flow Service calculates future balances; Number of days to calculate on the
Cash Management tab of Service Options caps the horizon (default 62, maximum
999) and gives the In Future column. Forecast Cash Flow Reset batch job
forces an intraday recalculation (foops section 4.5). A forecast that has not
been reset can carry stale holdings.

## Rolling of expected dates on unexecuted orders

amgsg section 6.6, page 79: "The default behaviour in SimCorp Dimension is to
roll the expected trade date to today's date and adjust the expected payment
date to reflect the new trade date." Freezing needs an instrument segment in
"Instrument segment to freeze trade date" on the Options tab of Order
Options. An order created on day D that is still unexecuted on D plus 1 will
show trade date D plus 1 and payment date D plus 2 in the Cash Viewer, one
business day later than the template assumes.

## Bank accounts shared across portfolios

amgsg section 5.1, page 65: "Cash balances are not restricted to the current
selection in the Data Selector applet. If, for example, a bank account is
used in several portfolios, payments, and holdings in the account originate
from all the portfolios, and not just the portfolio selected."

## Fund certificate cut off

amcv section 3.8, page 22: for fund certificates with cut off times the
payment date "is updated as if the simulation or order were traded right
now"; after the cut off "the Cash Viewer is updated and moves the payment to
the next available date". Relevant to HISA and mutual fund orders placed
late in the day.
