---
name: simcorp-pricing-precedence
description: "Test which pricing profile row SimCorp Dimension actually applies to a position: capture a profile and its segments in the Citrix client (PROD read only), build the expected coverage matrix, read the applied definition in Pricing and Key Ratios Calculations, diff and diagnose. Use for pricing profile precedence, segment order, why the wrong pricing definition or price won, holding key versus instrument segments, MAIN profile coverage, or segment membership tests."
---

# SimCorp Pricing Profile Precedence Test (Nicola PROD, read only)

A pricing profile is a table of rows, each pairing an instrument type and a segment with a priority and a pricing definition. When the profile is evaluated for a position, exactly one row wins. The problem this skill solves: the row that wins is not always the row people expect, and nobody can say from the window alone whether an instrument level segment (Securities table, for example Security type = HISA) or a holding key level segment (Holding keys table, for example Line of Business, Party, NAV Frequency) takes precedence, or why a priority 5 row beat a priority 1 row. Captured from a live demonstration in PROD on 2026-09-06 (Citrix HTML5 client at nicola-sso.simcorpcloud.com, PROD tab in Edge, SimCorp Dimension 26.04).

The skill produces an Excel coverage matrix (expected winner versus observed winner per instrument type and segment) and a diagnosis per mismatch. It never changes anything in PROD. Theory of ladders, price methods and price types lives in simcorp-data-management-specialist; read it when the question moves from which row won to which ladder step won. Extraction design belongs to simcorp-extraction, schema checks to simcorp-dex-validator.

## Operating constraints

1. Evidence is UI only. All capture and observation goes through the Citrix tab using the browser or computer-use tools. No SQL against SCDAT for this skill unless the user changes that decision.
2. PROD is read only. Never press Save in Pricing Profiles, never change a field in General Segments or Edit Table, never run a calculation that writes prices. Close every dialog with its X or Close. If a step would require an edit, stop and state it as a blocker.
3. Screenshots are the source of truth for IDs, captions and conditions. Never invent segment IDs, definition names, table groups or conditions. Everything named below was seen in the demo and must be re-captured live on every run because profiles change.
4. Never hardcode inputs. Confirm the inputs in the next section before starting.

## Inputs to confirm before starting

- Profile ID. The demo used MAIN (Main Pricing Profile). The File menu recent list also showed FUNDS_AM_ALTS_LT (Funds whole Pricing Profile with Alts LT), OM_MAIN (Order Options Main Pricing Profile, no decomp) and FUND_DECOMP (Fund decomp fund only). Ask which one, and whether more than one is in scope.
- Consumer binding. Which job, portfolio calculation or key ratio run is bound to that profile. A mismatch is often a different profile being consumed, not a precedence problem. Ask, and record the answer in the deliverable.
- Instrument types in scope. Default to every instrument type present in the profile; the user may narrow to one (the demo focused on Fund certificate).
- Test population. One or more real instruments or holding keys per segment the user expects to be covered, plus the position that produced the surprise. Ask for IDs; do not pick them.
- Calculation date and key ratio used in Pricing and Key Ratios Calculations. Ask; default to the date of the surprise.

## Stage 1: Capture the profile

1. In the SimCorp Dimension home window type pricing in the search box. The task list under Data > Market Data > Profiles includes Pricing Profiles, Pricing Definitions, Pricing and Key Ratios Calculations, Pricing and Key Ratios Definitions, Pricing Definition Validation Rules and Credit Pricing Model Manager; Controlling > Trade Control holds Trade Control Pricing Definitions and Pricing Profiles, which are a different object and out of scope here.
2. Open Pricing Profiles, File > Load, pick the profile. General information shows ID and Name. The grid columns are Instrument type, Segment, Priority, Pricing definition, Quotation currency, XpressInstrument type, XIM subcontract, From date, To date, Drawn, Key ratio mapping, Formula, Legged instrument.
3. Click the Priority header to sort ascending; the window reloads in that order. Capture every row, scrolling until the last row. Right-click a cell for Filter, Sort Rows, Show Values, Field Properties, View Properties, View Audit Trail, Explain Restrictions and Help; use Filter on Instrument type when the profile is long. Do not use Delete Row, Insert Row or Default Values.
4. Record every column for every row, including blanks. Blank Segment, From date, To date, XpressInstrument type and Quotation currency all matter for the expected winner.

Worked capture from the demo (MAIN, Fund certificate rows in priority order): PR_W_NWM_DF 1 WEALTH_DAILY, PR_W_NWM_WF 2 WEALTH_WEEKLY, PR_W_NWM_MF 3 WEALTH_MONTHLY, PR_W_NWM_QF 4 WEALTH_QUARTERLY, PR_W_MAN_PRD 5 WEALTH_MANUAL, PR_WEALTH 6 WEALTH_MAIN, PR_ISS_NICOLA 10 FUNDS_NICOLA, PR_HISA 15 FUNDS_HISA, PR_ALTS_DI 20 FUNDS_ALTS_DI, PR_MUT_FD 25 FUNDS_MUT_FD, PR_BBG_SMF 50 FUNDS_PUBLIC, blank segment 60 FUNDS_FC_CATCH_ALL. Row 1 of the profile had a blank instrument type with segment PR_NWI340 at priority 1 and definition FUNDS_AT_COST; Bank account and ALM sat at priority 1 on BOOKED_PRICE; FX forward at priority 1 on FX_FORWARDS. Treat this as an example of the shape, not as current data.

## Stage 2: Capture every segment definition

1. Right-click the Segment cell of a row, Edit Table. The General Segments window opens read only for viewing: ID/Name, Table group/Table, Search condition (Field, Operator, Value), Resulting search condition, Static segment tick box, Execute and Select buttons, Save as SQL, Edit SQL, Build SQL.
2. Record per segment: ID, Name, Table group, Table, the full Resulting search condition line by line, and whether Static segment is ticked. Close with the X. Repeat for every distinct segment in the profile.
3. Classify each segment by Table group. Two kinds were seen: Instrument segments (Table group Instrument, Table Securities, for example PR_HISA with Security type = HISA) and Holding key segments (Table group Holding keys, Table Holding Keys, for example PR_W_NWM_DF with P->Line of Business (Portfolio) (*) = WEALTH, S->Party (*) = NICOLA, S->NAV Frequency (*) = DAILY). Record any other table group as its own class.
4. Execute and Select were greyed out in the PROD demo. If they are enabled, Execute lists the members and is the fastest membership check; if not, membership is established attribute by attribute in Stage 4.

## Stage 3: Build the expected coverage matrix

Build the xlsx with the xlsx skill. Four sheets, no arrows, no dashes, no colour coding that carries meaning without a text status.

1. Profile rows: the Stage 1 capture verbatim, one row per profile line, plus a Segment level column (Instrument, Holding key, Other, Blank) from Stage 2.
2. Segments: the Stage 2 capture, one row per segment, with each condition on its own line in one cell or split into Condition 1, 2, 3 columns.
3. Coverage: one block per instrument type. Rows are the profile lines for that type in priority order; columns are Priority, Segment, Segment level, Conditions, Pricing definition, Key ratio mapping, Date window, Drawn, and a Covers column stating in words which positions this row is expected to catch given the rows above it. The last row of each block must be a blank segment catch all; if there is none, flag the gap as a finding, because any position matching no segment has no price from this profile.
4. Test cases: one row per test position. Columns: Instrument ID, Holding key or portfolio, Instrument type, Attribute values relevant to the segments (Security type, Line of Business, Party, NAV Frequency and any other condition field), Expected segment, Expected priority, Expected pricing definition, Observed pricing definition, Observed price or key ratio, Status (Match, Mismatch, Not evaluated), Diagnosis.

Expected winner rule to apply, taken from simcorp-data-management-specialist and treated as the hypothesis under test: the row must match the instrument type, the position must satisfy the segment condition, the calculation date must sit inside From date and To date when set, the Drawn flag scopes the row to drawn positions, and among the qualifying rows the lowest priority number wins; a blank segment qualifies everything of that instrument type. Where two qualifying rows share a priority, record the expected winner as Tie and let Stage 4 decide.

## Stage 4: Observe the applied definition

1. Open Pricing and Key Ratios Calculations (Data > Market Data > Profiles). Run it for the test population on the agreed date with the agreed profile and key ratio. Confirm on screen that the profile shown is the one under test before reading anything.
2. For every test position read the pricing definition (and price type or key ratio value) the calculation reports as applied. Record it in the Observed columns of the Test cases sheet, with a screenshot reference.
3. Establish membership for each test position against the expected segment attribute by attribute: open the instrument record for instrument segments (Security type and any other condition field) and the holding key or portfolio record for holding key segments (Line of Business on the portfolio, Party and NAV Frequency on the holding key side, as the P-> and S-> prefixes in the condition indicate). A position that fails any one condition is not a member, whatever the segment name suggests.
4. Set Status per row: Match when observed equals expected, Mismatch otherwise, Not evaluated when the calculation returned nothing for the position.

## Stage 5: Diagnose every mismatch

Work the hypotheses in this order and record the first that explains the observation; keep going only when it does not.

1. Wrong profile. The consumer that produced the surprise is bound to a different profile than the one captured. Check the binding named in the inputs before anything else.
2. Membership failed. The position does not satisfy every condition of the expected segment (in the demo the daily wealth segment needs Line of Business WEALTH and Party NICOLA and NAV Frequency DAILY, all three). Then the next qualifying row in priority order wins, which is exactly how a priority 5 manual row can beat a priority 1 daily row. This is the most common cause and is settled by Stage 4 step 3.
3. Evaluation level. Holding key segments can only be evaluated when the calculation runs with a holding key or portfolio context. A run at instrument level cannot test a Holding keys segment, so only instrument level and blank segments compete. Compare the run level of the calculation that produced the surprise with the run level used in Stage 4, and re-run at the other level to prove it.
4. Row scope. From date and To date exclude the calculation date, the Drawn flag excludes an undrawn position, XpressInstrument type or Quotation currency narrows the row.
5. Priority tie. Two qualifying rows at the same priority; record which one won and whether it is the earlier row in the unsorted window, then state the tie rule as an observed fact for this environment, not as a product rule.
6. Segment is static. A ticked Static segment does not re-evaluate its condition; membership was frozen when it was built.

If none of these explains a mismatch, log it as Open with the screenshots attached and raise it as a SimCorp question through the usual support route; do not guess an engine rule.

## Stage 6: Deliver

1. Finish the xlsx: every test case has a Status and, for Mismatch, a Diagnosis naming the hypothesis number and the attribute values that prove it. Add a Findings sheet listing coverage gaps (instrument types without a catch all, segments referenced by no row, rows no position can ever reach because a lower priority row already covers everything they cover).
2. State the precedence rule as verified for this environment in one paragraph on the Findings sheet, written from the evidence, with the cases that established it.
3. Deliver the file to the user; when the SimCorp working folder is connected, save it beside the other pricing traceability material.

## Verification checklist

Before declaring done: profile ID and consumer binding confirmed; every profile row captured with all columns; every distinct segment captured with table group, table and full condition; every instrument type block in Coverage ends in a catch all or a flagged gap; every test position has attribute values for every condition field of its expected segment; every Mismatch has a diagnosis or is logged Open; nothing was saved or changed in PROD (Pricing Profiles closed without Save, no General Segments edit).

## House style

Full sentences, no dashes, middots, arrows or maths glyphs in deliverables; roles and teams rather than individual client names in shared material; segment IDs, definition names and field captions exactly as they appear on screen.