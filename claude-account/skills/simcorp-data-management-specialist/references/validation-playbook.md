# Validation playbook: extractions X1 to X8, checks and evidence protocol

The extraction pack lives in the PROD_Extraction_Spec sheet of the lineage workbook and the runbook NWM_PROD_Pricing_Extraction_Runbook_v1.docx. The technical support team with production read access runs it; validation is a row for row diff against the workbook baselines. Extraction DESIGN work routes to simcorp-extraction; schema checks route to simcorp-dex-validator.

## The eight extractions

- X1 Profile waterfall. Base PRICEPROFSSUB filtered to MAIN and ALTS_AM via PRICEPROFS, joined to PRICEDEFS, SEGDEFS, KEYRATMAP, FORMULAS. Settles blank mapping questions, dated rows, drawn rows, priority ties. Baseline: MAIN_Profile_Rows (43) and ALTS_AM_Profile_Rows (47).
- X2 Definition ladders. Base PRICEDEFSSUB joined to PRICEDEFS, with method, type and max age domain text. Baseline: MAIN_Def_Ladders (68 steps) and ALTS_AM_Def_Ladders.
- X3 Key ratio mapping rosters. KEYRATMAP with sub rows (confirm the physical sub table name in the schema first; the CEI object is tKEYRATMAPSUB), joined to FORMULAS and KEYRATDEFS. Settles the roster contradiction and the test formula cleanup. Baseline: KRM_Rosters (124 rows).
- X4 PKR bindings. PRIKEYDEFS with the profile join, 5 rows. Settles which profile FO_TRADED binds (finding F01). The single most important small extract.
- X5 Realised prices. Base PRICES joined to SECURITIES, MANDATORY price date filter Last360 preceding, restricted to the alternative and loan population if volume requires. Feeds the orphan and starvation check.
- X6 Profile usage. One extract per base: PORTFOLIOS, FUNDS, MPDEFS, DECOMPSUBMASTER, PRIKEYDEFS, filtered to the profiles in scope. This is the blast radius before any change.
- X7 Domain translations. Full INSTYPE and PRICETYPE domains via Show Values or the translation source the DEX tool uses. The price METHOD domain 9 to 74 is already captured; codes 1 to 8 of it still need the top of the value list.
- X8 Deep configuration export. Same deep export as the 2026-05-25 TEST baseline, from the Pricing and Key Ratios Definitions window, for FO_TRADED and MULTI_ALTS with referenced child objects. Byte level content diff against the TEST CEI set.

## Acceptance checks

1. Row for row diff of X1, X2, X3 against the baselines. Any delta becomes a Findings row with a source tier, never a silent baseline edit.
2. Binding check: X4 rows decide F01; document the answer and update the register.
3. Orphan and starvation cross join: distinct PRICETYPE values in X5 against the types consumed in X2. Populated but unconsumed equals orphan; consumed but unpopulated equals starvation. The ALTS_AM price type is the known orphan until resolved.
4. Ladder pattern check on X2: Manual Override first at 0, cycle matched max ages, terminal step present, and no AM facing definition whose only terminal step is Booked price.
5. Collision check on X1: equal priority within instrument type and segment without a discriminator is a defect (current known tie: the XpressInstrument pair).
6. Domain refresh from X7 into the code map sheets; hardcoded codes anywhere are a defect.

## Evidence protocol

Every fact carries a tier: PROD screen or export, then TEST CEI export, then trace documentation, then manual text, then a name alone. Screenshots are transcribed cell by cell, truncated cells marked as truncated, rows below the visible fold marked unverified. Contradictions are logged as CONTRADICTED with both sources and the extract that settles them; they are never silently resolved. New evidence updates the Findings sheet, the Notion page and the project memory in the same session.

## Cadence

Batch group A, governance: X1, X2, X3, X4, X6, X7 weekly and on any config change. Batch group B, daily: X5 and the PRICHKERRORS exception pull after the end of day chain. Route daily exceptions to the data management team with the runbook priorities.

## Current open items

FO_TRADED binding (X4). ALTS_AM price type disposition (X5 plus import owner). ALTS_AM rows 33 to 47 and the WEALTH, FUNDS, FUNDS_AM_ALTS_LT profiles (X1 or screen). PRICETYPE domain and Domain-67 codes 1 to 8 (X7). MAIN blank mapping reconciliation against the five mapping target (X1 plus X3).
