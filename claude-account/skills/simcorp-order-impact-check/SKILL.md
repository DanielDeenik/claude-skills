---
name: simcorp-order-impact-check
description: "Set up and read the SimCorp Asset Manager AR approval grid so a pending order's impact on household asset allocation is visible: the Analysis Properties settings, the reload after changing them, how an Order row reads including a sell as a negative weight, the roll up arithmetic, and the checklist for when an order does not appear."
---

# SimCorp Order Impact Check (Nicola Asset Manager)

A reviewer needs to see what a pending order does to a household's asset allocation before approving it. This skill is the setup that makes the order visible, how to read it, and what to check when it does not appear. Grounded in PROD captures of 10 and 14 September 2026 on the AR APPROVAL and AR APPROVAL 2 layouts, plus amscn 1.1 for the Aggregation options and amacf 5.2 for pre simulation values already including orders. Column captions here are client specific and come from the screen, never from a manual.

The end to end approval flow lives in simcorp-ar-approval. Rescaled field theory, distribution sets and the full position type roster live in simcorp-am-weight-layouts. Bands as compliance rules live in simcorp-compliance-rules. Missing prices live in simcorp-data-management-specialist.

## The setup

Confirm each of these, never assume them.

1. Layout: AR APPROVAL or AR APPROVAL 2, sub layout Approval Layout. Tabs Household Orders for Approval, Cash Viewer, Order Outbox, Portfolio Summary.
2. Data Selector: load the approval group under review from the AR Approval folder (1. AR Approval Group upward). The grid stays empty until a group is loaded.
3. Analysis Properties, opened with Properties on the Analysis ribbon group: Settings template WEALTH, Analytics configuration PM_RAPAC, Reporting currency CAD.
4. Aggregation: None or Within position type. Both keep the order on its own row and either is correct for this task. Across position type merges everything on a holding key into one row, so the Order label disappears (amscn 1.1). This is the single setting that most often hides the order.
5. Grid grouping: Household Name, then Sub Asset Class, then Position scope. Without Position scope as the third level nothing is labelled Order.
6. Columns: Current Weight Post-Sim, Target Weight (%), Deviation from Target (%).
7. Decomposition on for the view, which shows as Dec inside the Position scope of the look-through rows.

## Reopen after changing a setting

Changing Aggregation and clicking OK empties the grid and reloads it. On 14 September that reload took about thirty seconds with the status bar reading Working. The households collapse, so expand the household and then the sub asset class again afterwards. A grid that looks empty during the reload is not a defect, and the order row is not missing while a household is collapsed. This reopen is the step reviewers skip before reporting that trades do not show.

## Reading the order row

Position scope names the position types present on one holding key, joined with a plus sign: Pf a holding, Mp a model component, Order a pending order, Dec a look-through row from decomposition. Under a sub asset class the order is its own child row, labelled Order when nothing else sits on that key and Order+Mp when the model also carries a target there. Expanding that row once more shows the portfolio, so an order placed in the cash account and one placed in a registered account are separate lines.

A sell carries a NEGATIVE weight on its Order row. On 14 September, US Real Estate read Pf+Order+Mp 9.95 against target 10.00, split into Mp 0.00 with target 6.67, Order+Mp minus 4.63 with target minus 1.55, and Pf+Mp 14.58 with target 4.88. The order weight is therefore inside Current Weight Post-Sim and inside the deviation. The target is apportioned across the scope rows as well, so never read the target on a single scope row as the model target for the class; only the sub asset class row carries that.

The cash leg of every order lands on the Cash row, whose Position scope then includes Order. On the same household the Cash row read 11.21 as Dec 3.05 plus Order 8.14 plus Pf 0.01, and the Order line itself split into three portfolio lines of 1.69, 4.66 and 1.80.

## Two verifications, run both

Scope rows must sum to their sub asset class row within rounding, on weight and on target. US Real Estate above: 0.00 minus 4.63 plus 14.58 equals 9.95 exactly, and 6.67 minus 1.55 plus 4.88 equals 10.00 exactly. The Cash rows summed to 11.20 against 11.21 shown, which is rounding.

Sub asset class weights must sum to the household total. The 14 September household summed to 100.00 exactly across twenty one classes. That total is forced by the rescaling, so it proves the read is complete; it is never evidence that the household is on target.

If either check fails, a scope row is filtered out or the grouping is not on Position scope. Fix the grid before discussing the numbers.

## When the order does not appear under its sub asset class

Work down this list and stop at the first one that explains it.

1. Order Outbox: is the order actually pending for that household. If not, nothing else matters.
2. Aggregation: is it Across position type. Change it to None or Within position type and let the grid reload.
3. Grouping: is Position scope the third grouping level.
4. Expansion: the order is a child row and is hidden while the household or the sub asset class is collapsed.
5. Timestamps: the capture being discussed and the grid on screen may be from different moments, and orders created or executed in between change the rows.
6. The Cash rows: read them before concluding anything. On 10 September a household showed Infrastructure as Dec+Mp 0.00 with no Order row, while the two cash rows were 3.80 and 0.32 higher than the next day. That 4.12 is exactly what appeared under Infrastructure the next day as Pf+Mp 3.79 plus Order+Mp 0.33. The holding and its order were present all along, inside the look-through rows.

## The Dec only pattern, observed twice, not yet explained

In both households captured, an Order row appeared under a sub asset class only where that key also carried a Pf holding. Where the fund appeared as Dec only or Dec+Mp with no Pf, the sub asset class read 0.00 or near it and no Order row was shown. On 14 September the order card opened from the grid was a sell of a bond fund mapped to Investment Grade Bonds, and Investment Grade Bonds on that same grid read Dec+Mp 0.00 against target 6.00 with no Order component, while US Real Estate, which did carry Pf, showed its order normally.

Two candidate causes, neither proven, both to be tested before either is quoted:

- Look-through replaces the fund certificate with its components, so the fund's value and its order land on the component rows (for a bond fund, partly on Cash and Cash Equiv.) rather than under the fund's own sub asset class.
- The decomposed components have no price, leaving the row at 0.00. Private Equity, Infrastructure and Investment Grade Bonds are the same three classes that read 0.00 with decomposition on in the earlier pricing review, so run Search Missing Prices on the components before assuming a look-through effect.

Report this as an observation with the arithmetic attached. Do not present either cause as the answer, and do not tell a reviewer that an order is simply slow to register: on 10 September the cash arithmetic ruled timing out as the explanation.

## What to hand back

A reviewer question is answered with: the settings that were in force, the sub asset class row with its scope split, the two sums that prove the split is complete, and either the order row or the reason it is not there from the checklist. Where the reason is the Dec only pattern, say which of the two candidate causes is being tested and by whom.

## House style

Full sentences. No dashes, middots, arrows or maths glyphs. Negatives written as minus or shown in parentheses. Roles and teams, never individual client names, in anything shared. Household names and portfolio codes are client data and stay inside the working session. Screenshots are the source of truth for column captions and for every number quoted.