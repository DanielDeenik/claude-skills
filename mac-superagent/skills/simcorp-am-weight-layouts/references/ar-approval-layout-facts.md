# AR APPROVAL layout, verified field facts

Read directly out of the exported layout file AR_APPROVAL.xml on 1 September 2026 (Layouts Version 26.04, ExportVersion 4.0, Layout name AR APPROVAL, Guid db532fe1-731a-408d-b2a8-9c23a975ba06, owner number 94, 6.27 MB). Everything here is from the export, not inferred. Use these names verbatim; do not re invent them.

## The five weight columns are rescaled fields

A layout records a rescaled key ratio by appending the distribution set GUID to the delivered field name. In the Household Summary all five weight columns carry the SAME suffix d73b5589-b7cd-46bd-a201-3fa7ba3abe73, whose GridDistributionSetsCollection FieldNamePath is CustomField@Household Name. So every weight in that view is rescaled so each household is its own 100 percent, which is why a household row reads exactly 100.00 and the deviations sum to zero at household level.

| Screen caption | Internal name | Meaning |
|---|---|---|
| Current Weight (%) Pre-Sim | DirtyValueDistributionPreSimulation + set | weight before simulation, includes released orders |
| Simulation Weight (%) | DirtyValueDistributionSimulation + set | the simulation impact |
| Current Weight (%) Post-Sim | DirtyValueDistribution + set | weight after orders and simulations, the input cell |
| Target Weight (%) | ModelDirtyValueDistribution + set | the MODEL portfolio weight, captioned Target Weight (TAA) on a sibling sheet |
| Deviation from Target (%) | ModelActiveBet + set | post weight minus model weight in percentage points |

CONSEQUENCE, settled: the client target is model fed and the client deviation column IS the delivered model active bet. No user defined key ratio, no formula. The matching compliance rule is therefore Compare with model, not a list or an external value.

## Distribution sets registered in the layout

d73b5589-b7cd-46bd-a201-3fa7ba3abe73 Household Name (drives all five live columns)
3ca8774e-a42e-40c3-b123-00148b61d4c5 PortfolioId (ModelActiveBet variant already generated, no caption, no format: this is the untitled truncated column seen on 31 August)
f9143f23-ff50-47a0-84ab-8bb0818c52b5 Sub Asset Class and Portfolio together (only one Selection Field is ever used, so this set does not do what its name suggests)
1f6e5461-2d2d-4ca3-a533-0980f8216531 Model portfolio
6359a33f-2ce4-4e4d-95e7-0dbc200ae059 Portfolio group name
dead7743-f47a-4035-a476-a7a6399046c0 Custom field on portfolio
Several further model portfolio and portfolio group sets exist with filtration on.

To build a per portfolio view, add the Portfolio rescaled variants of the other four fields; only the deviation exists today.

## Conditional format, and the unit trap

The live band on the deviation column is stored as: Condition NotBetween, FirstLimit -0.02, SecondLimit 0.02, UseBackColor true with ARGB -272971 (pink), UseImage true with ImageName Failed (the red dot), ApplyToDataCells and ApplyToSummaryCells true, GroupFieldNames All. Sibling sheets carry variants: LessOrEqual 0.03 with a red font, Less than 0 with Arrow_good and Greater than 0 with Arrow_bad, and a Greater than 0.02 with a Good image on the current weight column.

LIMITS ARE FRACTIONS, NOT DISPLAY PERCENTAGES. 0.02 flags at two percent on screen. A three percent band is entered as -0.03 and 0.03. Entering 3.00 sets a three hundred percent threshold and the column never flags. This is the most likely build error on this layout.

OPEN CONFIRMATION: the export carries -0.02 and 0.02 while the 1 September screen leaves 2.56 and 1.73 unflagged and flags 4.21 and 7.27, which is three percent behaviour. Either the live grid was changed after the export or a second format applies. Confirm in the live layout before quoting the stored value.

## Grid structure

Ordered sortings: Household Name descending, Sub Asset Class ascending, GroupID, PortfolioId, Node level 3, Node level 2, Node level 4 descending. Group count three. PortfolioId is already in the grid but hidden, so adding Portfolio as a grouping level only needs it shown. Sub Asset Class is the grid field GroupCode.$ID=Sub Asset Class###, a security group code, which is exactly what the compliance For each statement can group on.

AlignmentTargetFieldName is ActiveBetBenchhmark (benchmark active bet, spelling as stored), so the alignment ribbon targets the benchmark rather than the model. Check before using To Model or To Benchmark for target driven rebalancing.

## Deliverables built from these facts

NWM_AR_APPROVAL_PerPortfolio_Layout_Build_2026-09-01.xlsx in `i. Client - Nicola Wealth/Performance Testing/` carries the field map, the eight build steps, the conditional format values and six verification checks.
