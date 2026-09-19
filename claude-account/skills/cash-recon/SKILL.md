---
name: cash-recon
description: >
  Reconcile SimCorp Dimension cash (Asset Manager Cash Viewer, Portfolio
  Holdings cash rows, the CM_DAILY Daily Cash Report) against the Nicola
  offline Cash Management Template (csh sheet) and the custodian balances it
  is fed from. Use when Jason's template column N (Total Available Cash) does
  not match SimCorp, when a Cash Viewer balance or movement needs explaining,
  when an order lands on a bare currency row instead of a bank account, when
  fund flows look double counted, when a HISA or mutual fund trade shows on
  the wrong value date, or when someone asks why the cash in Asset Manager
  differs from the custodian. Grounded in Cash Viewing in Asset Manager
  (amcv, September 2025), Asset Manager Getting Started (amgsg), Settlement
  Defaults (setdef), Front Office Configuration (foconfig), Cash Management
  (cashman), Release Notes 26.04 and the Nicola Cash Management Phase 2
  configuration document, plus the worked case of 9 September 2026.
---

# cash-recon

Cash reconciliation between SimCorp Dimension and the offline Cash Management
Template used by the Nicola trading desk. The skill answers one question in a
fixed order: for each bank account and value date, why does SimCorp show a
different number from the template and from the custodian, and which of six
known causes produced the difference.

## Inputs you must have before starting

1. Two template workbooks (xlsm): the previous day's file, whose column
   "Total Available Cash" is the expectation for today, and today's file, whose
   column "Credit/Debit Balance" is the custodian balance this morning. Both
   live on the csh sheet. Read references/03-template-anatomy.md first; the
   column letters are not stable, locate columns by header text.
2. A Cash Viewer export from Asset Manager with Show Movements set to Actual
   Dates (Options menu) so that every column is a movement on a payment date.
   The export carries portfolio rows, currency rows and account rows in
   column A and B. A row whose account label is a plain currency code is a
   cash position with no bank account. Those rows are findings, not noise.
3. The account map CSV (references/account_map_nicola_2026-09-09.csv is the
   starting point). Every row carries its source. Never invent a mapping; when
   a template account has no SimCorp row, add the row with source "unmapped"
   and ask.
4. Optional: the Multiple Portfolio Orders grid export with the Bank account
   column added, and Cash Balance Details captures for the cells in question.

## Procedure

Step 1. Run scripts/cash_recon.py with the two templates, the export, the map
and the value date. It writes one sheet, Recon, in the house spreadsheet
style: expected, actual, actual less expected, SimCorp balance on the date,
SimCorp less actual, note, and below it every bare currency row with its
non zero movements.

Step 2. Read the actual less expected column first. This is Jason's own
model against the custodian. A zero on the Desjardins rows with a non zero
expectation means the DJD sheet in today's file is empty, not a real
difference. Differences under about one percent of the fund flow are the
template's normal error.

Step 3. Read SimCorp less actual per account and classify each difference
with references/04-recon-method.md. The six causes, in the order to test:
payment date perspective (the Cash Viewer is value dated, the custodian is a
morning balance), rolled expected trade date on unexecuted orders, fund flow
counted twice (forecast transaction plus actual flow on the same date),
partial fill residual on an order without a bank account, order or
transaction with no bank account at all (bare currency row), and stale or
empty feeding sheets in the template.

Step 4. For every difference that is not explained by the export alone, pull
the Cash Balance Details for that account and date (right click the cell,
Show cash details) with the fields Payment security name, Business
transaction code, Instrument type, Payment type, Order number, Transaction
No., Payment nominal, Trade date, Settlement Date. Group by Business
transaction code. The recipe and what each field proves is in
references/01-cash-viewer-mechanics.md.

Step 5. For every bare currency row, open the order in the Order Outbox or the
Portfolio Orders window and read its Bank account field and its fill state.
The defaulting chain that should have filled it is in
references/02-bank-account-defaulting.md. Report the order number, the
missing Settlement Our Defaults row (portfolio plus settlement currency) or
the option that blanked it, and the amount parked on the currency.

Step 6. Write the result as one line by line table per account and value
date with the four columns custodian, template expected, SimCorp, difference,
negatives in parentheses, and one sentence per row naming the cause and the
evidence cell. Full sentences, no dashes, no arrows.

## Hard rules

Never compare a SimCorp balance on date D to the custodian without stating
which payment dates are inside D. Never call a difference "timing" without
the Cash Balance Details row that carries the settlement date. Never treat a
bare currency row as a display artefact; it is money with no account. Never
assume the account map; the CSV rows carry their evidence. Never rebuild the
template logic from memory; read the formulas in the file at hand (the
Trading Summary, DJD and dph cash bal sheets change daily and the 0909 file
of 9 September shipped with an empty DJD sheet and a 9/4 Trading Summary).

## Files

references/01-cash-viewer-mechanics.md: what a Cash Viewer cell contains and
how to read the details, with manual sections.
references/02-bank-account-defaulting.md: how an order gets a bank account
and the three ways it ends up without one.
references/03-template-anatomy.md: the csh sheet, its feeding sheets and
formulas, the account map.
references/04-recon-method.md: the six causes, the tests, the report shape.
references/05-worked-case-2026-09-09.md: every number of the first run.
references/06-source-index.md: manuals, pages and client documents used.
scripts/cash_recon.py: the recon table builder.
