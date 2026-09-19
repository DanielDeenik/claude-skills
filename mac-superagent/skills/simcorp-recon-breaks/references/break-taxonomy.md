# Break classification taxonomy

Thirty eight classification codes in seven families. Every code was derived from the actual
break population and the working comments recorded against it, not invented. Load these as
Classification ID values in a General Reconciliation Classifications setup and attach the
setup to each reconciliation through Reconciliation classification group ID.

Every break gets exactly one classification code and exactly one disposition code. If two
causes contribute, classify the one that carries the larger part of the difference and record
the second in the free comment, then keep investigating until the whole difference is
explained. A partly explained break is not classified.

## Family TIM. Timing. The break is real today and gone tomorrow

| Code | Name | What it looks like |
|---|---|---|
| TIM-01 | Settlement timing | Booked in SimCorp on trade date, present in the custodian file on settlement date. Futures and bond trades dominate. Confirm the next date file carries the position |
| TIM-02 | Custodian pricing lag | The custodian has not yet priced the security, so market value or price differs while quantity agrees |
| TIM-03 | Stale price date in SimCorp | SimCorp used the prior day price. The record reconciles on the next run |
| TIM-04 | Prior date break not yet re run | The item belongs to an earlier reconciliation date that has not been re executed, so it stays open in the current view |
| TIM-05 | Counterparty processing lag | The counterparty has not yet processed a statement, notice, corporate action or identifier change that SimCorp already reflects |

## Family PRC. Price and valuation

| Code | Name | What it looks like |
|---|---|---|
| PRC-01 | No price in SimCorp | Price or market value is zero or blank on the SimCorp side while quantity agrees |
| PRC-02 | Price feed import failure | The price exists at the vendor but did not import. Affects a block of instruments at once, so look for the pattern before treating it as a single break |
| PRC-03 | Price source difference | Both books priced the security from different sources. Difference sits just above the market value tolerance |
| PRC-04 | Missing or outdated fund valuation | For fund and commitment holdings the latest statement value is not in the valuation history, or the valuation date is wrong, so post valuation transactions apply to the wrong base |
| PRC-05 | Price scaling or unit factor error | The two books express the same holding on different scales, for example a contract multiplier or a pricing factor applied on one side only |

## Family QTY. Quantity, position and transaction

| Code | Name | What it looks like |
|---|---|---|
| QTY-01 | Transaction missing in SimCorp | The custodian or counterparty shows activity that SimCorp never booked. Cash breaks almost always start here and flow into position |
| QTY-02 | Transaction missing at the counterparty | SimCorp booked activity the other book has not |
| QTY-03 | Direction or sign wrong | The transaction exists on both sides but the sign is inverted, so the balance moves the wrong way. Prove it by netting the movements against the prior day balance |
| QTY-04 | Corporate action not processed | Stock split, dividend reinvestment, distribution or similar missing, applied with the wrong factor, or applied on one side only |
| QTY-05 | Paydown or repayment not generated | The loan event did not produce its transaction, so quantity and market value both drift |
| QTY-06 | Immaterial rounding | A cent or a fraction of a unit. Real but not an error. Classify, comment and match. Do not widen the rule |
| QTY-07 | Recallable, unfunded or commitment scope | The two books count recallable amounts, unfunded commitment or out of commitment items differently, so quantity differs while market value agrees |

## Family STA. Static data, identifiers and mapping

| Code | Name | What it looks like |
|---|---|---|
| STA-01 | Identifier absent on one side | The external record carries no security identifier, so nothing can pair. Everything else agrees |
| STA-02 | Identifier convention mismatch | Both sides have an identifier but in different conventions, or one side changed its identifier |
| STA-03 | Instrument type absent or wrong | Instrument type did not load, or the instrument was set up under the wrong type |
| STA-04 | Account not set up | A bank account, sub account or currency exists in the external file but not in SimCorp, typically showing as a zero balance no match |
| STA-05 | Transaction code translation missing | The external transaction code has no translation into a SimCorp business transaction code, so the transaction cannot pair |
| STA-06 | Entry type missing in the interface | The interface layer rejects or drops the transaction because the entry type has no matching side. The transaction never reaches the reconciliation |
| STA-07 | Wrong portfolio or fund | The holding is booked under the wrong portfolio, fund or vehicle, so it appears as a no match on both sides |

## Family MET. Methodology and scope. Both books are correct

| Code | Name | What it looks like |
|---|---|---|
| MET-01 | Component classification difference | The same cash movement is classified differently, for example part of a call booked as a management fee on one side and as call for investment on the other |
| MET-02 | Day count convention difference | Accrued interest differs because the two books use different day count conventions. Normalise both to the same convention before judging the difference |
| MET-03 | Accrual scope difference | One book carries payment in kind interest, a fee accrual or a receivable that the other excludes |
| MET-04 | Amount based versus unit based | The holding is modelled on an amount basis in one book and a unit basis in the other, so quantity can never agree while market value does |
| MET-05 | Counterparty record is wrong | Investigation proves the SimCorp record is right and the other book must correct. The break stays open until they do |

## Family MIG. Migration and opening balance

| Code | Name | What it looks like |
|---|---|---|
| MIG-01 | Opening balance absent or wrong contract | No opening balance, an opening balance on the wrong contract, or one set up on the funded portion only |
| MIG-02 | Global amounts wrong | Facility or contract global amounts were loaded incorrectly, which then breaks every derived event such as paydowns and repricing |
| MIG-03 | Record absent from the upload | The item was never in the load file. It goes on the delta file |
| MIG-04 | Deliberately out of scope | Removed from the migration on purpose, for example an item in default, a new facility, or one whose notices are not yet processed |
| MIG-05 | Duplicate or superseded record | An earlier load left a record that a later load duplicated or replaced. Both sides now appear |

## Family FED. Data delivery and run integrity

| Code | Name | What it looks like |
|---|---|---|
| FED-01 | File absent, empty, late or misnamed | The external file did not arrive, is empty, sits in the wrong folder, is open in Excel, or does not match the expected naming convention |
| FED-02 | File flagged as processed | The reference file shows as processed from an earlier run, so the data does not load. The processed flag must be toggled back before re running |
| FED-03 | Snapshot stale | The break was fixed in the source application but the reconciliation has not been re executed, so it still shows |
| FED-04 | Erroneous cancellation pairing | A transaction was paired twice for cancellation, so the pair no longer nets to zero |

## Disposition codes

| Code | Disposition | Meaning |
|---|---|---|
| D1 | Self correcting | No action. Expected to clear on the next reconciliation date. Comment and let it age out |
| D2 | Explained | No system change is correct. Manually match with a comment that carries the explanation |
| D3 | Fix in SimCorp | Book, correct, reprice or set up the item in the relevant SimCorp application |
| D4 | Fix at the counterparty | The other book must correct. Raise it, record the date raised and track it |
| D5 | Fix in the interface | The transformation, mapping, entry type or translation layer must change |
| D6 | Fix in configuration | The reconciliation rule, tolerance, account, line or classification setup must change. Has a named owner and a change record |
| D7 | Out of scope | Deactivate the external record or exclude from the run. Only for No match records that are genuinely not reconcilable |
| D8 | Escalate | Cause is not understood, or the fix exceeds the reviewer's authority |

## Priority

Assign P1 to any break that changes a published NAV, any break above the fund materiality
threshold, and any break aged beyond the agreed limit. Assign P2 to breaks that are material
in value but do not touch a published NAV. Assign P3 to immaterial and self correcting breaks.
Work P1 to exhaustion before touching P2. Materiality thresholds are a client decision, so
read them from the agreed policy rather than assuming a number.

## Ageing

Age comes from the Number of days field, which SimCorp derives from Break date and the Bank
holidays setting on the reconciliation setup. With no Bank holidays setting the count is in
calendar days rather than business days, so confirm which is configured before quoting an age.
A break whose age is rising while its classification stays the same is a process failure, not
a reconciliation finding, and belongs in stage ten.
