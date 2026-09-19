# 04 Recon method: the six causes and how to prove each

Work per bank account and per value date. Always carry four figures side by
side: custodian morning balance (template column D), template expectation
(previous file column N), SimCorp Cash Viewer balance on the value date, and
the difference. Negatives in parentheses.

## Alignment rule

The custodian balance on the morning of day D contains everything that
settled up to and including D minus 1 at the custodian. The Cash Viewer
balance on day D contains everything SimCorp has value dated up to and
including D. A Cash Viewer export in movements mode labels each column with
the payment date; the balance on D is the cumulative sum of the initial
balance and every movement dated up to D. Check the alignment on an account
with no activity (110 AVS USD at 2,087.47 or 120 AVS USD at 497,779.33 on 9
September) before reading any other row.

## Cause 1: payment date perspective

Symptom: SimCorp on D is off by exactly one order or one trade amount that
the template counted a day earlier or later. Test: find the amount in the
Cash Balance Details of D or D plus 1 with Payment type Cash effect and read
its Settlement Date. Proof: the row's Settlement Date differs from the date
the template assumed. Typical case: a HISA or fund sale typed in column M
for next day availability but value dated T plus 2 in SimCorp.

## Cause 2: rolled expected trade date

Symptom: an order created on D shows Trade date D plus 1 and Settlement D
plus 2 in the details. Test: order number's first eight digits are the
creation date; compare with the Trade date column. Proof: amgsg 6.6, the
default is to roll unexecuted orders to today. Fix path: execute or cancel
the order, or freeze the instrument segment on Order Options.

## Cause 3: fund flow counted twice

Symptom: the SimCorp movement on the settlement day of fund subscriptions and
redemptions equals the template's Trading Summary figure plus the custodian's
actual fund flow. Test: compute actual fund flow = (custodian D today minus
custodian D yesterday) minus equity trades minus MFT trades minus manual
fund flows; add the template's column E; compare with the SimCorp movement.
On 9 September 2026 this tied to the cent on 300 AVS USD (14,388.43 plus
14,034.43 = 28,422.86) and to 0.03 on 300 AVS CAD. Proof: Cash Balance
Details for that date grouped by Business transaction code shows a ChargeCash
or CreditCash row on the security Internal Fund Cash Forecast (currency)
next to the actual subscription and redemption rows. Fix path: the forecast
transaction must be reversed or excluded when the actual flows book (Exclude
Payment Types on the Cash Viewer tab of the Settings Template, or the batch
that books the forecast).

## Cause 4: partial fill residual on an order without a bank account

Symptom: a Details row with Payment nominal smaller than the order nominal,
sitting on the bare currency row, and a second order for the same security
and quantity created the next day on the bank account. Test: open both
orders and read executed quantity, remaining quantity and Bank account.
Proof: amcv 3.7, the details show only the non booked part; the booked part
went to the bank account through transaction settlement defaults, the order
residual has no bank account. On 9 September: order 20260908000153 CARGOJET
INC, nominal 40,600 on the order list, 9,700 residual at (739,625.00) on the
bare CAD row of NWM110_A, and order 20260909000002 CARGOJET INC 9,700 at
(739,625.00) on 110 AVS CAD the same day. If the second order is the re
placement of the first order's remainder the amount is counted twice until
the first order is withdrawn.

## Cause 5: order or transaction with no bank account

Symptom: a bare currency row with a non zero movement. Test: the check list
in references/02. Proof: the order's Bank account field is empty and Explain
Order Defaults finds no settlement rule for portfolio plus settlement
currency, or Blank Dynamic Account unless in SC is ticked. On 9 September:
NWM240_A USD (8,100,000.00) on 9/23, and NWM300_A has no CHF account at all
while three TECN SW CHF orders exist (20260907001043, 20260907001037,
20260907000788).

## Cause 6: the template's own feed

Symptom: actual less expected is exactly the expected amount, or a round
number. Test: open the feeding sheet (DJD, dph cash bal, TradeSummary, Bulk
Fees) and check it has rows and a current date. Proof: the sheet is empty or
stale. On 9 September the DJD sheet was empty and the TradeSummary was dated
9/4.

## Order of testing

Alignment check first, then cause 6 (cheapest), then cause 1 and 2 from the
details of the value date, then cause 3 from the arithmetic, then causes 4
and 5 from the orders. Stop at the first cause that closes the difference to
the cent; if a residual remains, say so and name the cell that would settle
it.

## Report shape

One table per portfolio: rows are bank accounts, column groups are custodian,
template expected, SimCorp, difference, cause, evidence. Rows the other side
lacks (a SimCorp account with no template line, a template line with no
SimCorp account) stay in the table in their own block. Screenshots of the
Cash Viewer and of the details go before the table as context. No source
tags inside a client facing version; keep the evidence in a separate
register.
