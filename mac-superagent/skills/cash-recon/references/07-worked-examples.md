# 07 Worked examples, one per cause, all from 9 September 2026

Every figure is a cell in the two template files, the Cash Viewer export or
a Cash Balance Details row from the recorded session. Read each example as:
what the recon showed, the arithmetic, why SimCorp differs, the cell that
proves it, and what closes it.

## Example 0: the alignment check, and the mistake it prevents

Recon row 110 AVS USD: expected 2,087.47, actual 2,087.47, SimCorp 9/9
2,087.47. Recon row 120 AVS CAD on 9/8: SimCorp 489,816.72, custodian
489,816.71. Both prove that "Cash movement D" in the export is the payment
date D and that the balance on D is the cumulative sum through D.
The first pass of this recon read the NWM110 ladder one column to the right
and reported 29,220,354.69 as the 9/8 balance and a 20 million inflow on
9/8. The 20,912,549.95 is value dated 9/4 and the 9/8 balance is
9,285,555.46, only 108,567.98 above the custodian. Run Example 0 before any
other row; a flat account that ties on both dates is the calibration.

## Example 1: payment date perspective (the HISA sale)

Recon row 110 AVS CAD: expected 4,000,928.03, custodian 4,704,613.45,
SimCorp 9/9 (3,374,330.22), SimCorp 9/10 5,418,364.78.
Template arithmetic: 9,176,987.48 (custodian 9/8) plus 1,323,940.55 (fund
flows) minus 16,000,000.00 (equity buys) plus 9,500,000.00 (MFT, the BNST
HISA sale) = 4,000,928.03, all assumed available on 9/9.
SimCorp: the 9/10 details of 110 AVS CAD hold BNST Corporate Tiered
Investment Savings, order 20260908000384, Buy/Sell, Cash effect, 9,500,000.00,
trade date 9/9, settlement date 9/10. The 9,500,000.00 is in the 9/10
balance, not the 9/9 balance. The custodian's 9/9 morning balance already
contains it (the actual change of (4,472,374.03) only reconciles if the
9,500,000.00 has settled).
Why: the Cash Viewer is payment dated (amcv page 6). The HISA order carries
a T plus 1 payment date from its trade date, and the trade date is 9/9, not
9/8 (see Example 2). The template treats MFT as next day cash.
Proof cell: 110 AVS CAD, 9/10, Details row BNST, Settlement Date 9/10.
Closes it: compare the template's 9/9 expectation with the SimCorp 9/10
balance for HISA cash, or execute HISA orders on the day they are placed so
the payment date stays T plus 1 from placement.

## Example 2: rolled expected trade date

Order 20260908000384 (BNST) and order 20260908000153 (CARGOJET) both carry
the creation date 8 September in the order number, and both show Trade date
9/9/2026 and Settlement Date 9/10/2026 in the details.
Why: amgsg 6.6 page 79, an unexecuted order's expected trade date rolls to
today and the payment date moves with it, unless the instrument's segment is
in "Instrument segment to freeze trade date" on Order Options.
Proof cell: order number prefix against the Trade date column of the
details row.
Closes it: freeze the segment for fund certificates and HISA, or accept that
every order left unexecuted overnight moves one business day in the ladder
and reconcile on the rolled date.

## Example 3: fund flow counted twice

Recon row 300 AVS USD: expected 215,374.24, custodian 215,020.24, SimCorp
9/9 529,408.67.
Arithmetic: template Trading Summary (column E) 14,388.43. Custodian actual
fund flow = (215,020.24 less 500,985.81) plus 300,000.00 (the MFT sale) =
14,034.43. Sum 28,422.86. SimCorp movement on 9/9 = 529,408.67 less
500,985.81 = 28,422.86. Residual 0.00.
Same test on 300 AVS CAD: 523,647.39 plus 523,142.38 = 1,046,789.77 against
SimCorp 1,046,789.74, residual (0.03). On 240 AVS USD: (294,244.82) plus
(293,348.77) = (587,593.59) against (587,583.58), residual 10.01. On 120 AVS
CAD: 747,146.54 plus 745,536.34 = 1,492,682.88 against 1,497,682.82,
residual 4,999.94. On 240 AVS CAD the residual is (77,515.22), a third fund
flow sized item.
Why: SimCorp has both a forecast of the fund flow and the actual flow on the
same payment date. The forecast mechanism is visible on 9/10 as Internal
Fund Cash Forecast (CAD), ChargeCash, Transaction, 32,320.00. The actual
flows are the subscription and redemption transactions. When both are
booked for 9/9 the balance carries the flow twice.
Proof cell: 300 AVS USD, 9/9, Details grouped by Business transaction code:
one ChargeCash or CreditCash row on Internal Fund Cash Forecast (USD) of
14,388.43 and actual flow rows summing to 14,034.43.
Closes it: reverse or exclude the forecast transaction once actual flows
book (Exclude Payment Types on the Cash Viewer tab of the Settings
Template, or the batch that books the forecast), then re run the recon.

## Example 4: partial fill residual on an order with no bank account

Recon block "Cash account row (no bank account)": CAD, NWM110_A, 9/10,
(739,625.00).
Details of the bare CAD row: CARGOJET INC, Buy/Sell, Cash effect, Security
ID CAD, order 20260908000153, Payment nominal 9,700.00, (739,625.00).
Order grid: 20260908000153, CJT CN, nominal 40,600, estimated value
3,095,750.00, which is 76.25 per share. 9,700 at 76.25 = 739,625.00.
Details of 110 AVS CAD on 9/10: CARGOJET INC, order 20260909000002, Payment
nominal 9,700.00, (739,625.00), created the next day.
Why: amcv 3.7 page 21, the details show only the non booked part of a filled
order. The booked 30,900 went to 110 AVS CAD through transaction settlement
defaults; the order's own Bank account field is empty so its 9,700
remainder sits on the currency. If 000002 is the re placed remainder, the
ladder carries 739,625.00 twice.
Proof cell: order 000153 in the Order Outbox, executed and remaining
quantity, Bank account field; order 000002 origin.
Closes it: withdraw the 000153 remainder (or cancel 000002), and fill the
Bank account on orders that stay open, see references/02 check list.

## Example 5: order or transaction with no bank account at all

Recon block: USD, NWM240_A, 9/23, (8,100,000.00). Also NWM300_A has no CHF
row while orders 20260907001043 (4,945.00), 20260907001037 (1,978.00) and
20260907000788 (1,978.00) are CHF sells of TECN SW.
Why: the bank account on an order comes from Settlement Our Defaults keyed
on portfolio plus settlement currency (setdef 3.1, foconfig 21.2). No row
for NWM300_A plus CHF, or Blank Dynamic Account unless in SC ticked
(foconfig 17.4.1.5), leaves the field empty and the cash lands on the
currency. Assign Values does not fill settlement details.
Proof cell: the order's Bank account field, Explain Order Defaults, the
Settlement Our Defaults rows for the portfolio.
Closes it: create the missing bank account and settlement default row, or
correct the order, then confirm the bare row disappears from the export.

## Example 6: the template's own feed

Recon rows 120 DESJ USD, 240 DESJ USD, 300 DESJ USD: expected 1,621,628.46,
5,886.13, 1,915,988.83; actual 0.00 on all three; SimCorp equals the
expectation on all three.
Why: column D on the Desjardins rows is SUMIFS over the DJD sheet, and the
9 September file's DJD sheet is empty. The script flags it: "actual reads
0, check the feeding sheet (DJD or dph cash bal) is populated".
Second case: column K on NWM110 is typed as (16,000,000.00) while the seven
equity orders of 8 September total 15,993,924.10, a rounding of 6,075.90.
Third case: the Fund Flow (2) entries 69,000.00 and (50,000.00) on NWM241
have no source in the file, and the SimCorp 9/8 balances of 240 AVS CAD and
240 AVS USD differ from the custodian by 68,920.50 and (50,010.00).
Fourth case: TradeSummary in both files carries Period End Date 9/4/2026,
so column E is the 9/4 fund flow on 9 September.
Proof cell: DJD sheet row count, TradeSummary A2, csh K3, csh H25 and H26.
Closes it: refresh DJD and TradeSummary before comparing, and carry the
order values rather than rounded trade amounts in K and M.

## How the six read together on 110 AVS CAD

Expected 4,000,928.03 against SimCorp 9/10 CAD node 4,678,739.78: the node
holds the HISA on 9/10 (Example 1), the CARGOJET residual twice (Example 4),
a 32,320.00 forecast transaction, and whatever sits in the 9/9 outflow of
(12,659,885.68) and the 9/4 inflow of 20,912,549.95, which are still to be
pulled. Until those two cells are opened the 110 AVS CAD difference has a
list of known parts and one unknown remainder, and the report must say so.
