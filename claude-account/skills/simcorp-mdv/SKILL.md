---
name: simcorp-mdv
description: "Market Data Validation in SimCorp Dimension at Nicola: decode a Validate Market Data run, decide whether a warning is a break or a known exception, and change the rules, segments, severity or batch timing safely. Use when someone asks about MDV, the daily price exception run, missing or stale or variance price warnings, the MDV rule set or setups, the exception list, which exceptions belong in the daily check, who owns a missing price, or why the check produced nothing or produced hundreds of rows."
---

# Market Data Validation at Nicola

## Never do these

1. Never close a missing price by entering a price. Establish the verified value and why the feed did not deliver it, then import or update. Resolved means a clean re run, not a tick.
2. Never delete a row from the check to make it quiet. Exceptions leave the daily queue by carrying a reason code, never by deletion or by a narrowed segment.
3. Never put a Security ID literal in a segment condition. See the hardcoding section; there are already two in PROD and both are Dan's own stated anti pattern.
4. Never add an instrument type to an exclusion without first confirming the security actually carries that type. Warrant, Covered warrant and Right are three separate types and guessing has already produced a silently ineffective exclusion in PROD.
5. Never assume there is one rule set. There are two paths (below).
6. Never re-derive the live rules or segments from scratch. They are decoded below.
7. Never read max age as calendar days. It is business days on a holiday calendar.

## The two paths

| Path | Batch group | Setup | Window |
|---|---|---|---|
| Data management | DM_MKD_MDV | MDV | Validate Market Data |
| Fund admin NAV | FA_MDV | NDV_UAT | Validate Market Data |

NAV Procedures steps 1.3 and 1.6A. A UAT named setup sits in a live procedure. Always ask which path before answering, and never assume a rule change in one is visible in the other.

## Where the configuration lives

| Object | Window | Menu path |
|---|---|---|
| The rules | Market Data Validation Rules | Data, Market Data, More Price Tasks |
| The segments | General Segments | Reached by right clicking a segment cell in the rule grid, then Edit Table |
| The run | Validate Market Data | Data, Market Data, More Price Tasks |
| Purge | Cleanup Market Data Validations | Data, Market Data, Cleanup |
| Orphan purge | Cleanup Unreferenced Market Data Validation Details | Maintenance, System Maintenance, Cleanup |

Run configuration seen in PROD: Single validation rule MDV, Date TD, Include holdings on level "Temporarily and finally booked", Load only unapproved prices clear, Include portfolio selection from fund portfolio calculations clear, Segments and Portfolios tree showing Portfolio segments with P_LOB_FUND.

## The live rule set, read from the rule grid in PROD 15 September 2026

Setup ID `MDV`, name `Market Data Validation`. Seven rules. Every one of them was created by user `SC_JEFFBURTON`, a SimCorp consultant account, not a Nicola account. Ownership of this control has never been transferred.

| # | Validation rule | Price type | Holding segment | Instrument segment | Dev min | Dev max | From date | To date |
|---|---|---|---|---|---|---|---|---|
| 1 | FX VARIANCE | | MDV_FX | | -5.00 | 5.00 | TD-1BD | TD |
| 2 | MISSING FX RATE | | MDV_FX | | | | TD | TD |
| 3 | MISSING PRICE | | | MDV_PRICE | | | TD | TD |
| 4 | PRICE VARIANCE | | | MDV_INSTR | -5.00 | 5.00 | TD-1BD | TD |
| 5 | STALE PRICE | SS&C | | MDV_INSTR | | | | |
| 6 | STALE PRICE | Close | | MDV_INSTR | | | | |
| 7 | STALE PRICE | Manual Override | | MDV_INSTR | | | | |

Read this against the earlier export based reading, which described rules 1 and 2 as running via the FX profile, 3 and 4 via the pricing profile and 5 to 7 via price tables. Both are true and they describe different halves. The segment picks the population, and the profile or price table resolves the price for that population. The grid columns above are the population half.

The three stale rules carry no From or To date. Their Actual from date read 9/8/2026 and Actual to date 9/15/2026, which is five business days back, consistent with the documented five day window and with max age counting business days.

Currency was blank on all seven rows. No pricing profile column was displayed in this view. The grid supports Hide Field, so absence from the view is not evidence that a field does not exist.

Functional test pack: T001 missing PASS, T002 variance PASS, T003 stale SS&C PASS, T004 stale Close FAIL, T005 stale manual PASS. The FX rules have no test case and the pack predates 26.04. Note that rule 6 is configured identically to rules 5 and 7 in every visible column, so whatever makes T004 fail is not visible in the rule grid.

## The two segments, decoded 15 September 2026

Both are Table group `Instrument`, Table `Securities`. These were previously recorded as existing in no export on disk. They are now captured.

**MDV_PRICE**, name `Market Data Validation - Prices`, drives rule 3, MISSING PRICE.

As found: `Instrument type Not in Cash bucket;Bank account;ALM`

As left after Dan's 15 September edit: `Instrument type Not in Cash bucket;Bank account;ALM;Call money;Warrant` plus Right added in a second pass.

**MDV_INSTR**, name `MDV Instruments`, drives rules 4, 5, 6 and 7.

As found:
```
Instrument type Not in Cash bucket;Call money;Bank account;ALM;Warrant
NAV Frequency Not in WEEKLY;QUARTERLY;MONTHLY
```

As left after Dan's 15 September edit, a third condition was added:
```
Security ID <> NWI340
```

The NAV Frequency condition is the mechanism that keeps weekly, quarterly and monthly funds out of the daily check. NAV Frequency is Security Reporting Code 1, free code 11. That matters: it is the working precedent for tag driven exclusion, see below.

## How to change a segment safely

1. In Market Data Validation Rules, right click the Holding segment or Instrument segment cell on the rule row, then Edit Table. The General Segments window opens on that segment.
2. Select the condition line in Resulting search condition, then Edit. For an instrument type condition the Securities picker opens with Selectable items on the left and Selected items on the right.
3. Move the types, OK, then **Replace**. Forgetting Replace leaves the Value field updated and the condition unchanged.
4. File, Save, confirm the replace prompt, then File, Close.
5. Re run Validate Market Data and compare the result to the previous run before calling the change done.

The same context menu also carries View Audit Trail and Explain Restrictions. Use View Audit Trail before changing a segment somebody else built.

## The instrument type trap, observed

On 15 September, `Warrant` was added to MDV_PRICE and saved. On the re run, the Walgreens right `WBA RT` and both Wells Fargo credit facility rows `PDDLSPV WFC USD` and `PDDLSPV WFC CAD` left the result, which proves Call money and Right took effect. **The Constellation warrant `2299955D CN`, security name CONSTELLATION SOFTWARE-WT 40, was still reporting No price found after the change.**

The likely cause is that its instrument type is not `Warrant`. The Securities picker offers `Warrant`, `Covered warrant` and `Right` as three separate values. This is unconfirmed and must be checked on the security itself, not assumed.

The rule this produces: before adding a type to an exclusion, open the security and read its actual instrument type. An exclusion built on the wrong type fails silently, because the row simply keeps appearing and looks like an unrelated exception.

## Hardcoded identifiers, and what to do instead

There are now two Security ID literals for the same fund in PROD configuration:

- `Security ID <> NWI340` inside segment MDV_INSTR
- A portfolio segment named `P_LOB_FND_A<>340`, described as `P_LOB_FUND<>NWI340 - Asset Portfolios`

Dan added the first one himself as an expedient and immediately named the problem out loud: there should be a proper data management process where securities that are not priced are tagged, the tag should be stored in the system and referenced dynamically, so that a constant price with no update is a defined way of working rather than a literal buried in a segment.

He is right, and the mechanism already exists in the same segment. NAV Frequency is Security Reporting Code 1, free code 11, and MDV_INSTR already filters on it. Free code 19 is Pricing Source. The design that follows from this:

1. Dedicate a security free code to pricing exception reason. Free codes 11 and 19 are taken; the number for this one is still open.
2. Populate it per security with the reason, drawn from the exception taxonomy below rather than invented per case.
3. Replace both NWI340 literals with a condition on that free code.
4. The exception set then reports on the free code, so an exception is visible and attributable instead of silent.

Until that exists, every Security ID literal is a finding, not a fix. Record it as one.

## The exception taxonomy

The same population is maintained in two disconnected places. Reconciling them is an open gap.

Place one, the MDV segments above. Place two, the PROD Asset Manager layout EQUITIES, applet FO Price Check, tab No Price Found, whose filter reads:

`[Status] = 'No price found' And ([Security type] In ('CD', 'CMBS', 'CP', 'FX_CLHEDGE', 'FX_HDG_CAD', 'FX_HDG_USD', 'RIGHT', 'WARRANT') Or Is Blank([Security type]))`

| Category | Securities | Why it fires |
|---|---|---|
| FX forward legs | 140 rows | FX_FORWARDS prices as Spot plus tics plus Int. price Ccy, so a leg has no quote of its own |
| Credit facility | PDDLSPV WFC CAD and USD | Call money, accounting data only, no MAIN row at all. Now excluded by instrument type |
| Right and warrant | WBA RT, 2299955D CN | Held at zero by design. WBA RT now excluded; the Constellation warrant is not, see the trap above |
| Money market at cost | NWI340, NWI348 | Constant price by design, belongs on the stale rule not the missing rule |
| BVAL not supported | CA05614KAJ12, KAY88, KBA93 | BX PURE ABS, SSC route planned |
| Manually priced CP | CA89352NX923, CA292976X516 | Manual via Position price, no prior Manual price to compare against |
| Mortgages at book value | NAC, FN, MCAP, PCC, PHC, PQ, SP series | Accounting data, no price. Already out by segment |

Note the asymmetry: the FO Price Check filter works on Security type, the MDV segments work on Instrument type and NAV Frequency. They are not the same field, so the two lists cannot be kept in step by copying values between them.

## How to decode a run export

The export has 74 columns and carries rule parameters on every result row. Group by the rule fields to reconstruct the configured rules: Market data validation rule, Validation rule, Limit deviation maximum and minimum, Number of days, Pricing profile, FX rate profile, Instrument segment, Price table, Price type, Bank holidays, Earliest search date, From date, To date.

Pricing definition and Earliest search date on a result row are resolution attributes, not rule parameters. Do not read them as rule config.

Always reconcile arithmetically and state the identity. On 13 September: 153 warnings equals 140 FX forward legs plus 9 known exceptions plus 4 uncategorised, nothing unclassified, zero genuinely unexplained.

## Hard facts from the manuals

- Only rules classified ERROR stop the STP service. Warning and Information do not stop event creation and the service proceeds as usual (Fund Operations 5.4.6). Every Nicola rule is Warning today.
- Max age counts business days on a holiday calendar. On Thursday 10 September, max age 10 gave old date 26 August and max age 2 gave 8 September.
- When every step of the selected definition returns Not found, the search ends with No price and the position values at zero. There is no fall through to another definition (Pricing Structures 2.2.1).
- Booked price on a fund certificate in Asset Manager answers: Price method not supported. Instrument type Fund certificate or other factors may be incompatible. Every Booked price terminal is a no op there.
- The Validate Market Data Using Service Platform window ignores and skips holding key segments used in the pricing profile, because validation works at security level (Fund Accounting Setup 4.4.2). The plain window is the only one that supports holding key segments and position prices by portfolio. Rules 1 and 2 use a holding segment, so they are affected by this.
- The service platform window adds corporate action suggestion (Corporate action, Expected price, Deviation percent expected price), Use Previous Prices, inline Save Prices, Invalidate Selected and Invalidate Security, Show Manual Validations For User, and the Ignored flag.
- Market Data Validation Setups has a Rules section and a Copies section. Successful validation creates price and FX rate copies per the Copies section.
- Overrule deviations takes Never, Common level or High level.
- Business day validation is not automatic. Price types must be entered in the Price Types with Business Day Validation window (Market Data 3.2.3.3).
- Cleanup Market Data Validations deletes deviating records prior to a To date. The log file field is optional, so always name one and extract the register first.

## The findings that make the control unsound

1. It cannot stop anything. Every rule is Warning, yet NAV Flow Overview step 7 expects the operator to confirm the in process MDV safety check passes or stops for a known reason.
2. It runs before its own inputs. DM_MKD_MDV at 01:29 against position prices 03:00, SS&C 06:01 and 16:51, NBIN 07:01. That is the cause of constant fund units and no price money market rows.
3. Corrected data is never re checked. Backfills are not validated separately.
4. Two paths that can disagree, unreconciled.
5. Exclusions are carried as instrument type lists and Security ID literals inside two segments, so an exception is invisible once excluded and nobody can report on what was suppressed or why.
6. All seven rules are owned by a consultant account, SC_JEFFBURTON. There is no Nicola owner of record.

## Deliverables, do not rebuild

- `General & Architecture/Spreadsheets/NWM_MDV_Rule_Set_Design_2026-09-14.xlsx` three sets, every rule field by field, segments, bands, exception register
- `vi. Config & Architecture/Docs/NWM_MDV_Robust_Design_2026-09-14.html` five layer control model, 13 failure modes, severity, build order
- `iii. Training Modules/MDV_Operating_Guide_2026-09/` operating guide and evidence register
- Project memory: project_mdv_rule_set_design_2026_09_14, project_mdv_robust_design_2026_09_14, project_mdv_operating_guide_2026_09_04

The segment decode above is new as of 15 September and supersedes the note in those packs that the segment conditions were uncaptured.

## Open, do not answer from assumption

Which setup is production. Ownership per price source and who may confirm a price is verified, and who takes the rules over from SC_JEFFBURTON. The actual instrument type of 2299955D CN. Which free code number to dedicate to pricing exception reason, 11 and 19 being taken. The variance band per asset class; no price history is on disk, and the method is the 99.5th percentile of absolute day over day moves over 250 business days per pricing definition. Whether manually priced CP gets a reason code or the variance rule skips when no comparison exists. Whether business day validation is populated. What makes rule 6 fail T004 when its visible configuration matches rules 5 and 7.