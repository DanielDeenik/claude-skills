# The four reconciliation domains

Everything below is taken from the procedure documents, the SimCorp General Reconciliation
manual and the actual result exports. Items marked observed were read from the file drop or a
result export rather than from a procedure document, so confirm them against the setup before
relying on them in a deliverable.

## 1. Custodial reconciliation

Three lines run per custodian: transaction, cash balance and position. Each is driven by batch
job groups. Every custodian runs an archive job that moves the received file from the active
reconciliation folder to its archive folder, then the reconciliation job that imports the
external data and matches it against SimCorp. Position lines run a portfolio calculation job
between the two.

Active folder pattern in the test environment: the reconciliation funds folder holds one
subfolder per custodian, each with its own Archive subfolder.

### Batch job group and line identifiers seen in use

| Purpose | Identifier |
|---|---|
| Aviso transaction | RC_TRAN_AVISO |
| BMO transaction | RC_TRAN_BMO |
| BMO exchange traded derivatives transaction | RC_ETD_TRAN_BMO |
| BMO cash balance | RC_CASH_BAL_BMO |
| BMO exchange traded derivatives cash | RC_ETD_CASH_BMO |
| BMO exchange traded derivatives position | RC_ETD_POS_BMO (observed on a result export) |
| TD position | RC_POS_TD (observed on a result export) |

The Reconciliation Manager layout and the setup must both be switched to the matching
identifier before results are read, otherwise the wrong population appears.

### File naming conventions

Documented in the procedure documents:

| Custodian and line | Convention |
|---|---|
| Aviso transaction | YYYY_MM_DD_NWM_DailyTradeFile.csv |
| Aviso cash balance | YYYYMMDD_NWM_CFI_cash_bal*.csv |
| Aviso position | YYYY_MM_DD_NWM_ConsolidatedPositionFile |
| BMO position | TDPosition*YYYY-MM-DD*.csv |
| BMO exchange traded derivatives position | NBI_NICOLA_Position*YYYYMMDD*.csv |

An asterisk means any characters may appear in that place. Observed alongside these in the
file drop: BMO daily client activities and projected cash files, BMO settlement date position
files, BMO exchange traded derivatives cash and trade files, TD balances, positions and trade
activity files, TD exchange traded derivatives margin files, and Desjardins fixed width text
files carrying a client number and a file type code.

### Custodian behaviour that is expected and is not a break

- Aviso prices some securities a day late, so quantity agrees and price does not. Classify
  TIM-02 and expect it to clear.
- Desjardins and Aviso send zero balance accounts and currencies that do not exist in SimCorp.
  They arrive as No match with a zero balance. Classify STA-04 and set the accounts up, because
  the moment cash moves in one the break becomes real.
- Exchange traded derivatives trades settle the business day after trade date, so the position
  and cash lines break on trade date and match on settlement date. Classify TIM-01.
- Exchange traded derivatives execution and clearing fees appear in the counterparty file
  before they are booked, which produces a cash break equal to the fee total. Classify QTY-01.

## 2. Migration reconciliation

SimCorp Dimension against SS and C for each migration run. The break population is exported
from Results Monitor into a working workbook and worked there, with a Resolved column and a
Notes column added in front of the exported fields.

The break identifier follows the pattern LINE_YYYYMMDD_NNNNNNNN, for example a position break
carries a position prefix, the reconciliation date and a sequence number. Break identifiers are
assigned at the end of a run to every record that did not match automatically, and new
unmatched records with the same matching index inherit the same break identifier and date. That
is what makes ageing across runs possible.

Migration specific controls that sit alongside the reconciliation:

- Opening balance checks per facility and contract, reconciled against the notice and the
  counterparty investment summary.
- A delta file as the single route by which missing records enter a later load.
- A change log recording the workstream, the item, the change type, the action taken in SimCorp
  and its status.
- An exclusion list recording items deliberately left out of the migration and the condition on
  which they re enter.

## 3. NAV and variance reconciliation

Fund accounting reconciliations run per fund with their own numbered workbooks rather than
through Reconciliation Manager.

- Cash reconciliation per fund, reconciling the fund cash projection and composite against the
  custodian balances, with separate sheets per custodian and a due to and due from investor
  reconciliation.
- Position and market value reconciliation per fund, comparing the accounting position against
  the custodian and prime broker positions.
- Variance reconciliation per fund, which reconciles the change in market value against income
  and capital movements. The workbook header records a tolerance and a separate mutual fund
  tolerance. The units are recorded as basis points on the sheet while the values are held as
  decimals, so confirm the intended unit with the fund accounting team before quoting it.
- Month end NAV review per fund.

Breaks here are classified with the same taxonomy. The most common are PRC-01, QTY-04 and
MET-03.

## 4. Alternatives, private debt and accrued interest

Market value breaks between SimCorp and the counterparty for alternative investments are
identified in Reconciliation Manager and investigated in Alternative Investments Manager. Use
the default layout rather than a personal layout when panels are missing, search the investment
by part of its name, then work position, transactions and valuation in that order. Select All
Active before relying on the transaction list.

Reconciliation Manager does not show every transaction component for these instruments, for
example management fees and partnership fees, so component level differences must be
investigated in Alternative Investments Manager.

Minimum review for a fund or commitment holding:

1. Compare the latest recorded valuation with the supporting statement.
2. Confirm the valuation date is appropriate.
3. Review every transaction entered after the latest valuation date.
4. Compare each transaction component with the capital call or distribution statement.
5. Check unpaid commitment against the latest statement.
6. Investigate large cumulative cash or distribution differences.

Private debt adds loan facility, contract and position levels, so a break can originate at any
of the three. Accrued interest reconciliations compare interest receivable, standby and unused
fees and accruals against counterparty and servicer reports, where day count convention is a
first class cause and both sides must be normalised to a common convention before any
difference is judged.

## Source citations for this skill

Structure and mechanics in this skill trace to these documents. Cite the section, not the skill,
when a client asks where a rule comes from.

| Fact | Source |
|---|---|
| The seven status levels and what each means | General Reconciliation user manual, section 2.2 |
| Break tracking, Break prefix, Bank holidays setting and ageing | General Reconciliation, section 3.5 |
| Classification setup and the Reconciliation classification group ID | General Reconciliation, section 3.5 |
| Comment required for manual match, keep comments on re execution | General Reconciliation, section 3.5 |
| Deviation detail calculation by field type | General Reconciliation, section 4.4.4 |
| Analyse breaks, Find Unsettled Transactions, Find Corporate Actions | General Reconciliation, sections 4.4.3 and 4.6 |
| Match and un match records, Pending Changes, Save Results | General Reconciliation, section 4.4.5 |
| Cash Integrity fields and the residual difference | General Reconciliation, section 4.4.7 |
| Deactivating unwanted external records | General Reconciliation, section 4.4.8 |
| Partial re execution and the split field | General Reconciliation, section 4.3.3 |
| Sign off lifecycle, authorisation, Close Executions batch task | General Reconciliation, section 4.8 |
| Cleanup of alerts and results | General Reconciliation, sections 4.10 and 4.11 |
| Reconciliation Manager APIs version 1 and version 2 | General Reconciliation, section 5 |
| General reconciliation as a portfolio event, Approval status, Breaks prevent raise, snapshot | Portfolio Figures and STP, sections 2.5.19, 6.26 and 11.3.3 |
| General reconciliation as a fund event and multi class fund levels | Fund Operations 2.4.8 and 5.4.5, Fund Accounting Setup 5.10 |
| Position of reconciliation in the daily fund workflow | Fund Operations, section 5.4 |
| Payment reconciliation events and suspense payments | Portfolio Figures and STP 2.5.25, 2.5.28 and 2.5.31 |
| Cash Management linkage to payment reconciliation | Cash Management user manual, bank account transactions chapter |
| Reconciliation identifier on matched transactions | Matching user manual |
| Custodian batch job groups, file naming, tolerances and known behaviour | Client procedure documents for Aviso, BMO and BMO ETD, plus the alternatives break investigation guide |
| The classification code list | Derived from the recorded comments on the client break population |
