# Performance calc fundamentals — NAV-based, no proration

**Source:** `FW: Fund of Fund Performance` email chain, forwarded by Sara Behzadi
to Dan Deenik 10 Aug 2026 (original thread 8–12 Jun 2026). Parsed from the raw
.eml (body was base64-encoded; decoded via Python `email` module, not read
verbatim from the raw file).

## The question (Sara Behzadi, Senior Manager, Asset Management Operations — 8 Jun 2026, 7:39 AM)

> "I have a question regarding how performance is calculated for Fund of Funds
> (Core/DPA/DRE) as is related to the cash items (expense and fees) in the
> underlying funds. Does your team take special consideration for these
> performance items when calculating returns? For example, do fund expense get
> calculated as a lump sum into a single cash item bucket for Core fund or do
> they get prorated?"

## The answer (Steven Chen, CFA FRM, Senior Portfolio Performance Analyst — 8 Jun 2026, 8:19 AM)

> "Performance is calculated using the official NAV of the Fund of Funds.
>
> Since the NAV already reflects the underlying fund expenses and fees through
> the fund accounting and valuation process, we do not apply any special
> treatment when calculating returns. The expenses are therefore captured in
> the NAV and flow through to performance naturally.
>
> We do not separately prorate or allocate underlying fund expenses for
> performance calculation purposes."

**This is the single most load-bearing fact in the Performance domain for this
client.** Treat it as ground truth for "does X affect the Performance number"
questions unless a later, more specific, more authoritative correction
surfaces (e.g. a written confirmation that a *specific* fund or share class
does something different).

## Sara's follow-up (12 Jun 2026, 2:49 PM) — a decomposition/exposure-reporting proposal, NOT a Performance-calc proposal

> "One of the functionalities within SimCorp Dimension is the ability to
> allocate fund‑level expenses based on the prorated exposure of the
> underlying fund allocations. For example, if Nicola Core Fund incurs $1,000
> in expenses, those expenses can be allocated across the underlying funds
> rather than being held at the Core Fund level. This allocation can be
> performed using either equal-weight distribution, current asset weights, or
> target asset weights.
>
> From a design perspective, prorating expenses based on underlying
> allocations is important. If expenses are instead retained as a single cash
> line item, they would be reflected in the cash bucket, which would
> artificially deflate the model portfolio's exposure to Cash (specifically
> within the FI sleeve, which is intended to represent only the Nicola Money
> Market Fund). This would distort the Core Fund's true exposure to
> underlying investments.
>
> As such, we have aligned on allocating expenses, distributions, and
> withholding taxes across the underlying fund exposures, rather than leaving
> them as standalone cash entries. In terms of methodology, we propose using
> target asset weights rather than current weights for two key reasons:
>
> 1. Simplicity and stability – Target weights are relatively static and do
>    not fluctuate daily, making them easier to maintain and implement.
> 2. Operational consistency with NAV timing – When striking mid‑month NAV
>    for the Core Fund, daily and weekly funds can be incorporated using
>    current NAVs, whereas monthly funds rely on prior month NAVs. This
>    creates timing discrepancies that would add unnecessary complexity if
>    current weights were used.
>
> Given that actual allocations typically do not deviate materially from
> target weights, using target allocations provides a practical and
> operationally sound approach."

## Why this is two different SimCorp capabilities, not one

Read literally, Sara's proposal is about **exposure/decomposition reporting**
for the Core/DPA/DRE Fund-of-Fund's Model Portfolio — i.e. which asset-class
bucket a dollar of expense shows up under when a PM looks at the fund's
holdings — not about the TWR return calculation, which Steven has separately
and unambiguously confirmed is NAV-driven and does not prorate anything.

Both threads use the word "expenses" and both reference Model Portfolio /
underlying fund allocation, which is why they read as connected on a skim.
But nothing in either email confirms Sara's decomposition proposal ever
touches the Performance-calc mechanism Steven described. Treat the connection
between "Sara's target-weight allocation design" and "the Performance
calculation" as **not confirmed** — don't assert it as fact.

## Update (11 Aug 2026) — the connection IS now confirmed

A fuller version of this same email chain (subject: "Fund of Fund
Performance"), with later replies attached below the original Sara/Steven
exchange, was shared directly by the user on 11 Aug 2026. It resolves what
was previously an open item — **the ClickUp defect and Sara's target-weight
proposal are the same initiative, not just related-by-vocabulary.**

- **Sara Behzadi, 23 Jun 2026 9:56 PM** (forwarding the thread to Erhan
  Rifki, Jacek Bienias [SimCorp], Arjan Dekker, Dan Deenik): *"the decision
  related to fund of fund performance is to use target weights for
  allocating expenses, distributions and withholdings tax across underlying
  fund exposures."* This is a formal decision confirmation, not just Sara's
  personal proposal — it was aligned on in a prior call.
- **Erhan Rifki, 24 Jun 2026 3:08 PM** (to Jacek Bienias, cc Sara/Kasturi/
  Diana/Dan/Arjan): asks Jacek to check for reusable solutions from other
  clients; describes the target design explicitly as *"a process to allow
  an expense to be entered on aggregate for a fund, and for a system
  process to then allocate that expense out to the strategies followed by
  that fund"* — using **SAAM targets**, not live weights. Raises the
  interim question of parking the expense on **its own dedicated Model
  Portfolio**, and explains why CASH_FI was chosen over a fund-level MP:
  *"Were it not for the multi-strategy funds, we would have parked it on
  the fund level MP but this can't be applied consistently across the
  board hence allocating to CASH_FI."* Explicitly asks Sara to create a
  **Day 2 ticket for the full solution** and a **UAT Defect for the
  interim approach** once Jacek advises the MP — this is almost certainly
  the direct origin of the ClickUp defect "Fund Service Costs Not Getting
  a Model Portfolio" (see `pd-fund-service-cost-mp.md`).
- **Erhan Rifki, 24 Jun 2026 (same email)** — the historical-impact
  question, asked directly to SimCorp: *"if you could please comment on
  the impact of bringing this solution live after the system is already
  in production? Would we need to go back and distribute prior expenses
  from inception?"*
- **Erhan Rifki, 13 Jul 2026 7:37 PM** (follow-up, no response from Jacek
  in the intervening 19 days): *"Whilst Performance may be pushed from Day
  1, we do not want to have to rebook a history of expenses and
  distributions down the line when Performance is implemented. At a
  minimum, we need it confirmed that Performance won't care about what was
  booked in the system prior (I am a bit dubious about that)."* Confirms
  nothing has changed since 24 Jun — still parking on CASH_FI, running out
  of time.

**Update (11 Aug 2026, later same session) — Jacek answered.** SimCorp
(Jacek Bienias) directly confirmed: *"cash will be centralized in the
CASH_FI node under the Investment Structure tree. Fee payment itself
doesn't have impact on TWR. This means that until you make any changes to
portfolio positions (through Charge/Credit ALM transactions), you will not
see any impact on the TWR, either historically or going forward."* This
closes the historical-impact question Erhan had asked twice unanswered
(24 Jun, 13 Jul) — but the confirmation is scoped to changes that don't
touch portfolio positions via Charge/Credit ALM. See
`pd-fund-service-cost-mp.md` for why that scoping matters specifically for
the PD3 OID/S-FEE mechanism (which IS booked through Charge/Credit ALM) —
don't extend this confirmation to that mechanism without a separate check.

**Also unconfirmed:** what "Performance may be pushed from Day 1" means
precisely (Performance module go-live deferred to a later phase/release?)
— don't assume; ask Erhan/Sara directly if this becomes relevant to
sequencing advice.

## What would still confirm or deny remaining gaps

- A written statement from Steven Chen (or Performance team), or from
  Jacek/SimCorp, that answers Erhan's specific 24-Jun/13-Jul question:
  does re-tagging/reallocating already-booked expenses require restating
  any previously-reported number, and if so, which one (TWR return? a
  decomposition/exposure report? an attribution report?)
- The actual SimCorp screen/field Sara's design touches for a true
  SAAM-target-weight allocation (Investment Structure? Model Portfolio
  Components? A decomposition setting?) — §4.1.8 apportions on *actual*
  current MP positions, not SAAM targets, so it is at best a practical
  approximation of the adopted design, not a literal implementation of it
  (see `pd-fund-service-cost-mp.md` for the case for treating it as an
  acceptable interim/permanent approximation)
