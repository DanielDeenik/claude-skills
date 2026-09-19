# Model Portfolio tagging vs. decomposition — mechanics

All facts below are grounded in the Nicola Wealth Notion Solution Architecture.
Page titles are cited so a future session can re-fetch and verify rather than
trust this summary blindly.

## 1. Generic Fund Admin service costs are NOT asset-portfolio positions

Per **Fund Admin Setup UM §2.3.1 (p.19)**, fund service costs are *"typically
not associated with any particular position or transaction"* — they flow
through **Fund Scheme line types** (Service cost, Cost distribution — L36
asset side / L31 liability side, `F_Specific - Fees in Classes`), not through
the asset portfolio's holding structure.

**Empirical confirmation at Nicola** (source: `§18.29.5.7 — Empirical Decomp
Analysis from Decomp.xlsx (NWM250)`, 2 Jun 2026): across Decomposition L1
(21 rows), L2 (943 rows), L3 (943 rows), and the post-decomp Asset Manager
view AM_ON (1,045 rows for NWM250_A), **zero ALM/service-cost items ever
appear** — even though raw View Positions on NWM250 shows 28 ALM items (14 per
class: ACCOUNTING_FEE, AUDIT_FEE, CS_TRUST_FEE, FS_FEE, FUNDSERV_FEE, GST,
etc.). This is not the Decomp Profile filtering them out — they simply aren't
on the asset portfolios that decomposition reads in the first place.

**Consequence:** since generic fund service costs structurally aren't
positions by default, they don't carry a Model Portfolio tag by default —
MP is a position-level attribute. BUT this has a real, working opt-in
override — see §1a immediately below — so don't conclude "can't have an MP"
without checking whether the override is configured.

## 1a. The opt-in override: Fund Administration Setup §4.1.8

**"Set up service costs based on model portfolio positions"** is the native
mechanism that DOES give a Fund Service Cost a Model Portfolio, by
apportioning it across the fund's actual current MP-tagged positions. This is
the correct first place to look for any "fund service cost not getting a
Model Portfolio" question — before assuming the item is structurally
excluded per §1.

- Config: a `Base cost on model portfolio` field — one row per Model
  Portfolio, for the same Fund + ALM security ID.
- Prerequisite: the Fund Scheme Line for that cost must have **Reporting
  Details enabled**, or the apportionment doesn't run regardless of the MP
  rows configured.
- **Important limitation: this apportions on the fund's ACTUAL/current MP
  positions, not SAAM/TAA target weights.** If a design calls for
  target-weight-based allocation (as in Sara Behzadi's Fund-of-Fund proposal,
  `performance-calc-fundamentals.md`), §4.1.8 does not do that natively —
  that would need to be a custom addition, not the out-of-the-box behaviour.
- **Verified working at Nicola, not just theoretical**: a screenshot from
  NWM250's decomposed view shows 13 of 15 ALM/service-cost lines correctly
  carrying `Model Portfolio: CASH_FI` through this exact mechanism — only 2
  (`GST`, `FUNDSERV_FEE`) come through blank. The fix for those two is
  narrow: add their missing `Base cost on model portfolio` row on the Fund
  Service Cost Definition, the same way the other 13 are configured — not a
  redesign.
- Related fields on the same setup family: **§4.1.10.1 Certificate class**
  on the Fund Service Cost Definition (if empty, the cost charges to the
  master asset portfolio instead of the correct class — a different failure
  mode, same screen area); **§4.1.5 Service Cost Groups**; **§3.11.2/§4.1.7**
  FoF difference costs + a prioritized Service Cost → target-fund-ALM mapping.

**This does NOT resolve the Private Debt OID/S-FEE items.** Those go through
the separate PD3 ALM mechanism in §2 below — §4.1.8 is a Fund Admin
mechanism for generic service costs (management fees, audit fees, GST,
FUNDSERV_FEE, etc.), not for `PD_FD_SRV_COST_SETUP` ALM securities. Don't
apply one fix to the other's problem.

## 2. The exception: Private Debt Fund Service Cost Setup DOES create tagged positions

Private Debt OID amortization and fee accrual use a **different, client-custom
mechanism** that has nothing to do with the Fund Scheme line types above:

- Treatment: OID booked as unearned revenue (`LN_DEF_REV` cost, vs. the
  alternative `LN_BV_ADJ` book-value-adjustment treatment) is recognized via
  an **ALM** (Charge/Credit ALM window) and amortized monthly through the
  **Fund Service Cost Setup window** — a client-custom DFS pair:
  `DM_ALMS_PD` (creates the ALM record) + `PD_FD_SRV_COST_SETUP` (amortization
  parameters: fund, ALM, from/to date, calculation setup, default amount).
- This ALM security (e.g. `OID-AcuityTL17`, or fee-accrual securities like
  `S-FEE-FRANKLINRL`) **is a real holding on a real portfolio**.
- Verified worked example (source: `§18.29.2 — OID Amortization + Pricing`):
  ```
  Security ID:      OID-AcuityTL17
  Security type:     SRVCOST  (Service Cost — used for ALM amortization)
  Fund:               PDDLSPV
  Portfolio:          PDDLSPV_A
  Model Portfolio:    PRIV_DEBT
  Monthly Amount:     -$239.85
  Unearned Revenue:  -$3,466.90 (current ALM balance)
  ```
- Source: `PD 16 · Costs & OID`, `PD Solution Architecture` (OID Model
  Selection flowchart: Model 1 = `LN_BV_ADJ` book-value adjust; Model 2 =
  `LN_DEF_REV` unearned revenue → `DM_ALMS_PD` → `PD_FD_SRV_COST_SETUP` →
  monthly amortization).

**Consequence:** because these PD3 ALM securities ARE positions on a real
portfolio, they DO need a Model Portfolio tag to decompose/report correctly —
and this is exactly the mechanism the ClickUp defect "Fund Service Costs Not
Getting a Model Portfolio" is about (see `pd-fund-service-cost-mp.md`). Do not
generalize this PD-specific finding to Fund Admin service costs generally —
they are architecturally different mechanisms that happen to share the phrase
"Fund Service Cost."

## 3. The `Dec+Mp` scope — direct confirmation MP tagging is a decomposition concern

Source: `§18.29.5.7`. The post-decomp Asset Manager view (AM_ON) adds +102
rows on top of raw Decomp L3, broken into named position scopes:
- `Dec`: 1,025 rows (decomposed, ~L3 minus filtering + extras)
- **`Dec+Mp`: 13 rows — decomposed AND model-portfolio tagged, unique to the
  AM layer**
- `Order`: 4 rows (pending orders)
- `Pf+Mp`: 3 rows (portfolio level + model portfolio overlay)

`Dec+Mp` existing as its own named scope is direct structural confirmation
that "has a Model Portfolio tag" is a property Asset Manager tracks and
filters on for decomposed positions — reinforcing that MP tagging is squarely
a decomposition/exposure-reporting concern, not a Performance-calc input.

## 4. The 6 routes to exclude service costs from decomposition (if they DO leak in)

Source: `§18.29.5.4 — Excluding Service Costs from Decomposition (Cash
retained)`. If a service-cost-like item is incorrectly polluting the asset-
class decomposition (as opposed to correctly never appearing per §1 above),
ranked routes:

1. **Reclassify to Fund Scheme** (SimCorp-correct) — move to L36 asset / L31
   liability, `F_Specific - Fees in Classes`, via Fund Schemes window +
   Multi-class cost distribution (Fund Admin Setup UM §4.1.9 p.67)
2. **Segment filter** on Decomposition Calculation Settings — exclude the
   service-cost Instrument Type while keeping `Bank account` in
3. **IS unmap to Residual** — don't map service-cost Security Types to any L3
   IS leaf node; lands in N.A./Missing line
4. **Distribute residual OFF** + AM filter — pairs with route 3
5. **Holding type/Status filter** — tighten Decomp Calc Settings status group
6. **AM Filter Editor** (display-only, fastest tactical fix, doesn't touch
   the underlying calc)

Cash bank accounts should always **stay in** decomposition regardless of which
route is used — they're legitimate investment positions decomposing correctly
via the Fund Cert UM §9.2 invariant into `F_Market Value - Cash` (L4 asset
side). Only service-cost-type items should be excluded.

## 5. Investment Structure / Model Portfolio primer (for context)

Source: `18.19 IS/MP/MPC/SAAM/TAA Configuration & Operations Guide`.

- **IS (Investment Structure)** and **MP (Model Portfolio)** are GLOBAL. SAAM
  and TAA are always PER-MANDATE.
- MP has a **dual role**: (1) investment strategy tag, (2) TAA/rebalancing
  engine with Model Portfolio Components (MPC).
- Nicola's SAAM&TAA import file column 10 is **"Default Model portfolio"** —
  example value given in the verified format spec is `CASH_FI`. This confirms
  `CASH_FI` is a real, catalogued MP (part of the current 32-MP catalog), not
  an ad hoc value invented for a workaround.
- Rule: an MP may appear under only ONE IS node (single-node rule).
