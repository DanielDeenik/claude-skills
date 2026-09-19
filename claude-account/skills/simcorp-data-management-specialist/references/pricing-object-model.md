# Pricing object model and current NWM state

## Tables and keys (validated against the SCDAT schema)

- PRICEPROFS (14 rows TEST): profile header. PRICEPROFIK, PRICEPROF, PRICEPROFNAME, PRICEPROFTYPE.
- PRICEPROFSSUB (359): THE waterfall step table. PRIORITY (lower wins), INSTYPE, SEGIK to SEGDEFS, PRICEDEFIK to PRICEDEFS, KEYRATMAPIK to KEYRATMAP, FRMLIK to FORMULAS, FROMDATE, TODATE, DRAWN.
- PRICEDEFS (120): pricing definition dictionary only, never the steps.
- PRICEDEFSSUB (441): ladder steps. PRIORITY, PRICEMETHOD, PRICETYPE, MAXAGE.
- SEGDEFS (4501): segments. The scoping tool for waterfall rows.
- KEYRATMAP (9) with sub rows (CEI object tKEYRATMAPSUB, physical name to confirm in schema): FRMLIK per key ratio slot, child mapping, exclusion flag.
- KEYRATDEFS (7): EXPOSURE, SCALE_NOMINAL_ONLY, INFO, NOMINAL control scaling and aggregation.
- FORMULAS (1447): FRML, FRMLNAME, FRMLTXT script, KEYRATDEFIK, FRMLAPPL.
- PRIKEYDEFS (5): PKR definition, verified FK PRICEPROFIK to PRICEPROFS. Binds calc service and AM settings templates to one profile. PRIKEYSERVICES (3) runs it.
- PRICES (604,490): SECIK (verified FK to SECURITIES), CURIK, PRICETYPE, PRICEDATE (incremental key, Last360), PRICE, QUOTATION, DATASRCIK, PRISRCIK, EXCIK, LEGNO.
- PRICHKERRORS (70,453): price check exceptions per profile, definition, security, date, error.
- Consumers with a stored PRICEPROFIK: PORTFOLIOS, FUNDS, MPDEFS, DECOMPSUBMASTER.
- Portfolio calculation results: POSRCRESULTS and PFCKEYRATIOS, read back by the From portfolio calculation method and the AM alt fields.

## Runtime resolution

Profile from the consumer (portfolio, fund, MP, decomposition, or AM settings template via PRIKEYDEFS). Row from instrument type and segment match, lowest priority. Value from the definition ladder, first valid price by method, type and max age. Key ratios from the row's mapping. Exceptions to PRICHKERRORS.

## NWM profiles and bindings

- MAIN, 43 rows, 15 instrument types, 19 definitions, 4 mappings (NWM_FI_KRM, NW_KRM, NWM_EQ_KRM, NWM_FUND_KRM). Hygiene clean in the TEST export: no overrides, no dates, no drawn, no collisions. 17 rows carry no mapping.
- ALTS_AM, Name Asset Manager (Alts), 47 rows, 25 instrument type labels. PROD screen 2026-08-28 verified rows 1 to 32 exactly as the trace doc; drawn flag SET on the Bond GE_VAL_LFI_DRAWN_BONDS_TQ row; Swap rows dated, GE_VAL_OTC_IRS_TQ to 12/31/2020 and GE_VAL_OTC_IRS_TQ_ARR from 1/1/2021. 43 of 47 rows carry no key ratio mapping; Equity rows and the default carry PM_EQ, one XpressInstrument row carries CUSTOMKR1. Default row priority 99 GE_CLOSE_ALL_1D has NO mapping (settled 2026-08-28). Alternative investment rows value through the ALTS_AM definition, single step From portfolio calculation.
- WEALTH (19 unique rows, NW_KRM throughout), FUNDS (52) and FUNDS_AM_ALTS_LT (51) with legacy BVAL, PM_EQ, CUSTOMKR1: traced, not yet screen or export verified.
- Settings template routing: ALTERNATIVE INVEST > MULTI_ALTS > ALTS_AM (CAD). ASSET ALLOCATION, EQUITIES, FIXED INCOME, FOREIGN EXCHANGE, WEALTH > FO_TRADED. DEBT > GE-EOD > FUNDS (USD). MULTI_ALTS_LT > MULTI_ALTS_LT > FUNDS_AM_ALTS_LT (CAD).

## Findings register summary (canonical copy in the lineage workbook Findings sheet)

- F01 CONTRADICTED: FO_TRADED binds MAIN per the TEST deep export but WEALTH per the template scope doc. PRIKEYDEFS in production settles it.
- F02 OPEN: the ALTS_AM price type on imported alternative prices is consumed by no ladder in any traced profile. Orphan until the import owner repoints or retires it.
- F03: 43 of 47 ALTS_AM rows have no key ratio mapping.
- F04: 17 of 43 MAIN rows blank mapping, reconcile against the five mapping target.
- F05: mapping migration half done, legacy BVAL, PM_EQ, CUSTOMKR1, NW_KRM still live.
- F06 CONTRADICTED: NW_KRM roster 57 rows (CEI) versus 40 (usage doc).
- F07: test formulas KRTEST, TESTEQL, TEST_PRICE in live mappings.
- F08 RESOLVED: ALTS_AM default row mapping is blank (PROD screen).
- F09: instrument type labels beyond the resolved code map need the INSTYPE domain pull.
- F10: two XpressInstrument rows tie at priority 10 on three profiles.
- F11: curve dependent key ratios fail for bonds and loans from the AM without a theoretical price basis; the YTM family computes.
- F12: alt AM values come From portfolio calculation, not imported prices.
- F13: MAIN hygiene clean.
- F14: Par price type absent from the resolved price type map.
- F15: PROD screen matches the trace for ALTS_AM rows 1 to 32; rows 33 to 47 unverified.
- F16: Booked price not supported for AM and Compliance Manager while it terminates most ladders; price method domain 9 to 74 captured, price type domain still open.

## Where the baselines live

Workbook vi. Config & Architecture/Spreadsheets/SimCorp_Pricing_Lineage_MAIN_ALTS_AM.xlsx (also mirrored as sheets 20 to 28 of vi. Config & Architecture/SimCorp_DEX_MAIN_Pricing_Profile.xlsx). Runbook vi. Config & Architecture/Docs/NWM_PROD_Pricing_Extraction_Runbook_v1.docx. Analysis vi. Config & Architecture/Docs/NWM_Pricing_Profile_System_Analysis_v1.docx.
