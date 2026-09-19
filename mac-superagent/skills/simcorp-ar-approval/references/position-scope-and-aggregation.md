# Position scope, the roll up arithmetic, and the two review gates

Verified against the Household Orders for Approval grid captured 3 September 2026 at 11:40, sub layout New_AR_Approval, household filter Contains Household Name mark, status bar showing one order with three failures and twenty one passes. Field identities from the AR APPROVAL layout export read 1 September 2026.

## What the annotation is

Position scope is not assigned. The system builds it per row by listing which position types exist on that holding key, joined with a plus. Four types appear in this flow.

- Pf, a real portfolio position. Brings current weight.
- Order, a pending or released order on the same key. Split onto its own line so the reviewer sees it. Whether it moves the weight depends on the simulation setting, see gate two.
- Dec, a decomposition row, the look through of a fund holding into its underlying components. Brings weight and, unless a model line lands on the same key, no target. The decomposition reading is evidenced by the arithmetic below and by the daily decomposition chain at this client; it is not quoted in that wording in the manuals read, so mark it as evidenced rather than cited.
- Mp, a model portfolio component. Brings the target only and never any current weight.

The other six product types (watch list, preliminary, benchmark, benchmark only sum, simulation, surveillance) do not appear in this flow.

## The ten annotations seen, and what each does to the deviation

Pf+Order+Dec+Mp, everything present, a true deviation.
Pf+Order+Dec, no model line, target blank, the whole weight reads as a deviation.
Pf+Dec+Mp, held and decomposed and modelled, a true deviation.
Pf+Mp, the plain case and the cleanest to trade on.
Pf+Dec, no model line, a model gap not a trade.
Dec+Mp, nothing held directly, exposure only through look through, a true deviation that cannot be traded directly because it lives inside a fund.
Dec, look through only with no target, usually a classification gap.
Mp, model only, the pure underweight, deviation is minus the target. Invisible if the grid is filtered to orders.
Order+Mp, an order on a modelled key not yet held.
Order, an order alone with no holding and no model line, usually cash or an unclassified instrument.

## The roll up rule, proved

The subtotal is a plain sum of its scope rows. Nothing is netted or weighted, and a blank target counts as zero. Worked on Investment Grade Bonds, 3 September:

Dec, weight 1.02, target blank, contributes plus 1.02.
Mp on NWM220, weight 0.00, target 14.37, contributes minus 14.37.
Order+Mp on NWM220, weight 0.02, target 0.02, contributes 0.00.
Pf+Mp on NWM220, weight 16.39, target 9.56, contributes plus 6.84.
Sum: weight 17.43 against a shown 17.44 on rounding, target 23.95 exact, deviation minus 6.51 exact.

Consequences. The headline minus 6.51 is three different stories, so a reviewer sizing a trade on the subtotal alone buys the wrong amount. An unmatched Dec row always pushes the deviation positive, so look through gaps consume band capacity that real overweights need. The household total is forced to 100.00 and its deviations to zero by the household rescaling, so that zero is a construction check and never evidence that the household is on target.

## Gate one, is the number even a trade

Rows with a blank target are a model or classification gap, not an overweight. One captured household carried seven of them: International REITs 3.77, Venture Capital 0.70, Alternative Strategies 0.17, Diversified Private 0.14, Environmental Social and Governance 0.05, Missing minus 0.01, N.A. minus 0.02. International REITs alone is a 3.77 point false breach. N.A. means the classification tag is unmapped and Missing means the position is out of segment. Route these to the data owner and keep them out of the trading conversation.

## Gate two, is Post-Sim actually post trade

On 3 September, Post-Sim equalled Pre-Sim on every row of the household including the order rows, exactly as in the 2 September demonstration. The known cause is the Settings Template option that disables simulations in distribution set fields, on the System Performance tab, selected by default. Until it is cleared, approving on Post-Sim is approving on a pre trade number. Check it before every run.

## Band entry, reconciled

The Conditional Format dialog takes the numbers as they read on screen: Not Between 3 and minus 3. The layout file stores them as fractions, which is why an export of an earlier state shows 0.02 for a two point band. Both facts are true and there is no conflict; type 3.

## Compliance counter on the status bar

The status bar reports the latest check, the order count, and the failure and pass counts. On 3 September at 11:40 it read one order, three failures and twenty one passes. Three plus twenty one is twenty four, exactly the number of sub asset class rows in the household on screen, so a rule is evaluating per sub asset class. The grid banded nine of those rows, so the rule and the grid band do not agree. Before quoting either number, obtain the rule name, its limits, and whether it skips rows with no model component.

## Open items carried

Does a decomposition row add to the fund holding or replace it in the denominator; test on a household holding a single fund with Portfolio added to the grouping. Which level the compliance rule should evaluate at, per portfolio or household aggregate or both. What a reviewer does with a household that still breaches after the orders, which has never been answered and is the rule the approval step turns on.
