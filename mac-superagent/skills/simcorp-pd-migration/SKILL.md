---
name: simcorp-pd-migration
description: >
  The monthly Private Debt static-data migration into SimCorp Dimension for Nicola Wealth —
  building the PD1 Facilities, PD2 Contracts and PD3 OID templates from the migration
  database, what each template's key and mandatory columns are, uploading them, pulling the
  post-import extract, reconciling SimCorp against SS&C position data, classifying breaks as
  Match level 1 or Deviation, and issuing a delta or reupload. Use when asked what goes in
  PD1/PD2/PD3, which column carries a value, why an upload failed or deviated, how a facility
  moved between portfolios, or how the month's recon is evidenced. Trigger: PD migration, PD1
  facilities, PD2 contracts, PD3 OID, SCD template, upload checks, delta file, reupload,
  MIGR, position recon, list of deviations, SS&C recon, loan movement, PDDLSPV_A, NWM407_A,
  PDSMAISPV_A.
type: skill
---

# SimCorp Private Debt — Migration Upload and Reconciliation

Sisters: `simcorp-pd-notices` (where the month's events come from), `simcorp-pd-lifecycle`
(what each event does once booked), `simcorp-pd-valuation-cash` (pricing and NAV). This skill
owns **the bulk static-data load and the evidence that it landed correctly**.

## Portfolio and custody codes

| Portfolio | Custody | Model portfolio | SharePoint folder |
|---|---|---|---|
| `NWM407_A` | `407AVS` | `PRIV_DEBT` | `PDDLLP` |
| `PDDLSPV_A` | `PDDLSPV` | `PRIV_DEBT` | `PDDLSPV` |
| `PDSMAISPV_A` | `PDSMAISPV` | `PRIV_DEBT` | `PDSMAISPV` |

Uploads are prepared per portfolio group — the PDDL and PDDL SPV pair are usually built
together, PDSMA separately.

## The three templates

### PD1 — Facilities (one row per loan facility)
Key: **Facility ID** (max 16 chars, unique security ID). Column order as delivered:

Facility ID · Facility No. · Facility name (50) · SS&C ID (AdvisorWare ID) · ISIN · LoanX ID ·
CUSIP · Security type · Security group · Currency · Facility type · Min. drawdown amount ·
Switch date · Start date · Expiry date · Availability start date · Availability end date ·
Borrower · Seniority · Initial amounts date · Initial global commitment · Agent · Sponsor ·
Classification (Classification Assignment Scheme) · Classification level 5 · Country ·
Watchlist (Y/N) · Covenant · Type · Strategy · Pricing Source · Use commitment fee ·
Commitment fee block (calculation method, fee term, fee unit, fee rate, 1st fee from date,
1st fee payment date, day count convention, EOM convention, business day convention, fee
calculation rule) · the same block for Facility fee and Utilisation fee · then the trailing
columns carrying the initial amounts date and the two commitment figures.

Typical values: Security type `LOAN_SYN`, Security group `LOANFAC`, Classification scheme
`GICS` with a level-5 code, Seniority `SENIOR`, Country `US`, Watchlist `NO`, Covenant
`COVENANT` or `COV-LITE`, Type `DIRECT` or `CO-INVEST`, Strategy `DIRECT`, Pricing Source
`Quote` / `AT_COST` / `PAR`. Dates are `YYYYMMDD`.

**The last two PD1 columns** (the global commitment pair) follow a rule that depends on
facility type — term loan and fully funded DDTL match the notice amount, partially funded
DDTL uses the initial global commitment adjusted, revolvers and revolvers with an LOC have
their own treatment. Read the *PD Last two col.* tab of the upload-checks workbook before
setting them; do not guess.

### PD2 — Contracts (one row per contract, several per facility)
Key: **Facility ID + Contract name + Seq No.** Columns:

Facility ID · Contract name (`#1-Due YYMMDD` form) · Seq No. (use 0) · Agent bank ID ·
Currency · Global amount (of contract) · Pricing option (1 = floating) · Start date ·
Repricing date · Base rate · Spread · RAC rate · Reference rate · All-in rate · PIK rate ·
Day count convention · Coupon base accrued · Accrued interest method · Fixed rate
decompounding · Accrued interest · Accrued interest total · Business days convention ·
Compounding method · Contract schedule · Day count · End-of-month convention · Fixing date ·
Fixing days · Fixing reference date · Frequency term length / unit · … then portfolio,
custody, and the two position amount columns.

Minimum data set for migration is flagged per column in the *PD2 Contracts* specification tab.

### PD3 — OID
Header: `Security ID · Security name · Security type · Currency · Bank holidays · Fund ·
From date · To date · Monthly Amount · Balance Unearned Revenue · Portfolio · Model Portfolio`.

This is the unearned-revenue amortisation schedule — see `simcorp-pd-valuation-cash` for what
SimCorp does with it. A sister `PD3_Fees_Amortization` file exists for fee amortisation.

## Workflow

1. **Build** the CSVs from the month's migration database into
   `SCD Migration Template ▸ CSV_Files For Upload`. Files are named per portfolio group, e.g.
   `PD1_Facilities_PDDL & PDDL SPV_CSV.csv`, `PD2_Contracts_PDSMA.csv`, `PD3_OID_YYYYMMDD.csv`.
2. **Pre-validate** against the specification tabs — field length, mandatory flag and format
   are all listed per column in the upload-checks workbook.
3. **Upload** into SimCorp.
4. **Post-import extract** — pull the facilities extract for the date (the working files are
   named in the `LoanFacilities_YYYYMMDD_MIGR` pattern) and compare it back to the template.
5. **Reconcile** SimCorp against SS&C for the same date.
6. **Delta / reupload** for anything wrong.

## Reconciliation

The recon compares the SimCorp position against the SS&C position per facility. Each break
carries a **Source** of `Simcorp` or `SSC` on paired rows, plus:

- `Reconciliation status` — `Match level 1` or `Deviation`
- `RC_FUND_ID`, `H Security ID`, `H Security name`, `H Instrument type` (Loan Facility),
  `H Security type` (`LOAN_SYN`), `H QC`
- `Reconciliation date`, `Match index`, `Numb. of days`, `Break date`
- `HPFC Quantity`, `HPFC Price`, `HPFC Market Value Local` / `Base`
- `Break ID` in the form `POS_YYYYMMDD_########`
- Free comment, plus a `Comments` and `Completed` column the team works through

Recurring break causes seen in the evidence: inaccurate SS&C price data, pricing differences
when a facility is drawn, an unmatched opening balance, a buy executed on one side only, and
a paydown completed on one side only. A separate qualitative check compares security-level
static data — portfolio, custody, model portfolio, facility ID, name, facility type, LoanX ID,
AdvisorWare ID, dates, borrower, country, currency, sponsor, agent, watchlist, strategy.

Expiry-date drift between the two systems is tracked in its own deviation list with OLD and
NEW expiry date columns.

## Delta and reupload

Corrections are staged in a delta workbook with **`Remove PD2`**, **`Add PD2`** and
**`ADD PD1`** sheets. The dominant fix is re-pointing a contract between portfolios — the same
contract appears on the Remove sheet under one portfolio and on the Add sheet under the other,
with the amounts restated. New facilities go on the ADD PD1 sheet.

Facilities that move between funds are tracked on the **Loan Movement** tab: `PDDL to PDDL
SPV`, `PDDL SPV to PDDL`, and `New Loans`. Check this tab before concluding a facility is
missing from a portfolio — it may have moved on purpose.

## Rules

- Never invent a column. If a value is needed and the column is not in the template above,
  say which specification tab must be read.
- An empty extract proves the query returned nothing, not that the data is absent.
- A deviation is not a defect until the qualitative check says which side is wrong — both
  Simcorp and SSC rows are present for a reason.
- Amounts are global at contract level and Nicola's share at position level. Do not mix them.
