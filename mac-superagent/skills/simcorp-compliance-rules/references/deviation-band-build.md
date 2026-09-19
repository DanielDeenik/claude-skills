# Deviation band build, full detail

Worked pattern for the plus 3.00 and minus 3.00 percentage point band per sub asset class per portfolio at NWM. Sources: cmmgr March 2026 sections 7.5.4 to 7.5.8, 7.9 and 16; cmrbg September 2025 sections 3.4, 3.5, 3.11 and 3.12; amsim 3.7; environment captures 25 to 31 August 2026.

## Core rule, window entries

Rule Library, Global rules node, right click the folder, New Rule. In the Global Rule Definition window: Rule name SAC TARGET BAND [min] [max] pp (the tokens display each assignment's own limits). Rule type basis Holdings (Compare rules only work on Holdings). Scope Aggregate, fixed for global rules. Additional properties: select the model portfolio source; for TAA model weights floating with the market select Client specific, floating (TAA); models can also be attached under each portfolio in the Hierarchy (right click, Add model portfolio, sourced from Strategic Asset Allocation and TAA). Rule criteria: Limit, percent notation on Dirty value, For each Sub Asset Class, Compare with model. Compare with model is the absolute difference in percentage points; do not use Compare (%) with model, which is the relative ratio. Limits: Fail above 3.00, Fail below -3.00, Warn above 2.00 and Warn below -2.00 optional. Save as Draft, run Test validation, activate only after the performance gate.

Expected validation output: one pass or fail per sub asset class per assignment unit, with portfolio weight, model weight and the difference in the result details, and one alert per failing group post trade.

## Scale variant

Compare to scale with model adds From weight (%) and Up to weight (%) columns to the Limits section. Single row pattern: From weight 1.00, Up to weight empty, Fail above 3.00, Fail below -3.00. Model weights of at least 1.00 percent are held to the band; smaller targets are not evaluated. An empty bound runs to infinity. Extra rows create tiered bands per weight interval, each evaluated separately.

## List fallback, only if the target is not model fed

Attribute Configuration: select Selectable in lists on the Sub Asset Class attribute. Lists window from the Rules ribbon: New on the Sub Asset Class folder, List type Percentage, per value minimum target minus 3 and maximum target plus 3, time series via the From column. Attach the list to the For each statement of a plain relative rule through the Attributes List window (sort the Type column to show lists). Enter the rule's own default limit for unlisted values. Add the No empty groups from lists element if empty groups must not report. Trap: a list inside an In list condition is treated as Basic and its values are ignored. If targets live outside SimCorp entirely, the External Values window imports externally calculated key ratios per portfolio for rules; external values are not reachable from Compliance Manager .NET formulas.

## Assignments

Households: assign the global rule to the household portfolio group nodes via the Assignments tab, the Edit Global Rule Assignments command, or by dragging onto the Hierarchy. Wider bands per household as individual limits on the assignment. Mandate tier: one business entity per mandate value; the entity carries the mandate wide rule set; membership via Open related. Constraints: business entities cannot be aggregated, global rule scope is fixed to Aggregate, matrix lists apply only to portfolios, funds and model portfolios.

## Data preconditions, all must pass before activation

1. Model weights populated daily by the modelling preparation job; no all zero model columns.
2. Sub Asset Class tag complete; N.A. means the tag is unmapped, Missing means out of segment.
3. The Sub Asset Class attribute appears in the For each picker; Selectable in lists only needed for the list fallback.
4. Branch valuation aligned: the compliance branch's Price and key ratios definition must produce the same dirty values as the front office setup on a sample household.
5. No price check exceptions on in scope portfolios on the validation date; missing prices misstate every weight.
6. The target source confirmed once from the Target Weight field properties; it decides the core rule against the model versus the list fallback.

## Performance gate

Context: the client compliance engine has a simulations latency history (231 incidents, median near 100 seconds) and the August 2026 order baseline ran with zero rules, so no baseline includes a live band rule. Steps: Test validation on a ten order set with the rule in Draft (results not saved); activate on one household and repeat; assign to all households and repeat; record wall clock per Validate and per Release each time. If deltas need explaining, run the service tracing procedure from simcorp-service-tracing (tracing is set at service startup and dies with the service; verify the activation entries in the service log before testing). If slow, apply a denominator condition to optimise the relative rule before de scoping. Decision gate: activate mandate wide only inside the agreed per order budget; otherwise run post trade only, where alerts still fire, and keep the pre trade check on the grid colour flag.

## UAT cases

TC1 in band pass: simulate a variance inside the band, create the fund trade order, Validate; the rule passes every group and Release lands in Working orders. TC2 overweight breach: variance beyond plus 3 on one fund; the rule fails that group only and the pre trade action matches the Priorities configuration. TC3 underweight breach: sell a group more than 3 points below its model weight; the rule fails on the underweight side, which the grid shows on the model side rows. TC4 post trade alert: release a breach and run post trade validation; exactly one alert for that group on that household. TC5 grid agreement: the rescaled active bet column and the rule result details name the same breaching groups with the same deviation within rounding. Confirm the UAT portfolio group and fund set before running; recorded demo objects are the demonstrated instance, not defaults.

## Verified example, household G00003896, 31 August 2026 TEST

Portfolio weights 16.02, 0.00, 0.00, 83.98, 0.00 against model weights 0.00, 0.00, 33.78, 43.88, 22.33 give differences 16.02, 0.00, -33.78, 40.10, -22.33 which sum to 0.01, zero within rounding. Four of five groups breach a 3 point band. The mockup page NWM_DeviationBand_Rule_Mockup_2026-08-31.html renders this example.

## Scope, how the rule works across portfolios (cmrbg Getting started, Scope section)

The Scope field decides what one assigned rule evaluates. Aggregate sums every portfolio beneath the assignment into one evaluation (the manual example: portfolios of 10, 30 and 20 under one folder against Fail above 25 aggregate to 60 and the rule fails once). Portfolio group evaluates individually per portfolio group under the folder. Portfolio evaluates individually for each portfolio and fund under the folder, each with its own separate result and alert, which the manual calls an efficient way of having one centrally maintained rule apply to many portfolios. Global rules are FIXED to Aggregate; the Usage button can exclude single portfolios from an Aggregate rule. Directly assigned rules are ALWAYS Scope Portfolio for pre trade performance, so the rule does not validate holdings outside the portfolio in which the order or simulation is created.

Consequence for the band: a global rule on a household node evaluates the household as one aggregated portfolio, one band result per sub asset class for the household total. For the band per portfolio within its own 100 percent, matching the rescaled by portfolio column, create the rule ON A FOLDER in the Hierarchy with Scope Portfolio instead of using a global rule; each portfolio then gets its own pass or fail per sub asset class against its own model. Trade off: the [min] and [max] individual limits per assignment exist only on global rules, so per portfolio bands with different widths need lists or separate rules. How Compare with model resolves the model when several portfolios with different models aggregate at group level is NOT stated in the manuals read; treat group level model comparison as unverified and prefer Scope Portfolio, where each portfolio pairs with its own model source.

## Order impact in the evaluation

Rule type basis Holdings: during pre trade and post trade validations Compliance Manager considers orders and simulations as EQUIVALENT to holdings, so the band always evaluates the post order weight. Pre trade fires in Asset Manager when the order or simulation is created or validated; pre trade triggers can reduce group level evaluation scope. Conservative pre trade validation (Compliance Configuration, Pre trade section, Use conservative checks): released working orders whose exposure sign moves the value AWAY from the limit are excluded from the check and shown in the Excluded by conservative check folder of Compliance Details, with a Conservative check column in the Pre trade Monitor. Automatic detection reads the exposure sign against Fail above or Fail below; for a rule with BOTH set, like this band, force the behaviour per rule in Additional Properties, Conservative pre trade behaviour (Default, Minimum, Maximum, Off). Recommendation for the band: set it explicitly, or Off, because automatic sign detection is designed for one sided limits and a sell that reduces an overweight must still count on the underweight side. Grid agreement: the Asset Manager rescaled columns ignore orders and simulations until the Settings Template option Disable simulations in distribution set fields is cleared; clear it or the grid and the rule disagree about open orders.
