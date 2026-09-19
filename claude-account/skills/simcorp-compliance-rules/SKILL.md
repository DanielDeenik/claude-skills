---
name: simcorp-compliance-rules
description: "Build and govern Compliance Manager rules, with the sub asset class target band as the worked pattern."
---

# SimCorp Compliance Rules

Build Compliance Manager rules that enforce or investigate portfolio construction limits, with alerts, pre trade validation and audit, instead of grid formatting. Grounded ONLY in the local manuals `ii. Manuals & Documentation/PDFs/cmmgr.pdf` (Compliance Manager user manual, March 2026), `cmrbg.pdf` (Rule Building Guide, September 2025), `amgsg.pdf` (Asset Manager Getting Started, September 2025) plus environment screenshots. Never invent a window name, menu item, field or code; when a label is not in these sources, say so and mark it open. Treat NotebookLM or other synthesis output as claims to check against these manuals, never as a source.

## The rule family map

1. Absolute rules restrict a key ratio in absolute terms (market value, duration).
2. Relative rules divide a numerator by a denominator. The percent notation on a measure is the short form; Relative to is the explicit form for unlike numerator and denominator. With the percent notation any grouping applies to the numerator only; the denominator stays all holdings of the assignment unit. Grouping on a Classification inside a Compare rule needs Relative to (cmrbg 3.10.2); a Security Group Code takes the percent notation (cmrbg 3.5).
3. For each adds grouping to absolute or relative rules. Grouping accepts attributes, security group codes, buckets, custom attributes and lists. Validation returns one pass or fail AND one alert per group.
4. Benchmark rules relate the portfolio to a benchmark. Compare with benchmark is the absolute difference in percentage points; Compare (%) with benchmark is the relative ratio. Model portfolio rules are identical with the model swapped in: Compare with model, Compare (%) with model, and the In model portfolio operator. The Model portfolio check box in Additional properties TICKED means a freely defined model; CLEAR means the TAA specified model of each portfolio (cmrbg 2.5).
5. Scale rules (Compare to scale with benchmark or model) vary the allowed deviation with the target weight through From weight (%) and Up to weight (%) rows, each with Fail above (pp) and Fail below (pp). An empty bound runs to infinity. A From weight threshold excludes tiny targets from evaluation.
6. Lists (Basic, Percentage, Amount) carry per attribute value limits. A Percentage list quoted in the For each statement gives every group its own band with the rule's own limit as the default for unlisted values. A list inside an In list condition is treated as Basic and its values are ignored. Percentage and Amount lists take a time series of limits via the From column.
7. Global rules live only in the Global rules node of the Rule Library, have Scope fixed to Aggregate, and are assigned via the Assignments tab or by dragging onto Hierarchy nodes. [min] and [max] in the rule name show each assignment's limits. Matrix lists give per assignment unit values only for portfolios, funds and model portfolios.
8. Verify Asset Allocation rules take limits from SAAM, check every Investment Structure node without For each, and are the ONLY documented pattern for decomposition across multiple portfolios: Decomposition property Fund Certificates, a decomposition profile with Model portfolio level set, SAAM on every portfolio and one shared Investment Structure (cmrbg 8.1, 8.1.1).

## The level rule (settles every across portfolios question)

Rules on higher levels than portfolio, such as aggregated rules on folders, households or business entities, can only use a benchmark or model specified directly on the rule (cmrbg 3.10). A TAA or client specific model therefore works only where the rule evaluates per portfolio: a rule created on a Hierarchy folder with Scope Portfolio, or a global rule assigned to individual portfolios. A business entity takes only global rules and legal sets, so its result is always one Aggregate figure for the whole entity and never per member portfolio (cmmgr 7.1, 7.5.7). The global rule note in cmmgr 7.5.8 cautions against portfolio specific benchmarks and Verify asset allocation on non matching assignment unit types.

## Worked pattern one: sub asset class target band, per portfolio

Rule created on the Hierarchy folder holding the portfolios (New Rule opens the Compliance Rule Entry window): Scope Portfolio, Rule type basis Holdings, Model portfolio check box clear for TAA. Criteria: Limit, percent notation on Dirty value, For each Sub Asset Class (the security group code fed by the Model Portfolio Tag), wrapped as Compare with model. Limits: Fail above 3.00 and Fail below 3.00 under the model weight, warnings optional. The manual's own benchmark example is this rule with GICS Sector and 5 point limits. Save as Draft, test, measure before activating. The 31 Aug 2026 build pack placed a global rule on households with the TAA model; per the level rule that assignment only works with a model specified on the rule, so use the folder rule for TAA targets. Files: NWM_DeviationBand_Build_Pack_2026-08-31.xlsx and NWM_DeviationBand_Rule_Mockup_2026-08-31.html in `i. Client - Nicola Wealth/Performance Testing/`, and the deviation-band-build reference of the canonical skill copy under `ix. SimCorp SuperAgent/skills/`.

## Assignment model

Households are the portfolio group nodes already in the Hierarchy. Business entities (Business Entities window, shared with Front Office, Risk and Performance) cross portfolio group boundaries: a portfolio belongs to zero to many, each entity carries its own rule set, membership is inspected via Open related, individual entities cannot be aggregated or expired manually, and an empty new entity is hidden. Per the level rule an entity or household rule takes a model specified on the rule only.

## Worked pattern two: look through order impact investigation

Same folder rule with Mode Pre-trade, Decompose Fund certificates and a Decomp. profile whose Model portfolio from level is filled, kept Draft. Draft rules are not validated until activated (cmmgr 7.5.10), so live orders are untouched. Run it from the Portfolio Sheet, Multiple Portfolio View or Single Security Targeting with Test on the COMPLIANCE ribbon: Test runs active and draft pre trade rules against simulations, preliminary transactions, orders and positions in the data selection, private and unsaved (amgsg 6.1). Read Compliance Results, Result Details, with Decomposed from security and Decomposed from instrument type added (cmrbg 9). Not documented and therefore proven by test: whether a fund certificate order is looked through in pre trade, and whether constituents map to the model's sub asset classes. Pack: NWM_LookThrough_OrderImpact_Rule_Build_Pack_2026-09-11.xlsx in the same folder.

## Decomposition settings

Branch default decomposition profile in Compliance Configuration, overridden per assignment unit (right click, Settings, Decomposition profile) and per rule (Decomp. profile). Decompose options include Alternative investments, Ccy futures, Fund certificates, Index CDS/CCDS, Index derivatives, Total return swaps and XpressInstruments. Keep the Asset Manager view and the rule on the same profile or the grid and the rule disagree by construction. Decompositions of large funds are a known pre trade performance inhibitor (cmrbg 13.15).

## Runtime and governance

Rule states: Draft (italics), Active, Future Active, Inactive, Expired. Post trade validation runs Active rules; Test also runs Drafts without saving results. Mode sets the contexts: Pre-trade, Post-trade, Online, Trading, Rebalancing. Pre trade validation covers holdings, proposed orders, generated simulations and working orders. The Priorities window maps rule priority and result type to the allowed pre trade action, so a rule can warn with override or block. Each failing group raises its own alert with Active and Passive classification. Online Compliance shows Free to max, Percentage of max (100 is at limit, 110 is breached by 10) and Fail above. Rules and lists carry four eyes and audit history.

## Hard rules

1. Never compute a weight or deviation in a Compliance Manager formula. User defined key ratios there are security level only, and .NET formulas aggregate strictly as the sum of holding level results.
2. Never place a normal rule in the Trading limits folder.
3. The compliance branch carries a mandatory Price and key ratios definition; align it with the front office key ratio setup. Adding a portfolio group to a branch is permanent.
4. Model and benchmark rules with many constituents grow the compliance result tables; client specific benchmarks grow them most. Measure with a Draft before broad activation, and use a denominator condition to optimise a slow relative rule before de scoping it.
5. This client's compliance engine has a latency history on simulations. No activation without a measured per order Validate delta on a test set, gated against an agreed budget.
6. House style on every deliverable: full sentences, no dashes, middots, arrows or maths glyphs, roles and teams never individual names.

## Scope boundary

General SimCorp Q&A belongs to simcorp-super-agent. The Asset Manager grid side of weights and deviations belongs to simcorp-am-weight-layouts. TWR and performance mechanics belong to simcorp-performance-specialist. Pricing profiles and price data quality belong to simcorp-data-management-specialist. Flow mapping and measured overlays belong to simcorp-fo-flow-architect. Service level tracing belongs to simcorp-service-tracing.

## Verification

Before shipping any rule design: every window, field and menu label traces to cmmgr, cmrbg, amgsg or a screenshot; the level rule is checked against the chosen assignment; the deviation output is checked for the zero sum property per assignment unit; the Draft and Test gate has been run; the deliverable passes the banned glyph grep.