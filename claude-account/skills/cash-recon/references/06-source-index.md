# 06 Source index

All manuals sit in ii. Manuals & Documentation/PDFs (SimCorp Dimension
September 2025 set unless stated). Page numbers are the printed page in the
footer. Convert with pdftotext -layout before grepping; the corpus recipe is
in project memory (reference_ full corpus sweep).

## SimCorp manuals used

amcv.pdf, Cash Viewing in Asset Manager, September 2025. Section 2 page 6
(payment date perspective), 2.3 page 8 (components of a balance), 2.4 page 9
(cash ladder), 3.1 page 11 to 12 (rows per bank account, identifying
fields), 3.3 page 16 (warning icons), 3.4 page 17 to 18 (Details section,
Cash Balance Details window, fields), 3.5 page 18 to 19 (Include Orders
None, Allocated, Filled, All; Include Simulations; Include FX Simulations),
3.6 page 20 (historical mode), 3.7 page 21 (fills, non booked part), 3.8
page 22 (fund certificate cut off), 4.2 page 27 (Settings Template Cash
Viewer tab: term structure, bank holidays, historical days, display payment
for subsequent dates, exclude payment types, short term instruments as
cash), 4.4 page 29 (Forecast Cash Flow Service, Number of days to
calculate), 4.5 page 29 (historical mode prerequisites).

amgsg.pdf, Asset Manager Getting Started, September 2025. Section 1.8 page
14 (cash management overview), 3 page 51 (Position Scope mnemonic, Pf+Order
= Portfolio Order), 5.1 page 65 to 66 (Cash Viewer prerequisites, bank
account shared across portfolios note), 6.6 page 79 (freeze expected trade
dates, default rolling).

amsim.pdf, Simulations in Asset Manager, March 2026 edition on disk. Create
simulation result list (cash balance added for the default currency bank
account and cash bucket), Position Scope values Sim, Pf+Sim, Order+Sim,
Pf+Order+Sim.

amscn.pdf, Simulations in Asset Manager Configuration, September 2025.
Section 1.7 page 13 to 14 (cut off times, extended settlement days for fund
certificates).

setdef.pdf, Settlement Defaults, September 2025. Section 3.1 page 8
(Settlement - Our Defaults), 3.2 page 9 (by counterparty), 3.5 page 10
(dynamic bank account ID), 3.6 page 11 (Transaction Options Defaults tab),
3.7 page 12 (status levels for automatic settlement defaults), 5 page 15
(T+1 settlement cycle).

foconfig.pdf, Front Office Configuration, September 2025. Section 3.9 page
53 (Forecast Cash Flow Service), 17.4.1.5 page 197 (Order Options, Options
tab: Blank Dynamic Account unless in SC, SC then QC then PC search),
17.4.1.6 page 198 to 199 (Options 1 - Portfolio Master tab: Use the first
rule in order defaults, Overwrite values with order defaults), 21.2 page 262
to 263 (order default types and priority).

Front Office Configurations.pdf, March 2026 edition. Section 3.9 page 50 to
51 (same service, In Future date, default 62 days, maximum 999).

foops.pdf, Front Office Operations, September 2025. Section 4.5 page 25
(Forecast Cash Flow Reset batch job).

cashman.pdf, Cash Management, January 2012. Section 3.5 page 11 (Default
cash position), 3.6 page 11 (Settlement days), 3.7 page 12 to 13 (Valid
within). Cash management user manual.pdf (newer edition) chapter 5 (managing
cash positions on a given day).

sysoptns.pdf, System Options. Currency options: Default settlement Ccy from
quotation Ccy (else portfolio Ccy), Allow settlement in any currency,
Transaction's portfolio Ccy must equal the bank account's portfolio Ccy.

cabu.pdf, Performance Cash Buckets, September 2025. Section 3 page 9
(Default cash position on cash buckets).

relnot2604.pdf, Release Notes 26.04, March 2026. Section 3.13 page 19
(bank accounts on OTC order simulations, Default cash position fallback).

## Client documents

Nicola Wealth - Configuration Document - Cash Management - Phase 2.docx
(i. Client - Nicola Wealth/Config Docs/Docs, version 1.0, 9 May 2025).
Section 3.1.4 Charge/Credit Cash (fees booked through the Charge/Credit Cash
window, Base File 1656, CreditCash for negative values, TP_TC_FEE_ and
TP_TC_CRD_ batch job groups per custodian AVISO, BMO, DESJ). Section 3.2
Cash Transfer (TP_TC_CASH_TRANSFE_N). Section 3.3 Outbound Interface Daily
Cash Report: Cash Management setup CM_DAILY, term structure CM_DAILY (1BD to
5BD), extraction definition, setup and exporter CM_DAILY_CASH_REPORT, batch
job group CM_DAILY_CASH_REPORT, file DAILY_CASH_REPORT_YYYYMMDD.csv under
ActiveData\Interfaces\Out\Cash Management\Daily Cash Report, 17 fields
(Booking date, Bank Account ID, Real bank account, Portfolio group,
Portfolio, Payment SC, Security ID, Trade date, Settlement date, Trans.code,
Transaction No., Nominal, Currency, Custodian, Custody, Counterparty,
Movement type). This report is the SimCorp side replacement for the offline
template and the natural input for the recon once it runs daily.

Nicola Configuration Document D3 section 9 (order defaults, on record in
project memory): nine order default types, Portfolio Master defaults win,
Assign Values not used for settlement details.

## Session evidence

Dan's recorded Cash Viewer session of 9 September 2026 (Cash Balance
Details of the bare CAD row and of 110 AVS CAD on 9/10 and 8/31), the three
screenshots of 9 September (Multiple Portfolio Orders, Portfolio Holdings,
Cash Viewer balances), Jason Carter's Teams message of 9 September with the
two template files and the Cash Balance export.
