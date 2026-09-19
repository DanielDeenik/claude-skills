# Reconciliation architecture and integration

How the reconciliation platform is assembled, where a break can be created, and which
neighbouring modules depend on the reconciliation status. Every statement here traces to a
SimCorp manual section named in `evidence-register.md` of the solution architecture pack.

## The six layers

1. **Source layer.** SimCorp Dimension holdings, cash management data, portfolio calculation
   output and transactions on the internal side. Custodian, fund administrator and prior book
   of record files on the external side.
2. **Delivery layer.** External files land in the reconciliation folder for their counterparty.
   An archive batch job group moves each file to that counterparty's Archive folder. Reference
   Files setups define the file, its naming convention and its opening mode. A file can only be
   assigned to an event when its Opening mode is Read only or Read only with scan for files.
3. **Configuration layer.** General Reconciliation Fields select which internal fields may be
   used. General Reconciliation Rules define identification and comparison per field, with a
   field type that decides how a deviation is calculated. General Reconciliation Lines bind a
   rule set to a reconciliation type. The General Reconciliation setup binds internal data,
   external data, tracking, classification and statistics settings together.
4. **Execution layer.** Four modes exist and they produce the same results table: manual
   execution in the General Reconciliation window, batch job execution, a portfolio event, or a
   fund event. Position lines run a portfolio calculation before matching.
5. **Exception layer.** Reconciliation Manager carries the Reconciliations applet, Results
   Monitor, Deviation Details, Alerts Inbox and Pending Changes. This is where classification,
   comments, manual matching, deactivation and partial re execution happen.
6. **Reporting and automation layer.** View General Reconciliations, the dashboard widgets, and
   the Reconciliation Manager APIs.

## The execution lifecycle, which is separate from the break status

A reconciliation execution has its own sign off status: Open, Closed, Signed off, plus Re open
and Delete. This is not the same thing as the status of a record inside the run.

- You cannot move an execution from Open to Signed off in one step. It goes Open, then Closed,
  then Signed off, and each target status needs its own authorisation profile. Authorisation is
  configured in the General Reconciliation Approval Configuration window.
- Once an execution is Closed or Signed off, results can no longer be recalculated or changed.
  Alerts on those results are set to Resolved automatically and to Closed the next day.
- Do not sign off while a re execution is running. The Re execution started at field in the
  Reconciliations applet is populated for the duration and cleared on completion, and the state
  is checked every ten seconds.
- Bulk closing is available as a batch task, General Reconciliation, Close Executions, driven by
  reconciliation setup, date and optionally segment. The batch job user needs the same
  authorisation as an interactive user.
- To keep an audit trail of sign off and of match changes, auditing must be enabled on the
  General Reconciliation Runs table, POSRCRUNS.

Closed and signed off executions are deleted automatically once their number exceeds the
Maximum number of results value on the General Reconciliation Settings sub window. Setting that
field to zero retains everything.

## Straight through processing integration

General reconciliation can run as a portfolio event or as a fund event inside the daily
workflow, and this is the control that stops an unreconciled book being used downstream.

The event runs in three steps. Internal data is imported from the database, external data is
imported from the assigned file, then matching runs and the event is created with a status.

Settings that matter:

- **Approval status** is the minimum reconciliation status every included fund or portfolio must
  reach. When all records are at or above it, the event is created Approved. When one record in
  any reconciled fund or portfolio is below it, the event is created Generated. Setting Approval
  status to No match, the lowest level, means the event is approved even with deviations
  outstanding, which defeats the control.
- **Breaks prevent raise**, a check box on the event entry in the Portfolio Event Groups or Fund
  Event Groups window, blocks a user from raising the event to Approved while breaks are
  pending. Every break must be addressed first, for example by manual matching.
- **Import only internal data** creates a snapshot of the internal side and terminates the
  event there. A later event on the same event date reuses the snapshot instead of re reading
  the database. This is how a general ledger reconciliation is taken before other events change
  general ledger holdings, then completed once the external file arrives.
- **Import file** assigns a Reference Files setup and overrides the reference file held on the
  General Reconciliation window. Per portfolio or per fund files are assigned in the Portfolio
  Specific Event Parameters or Fund Specific Event Parameters window and override the event
  level file.
- **Ignore invalid external data** on a reconciliation field filters the imported records to
  those whose value matches the internal side, for example only the portfolios being reconciled.
- **Statistics per portfolio** and **Statistics per fund** produce matched, deviation and
  unmatched counts per portfolio or fund in View General Reconciliations rather than only per
  reconciliation line.

Manual matching and events run side by side. Matching a result in the General Reconciliation
Results window makes SimCorp look for a corresponding event that is not yet approved and
approve it automatically when the Approval status settings of all related setups allow it.
An approved event stays approved even if the match is later reversed.

Deleting a general reconciliation event deletes only the event, never the reconciliation data.

Fund events can run at several levels in a complex fund structure: per class fund in a multi
class fund, per sub fund in a master and sub fund structure, or at the multi class or master
fund level.

## Position in the daily fund workflow

In the documented fund workflow, general reconciliation is executed early, immediately after
market data import and before market data validation, before transaction status is raised, and
well before payments are marked and the payment reconciliation status is raised. Running it
late defeats its purpose, because the figures it protects have already been calculated.

## Neighbouring modules that depend on reconciliation status

- **Payment reconciliation** is a separate module with its own manual and its own events: Mark
  all reconcilable payments, Raise payment reconciliation status driven by a Payment
  Reconciliation Status setup, Set suspense payment, and a bulk FX rate update on payment
  reconciliations. A suspense payment sits on a bank account holding payments not yet reconciled
  so external accounts can be shown whatever their match status, and is dissolved by contra
  posting when the real transaction is entered.
- **Cash Management** has a system configuration setting, Cash management module is linked to
  payment reconciliation module. When it is on, unreconciled transactions count as unfinished
  and only positions built from reconciled transactions enter calculations such as accrued
  interest. A second setting, Bank account transactions are not subject to payment
  reconciliation, exempts cash management transactions. Read both before explaining why an
  accrued interest calculation refuses to run.
- **Matching** assigns a reconciliation identifier to matched transactions, visible in the
  Payment Reconciliation sub window of View Transactions in the Reconciliation payments section.

## Automation surface

The Reconciliation Manager APIs expose the same data the manager shows, over the OData web API.

Version 1 provides GET Executions, GET Results, GET Deviations and POST Comments. Version 2 adds
GET Setups, GET Classifications and POST Classifications, which is what makes an external break
log able to write classifications back rather than only read them.

GET Executions is queried by reconciliation setup, reconciliation date range, sign off status,
fund, portfolio, portfolio group, calculation segment, reconciliation segment, execution key and
a maximum record count. Its response carries exactly the daily reporting cut: automatic matched,
manual matched, derived matches, level 1 through level 4 matches, records with deviations, not
matched records, under investigation, internal records, external records, deactivated, plus the
sign off status and free comment. A comment posted through the API can be up to 2,000 characters.

## Retention and cleanup

Alerts are cleaned by a batch task, General Reconciliation, Delete Closed alerts, with a
minimum number of days an alert must have been closed. Results are cleaned through a Clean Up
General Reconciliation setup scoped by date range, setup, segment, fund, portfolio, portfolio
segment, portfolio group or calculation segment, run manually or by the batch task Cleanup
General Reconciliations, Execute. Set the To date well into the past so recent data survives
for audit.

## Gaps in the corpus

The Payment Reconciliation user manual is not held locally, so payment reconciliation mechanics
beyond the event names above are UNVERIFIED. The Internal General Ledger and Group Currency
Accounting manuals are likewise not held, so the general ledger reconciliation path is known
only through the portfolio and fund event descriptions.
