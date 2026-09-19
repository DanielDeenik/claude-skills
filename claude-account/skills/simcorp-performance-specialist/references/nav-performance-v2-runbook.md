# NAV Performance v2 — Shadow Asset Portfolio Build Runbook

**Source:** `🛠️ NAV Performance v2 — Build Runbook (What to Configure)`, Notion,
created 10 Jun 2026, child of `📈 NAV Performance — Temporary Solution Design
(v2, Shadow Asset Portfolios)`. Traced to `NAV Performance - Temporary solution
design at Nicola.docx`. Values shown in backticks are taken verbatim from the
design doc; `<…>` are per-fund/client placeholders.

## What this design is for

A **temporary solution** for calculating Performance on structures that lack a
native Asset-type portfolio to hang TWR calculation off (PE-style structures).
It creates dummy "shadow" Asset portfolios purely to carry fixed-nominal
fund-certificate positions that isolate TWR to NAV/GAV price movement plus
dividends — decoupled from the real liability portfolio's subscription/
redemption activity.

## Build order

1. **Portfolio group type = `Performance`** (technical)
2. **Parent dummy portfolio group `PE_NAV`** — all shadow portfolios grouped
   under it
3. **Shadow Asset portfolios**, one per fund share class: type `Asset`,
   Accounting principle `FO_L`, ID `PE_<portfolio liability Id>`, group
   `PE_NAV`. ❓ **CONFIRM**: creation method (flat-file upload vs. manual) —
   not specified in the design doc
4. **Assign Investment Structure** to each shadow — enables historical upload
   to IAP. ❓ **CONFIRM**: which specific IS to assign — the doc says one must
   be assigned but doesn't name it
5. **Holding keys `NAV_NET` / `NAV_GROSS`** — the doc labels these the "Model
   Portfolio" holding key, but is explicit this is **a position-level
   segmentation tag, not a strategy/target Model Portfolio** in the
   asset-allocation sense. **This is a genuine naming collision worth flagging
   any time someone asks "does v2 use Model Portfolio tagging" — the answer
   is "yes, but not the kind you're probably thinking of."** ❓ **CONFIRM**:
   mechanism — the validated Part B runbook (for other Performance designs)
   achieves a model-portfolio split via transaction stamping / Financial
   Accounting Principles; unclear whether v2 uses genuine MP stamping or a
   holding-segment key instead
6. **Price types**: `Fund NAV` (drives Net) and `Fund GAV` (drives Gross) —
   both must be populated in the Prices window or performance can't calculate
7. **Pricing profile**: `NAV_NET` → Fund NAV price type; `NAV_GROSS` → Fund
   GAV price type
8. **Two fund-certificate positions per shadow**, fixed at `1,000,000` units,
   unchanged over time (establish via opening-balance transaction, no ongoing
   balance changes — do NOT replicate real fund issues/redemptions).
   ❓ **CONFIRM**: which fund certificate instrument backs each position
9. **Distributions** via standard asset-servicing/corporate-action workflow —
   dummy portfolios must be included in the CA workflow (the one workflow
   they must be in)
10. **Performance calc & TWR**: two IAP measures, Net TWR (holdings tagged
    `NAV_NET` only) and Gross TWR (`NAV_GROSS` only). ❓ **CONFIRM**: division
    of labour — prior design ran SCD Performance engine then pushed to IAP via
    API; v2 states TWR is calculated **in IAP on the fly** — unclear whether
    SCD Performance module still runs or IAP consumes holdings directly
11. **Batch job group `PE_PM_WORKFLOW`** — shadows included automatically, no
    extra config
12. **Exclusions**: exclude dummy portfolios from ALL reconciliation
    workflows and settlements; the one workflow they must be in is the
    corporate-action workflow (step 9)
13. **Historical performance upload** directly into IAP (requires IS from
    step 4)
14. **Verification checklist** (10 items) — group/portfolio naming, exactly 2
    fixed-nominal positions per shadow, pricing resolution, TWR production,
    cash-flow isolation (test subscription/redemption must NOT move the
    shadow position), distribution flow, reconciliation/settlement
    exclusion, batch pickup, DWH-not-IAP reporting (IAP market value is
    non-representative due to fixed nominal), historical upload success

## Open items table (all 5, as of the source doc)

| # | Open item | Needed for step |
|---|---|---|
| 1 | Portfolio creation method (flat-file upload vs manual) | 3 |
| 2 | Which Investment Structure to assign | 4 |
| 3 | Holding-key mechanism (model-portfolio stamp vs holding segment) and where it's set | 5, 7 |
| 4 | Backing fund-certificate instrument per position | 8 |
| 5 | Calc topology — SCD Performance engine + API vs IAP direct | 10 |

**Any question about this design that touches one of these five items should
be answered as "open, unconfirmed" — not resolved by inference from generic
SimCorp Performance-module knowledge.** The design doc itself flags these as
unresolved; a future session finding an answer should update this file and the
source Notion page together, not just answer verbally.
