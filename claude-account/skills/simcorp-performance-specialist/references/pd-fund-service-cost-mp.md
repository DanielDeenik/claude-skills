# The ClickUp defect — "Fund Service Costs Not Getting a Model Portfolio"

**Source:** ClickUp task, Program: SimCorp, Project: SCD D2 - Fund, List:
Functional Test - Defects (https://app.clickup.com/9014072735/v/li/901412738135).
Text pasted into chat 10 Aug 2026 — no direct file/API access to the ticket,
its attachments, or its images.

## What's confirmed from the pasted thread

- **The defect (Sara Behzadi, original note):** funds being NAV tested aren't
  getting a Model Portfolio assigned on service costs.
- **Erhan Rifki, 20 May 2026:** flagged the Bolton/NWM110_A case specifically
  — Bolton has its own Model Portfolio to track performance separately from
  internally-managed assets, but NWM110_A doesn't explicitly allocate any
  target to it. Referenced a SharePoint doc (basic MP mappings) and a OneDrive
  Investment Structure.xlsx Allocations tab (CORE, 270, 330) as prep material
  for SAAM/TAA — explicitly **not** a direct requirement for how fund expenses
  should be allocated. Noted the solution "may have to be a Day 2 thing," and
  specifically flagged: *"it's tricky with Performance as you have to get
  things right at the start... May have to run by Performance consultant what
  happens if we only start allocating these from a point in time forward."*
  For migration, nothing was allocated — parked on `DVSF_PRIV`/`DVSF_RE` in
  UAT (which Erhan notes doesn't logically apply — that pertains to a client
  holding the fund, not what the fund itself has) or on default MP `CASH_FI`
  in MIGR.
- **Ankur Walia, 5 Jun 2026:** as PM, deprioritized behind HIGH-priority
  Functional Testing defects unless this is an absolute blocker.
- **Erhan Rifki, 17 Jul 2026 (interim workaround, implemented):** *"The
  expenses will get CASH_FI as a placeholder, and OID, I-FEE, S-FEE will get
  PRIV_DEBT. Beyond that will have to be a Day 2 problem come what may."* He
  states he's asked SimCorp (Jacek) several times for a solution "recycled
  from another client" and for the consequences of not having this in place
  from inception — no responses received. States he is "not chasing this
  anymore." Attached `Email-MPAllocation.pdf` (not accessible from this
  session — only the ClickUp comment text was pasted, not the file itself).
- **Diana Liu, 17 Jul 2026 / Kasturi Ghosh, 28 Jul 2026:** status check-ins,
  no resolution recorded in the pasted thread.

## What's grounded from the Solution Architecture (connects the dots on *why* this is happening)

Per `model-portfolio-decomposition.md` §2: Private Debt OID/fee-accrual ALM
securities (created via the client-custom `PD_FD_SRV_COST_SETUP` /
`DM_ALMS_PD` DFS pair) sit on a real portfolio holding and are expected to
carry a real Model Portfolio tag — the verified OID-AcuityTL17 example shows
`Portfolio: PDDLSPV_A`, `Model Portfolio: PRIV_DEBT`. This matches Erhan's
placeholder scheme exactly: `PRIV_DEBT` is being used as a stand-in MP for
OID/I-FEE/S-FEE ALM positions, and `CASH_FI` (a real, catalogued default MP
per `18.19`) as a stand-in for generic expense positions — i.e. the interim
fix is tagging these positions with *plausible but not-necessarily-correct*
MPs so they don't break decomposition, pending a real allocation rule.

**`I-FEE` could not be found anywhere in the Solution Architecture or Wiki** —
only `S-FEE` is documented (e.g. `S-FEE-FRANKLINRL`, per `§18.28.5 — Trans
Code Calculations · NWM407 Pilot`). Treat `I-FEE` as an ungrounded term until
confirmed — don't assume it's a typo for `S-FEE` or invent what it stands for.

## What's NOT confirmed — don't assert these as fact

1. ~~Whether this defect is the same initiative as Sara's target-weight
   expense-allocation proposal~~ — **CONFIRMED 11 Aug 2026.** A fuller
   version of the "Fund of Fund Performance" email chain (shared directly
   by the user) shows Erhan asking Sara on 24 Jun 2026 to create *"a UAT
   Defect [for] the interim approach once Jacek advises which MP he would
   prefer to have these parked on"* — immediately after describing the
   target-weight/SAAM allocation design. This is almost certainly the
   direct origin of the ClickUp defect. See
   `performance-calc-fundamentals.md` → "Update (11 Aug 2026)" for the full
   chain. They are the same initiative: the ClickUp defect is the
   interim/UAT-visible symptom of the not-yet-built target-weight
   allocation design.
2. ~~Whether the missing MP assignment has ever been shown to affect a
   reported Performance/TWR number~~ — **CONFIRMED by SimCorp 11 Aug 2026.**
   Jacek Bienias answered Erhan's exact 24-Jun/13-Jul question directly:
   *"cash will be centralized in the CASH_FI node under the Investment
   Structure tree. Fee payment itself doesn't have impact on TWR. This
   means that until you make any changes to portfolio positions (through
   Charge/Credit ALM transactions), you will not see any impact on the TWR,
   either historically or going forward."* This closes the loop between
   Steven Chen's client-side claim and an actual vendor confirmation — it
   is no longer just this session's inference.

   **But read the caveat precisely — it is scoped, not blanket.** Jacek's
   "no impact" is conditioned on *not* changing portfolio positions via
   Charge/Credit ALM transactions. Re-tagging a position's Model Portfolio
   field (which is what the §4.1.8 fix does — see §1a in
   `model-portfolio-decomposition.md`) is not a Charge/Credit ALM
   transaction, so that fix is now cleanly confirmed as TWR-safe, both
   historically and going forward — proceed with confidence.

   **The PD3 OID/S-FEE mechanism is a different case, and Jacek's caveat
   applies to it directly — BUT internal team discussion (13 Aug 2026,
   reacting to Jacek's reply) reframes why this may matter less in
   practice than it first appeared.** Per §2 in
   `model-portfolio-decomposition.md`, OID/fee-accrual ALM securities for
   Private Debt are booked and amortized *through the Charge/Credit ALM
   window* (`DM_ALMS_PD` / `PD_FD_SRV_COST_SETUP`) — that is exactly the
   mechanism Jacek named as the one that CAN affect TWR. Read narrowly,
   that means Jacek's confirmation does not automatically cover a future
   change to OID/PRIV_DEBT tagging.

   However, in the internal thread following Jacek's answer, the view
   pushed back on treating OID/PRIV_DEBT as a placeholder awaiting a future
   change at all: *"OID will go on PRIV_DEBT, not CASH_FI. Those OIDs
   should live with the investment in principle, it is a design outcome
   that they happen to be ALMs but they are not fund expenses."* And on
   whether it might need to be "undone" later: *"I don't think OID needs
   to be undone. There is no other place it makes sense for it to live.
   And those funds are single model anyway. If they were all single model,
   we'd just use that single model instead of CASH_FI. It's the
   multi-strategy funds that present the challenge."*

   **This reframes the risk picture.** CASH_FI is a genuine interim
   placeholder for generic expenses on multi-strategy funds, standing in
   until the target-weight design is built — that's the one that's
   expected to change later, and Jacek's confirmation covers changing it.
   PRIV_DEBT for OID is being described as the correct, permanent,
   by-design answer for single-model PD funds, not a stand-in — so there
   may be no future "change it back" event to worry about at all. That's
   this session's read of an internal team discussion, not a SimCorp-
   confirmed fact — attribution of individual speakers in the pasted
   thread is not fully certain (no message headers), so treat the
   reasoning as directionally right rather than verbatim-attributed. If a
   change to OID/PRIV_DEBT tagging is ever actually planned, it still
   needs its own confirmation from Jacek, since his answer explicitly
   excludes Charge/Credit ALM transactions — but as of 13 Aug 2026 nobody
   is currently proposing to change it.

   **One more thing Jacek's answer raises, not yet interpreted:** "cash
   will be centralized in the CASH_FI node under the Investment Structure
   tree" sounds like it's describing built-in IS routing behavior for
   cash-type items generally, not necessarily endorsing CASH_FI as a
   correct resting place for these specific expense positions. It reads as
   consistent with — not a contradiction of — Sara's original 12-Jun
   concern about cash-bucket distortion in the FI sleeve. Don't read this
   line as "SimCorp says leaving it on CASH_FI is fine" without asking
   Jacek to clarify what he meant.
3. **What SimCorp (Jacek) ultimately proposed, if anything** — Erhan states
   there were no responses as of 13 Jul 2026 (email) / 17 Jul 2026 (ClickUp,
   "not chasing this anymore"). The referenced `Email-MPAllocation.pdf`
   attachment might contain a resolution but wasn't accessible in this
   session.
4. **The multi-strategy-fund constraint, and how it connects to §4.1.8.**
   Erhan's 24-Jun email explains WHY expenses were parked on CASH_FI
   instead of a fund-level MP: *"Were it not for the multi-strategy funds,
   we would have parked it on the fund level MP but this can't be applied
   consistently across the board."* This is a real design constraint worth
   naming explicitly: a single fund following multiple strategies can't be
   represented by one fund-level MP. Fund Administration Setup §4.1.8
   already supports **multiple `Base cost on model portfolio` rows for the
   same Fund + ALM security ID, one row per Model Portfolio** — i.e. it can
   split a single service cost across several MPs, not just tag it with
   one. That's structurally the right shape for a multi-strategy fund,
   even though (per item 2 above and `performance-calc-fundamentals.md`)
   §4.1.8 apportions on *actual current* positions rather than *SAAM
   target* weights, which is the gap between it and the formally adopted
   design. Whether §4.1.8's actual-position apportionment is close enough
   to target weights to adopt as-is is a judgment call Nicola should make
   explicitly — Sara's own 12-Jun email already argues *"actual allocations
   typically do not deviate materially from target weights"*, which is a
   real, source-grounded argument in favor of accepting the approximation
   rather than building something custom.

## The setup/config fix path — split by which mechanism applies

**For generic Fund Admin service costs (management fees, audit fees, GST,
FUNDSERV_FEE, etc.):** the native fix is **Fund Administration Setup §4.1.8**
— see `model-portfolio-decomposition.md` §1a for the full field-level detail.
This is verified working at Nicola already (13/15 ALM lines on NWM250 show
correct `CASH_FI` tagging through it) — the fix for the remaining gaps is
adding the missing `Base cost on model portfolio` row per ALM security ID,
not a redesign. Note this apportions on actual current MP positions, not
target weights — a real constraint if Sara's target-weight design
(`performance-calc-fundamentals.md`) is meant to apply here.

**For PD's OID/S-FEE ALM securities specifically:** §4.1.8 does NOT apply —
these are booked through the separate client-custom `PD_FD_SRV_COST_SETUP` /
`DM_ALMS_PD` DFS pair and carry their Model Portfolio as a direct position
attribute (verified: `Portfolio: PDDLSPV_A`, `Model Portfolio: PRIV_DEBT` on
OID-AcuityTL17). **Which screen or field actually sets that MP for a PD3 ALM
security is not confirmed in this corpus** — candidates are a field on the
`PD_FD_SRV_COST_SETUP` import template itself, the target portfolio's default
MP, or the general "transaction stamping" mechanism described in the
Performance Management Setup Guide (Part B7: mandates stamp transactions
with a model-portfolio stamp via Financial Accounting Principles / Nominal
framework) — but none of these has been directly traced to the PD3 ALM
import path. This is the one open item worth checking against the actual
`PD_FD_SRV_COST_SETUP` DFS field list rather than guessing.

## Next steps to close these gaps

- Get the `Email-MPAllocation.pdf` attachment and the three ClickUp images
  staged into a session (device bridge or direct upload) — they weren't
  reachable from pasted text alone.
- ~~Confirm with Erhan/Sara whether the target-weight design and the PD
  MP-tagging defect are the same workstream~~ — done, see item 1 above.
- Get a definitive, scoped answer to Erhan's unanswered question — not by
  re-sending the open-ended "what's the impact" email that already went
  unanswered twice, but by putting the TWR-vs-decomposition distinction
  above to Steven Chen/Jacek as two separate, closed questions they can
  each answer in one line.
- Get Nicola to explicitly decide (this is a business/reporting-policy
  decision, not a SimCorp config question): a cutover date policy for
  decomposition/exposure reports once MP tags are corrected, so "would we
  need to restate history" has a concrete answer regardless of what
  SimCorp says.
- If/when a real allocation rule is designed for OID/I-FEE/S-FEE/expense
  positions, update this file and promote a Wiki page — this is currently a
  genuinely open item, not something the KB has already resolved.
