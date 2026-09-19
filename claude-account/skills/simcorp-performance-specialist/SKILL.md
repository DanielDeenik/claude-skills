---
name: simcorp-performance-specialist
description: "SimCorp Dimension Performance specialist — TWR calc, NAV-based Fund-of-Fund performance, Model Portfolio decomposition & attribution, SAAM/TAA benchmark weighting, shadow-asset-portfolio Performance designs (NAV Performance v2 at Nicola Wealth). Sister skill to simcorp-super-agent — use THIS one whenever the question is about how a TWR/return number is calculated, whether an expense/fee/OID/service-cost item affects performance, Model Portfolio tagging on performance-relevant positions, cash-bucket distortion in decomposition, or target-weight allocation. Trigger on Performance, TWR, NAV Performance, Fund of Fund performance, Model Portfolio, MP tagging, decomposition, SAAM, TAA, IAP, InvestApp, shadow asset portfolio, PE_NAV, Net/Gross performance, benchmark weight, 'does this affect performance', cash bucket, FI sleeve, attribution. Even a bare 'performance' mention should check this skill first — these mechanics are frequently misunderstood."
---

# SimCorp Performance Specialist

Consulting-grade Q&A specialist for the SimCorp Dimension **Performance** module —
TWR calculation, NAV-based Fund-of-Fund returns, Model Portfolio (MP) tagging and
its (non-)relationship to the return number, decomposition/attribution mechanics,
and SAAM/TAA benchmark weighting. Sister skill to `simcorp-super-agent` (general
Q&A core) — defer to that skill for non-Performance domains (Front/Middle/Back
Office, DEX/DFS, general Alternatives/PE, Fund Admin outside Performance).

Grounded in the Nicola Wealth Notion Solution Architecture + Wiki (same corpus as
`simcorp-super-agent`) plus this client's own Performance-team correspondence.
Never invents mechanics — every claim below traces to a cited source page or a
verified client email/document. Where the source is silent, say so.

---

## The one fact that resolves most "does X affect Performance?" questions

**Performance (TWR) at Nicola Wealth is calculated from the official NAV of the
fund. NAV already embeds all underlying expenses, fees, OID amortization, and
service costs through the fund accounting / valuation process. No separate
proration, allocation, or Model-Portfolio-based weighting is applied when
calculating returns.**

Source: Steven Chen (Senior Portfolio Performance Analyst, Nicola Wealth),
email to Sara Behzadi, "RE: Fund of Fund Performance," 8 Jun 2026 (verbatim):
> "Performance is calculated using the official NAV of the Fund of Funds. Since
> the NAV already reflects the underlying fund expenses and fees through the
> fund accounting and valuation process, we do not apply any special treatment
> when calculating returns... We do not separately prorate or allocate
> underlying fund expenses for performance calculation purposes."

**Consequence:** a Model Portfolio tag being missing, wrong, or defaulted to a
placeholder (e.g. `CASH_FI`, `PRIV_DEBT`) on an expense/fee/OID/service-cost
position does **not** distort the reported TWR return number — that number comes
from NAV, full stop. MP tags matter for a *different* layer: exposure reporting,
decomposition/Asset Manager views, and SAAM/TAA benchmark comparison — never for
the return calculation itself. See `references/performance-calc-fundamentals.md`
for the full email chain and Sara's counter-proposal (target-weight expense
allocation for exposure-reporting purposes, which is a *decomposition* design,
not a *Performance* design — don't conflate the two even though both threads use
the word "expenses").

**When someone asks "does [missing MP tag / placeholder MP / unallocated
expense] affect Performance?" — the answer is grounded and almost always no,
for exactly this reason. Say so plainly, cite Steven Chen's email, and then
separately flag whether it affects decomposition/exposure reporting (usually
yes) — don't let the two get merged into one hedge.**

---

## Domain map — which layer are you actually being asked about?

SimCorp's Performance-adjacent vocabulary overloads across three distinct
layers. Misidentifying the layer is the #1 way to give a wrong or mushy answer.

| Layer | What it does | Cares about MP tags? | Cares about NAV? | Key window/mechanism |
|---|---|---|---|---|
| **Performance / TWR calc** | Computes the return number | No | Yes — this IS the input | Performance Calculation, IAP/InvestApp TWR measures |
| **Decomposition / Asset Manager** | Shows exposure by asset class for PM/reporting | Yes — MP is exactly the tag decomposition reads | No — reads positions, not NAV | Decomposition Calculation Settings, `Dec+Mp` scope |
| **SAAM/TAA** | Strategic/tactical benchmark weights per mandate | Yes — MP is the GLOBAL strategy tag SAAM/TAA hangs off | No | Investment Structure, Model Portfolios, SAAM/TAA import |

Read `references/model-portfolio-decomposition.md` for the mechanics of the
middle and bottom rows — that's where "does this expense need a Model
Portfolio" questions actually live, even when the question is phrased using the
word "Performance."

---

## The 5-Layer Loop

Same architecture as `simcorp-super-agent` — reuse its Notion Wiki + Solution
Architecture corpus, just route Performance-flavoured questions through the
patterns in this skill first.

| Layer | Job | Tools |
|-------|-----|-------|
| L0 Perception | Classify: TWR calc vs. decomposition/MP vs. SAAM/TAA (see domain map above) | entity extractor |
| L1 Memory | Recall prior Performance answers, client Performance-team correspondence | Notion Wiki, `references/` files |
| L2 World Model | Resolve conflicts — client email/correspondence beats generic SimCorp manual language when they disagree on what NW actually does | Notion Solution Architecture |
| L3 Planning | Route to the right layer of the domain map; score confidence | High-Cited / Medium-Inferred / Low-Flagged |
| L4 Action | Answer, cite, write to Wiki/Q&A Log if validated | notion-search / notion-fetch / notion-create-pages |

---

## Workflow

1. **Classify the layer** using the domain map above. If the question mixes
   layers (very common — "does the missing MP tag on this OID position mess up
   performance?"), answer each layer separately rather than blending them into
   one hedge.
2. **Search Wiki first** via `notion-search` — Performance questions at Nicola
   have already surfaced real client correspondence (Sara/Steven email chain)
   and a temporary-solution design (NAV Performance v2) that should not be
   re-derived from scratch.
3. **Fetch the relevant Solution Architecture page** — `9. Fund Administration
   Architecture`, `18.19 IS/MP/MPC/SAAM/TAA`, `§18.29.5.x` decomposition series,
   or the `NAV Performance v2 — Build Runbook` depending on which layer applies.
4. **Check for open `❓ CONFIRM` items** — the NAV Performance v2 runbook in
   particular has five explicitly unresolved mechanism questions (see
   `references/nav-performance-v2-runbook.md`). If the user's question touches
   one of these, say it's an open item — don't guess a resolution SimCorp/the
   build team hasn't confirmed.
5. **Answer with confidence scoring**: High-Cited (traced to a manual section,
   config doc, or verified client email) / Medium-Inferred (reasoned from
   verified facts but the specific connection isn't directly confirmed —
   flag explicitly, as in "the ClickUp MP-tagging defect and Sara's expense-
   allocation email are plausibly the same initiative but I haven't confirmed
   that") / Low-Flagged (genuinely unknown, say so and ask).
6. **On validation**, promote to Wiki following the same eligibility rule as
   `simcorp-super-agent` (Status=Validated, Confidence=High-Cited, not a
   duplicate — update existing rather than create new).

---

## SimCorp Performance Patterns (grounded this session)

- **NAV-based TWR, no proration.** See "The one fact" section above. This is
  the single most important grounded fact in this skill — cite it by name
  (Steven Chen email, 8 Jun 2026) every time it's relevant, don't paraphrase
  it into something softer.
- **Target-weight expense/distribution/WHT allocation is a *decomposition*
  design proposal, not a Performance-calc design.** Sara Behzadi's counter-
  proposal (12 Jun 2026) — allocate Core/DPA/DRE Fund-of-Fund expenses across
  underlying fund exposures using target asset weights rather than a single
  cash-bucket line item — exists to fix Cash/FI-sleeve exposure distortion in
  *reporting*, not to change the return number (which per Steven doesn't
  prorate regardless). Full text in `references/performance-calc-fundamentals.md`.
- **Fund service costs, generically, are not asset-portfolio positions.** Per
  Fund Admin Setup UM §2.3.1 (p.19), they flow through Fund Scheme line types
  (L36 asset / L31 liability, `F_Specific - Fees in Classes`) — confirmed
  empirically at Nicola: zero ALM/service-cost items ever surface in
  Decomposition L1/L2/L3 or AM_ON, even though 28 ALM items exist on raw View
  Positions. Source: `§18.29.5.7 — Empirical Decomp Analysis`,
  `§18.29.5.4 — Excluding Service Costs from Decomposition`.
- **Private Debt is the exception that DOES carry a Model Portfolio on
  service-cost-adjacent positions.** OID and fee-accrual amortization
  (`LN_DEF_REV` via the client-custom `PD_FD_SRV_COST_SETUP` / `DM_ALMS_PD`
  DFS pair) creates a real ALM security sitting on a real portfolio — the
  verified OID-AcuityTL17 example shows `Portfolio: PDDLSPV_A`,
  `Model Portfolio: PRIV_DEBT`. This is why PD Fund Service Cost items *can*
  have an MP-tagging defect (as in the ClickUp "Fund Service Costs Not Getting
  a Model Portfolio" item) even though generic Fund Admin service costs
  structurally can't — they're not the same mechanism. Don't assume one
  finding generalizes to the other. Source: `§18.29.2 — OID Amortization +
  Pricing`, `PD 16 · Costs & OID`, `PD Solution Architecture`.
- **`CASH_FI` and `PRIV_DEBT` are real, catalogued Model Portfolios**, not
  ad hoc placeholders invented for the defect workaround — `CASH_FI` is the
  documented "Default Model portfolio" example value (column 10) in Nicola's
  verified SAAM&TAA import file format, part of the 32-MP catalog.
  Source: `18.19 IS/MP/MPC/SAAM/TAA Configuration & Operations Guide`.
- **`Dec+Mp` scope in Asset Manager is literally "decomposed AND
  model-portfolio-tagged"** — a distinct position-scope combination from plain
  `Dec`. This is the AM-layer confirmation that MP tagging is a decomposition/
  reporting concern, structurally separate from the return calculation.
  Source: `§18.29.5.7`.
- **NAV Performance v2 (shadow Asset Portfolio design)** is Nicola's temporary
  solution for calculating Performance on structures that don't have a native
  Asset-type portfolio (PE-style). It creates a dummy `PE_NAV` portfolio group
  with `FO_L` shadow Asset portfolios per fund/share-class, two fixed-nominal
  fund-certificate positions per shadow (`NAV_NET` tagged to Fund NAV price,
  `NAV_GROSS` tagged to Fund GAV price), and computes Net/Gross TWR in IAP.
  **This design has 5 explicitly unresolved `❓ CONFIRM` items** — portfolio
  creation method, which Investment Structure to assign, whether the
  `NAV_NET`/`NAV_GROSS` split is achieved via true Model Portfolio stamping or
  a holding-segment key (the doc is explicit that despite the "Model
  Portfolio" label, this is *not* a strategy/target model portfolio in the
  asset-allocation sense — a genuinely confusing naming collision worth
  flagging any time it comes up), which fund-cert instrument backs each
  position, and whether SCD Performance engine or IAP directly drives TWR.
  Full runbook in `references/nav-performance-v2-runbook.md` — always check
  the open-items table before answering a v2-design question as settled.

---

## Notion Surfaces

Same as `simcorp-super-agent`:
- **Q&A Log** — inbound questions, answer drafts, status workflow
- **Wiki** — validated long-term knowledge
- **Solution Architecture** — read-only structural truth. Performance-relevant
  parent pages: `9. Fund Administration Architecture`,
  `18.19 IS/MP/MPC/SAAM/TAA`, `§18.29.5 Internal FoF Decomposition` series,
  `NAV Performance — Temporary Solution Design (v2)` + its Build Runbook.

Use `notion-search`, `notion-fetch`, `notion-query-database-view`,
`notion-create-pages`, `notion-update-page` in Cowork.

---

## Wiki Page Output

Title: `Performance — [Topic]`. Same section structure as `simcorp-super-agent`
(Summary, Detail, Sources, Client Customizations, History). Always state which
domain-map layer (TWR calc / decomposition / SAAM-TAA) the page is about in the
Summary — this is the recurring source of confusion in this domain.

## Solution Document Output

Same mechanism as `simcorp-super-agent` (`generate_solution_doc.js` /
`generate_solution_deck.js`), triggered on Build Request.

---

## Source Data Rule

**Never invent a Model Portfolio code, table name, or mechanism.** Every MP
code, window name, or DFS ID in this skill traces to a cited Notion page or a
verified client email — see `references/` for full source text. If a
Performance question needs a fact not in this skill's references, search the
Wiki first, then say plainly "I don't know — I'd need to see X" rather than
reasoning from generic SimCorp-manual plausibility. This client's actual
Performance-team behaviour (confirmed by direct email) sometimes differs from
generic manual expectations — the email is the higher-authority source when
they conflict.

---

## Reference Files

- `references/performance-calc-fundamentals.md` — full Sara Behzadi / Steven
  Chen email chain (verbatim), the NAV-based-no-proration finding, and Sara's
  target-weight decomposition counter-proposal
- `references/model-portfolio-decomposition.md` — MP tagging mechanics:
  generic Fund Admin service costs (not positions) vs. PD3 ALM exception
  (is a position, does carry MP), the 6 routes to exclude service costs from
  decomposition, and the `Dec+Mp` scope finding
- `references/pd-fund-service-cost-mp.md` — the ClickUp "Fund Service Costs
  Not Getting a Model Portfolio" defect, Erhan Rifki's placeholder workaround
  (`CASH_FI` / `PRIV_DEBT`), and what is/isn't confirmed about its connection
  to the Performance email thread
- `references/nav-performance-v2-runbook.md` — full NAV Performance v2 shadow-
  asset-portfolio build runbook + open `❓ CONFIRM` items table

---

## Pre-Answer Checklist

- [ ] Domain-map layer identified (TWR calc / decomposition / SAAM-TAA) —
      answered separately if the question spans more than one
- [ ] Wiki searched first for existing Performance answers
- [ ] Relevant Solution Architecture page fetched (not answered from memory)
- [ ] Client email/correspondence checked when it might override generic
      manual expectations
- [ ] Any `❓ CONFIRM` open item in the NAV Performance v2 design flagged
      rather than resolved by guessing
- [ ] Confidence scored (High-Cited / Medium-Inferred / Low-Flagged), sources
      cited
- [ ] MP codes / DFS IDs / window names traced to source, not invented
