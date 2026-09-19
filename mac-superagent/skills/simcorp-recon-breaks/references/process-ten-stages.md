# The ten stage break resolution process

Run the stages in order. Stage 4 before stage 5 is the rule that makes the population shrink,
because one classification normally explains many breaks at once.

## Stage 1. Confirm the run is valid

Do not look at a single break until the run itself is proven. An invalid run generates a break
population that is entirely artificial and wastes a day.

1. Confirm the external file arrived, is closed, sits in the expected reconciliation folder and
   matches the expected naming convention for that custodian and line.
2. Confirm the archive batch job group moved the file to the archive folder.
3. Confirm the reference file is not flagged as processed from an earlier run. If it is,
   toggle the processed flag back before executing, otherwise the data will not load.
4. Execute the reconciliation batch job group for the reconciliation date. Position lines also
   need the portfolio calculation job to run before matching.
5. Read the run log. It reports how many records matched, deviated and did not match.
6. Open Functions then Error List in the General Reconciliation window and clear any retrieval,
   import or matching errors before proceeding.

If any of these fails, the classification is FED-01 or FED-02, the disposition is D5 or D6, and
the correct action is to fix the delivery and re run, not to investigate breaks.

## Stage 2. Freeze and export the population

1. Open Results Monitor in Reconciliation Manager and load the setup and date. Confirm the
   layout and setup shown in the corner match the reconciliation you intend to review.
2. Work from your own copied view. Never edit a shared view, because other users depend on it.
3. Export the full result set to the break log with the columns listed in
   `break-log-schema.md`. This is the frozen population for the day.
4. Record the run totals per status. These are the denominators for every later count.

## Stage 3. Triage by status, value and age

1. Sort by status in this order of attention: Deviation, No match, Match level 2,
   Match level 1. Automatic, derived and manual matches need no investigation.
2. Within each status sort by absolute break value descending, then by Number of days
   descending.
3. Assign priority using the rule in `break-taxonomy.md`.
4. Group by Matching index so both sides of the same break are reviewed together, and by
   Break ID so the same break is tracked across dates.
5. Look for blocks before individual items. A single price feed failure, a single missing
   account setup or a single missing translation usually explains dozens of rows.

## Stage 4. Classify every break

1. Assign one classification code from the taxonomy to every break in the population,
   including the ones you expect to self correct.
2. Enter it in the Classification field in Results Monitor so it lives in SimCorp and not only
   in the workbook.
3. Where a classification is not yet obvious, mark the record with the Investigation check box
   and leave the code blank until stage 5 proves it. Blank is honest. A guessed code is not.
4. Count the population by code. That count is the report, because it says where the process is
   failing rather than how many rows are open.

## Stage 5. Investigate by code

Use the matching playbook in `investigation-playbooks.md`. Each playbook names what to open,
what to compare and what evidence proves the cause. The general order inside any break is
position first, then transactions, then valuation, because that is the order in which a
difference is created.

Two SimCorp aids are underused and belong in most investigations. Find Unsettled Transactions
shows transactions that have not settled for the position, which resolves most timing breaks in
one step. Find Corporate Actions shows corporate actions attached to the holding, which
resolves most quantity breaks that no transaction explains.

## Stage 6. Decide the disposition and fix at the correct layer

1. Assign one disposition code.
2. Fix at the layer that caused the break, never at a layer downstream of it. A missing
   transaction code translation is fixed in the interface, not by booking a manual transaction.
   A wrong opening balance is fixed in the migration load, not by adjusting the position.
3. Correct an item only once the root cause is understood. Never adjust a transaction because a
   difference exists.
4. Where the fix belongs to the counterparty, raise it, record the date raised and the person
   or team it went to, and keep the break open until they confirm.
5. Where the fix is a configuration change, it needs an owner and a change record. Widening a
   tolerance to clear a break is a configuration decision, not a resolution.

## Stage 7. Document the break

Every break carries four things in the free comment, written so another reviewer never repeats
the work.

1. What was reviewed, naming the windows and the supporting documents.
2. What caused the break, stated as a fact with its evidence.
3. What remediation was completed, or that none was required.
4. The final outcome, meaning resolved, explained, or open and awaiting a named party.

Where the setup requires a comment or a classification on manual match, SimCorp will not save
the match without it. Treat that as the standard everywhere, not only where it is enforced.

## Stage 8. Re execute and re verify

1. Copy the break comments out before requesting any refresh. Comments have been lost on
   refresh before, and the comment is the deliverable.
2. Re execute the reconciliation, or run a partial re execution from Results Monitor for the
   selected split field values when only part of the population changed.
3. Reload the results and confirm each break either cleared, moved to a better status, or is
   still explained by its recorded classification.
4. Where a break did not move, the classification was wrong. Return it to stage 4 rather than
   re commenting it.

## Stage 9. Close, approve and sign off

1. Approve manual matches where four eyes approval is configured. A requested match is not a
   match until the second user saves the approval.
2. Sign off the reconciliation execution once every break is either matched or carries a
   classification, a comment and a disposition.
3. Record the closing position: totals by status, totals by classification code, value of open
   breaks, and the oldest open break.

## Stage 10. Control the recurring and ageing population

1. Any classification code that appears in three consecutive runs is a process defect. Raise it
   as a defect against the owning layer rather than reclassifying it every day.
2. Any break whose age keeps rising with an unchanged classification has no owner. Give it one.
3. Deactivate external no match records that are genuinely out of scope so they stop inflating
   the population, remembering that deactivated records leave the statistics and cannot be
   matched later.
4. Report the trend by classification code, not the row count. The row count says how busy the
   team was. The code trend says what to fix.
