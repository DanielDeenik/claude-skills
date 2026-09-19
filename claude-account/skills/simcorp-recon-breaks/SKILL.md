---
name: simcorp-recon-breaks
description: >
  Reconciliation break resolution in SimCorp Dimension for Nicola Wealth. Covers the seven
  reconciliation status levels and the tolerances that produce them, the four recon domains
  (custodial cash, position and transaction against Aviso, BMO, BMO ETD, Desjardins, TD, TD ETD
  and NBIN; migration recon against SS and C; NAV and variance recon; alternatives, private debt
  and accrued interest), a thirty eight code classification taxonomy, and the ten stage process
  to triage, classify, investigate, fix, document, re run and close every break. Use whenever
  the user mentions a recon break, deviation, no match, match level, break ID, Reconciliation
  Manager, Results Monitor, an unmatched position or cash balance, a custodian file that will
  not match, an opening balance check, or asks how to categorise, investigate, fix, age,
  escalate or sign off recon items, how the reconciliation is wired into the daily portfolio
  and fund event workflow, or asks for a recon architecture or diagram.
---

# SimCorp Reconciliation Breaks

This skill owns break resolution: what a break is, why it exists, how it is categorised, how it
is fixed and how it is closed. Sisters: `simcorp-pd-migration` for the bulk static data upload
that creates migration breaks, `simcorp-pd-lifecycle` for the loan events behind private debt
quantity breaks, `simcorp-pd-valuation-cash` for pricing and cash flow behind valuation breaks.

## Rule 1. Two axes, never one

Every break carries two independent labels and they must never be confused.

**Reconciliation status** is assigned by SimCorp Dimension from the configured rules. The
analyst cannot choose it. It tells you how far apart the two records are, not why.

**Classification** is assigned by the analyst in the Classification field of Results Monitor
or the General Reconciliation Results window. It tells you why. Classification values come
from a General Reconciliation Classifications setup (Group ID, Classification ID,
Classification Name, Description) that is attached to the reconciliation setup through
Reconciliation classification group ID on the Settings sub window. The full code list is in
`references/break-taxonomy.md`. Never invent a classification value that is not in that setup.

A break is only complete when it carries a status, a classification, a free comment and a
disposition. A status alone is not an answer.

## Rule 2. The seven statuses and what each one means

| Status | Meaning | Analyst action |
|---|---|---|
| Automatic match | Matched with no rule violated | None beyond approval if configured |
| Derived match | Matched because another record with the same Break ID and date matched | Confirm the parent match was correct |
| Manual match | A user overruled at least one violated rule | Comment is mandatory, keep the audit trail |
| Match level 1 | Pairs, quantity exact, another field outside tolerance, normally price or market value | Investigate the value difference |
| Match level 2 | Pairs, market value aligns, quantity differs | For commitment based holdings often expected, for unit based holdings investigate a missing buy or sale |
| Deviation | Pairs but at least one rule is violated, quantity and market value may both differ | Highest priority, usually a missing or wrong transaction or a stale valuation |
| No match | Cannot be paired at all | Data is missing, corrupt or insufficiently transformed. Usually static data, mapping or a wholly absent record |

Levels run 1 through 4 and are evaluated in order. Each level only runs if the previous level
produced no match. Match level 1 is the first and strictest level, not the loosest.

## Rule 3. The tolerances that produce the status

Do not guess a tolerance. Read it from the General Reconciliation Rules setup for the line in
question. The values in use on the current custodial setups are:

- Cash balances must match exactly. Cash is bank account movement, so any difference is real.
- Position quantity must match exactly. Any quantity difference falls to Deviation.
- Position market value tolerance is 0.5 percent. Above that the record falls to Deviation or
  Match level 1 depending on which field broke.
- Transaction payment amount tolerance is 0.01 absolute.

If a break sits just outside tolerance and the cause is rounding or a one cent difference, that
is a classification of immaterial rounding, not a licence to widen the rule. Rule changes are a
configuration decision with an owner, not a break resolution step.

## Rule 4. The reconciliation is a snapshot

Reconciliation Manager shows a point in time snapshot. A correction made in Asset Manager,
Alternative Investments Manager, Dealer or Loan Facilities does not appear in the loaded
results. The reconciliation must be re executed through the applicable batch job group or a
partial re execution before the break can be called resolved. Retain a separate copy of break
comments before requesting a refresh, because comments have been lost on refresh before.

## Rule 5. The execution has its own lifecycle

The sign off status of a reconciliation execution is a separate thing from the status of a
record inside it. An execution runs Open, then Closed, then Signed off, and it cannot skip a
step. Each target status needs its own authorisation profile, set in the General Reconciliation
Approval Configuration window. Once an execution is Closed or Signed off its results can no
longer be recalculated or changed, and its alerts are resolved automatically. Never sign off
while the Re execution started at field in the Reconciliations applet is populated.

When reconciliation runs as a portfolio or fund event, two settings carry the control. Approval
status is the minimum record status every included fund or portfolio must reach before the event
is created Approved rather than Generated; setting it to No match approves the event with
deviations still open. Breaks prevent raise, on the event entry in the Portfolio Event Groups or
Fund Event Groups window, stops a user raising the event to Approved while a break is pending.
Detail is in `references/architecture-and-integration.md`.

## The four domains

Detail, setups, batch job groups, file naming and folder paths are in
`references/recon-domains.md`. In summary:

1. **Custodial recon.** Transaction, cash balance and position lines against Aviso, BMO, BMO
   ETD, Desjardins, TD, TD ETD and NBIN. Run daily by batch job group. Position lines also run
   a portfolio calculation before matching.
2. **Migration recon.** SimCorp Dimension against SS and C for each migration run, plus opening
   balance checks and delta file control. Break population is tracked in a workbook with
   Resolved and Notes columns alongside the exported Results Monitor fields.
3. **NAV and variance recon.** Fund accounting NAV review, variance recon per fund against a
   tolerance expressed in basis points, and cash projection and composite cash reconciliation.
4. **Alternatives, private debt and accrued interest.** Market value breaks investigated in
   Alternative Investments Manager and Asset Manager, plus interest receivable, standby fee and
   accrual reconciliations where day count convention is a first class cause.

## The ten stage process

Full step by step detail is in `references/process-ten-stages.md`. The stages are:

1. Confirm the run is valid before looking at a single break.
2. Freeze and export the population.
3. Triage by status, value and age.
4. Classify every break with a code from the taxonomy.
5. Investigate by code using the matching playbook.
6. Decide the disposition and fix at the correct layer.
7. Document the break so no one repeats the work.
8. Re execute and re verify.
9. Close, approve and sign off.
10. Control the recurring and ageing population.

Never run stage 5 before stage 4. Classifying first is what makes the population shrink,
because one classification usually explains many breaks at once.

## Hard rules

- Never manually match a break to make it disappear. Manual match is for records that are the
  same economic item with a minor difference that investigation has already explained.
- Never correct a transaction because a difference exists. Correct it because the root cause is
  understood and the correction is the fix for that cause.
- Never treat a timing difference as an error. If it will self correct on the next
  reconciliation date, classify it, comment it and let it clear.
- Never guess a SimCorp window, field, setup name or tolerance. Read it from the setup, the
  manual or a screenshot, or say that you do not know.
- Never leave a break with a status and no comment. The comment is the deliverable.
- Deactivate an external record only when it has No match status and is genuinely out of scope.
  Deactivated records are excluded from statistics and cannot be matched later.

## References

- `references/break-taxonomy.md` The full classification code list, the disposition codes,
  the priority rule and the ageing rule.
- `references/process-ten-stages.md` The ten stages in full, with what to do at each one.
- `references/investigation-playbooks.md` A playbook per classification family telling you what
  to open, what to compare and what evidence proves the cause.
- `references/recon-domains.md` Setups, batch job groups, file naming, folder paths,
  tolerances and known behaviour per custodian and per domain.
- `references/break-log-schema.md` The break log column set, the export field list from
  Results Monitor and the reporting cuts.
- `references/architecture-and-integration.md` The six layers, the execution lifecycle,
  event integration, dependent modules, the API surface and the retention rules.
- `references/diagrams.md` The nine diagram sources, source tagged, with the shared styling.
