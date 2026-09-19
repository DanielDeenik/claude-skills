---
name: simcorp-pd-valuation-cash
description: >
  Private Debt valuation, OID and cash management in SimCorp Dimension for Nicola Wealth —
  the three pricing sources and their pricing definitions, the MidCap price import chain and
  its batch jobs, the no-fall-through pricing gotcha, the two OID treatments (book value
  versus unearned revenue amortised through ALM), the Loan Facilities Cash Flow Calculation
  and exactly what it includes and excludes, and the Wells Fargo Call Money credit facility
  with its borrow, repay and interest transaction codes. Use when asked how a loan facility
  is priced, why a price is zero or stale, where MidCap prices come from, how OID is
  amortised, what the cash-flow forecast covers, or how fund-level borrowing is booked.
  Trigger: PD pricing, pricing source, QUOTE AT_COST PAR, MidCap price file, AGM_SSC,
  DM_NW_MD_LF_PRICE, Explain Price Search, OID, unearned revenue, LN_DEF_REV, LN_BV_ADJ,
  fund service cost, LF_CASH_FLOW, loan facilities cash flows, Call Money, WdrMoney,
  DepMoney, AS_CM_INT, Wells Fargo credit facility, LoanMktValue.
type: skill
---

# SimCorp Private Debt — Valuation, OID and Cash

Sisters: `simcorp-pd-lifecycle` (events and transaction codes), `simcorp-pd-notices` (notice
intake and keying), `simcorp-pd-migration` (bulk static-data load and position recon). This
skill owns **how a facility is valued and how cash moves at fund level**.

## Pricing sources

The valuation method follows the **Pricing Source on static data, Security Free Code 19**.
Every loan must carry one of three values, and the value selects the pricing definition:

| Pricing Source | Price method | Requirement |
|---|---|---|
| `QUOTE` | Quoted price | A **Close** price in the Prices window, no more than **30 days** old (configurable) |
| `AT_COST` | Booked price | No price entry needed — valuation follows the booked price of the holding |
| `PAR` | Quoted price | A **Par** price in the Prices window, **no maximum age**; par is expected to be 100 |

**The critical gotcha:** when the priority pricing source returns no price, SimCorp does **not**
fall through to the next definition. It uses zero and raises an error in Explain Price Search.
This is the opposite of what most people expect, so a missing price shows up as a zero
valuation rather than a stale one. Always check Explain Price Search before explaining a
market-value break.

Market value: `LoanMktValue = Face × Price / 100`. For an undrawn DDTL the unfunded portion is
valued at `Undrawn × (Price − 100) / 100`.

## Getting prices in

Three routes:

1. **Manual** — a user enters a price in the Prices window.
2. **MidCap batch import** — the AGM_SSC file `AGM_SSC_NICOLA_POSITION_YYYYMMDD.csv` is
   dropped into the MIDCAP Working folder and picked up by batch job group
   **`DM_NW_MD_LF_PRICE`** (unscheduled — Nicola chooses a slot or a file trigger):
   - `DM_NW_MD_PRI_MIDCP_I` imports the prices, using the `MARKET_DATA` queue
   - `DM_NW_MD_PRI_MIDCP_A` archives the file from Working to Archive with a
     `MMDDYYYY_HHMMSS` timestamp
   - DFS `NWM_MD_LF_PRICES`, base filter `BASE_1484` (Prices)
3. **Data Format Setup** — DFS `SIM_MD_PRICES` using the SIM – Prices template.

Other configured import tools: `DM_ALMS_PD` (create ALM securities for PD),
`SIM_SD_CALLMONEY` (Call Money static data), `PD_FD_SRV_COST_SETUP` (fund service cost setup).

## Original Issue Discount — two treatments

**Route A — into book value.** Cost `LN_BV_ADJ` is added to the drawdown transaction, reducing
book value. Nothing further to maintain.

**Route B — unearned revenue, amortised.** Cost `LN_DEF_REV` on the drawdown, then:
- One **ALM security per unearned-revenue balance to be tracked** — created with DFS
  `DM_ALMS_PD`. The ALM's security ID and name are client-specific but should align with the
  loan facility they belong to, and the **currency must match the quotation currency of the
  facility's contracts**.
- Amortisation is configured in the **Fund Service Cost Setup** window: fund, the ALM to
  amortise, from date, to date, calculation setup and default amount. This reduces the
  unearned-revenue ALM balance.
- It runs **monthly** as part of the fund administration workflow, through the Charge/Credit
  ALM mechanism.
- The schedule is loaded in bulk by the PD3 OID template — see `simcorp-pd-migration`.

Worked example (Acuity TL17): unearned revenue balance −$3,466.90, monthly amortisation
−$239.85, period 2026-04-01 to 2027-06-30 (15 months).

ALM lines sit at fund level with no security position, so they will not appear on a
position-level extract.

## Cash-flow forecast

**Loan Facilities Cash Flow Calculation**, executed via batch job group **`LF_CASH_FLOW`**.
It runs over historical or future date ranges.

1. The user enters setup ID, description, portfolio, segments, framework and date range.
2. Forecast settings can discount future cash flows by a chosen yield curve; otherwise Fixed.
3. **Update static data** must be ticked if the forecast cash flows should be written back to
   the facility under Functions ▸ Estimated Irregular Cash Flow. The result is then visible in
   the Irregular Cash Flow Time Series view, showing **global** amounts.
4. Leave Security ID blank to run every loan facility; populate it to run one.

Results land in the **Loan Facilities Cash Flows** window and show the **investor
proportionate share**. *Save cash flows* becomes available after execution; re-running and
saving the same setup ID **overwrites** the previous results.

**Includes:** loan facility fees (projected across the date range), and repricing, combine,
split, paydown and drawdown transactions **where an Event is saved on the facility's static
data**.

**Excludes:** commitment transactions, and Trade Manager transactions.

Never present the forecast as a complete cash picture without stating those exclusions.

## Wells Fargo credit facility — Call Money

The fund's own borrowing, not a loan asset. Instrument type **Call Money**, which combines
deposit, bank-account and credit-facility characteristics, has no maturity, and accrues
interest at a money-market rate.

- Static data: the Call Money window, imported with DFS `SIM_SD_CALLMONEY`. Payment terms and
  rates sit in the sub-windows. **Transfer accrued interest** is expected to be checked with a
  bank account specified, so interest is paid straight to that account.
- Transactions are created manually by users in the **Call Money Payments** window:
  - `WdrMoney` — borrow / withdraw → produces a **negative** position
  - `DepMoney` — repay / deposit
- Interest: **Create Interest Transactions**, code `PayOutAddInt`, generated daily by batch job
  **`AS_CM_INT`** inside batch job group **`AS_CR_EOD`**. No transaction is created if the
  interest date does not line up with the dates on the Call Money static data.
- Reference-rate fixings apply to Call Money fixings as well.

## Where it is visible

Asset Manager view **“NWM Private Debt – Portfolio Mgt. 1”** — LoanMktValue, clean price,
unrealised P&L and balance book value QC on the Positions tab; bank accounts and the short and
future cash-flow term structure on the Cash Viewer tab. The negative Call Money position and
its interest show in the Cash Viewer and on the specified bank account.

## Rules

- A zero market value on a QUOTE facility means no price was found, not that the loan is
  worthless. Check Explain Price Search first.
- Do not describe a facility's valuation without naming its Pricing Source — the three routes
  behave differently and only QUOTE has a staleness limit.
- Cash-flow forecast figures are the investor's proportionate share, not global amounts, while
  the static-data write-back shows global amounts. State which one you are quoting.
- ALM and Call Money are fund-level. Neither carries a loan security position.
