# Investigation playbooks by classification family

One playbook per family. Each names what to open, what to compare and what evidence proves the
cause. Nothing here replaces reading the setup: if a window, field or tolerance is not visible
in front of you, say that you do not know rather than assuming it.

## TIM. Timing

Open the break in Results Monitor and read the trade date and settlement date on the SimCorp
side. Then open the next business date external file for the same account and look for the
same item.

- Proof for TIM-01: SimCorp carries the item on trade date, the custodian file carries it on
  the settlement date, and the next date file shows the position agreeing. Run Find Unsettled
  Transactions to confirm the transaction is unsettled rather than missing.
- Proof for TIM-02 and TIM-03: quantity agrees exactly and only price or market value differs,
  and the price date on one side is a prior business day.
- Proof for TIM-04: the break date is earlier than the reconciliation date, and the item is
  present and correct in the file for its own break date.
- Proof for TIM-05: the counterparty statement or notice supporting the change is dated after
  the reconciliation date.

Disposition is D1 in every case. Comment the expected clearing date and let it age out. Do not
manually match a timing break, because manual matching hides the very control that catches a
transaction that never arrives.

## PRC. Price and valuation

For listed instruments compare price and market value at the position level, then open the
price on the SimCorp side and read its price date and source.

- Proof for PRC-01: SimCorp price or market value is zero or blank while quantity agrees.
- Proof for PRC-02: the same symptom appears across a block of instruments of the same type on
  the same date. Treat the block as one finding with one owner.
- Proof for PRC-03: both sides carry a price, the difference is a small percentage above the
  market value tolerance, and the two prices trace to different sources.
- Proof for PRC-05: the ratio between the two values is a round factor such as a contract
  multiplier or a pricing factor.

For fund and commitment holdings, open the investment in Alternative Investments Manager or
Asset Manager and work the valuation path. Compare the latest recorded valuation against the
most recent supporting statement, confirm the valuation date is appropriate, then review every
transaction entered after that valuation date. SimCorp starts from the latest valuation and
applies later transactions, so a wrong valuation date breaks the market value even when every
transaction is correct. That is PRC-04.

## QTY. Quantity, position and transaction

Right click the break and select Show Holdings, then View Holdings, to see whether the position
changed and when. Then open the transaction history for the same holding. For alternatives
select All Active before relying on the transaction list, because the default view can include
cancelled transactions.

- Proof for QTY-01 and QTY-02: the transaction appears in one book with supporting
  documentation and is absent from the other.
- Proof for QTY-03: net the booked movements against the prior day closing balance and compare
  the result with the external closing balance. The difference equals twice the suspect amount
  when a sign is inverted. The Cash Integrity window does this arithmetic for cash accounts and
  reports SimCorp closing balance, external closing balance, net closing balance, netted
  payments and the residual difference. A non zero residual means the account is not reconciled.
- Proof for QTY-04: run Find Corporate Actions on the holding. A quantity change with no
  transaction and a corporate action on the same date is a corporate action break.
- Proof for QTY-05: the loan event exists on the facility or contract but produced no
  transaction, and the position still carries the pre event balance.
- Proof for QTY-06: the difference is a cent or a fraction of a unit and the underlying
  economics are identical.
- Proof for QTY-07: market value agrees while quantity differs, and the gap equals the
  recallable, unfunded or out of commitment amount on the statement.

Cash first, then position, is the order to work a custodian break. A cash mismatch nearly
always means a transaction is missing in SimCorp, and that same missing transaction then flows
through to the position line.

## STA. Static data, identifiers and mapping

Compare the identifier fields on both sides of the pair, and the instrument type, before
looking at any value.

- Proof for STA-01: the external record has no security identifier while quantity, account and
  currency all agree exactly. This is the classic manual match candidate, because investigation
  has proven the two records are the same item.
- Proof for STA-02: both identifiers exist, differ in convention, and resolve to the same
  instrument.
- Proof for STA-03: instrument type is blank or wrong on one side.
- Proof for STA-04: the external file carries an account or currency at zero balance that does
  not exist in SimCorp. Expected during setup, and it will produce a real break the moment cash
  moves in that account, so it must be set up rather than ignored.
- Proof for STA-05: the two records agree on everything except the business transaction code,
  and the external code has no translation configured.
- Proof for STA-06: the transaction is absent from the reconciliation on both the internal and
  interface side, and the interface log shows it was not stored because the entry type had no
  matching side.
- Proof for STA-07: the same instrument appears as a no match in two portfolios, one with each
  side.

STA-01, STA-02 and STA-05 are the legitimate manual match cases. Select the internal record and
the external record, use Match Records, then Save Results, and add the comment that explains
why they are equivalent. STA-04, STA-05 and STA-06 are fixed in setup or in the interface, not
by matching.

## MET. Methodology and scope

These breaks are the ones where both books are correct. The work is proof and documentation,
not correction.

- For MET-01, lay the SimCorp transaction components beside the counterparty breakdown of the
  same event and show that the totals agree while the component split differs. Verify the
  SimCorp booking is right before concluding this, because a genuinely missing component looks
  identical at the total level.
- For MET-02, read the day count convention on both sides, normalise both accruals to a common
  convention, and show that the normalised figures agree. A gap that survives normalisation is
  not a convention difference.
- For MET-03, identify the accrual the other book carries and confirm from the loan or fund
  terms which treatment is correct for the reporting basis.
- For MET-04, confirm the modelling basis on each side. Where market value agrees, the item can
  sit at Match level 1 or 2 with a comment while the other book aligns its quantity.
- For MET-05, document the evidence that the SimCorp record is right, raise it, and hold the
  break open until the counterparty confirms the correction.

## MIG. Migration and opening balance

Work from the opening balance and the notice, not from the reconciliation row.

- Proof for MIG-01: the contract has no opening balance, the balance sits on a different
  contract, or it covers only the funded portion. Derived events such as paydowns then fail to
  generate, so MIG-01 and QTY-05 often appear together. Fix the opening balance first.
- Proof for MIG-02: global amounts on the facility or contract do not agree with the notice.
- Proof for MIG-03: the item does not appear in the load file at all. It goes on the delta file
  with an owner and a target load.
- Proof for MIG-04: there is a recorded decision to exclude the item, for example a facility in
  default or one whose notices are not yet processed. Record the decision and the re entry
  condition, otherwise the exclusion becomes permanent by accident.
- Proof for MIG-05: two SimCorp records exist for the same economic item, typically one from an
  earlier load. Delete the superseded static data and transactions rather than matching around
  it.

Replicate any migration fix in the test environment before applying it to the migration run,
and keep the delta file as the single route by which missing records enter.

## FED. Data delivery and run integrity

Handled in stage 1 of the process. If a FED code appears after stage 1, the run was accepted
when it should not have been. Re run rather than investigate, then check whether the same code
appeared on a previous date, because a repeating FED code is a delivery defect with an owner
outside the reconciliation team.
