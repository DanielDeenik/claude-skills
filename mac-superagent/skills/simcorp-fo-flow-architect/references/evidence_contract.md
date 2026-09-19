# Evidence contract

Only the four source classes below may feed a data overlay. Any other input
(estimates, recollection, vendor claims, ticket anecdotes) is refused as
overlay data; it may be quoted in an Open Questions list with its origin named.

## 1. System response log exports (SRM)

The System Runtime Measurements facility described in Front Office Operations
manual section 5.1 (foops, September 2025). Export arrives as a workbook with
context tabs per application. Required columns: Application, Machine, Setup,
Setup ID, Total run time, User, Runtime, Started, Ended, Note.
Rules for use:
- The Note field is the unit of work label. Runs whose Note formats differ
  (for example "Number of orders: N, Create orders and release process" against
  a bare "Number of orders: N") are reported separately and never averaged.
- Machine names distinguish client workstation rows from server rows
  (TESMC1 pattern in the 19 August 2026 capture). Keep them separate.
- Elapsed figures come from the Runtime column as recorded; never recompute
  from Started and Ended without flagging any disagreement.

## 2. Order Events and Order Auxiliary Jobs captures

Screenshot transcriptions of the Events window and the Order Auxiliary Jobs
window per order, as in the 31 July 2026 workbooks. Rules for use:
- Transcribe field values verbatim, including misspellings. Three variants of
  "Executed" exist in the aux status field; exact string filters silently miss
  rows, so match loosely and report the variants.
- Aux job rows fire per edit, not per order. Row counts are evidence of edit
  activity, not of configured job count.
- Execute time "Now (outside commit sequence)" means inside the user save,
  on the critical path. "Deferred" means off it.

## 3. Oracle AWR, ASH and trace output

Only material actually returned by SimCorp's hosted DBA or produced by the
database trace facility (levels defined in ssam 5.11.1). Dan's own account has
no DBA rights, so nothing DB side exists until the DBA hands it over. TKProf
output must have its capture window verified against the flow window before
use; the 14 August 7z carried traces stamped 14 August, not 31 July.

## 4. Compliance order validation notes

The diagnostic string on Compliance order validation SRM rows: Orders,
LBQueueTime, QueueTime, CalcTime, SaveTime, Rules, AssignmentUnits,
AllPositions, ResultPositions, ConcurrentRequests, Mode, ResultDetailsStorage.
Rules for use:
- Rules=0 with AllPositions=0 means no compliance rules were evaluated. Such a
  run is evidence about the empty path only and must be labelled as such.
- ConcurrentRequests=1 means single user. Never present it as a load result.

## Mandatory reconciliations before any overlay

1. Register rows against distinct order numbers against allocated number range
   against SRM order counts. Print all figures; explain none away.
2. Register timestamps against SRM timestamps. A constant offset (three hours
   in both the 31 July and 19 August captures) is reported, not corrected
   silently; state which source is assumed local and why.
3. Every extraction setup run count against the order count it should track.

## Refusal behaviour

If asked to overlay from an inadmissible source, name the contract, state what
would make the source admissible, and offer the structure-only diagram with a
NOT MEASURED band instead.
