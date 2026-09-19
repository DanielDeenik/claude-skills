---
name: simcorp-pd-lifecycle
description: >
  Private Debt lifecycle events in SimCorp Dimension for Nicola Wealth — the Loan Facility
  object model (Party → Loan Facility → Contract → Transaction → Position), the twelve
  lifecycle events and which named Create Loan Facility Transactions setup books each one,
  the transaction-cost codes, the batch job group that creates the transactions, secondary
  trading via Trade Manager and Settle Loan Facilities, and where results show in Asset
  Manager. Use when asked what happens on a drawdown,
  paydown, repricing, spread change, combine/split, commitment increase/decrease or expiry;
  which LF_ setup or transaction code applies; whether an event moves cash; or how the
  facility/contract/position levels relate. Trigger: PD lifecycle event, loan facility
  transaction, LF_DRAW_PAYD, LF_REPRICE, LF_SPREAD_CHANGE, LF_SPL_COM, LF_EXPIRE,
  LF_CREATE_TRXNS, drawdown, paydown, repricing, rollover, combine, split, commitment
  increase, expire, Settle Loan Facilities, loan contract, private debt transaction code.
type: skill
---

# SimCorp Private Debt — Lifecycle Events

Sisters: `simcorp-pd-notices` (how the event arrives and gets keyed), `simcorp-pd-migration`
(bulk static-data upload and recon), `simcorp-pd-valuation-cash` (pricing, OID, cash flow,
Call Money). This skill owns **what each event does inside SimCorp and how it is booked**.

## Object model — Private Debt is not shaped like PE/VC/Infra

**Party (borrower) → Loan Facility → Contract(s) → Transactions → Position/Holding.**

- **Loan Facility** is the instrument type and the only PD security. Security group `LOANFAC`,
  which auto-generates the Security No. on save (changeable in Identification Default Rules).
  Facility types: Term, Revolving, Revolving/Term, Letter of Credit.
- **Contract** — one or more per facility. Every drawdown opens a new contract; a rollover
  reprices, combines or splits them. The contract carries currency, pricing option, reference
  rate, base rate, spread, RAC rate, PIK rate, all-in rate, day count, dates and frequency.
  Several contracts can be open at once on different terms.
- **Position** — per portfolio, with sub-holdings per contract. A facility can be shared
  across portfolios; SimCorp generates transactions per position.
- There is **no Investment Link** deal object as in the fund verticals. The facility is held
  directly as a security-master instrument.
- **Call Money** is a separate instrument type used for the fund's own credit facility, not
  for the loan assets — see `simcorp-pd-valuation-cash`.

## The events and how each is booked

Static data is edited in the **Loan Facilities** window; the transaction is then created by
**Create Loan Facility Transactions** using a named setup. All setups default to message
queue `TP_STP` for STP and save at Requested = Position.

| Event | Setup | Cash | Effect |
|---|---|---|---|
| Open facility / commitment | Open/Close Loan Facility (own window) | none | Commitment registered before any drawdown; Unfunded = Commitment |
| Drawdown | `LF_DRAW_PAYD` | out | New contract per draw; Funded ↑, Unfunded ↓ |
| Paydown | `LF_DRAW_PAYD` | in | Principal + accrued interest on the repaid portion |
| Repricing / rollover | `LF_REPRICE` | none | Rolls the contract onto new terms; principal carries over |
| Repricing + combine | `LF_COM_REPR` | none | Reprice and merge in one step |
| Combine | `LF_SPL_COM` | none | ≥2 contracts merged; facility totals unchanged |
| Split | `LF_SPL_COM` | none | 1 contract divided into ≥2; facility totals unchanged |
| Spread change | `LF_SPREAD_CHANGE` | none | New all-in rate from the term date; existing accrual unaffected |
| Commitment increase | `LF_IC_COMMITMENT` | none | Commitment and Unfunded up |
| Commitment decrease | `LF_DC_COMMITMENT` | none | Commitment and Unfunded down |
| Increase **or** decrease | `LF_IC_DC_COMMIT` | none | Either direction from one setup |
| Expire | `LF_EXPIRE` | none | Expires the unfunded portion at maturity so the holding goes to 0 |
| Fees | `LF_FEE` | in | Settles the accrued commitment / facility / utilisation fee |
| Reference rate fixing | `LF_REF_RATE_FIX` | none | Applies the fixing to the contract |
| Unsettled trades | `LF_UNSET_TD` | — | Today's unsettled loan facility trades |

**Combine and split are initiated from the Contracts tab** using the *Generate Rollover
Events* button: select the contracts, then populate the lower Opened Contracts grid with the
new terms. **Expire should be paired with a facility commitment decrease** (Loan Facility
static data ▸ Functions ▸ Global Commitment Changes). **Spread changes are entered on static
data** (Functions ▸ Spreads), not as a direct transaction. **Fee terms** live on static data
under Functions ▸ Fees.

**Batch job group `LF_CREATE_TRXNS`** creates the loan facility transactions. It runs daily
but only produces transactions where that day's static data has been updated. **The sort
order inside the group matters** — it mirrors the intraday order of PD transaction
processing. Ad-hoc creation is possible.

## Transaction costs

| Cost | Purpose | Used on |
|---|---|---|
| `LN_BV_ADJ` | Adjust book value, e.g. an OID on a drawdown | Drawdown |
| `LN_DEF_REV` | OID component held as unearned revenue instead of book value | Drawdown |
| `LN_MGMT_FEE` | Ad hoc management fee | Paydown, roll loan facility |
| `PD_MGM_FEE` | Ad hoc management fee from invoice | ALM |
| `FAC_INT_EXP` | Ad hoc interest expense from the waterfall | ALM |
| `SRV_FEE_APLO` / `_BONY` / `_SSC` / `_KPMG` / `_OTH` | Ad hoc service fees from the waterfall | ALM |
| Delay compensation | Missed interest accrual between expected and actual settlement | Settle Loan Facilities |
| Economic benefit / cost of carry | Settlement compensation components | Settle Loan Facilities |

The two OID routes are covered in `simcorp-pd-valuation-cash`.

## Secondary trading

1. **Trade Manager** — start from the template, complete the tabs, then **Validate**
   (mandatory-field pre-check) and **Execute** (saves the transaction).
2. If the settlement date is unknown, **uncheck Include settlement** and let the Settle Loan
   Facilities workflow handle it.
3. If accrued interest is included in the payment amount, choose **Paid On**.
4. Unsettled trades appear in **Unsettled Loan Facility Trades** (setup `LF_UNSET_TD`);
   right-click → **Settle Loan Facilities** to settle.

## Where results are visible

Asset Manager view **“NWM Private Debt – Portfolio Mgt. 1”**:
- Positions tab — nominal, market value, global commitment %, balance funded amount, balance
  unfunded amount, book value QC, accrued interest QC, facility accrued fee QC,
  unsettled loanfacility, LoanMktValue.
- Cash Viewer tab — bank accounts from the Data Selector, and the term structure for short
  and future cash flows.
- Contract-level detail sits under the facility on the Contracts and Events tabs.

## Rules

- Never state a setup name, cost code or window that is not in the table above or in the
  configuration document — say "not confirmed" instead.
- Commitment transactions and Trade Manager transactions are **excluded** from the cash-flow
  forecast; do not present forecast figures as complete without that caveat.
- A facility shared across portfolios generates transactions per position — check the
  portfolio before reading a balance.

See `references/EVENT_DETAIL.md` for the per-event field lists and the worked Acuity numbers.
