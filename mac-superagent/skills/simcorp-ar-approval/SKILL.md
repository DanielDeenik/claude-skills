---
name: simcorp-ar-approval
description: "Run, co-pilot, or document the Nicola Annual Review (AR) approval flow in SimCorp Asset Manager NONPROD: load an approval group, build the rescaled-by-household review grid, band the deviation from target, read the position scope split per household, then validate and approve or release the orders. Use for AR Approval, approval groups, Household Orders for Approval, deviation from target review, position scope questions, or UAT and training material for any of these."
---

# SimCorp AR Approval (Nicola NONPROD)

Annual Review approval: a reviewer takes one approval group (a batch of households assigned to that reviewer), sees where each household deviates from its model after the pending orders, and approves or releases the orders that pass. Captured from a live demonstration in the Nicola NONPROD environment on 2026-09-02 (Citrix HTML5 client at nicola-sso.simcorpcloud.com, NONPROD-User tab, SimCorp Dimension via Asset Manager). Two uses:

1. Execute or co-pilot: drive or guide the flow live in the Citrix session. SimCorp Dimension here is a Citrix-hosted Windows app with no API surface, so live execution goes through the browser or computer-use tools against the Citrix tab. Verify each stage before the next.
2. Document: UAT test cases, runbooks, defect repro steps, training notes. Use the exact object names below; never invent IDs, field names or paths. Screenshots are the source of truth for client specific column captions.

Theory of the rescaled fields, distribution sets and aggregation lives in simcorp-am-weight-layouts. Every Position scope annotation, the roll up arithmetic and the two review gates live in references/position-scope-and-aggregation.md; read it when a number looks wrong. Enforcement of the band as a compliance rule lives in simcorp-compliance-rules. The fund order to Aviso export chain lives in simcorp-mf-order-flow.

## Inputs to confirm before starting

Never hardcode these; ask when the task does not state them.

- Layout: the demonstration used the AR APPROVAL layout with sub layout Approval Layout (status bar shows New_AR_Approval). Tabs: Household Orders for Approval, Cash Viewer, Order Outbox.
- Approval group: Data Selector, Load Portfolios node holds 0. All, 1. Approval Group, 2. Approval Group, and FO_LOAD_GROUP10 upward. Ask which group the reviewer owns.
- Band: the deviation band in percentage points. Suggest 3 (the NWM convention, matching the SAC target band compliance rule) but confirm per run.
- Decision rule for approval: what a reviewer does with a household that still breaches after orders (approve anyway, hold, send back). This was not demonstrated; ask and record the answer in the deliverable.

## Stage 1: See the population

1. Asset Manager, Data Selector tab. Under Load Portfolios select 0. All, then Tools, Show Portfolios. The dialog lists every portfolio in scope with Portfolio (codes of the form 6DNxxx_MARG, _RRSP, _TFSA, _LIRA, _RESP, _CASH), Portfolio group (G000nnnnn, the household), Name (NBIN Client# ... - OPEN, RRSP, TFSA, LIRA, RESP-FAM) and Currency (CAD in the demo). Use it to confirm which households are in the run and which accounts each household holds; OK closes it.
2. Loading 0. All returns an empty grid in the demo (the layout only populates for an approval group), so do not treat an empty grid after 0. All as a defect.

## Stage 2: Load the approval group

1. Data Selector, Load Portfolios, select the approval group (demo: 1. Approval Group), Selection, Load. The window title changes to AR APPROVAL - 1. Approval Group and the Household Orders for Approval tab fills; the Order Outbox tab shows the pending order count (278 in the demo).
2. Grid grouping as delivered: Household Name, Sub Asset Class, Position scope. Default columns: Household Name, Sub Asset Class, Position scope, Portfolio group, Security ID, Dirty value distribution, pre-simulation, Dirty value distribution, Dirty value distribution (model), Active bet (model).
3. Gotcha: with the default (non rescaled) fields every household shows a different total (1.61, 6.88, 2.36 and so on) because the denominator is the whole data selection, not the household. Those numbers are not comparable across households and the band cannot be applied to them.

## Stage 3: Rebuild the grid on rescaled fields

Right-click any column header, Select Fields. In Available Fields type the field name into the filter box, select the row, and use the right arrow to add; select a row in Selected Fields and use the left arrow to remove. Category of every rescaled field is Key Ratios-Rescaled; the pre-simulation base field sits under Key Ratios-Pre Simulation.

Replace, one for one:

| Remove | Add |
|---|---|
| Dirty value distribution, pre-simulation | Dirty value distribution, pre-simulation rescaled by household name #1 |
| Dirty value distribution | Dirty value distribution rescaled by household name #1 |
| Dirty value distribution (model) | Dirty value distribution (model) rescaled by household name #1 |
| Active bet (model) | Active bet (model) rescaled by household name #1 |

After the swap every household row reads 100.00 in the three weight columns and 0.00 in the active bet column. That is the check that the household is now its own 100 percent. A household whose weight column reads 100.00 but whose model column is blank (Pacific Academy Household in the demo, position scope Pf+Order only) has no model weights, which is a data issue for the modelling preparation job, not a layout issue.

Captions: the layout later carried reviewer friendly captions for the same four fields: Current Weight Pre-Sim, Current Weight Post-Sim, Target Weight (%), Deviation from Target (%). Set captions on the Field Properties General tab; keep the underlying field the rescaled one.

## Stage 4: Band the deviation

1. Right-click the Active bet (model) rescaled by household name #1 column, Edit Properties, Conditional Format tab, New.
2. Condition Not Between, Value of the band (demo: 3) and the negative band (demo: -3). Tick Apply to data cells. On the Colour tab tick Use colour and Apply to row, pick the background. OK.
3. Put the band ONLY on the rescaled deviation column. On a weight column every 100.00 lights up.
4. Expand a household (demo: Yan Wang Household, G00015112). Breaching sub asset class rows light up; in the demo International REITs 18.04, Canadian Equity -3.48, US Equities -4.50, Diversified Private 7.69 and Global Small Cap -14.49 were outside plus or minus 3 while the household row itself stayed 0.00.

## Stage 5: Read the position scope split

Position scope is the third grouping level and names the set of position types present on one holding key: Pf held, Mp in the model, Order a pending order, and combinations when more than one exists on the same key. Expanding a sub asset class row splits its deviation by scope. Worked example, Yan Wang Household, US Equities (Pf+Order+Mp, Pre-Sim 4.69, Target 9.19, Deviation -4.50):

- Mp only, NWM240: target 6.89, nothing held on this key, contributes -6.89. This is the underweight row; a grid filter that keeps only Order rows hides it.
- Order, NWM241: Pre-Sim 0.00, Post-Sim 0.00, deviation 0.00. The order is split out on its own line so the reviewer sees where the order sits, but it carries no weight into the rescaled columns.
- Pf only, NWM241: held 0.41, no target, contributes +0.41.
- Pf+Mp, NWM240: held 4.28 against target 2.30, contributes +1.99.

Verification: the scope rows must sum to the aggregate within rounding (-6.89 + 0.00 + 0.41 + 1.99 = -4.49 against -4.50). If they do not, a scope row is filtered out or the grouping is not on Position scope.

The same security appearing on an Mp only row and a Pf+Mp row inside one household is consistent with the household being a group of several portfolios (MARG, RRSP, TFSA) where one portfolio holds it and another only has it in the model; add Portfolio to the grouping to confirm before stating it.

Gotcha, order impact: in the demo Post-Sim equalled Pre-Sim on every row including the Order row, so the pending orders were not flowing into the rescaled fields. The known cause is the Settings Template option Disable simulations in distribution set fields (System Performance tab), selected by default, which makes rescaled fields ignore orders and simulations until it is cleared. Check that setting before reading Post-Sim as post-trade, and before approving on the strength of it.

## Stage 6: Validate and approve or release

Not demonstrated in the recording; mechanics taken from the Order Outbox stage of simcorp-mf-order-flow and to be confirmed on first live run.

1. Order Outbox tab, select the pending orders for the households under review. Compliance, Validate, and read the Compliance Results panel.
2. Apply the decision rule agreed in the inputs: households whose post-order deviations sit inside the band and pass validation are approved or released (Approve/Release moves them from Pending orders to Working orders); breaching households are held or sent back per the rule.
3. Record, per household: group code, breaching sub asset classes with deviation, decision, and who decided. That record is the AR approval evidence.

## Verification checklist

Before declaring a group done: approval group loaded and title shows it; every household row reads 100.00 on all three weights and 0.00 on deviation; band applied only to the rescaled deviation column with the agreed value; scope rows of at least one breaching sub asset class sum to its aggregate; the simulation setting checked so Post-Sim is trustworthy; orders validated; decisions recorded per household; released orders in Working state.

## House style

Full sentences, no dashes, middots, arrows or maths glyphs in deliverables, roles and teams never individual client names in shared material (household names in this environment are test data but still do not repeat them outside the working session), and screenshots are the source of truth for column captions.