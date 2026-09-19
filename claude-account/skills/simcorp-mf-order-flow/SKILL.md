---
name: simcorp-mf-order-flow
description: Run, guide, or document the end-to-end Nicola mutual fund order flow in SimCorp Dimension NONPROD (26.04 TEST via Citrix). Covers the full chain in one pass. Load the Core UAT layout in Asset Manager, load a portfolio data selection (NWM250 family), filter sub asset classes in Portfolio Summary, simulate a rebalance by editing the Variance column, create fund trade orders with Assign Values, validate and Approve/Release them in the Order Outbox, execute the TP_AVISO_MF batch job group, and verify the Aviso outbound MutualFund CSV on the TEST-ActiveData share. Use whenever the task mentions creating mutual fund orders, fund trades, rebalancing NWM portfolios, the Order Outbox, Aviso outbound files, TP_AVISO batch jobs, or testing the order-to-export chain in the Nicola UAT environment, even if only one stage is named. Also use when writing UAT test steps, training material, or defect repro steps for any part of this chain.
---

# SimCorp MF Order Flow (Nicola UAT)

End-to-end flow: simulate a rebalance, create fund trade orders, release them,
run the Aviso outbound batch, and prove the file landed. Captured from a live
demonstration in the Nicola NONPROD environment on 2026-08-27. Two uses:

1. **Execute or co-pilot**: drive or guide the flow live in the Citrix session.
   SimCorp Dimension here is a Citrix-hosted Windows app with no API surface, so
   live execution goes through browser or computer-use tools against the Citrix
   tab. Verify the outcome of each stage before starting the next.
2. **Document**: produce UAT test cases, runbooks, defect repro steps, or
   training notes. Use the exact object names, paths, and gotchas below; never
   invent IDs or paths.

## Environment

- Entry: Citrix HTML5 client at nicola-sso.simcorpcloud.com (NONPROD-User tab),
  SimCorp Dimension 26.04 TEST.
- Layouts live under Home. The order flow uses the **Core UAT** layout in Asset
  Manager (a Wealth UAT layout also exists; confirm which stream the task is in).
- Demo portfolio group: **NWM250** (siblings NWM270, NWM330). Portfolio
  NWM250_A. Example securities: NWM22600 Nicola Bond Fund Class N-O CAD,
  NWM13600 Nicola High Yield Bond Fund Class N-O CAD, NWM54600 Nicola Credit
  Opportunities LP Class N-O CAD. Treat these as the demonstrated instance, not
  hardcoded defaults: ask which portfolio group and funds the task targets.

## Stage 1: Open the layout and load data

1. Open Asset Manager. On the Home tab pick Core, then **Core UAT** so the
   layout reconstructs (tabs: Portfolio Summary, Overview, Cash Viewer, Order
   Outbox, SAAM & TAA CHECK, New Security).
2. In the Data Selector pane, right-click the saved selection (e.g. NWM250) and
   choose **Load**. Right-click Edit shows which portfolios the selection holds
   if you need to confirm before loading.

## Stage 2: Filter and simulate in Portfolio Summary

1. Portfolio Summary is grouped by Look Through, Portfolio, Asset Class.
2. Filter the **Sub Asset Class** column to the classes in scope. Demo set:
   Canadian Equity, Global Small Cap, High Yield Bonds, International Equities,
   Investment Grade Bonds. The active filter shows in the bar at the bottom.
3. Compare Fund Weight Pre-Sim against Target Weight; the Variance column shows
   the active bet (red markers on breaches).
4. To simulate, type the desired post-trade variance directly into the
   **Variance** cell of each fund row and press Enter (demo: 2 on the high
   yield fund, 0 on the bond fund). Fund Weight Simulation, Fund Weight
   Post-Sim, and the simulated market value columns recalculate, and rows
   appear in the Simulations panel with expected trade and settlement dates.
   The intent is to neutralize deviations from target weight, so sanity-check
   that Post-Sim moves toward Target Weight before creating orders.

## Stage 3: Create orders

1. Review the Simulations panel: side, market values, expected trade date and
   settlement date per fund.
2. In the Assign Values ribbon group choose **Fund Trade**, then Buy or Sell.
   This converts the simulations into orders; the Order Outbox tab counter
   increments and the orders sit under **Pending orders**.
3. Each order gets an order number of form YYYYMMDDNNNNNNN (e.g.
   20260827000001) with an "Order created" event in Order Events.

## Stage 4: Validate and release

1. In the Order Outbox select the pending orders. Run **Validate** and check
   the Compliance Results panel for rule breaches before releasing.
2. **Approve/Release** moves them from Pending orders to Working orders.
3. Critical dependency: the Aviso extraction only picks up released orders. If
   the batch log later reports 0 records extracted, the near-certain cause is
   that orders were still pending. Release first, then run the batch.

## Stage 5: Execute the TP_AVISO_MF batch job group

1. From the layout Home search, search "batch job group" and open **Batch Job
   Groups** (Maintenance, Batch).
2. File, Load, then search on Batch job group = **TP_AVISO_MF** ("TP - Aviso
   Outbound file - Mutual Fund", log file SO_BATCH). Jobs inside, in order:
   TP_AVISO_MF_NO, TP_AVISO_MF_SWI_NO, TP_AVISO_MF (main), TP_AVISO_MF_SWITCH,
   TP_AVISO_MF_A (archive), TP_SFTP_EXECUTE_AVISO. All daily frequency.
3. Functions, **Execute** runs every job in the group.
4. Known benign noise in TEST: TP_AVISO_MF_A can fail with "No files scanned
   for reference file TP_AVISO_MF_I". Note it, but judge success on the main
   extraction jobs.

## Stage 6: Verify in the log

Open the batch log (Single Log Viewer). Confirm for the main TP_AVISO_MF job:

- "The extraction 'TP_AVISO_MF' is complete" with Status: Finished.
- "Records extracted: N" where N matches the released orders in scope. 0 with
  "There is no data to export" means nothing qualified (see Stage 4 gotcha).
- The export line carries the full destination, e.g.
  `\\TEST-activedata.private-nicola.simcorpcloud.com\TEST-ActiveData\ActiveData\INTERFACES\OUT\SFTP\OutboundFiles\Aviso\MutualFund_YYYYMMDD_HHMMSS.csv`
- TP_SFTP_EXECUTE_AVISO completed (the SFTP push step).

## Stage 7: Verify the outbound file

1. In File Explorer open the Aviso outbound folder:
   `\\TEST-activedata.private-nicola.simcorpcloud.com\TEST-ActiveData\ActiveData\Interfaces\Out\SFTP\OutboundFiles\Aviso\`
   Gotcha: the path copied from the log can lose its leading `\\` and host and
   File Explorer then throws "Windows can't find". Re-prefix with `\\` plus the
   host, or walk down from Network. Sibling custodian folders: BMO, SSC, TD.
2. Open the newest `MutualFund_YYYYMMDD_HHMMSS.csv`. Header (quoted CSV):
   Action, Client Account No, Fund Code, Switch to Fund Code, Amount, Quantity,
   Mutual Fund Account No, Dividend Distribution, NWM Fund Name, NWM Fund Code,
   Security Name, Currency, Trade Date, Settlement Date.
3. Check row count equals records extracted, and spot-check one row: Action
   matches order side, fund code and security name match the order, trade and
   settlement dates match the Order Outbox.

## Verification checklist

Confirm, in order, before declaring the flow complete: simulation moved
Post-Sim toward Target Weight; orders created with order numbers; compliance
validated; orders in Working (released) state; batch group executed; log shows
records extracted greater than 0 and the export path; CSV exists with matching
rows. If any check fails, stop and diagnose there; every later stage depends
on it.
