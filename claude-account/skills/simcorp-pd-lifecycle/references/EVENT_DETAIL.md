# Per-event field lists and verified worked numbers

Sources: `Private Debt Notices SOP.docx`, `Nicola Wealth Management – Private Debt - Trade and
Asset Servicing Handover.pptx`, `Nicola Wealth - Private Debt - Configuration Document.docx`,
`Sample Private Debt Notice Data.xlsx`, `Robert & Martin - 20260515 Upload Checks.xlsx`.

## Repricing / rollover — fields to complete on the contract line

Right-click the contract line in the lower pane of Loan Facilities, then complete or review:

Seq. No. (one higher than the last) · Currency · Pricing Option · Reference Rate · Start Date ·
Repricing Date · Interest From Date · Frequency Term / Unit · Global Amount · Base Rate ·
Spread · RAC Rate · PIK Rate · All-In-Rate · Fixing Reference Rate · Fixing Date · Day Count
Convention · Fixing Days · Bus. Days Convention · EoM Convention · Coupon Base Accrual ·
Accrued Interest Method · Fixed Rate Decompounding.

Confirm a new record appears under both the **Contracts** and **Events** tabs.

## Paydown — fields to complete

Seq. No. · Total Amount · Start Date · End Date · Frequency Term / Unit · Bank Holidays ·
End-Of-Month Convention. Then OK, and confirm the new Contracts and Events records.

The global paydown amount is populated on the **Paydowns** tab of the facility.

## Spread / margin change

Functions ▸ **Spreads** on the facility. Add a line with the **Term Date** and the **New
Spread**. If the notice's term date falls on a weekend, enter the following Monday. Then
**Apply Spread Change** and pick the contract the change refers to.

## Drawdown

Key information comes from the funding memo and wire-out (funded commitment, any discount or
OID, net funding, dates). Open the **Contracts** section, enter the drawdown details, then
right-click the client line and select **Create Drawdown**. Check the **Events** tab. The
batch job books the transaction at end of day. The opening balance is then set up in the
Opening Balance module.

Note from the SOP: for a **CAD** loan there is no need to populate *Amount (Portfolio
Currency)* in the main framework — filling it with the same amount would be wrong, because
the portfolio currency is USD.

## New loan facility

Extract from the Credit Agreement (start date, borrower name, maturity dates) and the
Assignment Agreement (assigned commitment, effective dates). In Loan Facilities enter facility
type, minimum drawdown, currency, bank holidays and fees; complete free codes and
classifications supplied by the PM team; save — a batch job then opens the position balance.

## Free codes on the Loan Facility

- **Codes 2** tab — Pricing Source, Watchlist.
- **Codes 4** tab — Covenant, Type, Debt Strategy.
- Selectable values per free code are defined in the corresponding Security Free Codes window
  (e.g. Security Free Codes 47); more values can be added later.
- Pricing Source is **Security Free Code 19** (Valuation handover, static data slide).

Observed values in the migration data: Covenant = `COVENANT` / `COV-LITE`; Type = `DIRECT` /
`CO-INVEST`; Strategy = `DIRECT`; Watchlist = `NO`; Seniority = `SENIOR`; Security type
`LOAN_SYN`; Security group `LOANFAC`; Classification scheme `GICS` with a level-5 code.

## Reference rates

Set up in **Reference Rate Definitions**. The rates relevant to this solution are **Term SOFR
1M (TSFR1M)**, **Term SOFR 3M (TSFR3M)** and **CORRA**. They are updated daily by the
Bloomberg request definition **`MD_REF_RATES`**, and loaded rates are visible in the
**Reference Rates** window. Fixings can be applied daily or retroactively per period, with an
overwrite flag. `TSFR2M` also appears in the June migration data.

## Verified worked numbers

**Acuity TL17** (from the migration and calculation work):
- Reference rate TSFR3M, fixing 2026-03-31 = 3.69961%, spread 5.90%, all-in 9.59961%
- Day count Act/360, coupon frequency 3 months, Nicola share $982,500
- Daily interest $261.99; Q2-2026 period interest $23,841
- OID on the `LN_DEF_REV` route: unearned revenue balance −$3,466.90, monthly amortization
  −$239.85, period 2026-04-01 to 2027-06-30 (15 months)

**Acuity DDTL17-B** (April 2026 repricing notice): contract `#1-Due 260731`, start 2026-04-30,
repricing 2026-07-31, global amount 23,200,000, base 3.66339 + spread 5.90 = 9.56339, fixing
2026-04-28, Act/360, 3 months.

## Global vs Nicola amounts

Notices and the migration database carry both a **Global** figure (the whole syndicated
facility or contract) and a **Nicola** figure (Nicola's share). PD2 contract uploads use the
global amount for the contract; the position carries Nicola's share. Never quote one as the
other — the migration database has explicit `Global Contract Amt` / `Nicola Contract Amount`
and `Global Repayment Amount` / `Nicola Repayment Amount` columns for exactly this reason.
