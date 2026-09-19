---
name: simcorp-compliance-rules
description: Build and govern Compliance Manager rules in SimCorp Dimension for NWM, with the sub asset class target band as the worked pattern. Covers rule structure (absolute, relative, For each grouping, Compare with benchmark or model, scale rules), lists with per group limits, global rules with per assignment limits, business entities, the Limits section, rule states and Test validation, Priorities and pre trade actions, alerts, Online Compliance, branch valuation, and the documented dead ends. Trigger on compliance rule, rule building, Compare with model, active bet limit, deviation band, target band, concentration rule, For each, rule list, matrix list, global rule, business entity, assignment unit, trading limit, pre trade validation, compliance alert, Online Compliance, rule library, cmmgr, cmrbg.
---

# SimCorp Compliance Rules

Build Compliance Manager rules that enforce portfolio construction limits, with alerts, pre trade validation and audit, instead of grid formatting. Grounded ONLY in the local manuals `ii. Manuals & Documentation/PDFs/cmmgr.pdf` (Compliance Manager user manual, March 2026) and `cmrbg.pdf` (Rule Building Guide, September 2025) plus environment screenshots. Never invent a window name, menu item, field or code; when a label is not in these sources, say so and mark it open.

## The rule family map

1. Absolute rules restrict a key ratio in absolute terms (market value, duration).
2. Relative rules divide a numerator by a denominator. The percent notation on a measure is the short form; Relative to is the explicit form for unlike numerator and denominator. With the percent notation any grouping applies to the numerator only; the denominator stays all holdings of the assignment unit.
3. For each adds grouping to absolute or relative rules. Grouping accepts attributes, security group codes, buckets, custom attributes and lists. Validation returns one pass or fail AND one alert per group.
4. Benchmark rules relate the portfolio to a benchmark. Compare with benchmark is the absolute difference in percentage points; Compare (%) with benchmark is the relative ratio. Model portfolio rules are identical with the model swapped in: Compare with model, Compare (%) with model, and the In model portfolio operator.
5. Scale rules (Compare to scale with benchmark or model) vary the allowed deviation with the target weight through From weight (%) and Up to weight (%) rows, each with Fail above (pp) and Fail below (pp). An empty bound runs to infinity. A From weight threshold excludes tiny targets from evaluation.
6. Lists (Basic, Percentage, Amount) carry per attribute value limits. A Percentage list quoted in the For each statement gives every group its own band with the rule's own limit as the default for unlisted values. A list inside an In list condition is treated as Basic and its values are ignored. Percentage and Amount lists take a time series of limits via the From column.
7. Global rules live only in the Global rules node of the Rule Library, have Scope fixed to Aggregate, and are assigned via the Assignments tab or by dragging onto Hierarchy nodes. Individual limits per assignment are shown by [min] and [max] tokens in the rule name. Matrix lists give per assignment unit values but only for portfolios, funds and model portfolios.

## The worked pattern: sub asset class target band

One global rule: name SAC TARGET BAND [min] [max] pp, Rule type basis Holdings, model portfolio source in Additional properties (Client specific, floating (TAA) for floating TAA weights). Criteria: Limit, percent notation on Dirty value, For each Sub Asset Class (the security group code fed by the Model Portfolio Tag), wrapped as Compare with model. Limits: Fail above 3.00, Fail below -3.00, warnings optional at 2.00 and -2.00. The manual's own benchmark example is this rule with GICS Sector and 5 point limits. Save as Draft, run Test validation (Draft results are not saved), measure before activating. Full step detail, the scale variant, the list fallback and the UAT cases live in references/deviation-band-build.md and in NWM_DeviationBand_Build_Pack_2026-08-31.xlsx in `i. Client - Nicola Wealth/Performance Testing/`.

## Assignment model

Households are the portfolio group nodes already in the Hierarchy. Business entities (Business Entities window, shared with Front Office, Risk and Performance) are portfolio groups that cross portfolio group boundaries: a portfolio belongs to zero to many, each entity carries its own rule set on top of the portfolio's own rules, and membership is inspected via Open related. Documented limits: individual business entities cannot be aggregated, they cannot be expired manually, and an empty new entity is hidden until populated. Map the mandate tier to one business entity per mandate value.

## Runtime and governance

Rule states: Draft (italics, tested but not enforced), Active, Future Active, Inactive, Expired. Post trade validation runs Active rules; Test validation also runs Drafts without saving results. Pre trade validation of orders and simulations happens automatically in Asset Manager; the Priorities window maps rule priority and result type to the allowed pre trade action, so a rule can warn with override or block. Each failing group raises its own alert with Active and Passive classification. The Online Compliance applet shows Free to max, Percentage of max (100 is at limit, 110 is breached by 10) and Fail above for rules set up for online use. Rules and lists carry four eyes and audit history.

## Hard rules

1. Never compute a weight or deviation in a Compliance Manager formula. User defined key ratios there are security level only, and .NET formulas aggregate strictly as the sum of holding level results. The rule engine does the aggregation.
2. Never place a normal rule in the Trading limits folder; it takes trading limit rules only, which are pre trade only.
3. The compliance branch carries a mandatory Price and key ratios definition; align it with the front office key ratio setup or the two surfaces disagree on weights. Adding a portfolio group to a branch is permanent.
4. Model and benchmark rules with many constituents grow the compliance result tables; client specific benchmarks grow them most. Measure with a Draft before broad activation, and use a denominator condition to optimise a slow relative rule before de scoping it.
5. This client's compliance engine has a latency history on simulations. No activation without a measured per order Validate delta on a test set, gated against an agreed budget.
6. House style on every deliverable: full sentences, no dashes, middots, arrows or maths glyphs, roles and teams never individual names.

## Scope boundary

General SimCorp Q&A belongs to simcorp-super-agent. The Asset Manager grid side of weights and deviations belongs to simcorp-am-weight-layouts. TWR and performance mechanics belong to simcorp-performance-specialist. Pricing profiles and price data quality belong to simcorp-data-management-specialist. Flow mapping and measured overlays belong to simcorp-fo-flow-architect. Service level tracing belongs to simcorp-service-tracing.

## References

references/deviation-band-build.md carries the full band build: window entries, scale variant, list fallback, assignments, data preconditions, the performance test plan and the UAT cases.
