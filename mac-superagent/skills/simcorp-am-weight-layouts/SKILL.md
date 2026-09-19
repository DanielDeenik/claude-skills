---
name: simcorp-am-weight-layouts
description: Asset Manager weight and deviation layouts in SimCorp Dimension for NWM household views. Covers the dirty value distribution triplet (pre simulation, input cell, simulation), distribution sets and rescaled key ratios per grouping, the Aggregation setting (Across, Within, None) and what each permits, Position scope semantics, the weight denominator options, Key Ratio Definitions with derived difference and contribution fields, conditional formatting bands, and the zero sum verification for per portfolio deviations. Trigger on Household Summary, dirty value distribution, active bet, rescaled by portfolio, distribution set, weight impact, current weight, target weight, deviation from target, position scope, aggregation setting, portfolio sheet weights, simulation column, key ratio definition.
---

# SimCorp AM Weight Layouts

Build Asset Manager layouts that show weights, targets and deviations per portfolio, including the order and simulation impact before trading. Grounded in amgsg, ampab, amacf, amscn (September 2025), amsim (March 2026), the help portal, and NWM environment captures of 25 to 31 August 2026. The Household Summary applet is client specific and not in the manuals; its column names come only from screenshots.

## The weight impact triplet

Select Fields, category Values Standard: Dirty value distribution, pre simulation (weight before, already including orders), Dirty value distribution (the input cell), and Dirty value distribution, simulation (the impact, defined as the difference of the other two; amacf 5.3, ampab 5.1, amsim 2.4). Simulate either way round: type a nominal and read the weight move, or overtype the distribution cell with the wanted weight and the system back solves the nominal. The impact column exists only for simulations; there is no per order delta field in Values Standard, so simulate first, read the impact, then Create and Release (amsim 3.7 validates compliance automatically).

## Aggregation setting, amscn 1.1

Analysis Properties, General, Aggregation. Across position type merges everything on a holding key into one row and is the ONLY option that permits in grid simulation. Within position type gives one row per position type (the Order line sits apart from the Pf and Sim lines). None gives every position, order and simulation its own row. Split rows and typing a target weight cannot coexist: keep a working layout on Across position type and a review layout on Within position type or None.

## Distribution sets and rescaled fields, amgsg 4.10

A distribution set grouped on a field makes every grouping value its own 100 percent and generates rescaled by field copies of the view's analytics under Key Ratios Rescaled. Grouped on Portfolio, the rescaled active bet at a sub asset class row IS the deviation from target inside that portfolio's 100 percent. Traps: only one Selection Field of a distribution set is used; the Settings Template option Disable simulations in distribution set fields (System Performance tab) is selected by default, so rescaled fields ignore orders and simulations until it is cleared; grouping on Position scope puts model only rows in their own bucket. Alternative denominator without any distribution set: the Options ribbon Distribution figures setting flips the standard distribution fields to per portfolio (ampab 5.1). Mixed denominators in one grid (a per portfolio column beside a whole data selection column) are the usual cause of weights that disagree on scale.

## Position scope semantics

Ten position types: Wl, PreLim, Order, Bm only (sum), Pf, Bm, Sim, Sur, Dec, Mp. A watch list row is a simulation without a nominal and carries no weight impact; only Sim combinations do. Underweights against the model live on the Mp only rows, so a grid filter that keeps only Order rows hides every underweight; include Mp, Pf and their combinations when the full deviation picture is wanted. Grid sorting on the field uses internal values, not the displayed text.

## Key Ratio Definitions

The aggregation layer for weights is the Key Ratio Definition (numerator key ratio over denominator key ratio), not any formula. The Difference and contribution and Benchmark and model portfolio check boxes on the definition generate the derived comparison fields. Key Ratio Mapping formulas expose only security level fields in the picker (Dirty price, Instrument type and similar) and can never see a holding balance, a portfolio sum or a model weight; see simcorp-netformula for what .NET formulas expose and the property naming traps.

## Bands and verification

The band is conditional formatting on the deviation column: Edit Properties, Conditional Format tab, Greater than 3.00 and Less than -3.00 (amgsg 4.7). Put it on the rescaled deviation column, never on a weight column, where every 100 percent total lights up as noise. Verification for any per portfolio deviation build: the deviations across one portfolio's groups must sum to zero within rounding (verified 31 August 2026 on household G00003896: 16.02 plus 0.00 minus 33.78 plus 40.10 minus 22.33 equals 0.01). All model dependent columns read zero until the modelling preparation job has populated model weights; that is a data problem, never a layout problem.

## Reading a layout export instead of guessing

A layout export (Layouts XML from the layout manager) is the fastest ground truth for a client specific view. A rescaled key ratio is recorded as the delivered field name with the distribution set GUID appended, and each set is registered in a GridDistributionSetsCollection with the grouping field in FieldNamePath. Grep the export for the set GUIDs, then for field names carrying each suffix, and the denominator of every column is settled without opening the client system. Conditional format limits are stored as FRACTIONS in ConditionalFormatLayoutContainer (0.03 is a three percent band), which is the most common build error on these columns. references/ar-approval-layout-facts.md carries the verified field map, set GUIDs, format values and grid structure of the NWM AR APPROVAL layout, including the finding that Target Weight is ModelDirtyValueDistribution and Deviation from Target is ModelActiveBet, both rescaled by Household Name.

## Scope boundary

Enforcement of a band with alerts and pre trade actions belongs to simcorp-compliance-rules. .NET formula syntax and argument types belong to simcorp-netformula. TWR and performance mechanics belong to simcorp-performance-specialist. Pricing and missing prices belong to simcorp-data-management-specialist. The end to end fund order flow belongs to simcorp-mf-order-flow. House style on every deliverable: full sentences, no dashes, middots, arrows or maths glyphs, roles and teams never individual names, and screenshots are the source of truth for client specific column names.
