---
name: simcorp-pd-notices
description: >
  The Nicola Wealth Private Debt notice workflow end to end — collecting notices from the
  Investment Ops mailbox and lender portals, filing them in the SharePoint SCD Notice
  Database by month, portfolio and facility ID, extracting the data into the monthly
  Migration Database, and keying the event into SimCorp. Carries the four notice event types
  and the field set each populates, the portfolio folder map, the human-review and linking
  steps, and the target-state AI classifier design. Use when asked
  what a private debt notice contains, which fields to pull from a Rate Set / Borrowing /
  Principal Payment / Margin Change notice, how notices are filed or linked, what the
  Migration Database columns mean, or how the document classifier is meant to work. Trigger:
  PD notice, loan notice, rate set notice, borrowing notice, principal payment notice, margin
  change notice, notice extraction, Loan Notice Extractor, notice database, migration
  database row, PD classifier, Copilot Studio classifier, AI intake.
type: skill
---

# SimCorp Private Debt — Notices and Data Entry

Sisters: `simcorp-pd-lifecycle` (what the event does once booked and which LF_ setup books
it), `simcorp-pd-migration` (the bulk PD1/PD2/PD3 upload and recon), `simcorp-pd-valuation-cash`
(pricing, OID, cash). This skill owns **how the event arrives and becomes a keyed record**.

## The four notice event types

Every notice resolves to one of four events. The file name of a notice from the agent portal
carries the type, e.g. `…-P-Rate Set-05292026.pdf`, `…-P-Borrowing-04172026.pdf`,
`…-P-Principal Payment-03312026.pdf`, `…-Margin Change-05012026.pdf`.

| Notice wording | Event | What it changes |
|---|---|---|
| Rate Set · Rollover · Repricing | **Repricing** | New contract terms from the repricing date |
| Borrowing · Drawdown · funding memo | **Drawdown** | New contract, funds advanced |
| Principal Payment · Paydown | **Paydown** | Principal repaid, contract amount reduced |
| Margin Change | **Spread Change** | New spread from the term date |

**Repricing notices without rate information are not downloaded** — wait for the matching Rate
Set notice, which carries the rates.

## Field set per event type

Common to every row: Source File · Notes · Event Type · Issuer · Facility · Facility ID ·
Contract Name · Seq. No.

- **Repricing and Drawdown** — Currency · Pricing Option · Reference Rate · Start Date ·
  Repricing Date · Frequency Term Length · Frequency Term Unit · Global Amount · Base Rate ·
  Spread · All-In-Rate · Fixing Date · Day Count Conversion · Fixing Days · Bus. Days
  Convention · EoM Convention · Coupon Base Accrued · Accrued Interest Method · Fixed Rate
  Decompounding
- **Drawdown only** — PIK Rate
- **Paydown and Drawdown** — Total Amount · Start Date · End Date · End-Of-Month Convention
- **Spread Change** — Term Date · New Spread (that is the whole row; the rate block stays empty)

Typical observed defaults: Pricing Option `Floating Rate`; Day count `Act/360`; Fixing Days
`2`; Bus. Days Convention `None`; EoM Convention `Same`; Coupon Base Accrued `Odd`; Accrued
Interest Method `International`; Fixed Rate Decompounding `No decompound`; Seq. No. `0`;
Contract Name in the form `#1-Due YYMMDD`.

## Collection and filing

1. **Investment Ops mailbox** — filter on the Private Debt category (maintained by the team),
   and review every notice email in the collection period, including notifications that a
   notice has been posted on a lender platform such as Debtdomain. Portal logins are in
   1Password. Download the attachments (PDF, MSG or EML).
2. **Month folder** — read the notice date and open the right month inside
   `SCD Notice Database – All Months` on SharePoint (e.g. July 2026).
3. **Migration Database** — run the Loan Notice Extractor skill over the notices and have it
   add rows to that month's database (e.g. *Private Debt – June Migration Database*). Complete
   the fields highlighted yellow for human review and check what the tool populated.
4. **Portfolio folder** — determined by the Nicola entity or lender named on the notice:

   | On the notice | Portfolio folder |
   |---|---|
   | NWM PD Direct Lending Limited Partnership | `PDDLLP` |
   | NWM PD Direct Lending SPV | `PDDLSPV` |
   | NWM SMAI SPV | `PDSMAISPV` |

5. **Facility ID folder** — matched from the facility name on the notice; create it if absent
   (e.g. `AUTO 2025DDTL`, `MICROSS DDTL`, `VORTEX TL6`). Upload the notice and confirm the file
   opens.
6. **Link it back** — Share ▸ Copy Link on the uploaded notice, find the matching record in the
   month's Migration Database, paste the link into the **Link to File** column and verify it
   opens the right notice.

Folder structure: `SCD Notice Database – All Months` ▸ *Month* ▸ (monthly Migration Database
workbook) ▸ *Portfolio folders* ▸ *Facility ID folders* ▸ uploaded notices.

## Migration Database columns

`Manually Entered in Simcorp` · `Irregular` · `Notes` · `Portfolio` · `Facility ID` ·
`Contract Name` · `Spread Change` · `Paydown` · `Drawdown` · `Repricing` (one Yes marks the
event type) · `Contract #` · `Global Contract Amt` · `Nicola Contract Amount` ·
`Global Repayment Amount` · `Nicola Repayment Amount` · `Basis` · `Interest Type` · `Term` ·
`# of Fixing Days` · `Start Date` · `End Date` · `Base Rate` · `Margin Rate` ·
`Spread Adj Rate` · `RAC Rate` · `PIK Rate` · `All-In Rate` · `Floor Rate` · `Commitment Fee` ·
`Link to File` · `Validated`.

Portfolio values in the database are the SimCorp portfolio codes (`PDDLSPV_A`, `NWM407_A`,
`PDSMAISPV_A`), not the SharePoint folder names. A row with note "Waiting on Rate Set and/or
Rollover" is a known-incomplete placeholder, not an error.

## Keying it into SimCorp

Search **Loan Facilities**, enter the facility name in the **Contract Name** field, press
Enter. Then per event type follow `simcorp-pd-lifecycle` ▸ `references/EVENT_DETAIL.md`, which
carries the exact field lists for repricing, paydown, spread change, drawdown and new
facilities. Always confirm the new record appears on **both** the Contracts and Events tabs.

## Target state — the AI document classifier

A Phase 1 prototype, **agent built and tested, orchestration flow not yet built**. Design:

- **Human gate** — a person confirms a document is PD-related and drops it into an
  `AI Intake` folder. The trust model is deliberately preserved.
- **Power Automate** orchestrates: trigger *When a file is created (properties only)* → read
  file content → extract text → call the agent → Parse JSON → route on confidence → write the
  audit row. Six stages, each built and tested before the next.
- **Copilot Studio agent** classifies only. Returns strict JSON: document type, borrower legal
  name, contract number, agent, confidence, reasoning, plus a nested object of rate fields for
  notices. Web search, Work IQ, tools and triggers are all disabled. It performs no file moves
  and no system writes.
- **Routing** — confidence at or above the threshold files to `Borrower ▸ Contract # ▸ Doc
  type`; below it goes to `Needs Human Review`. **The 0.85 threshold is a placeholder pending
  sign-off.** Folders are not auto-created in Phase 1 — a missing borrower folder should fail
  loudly to review.
- **Audit log** — `PD_Audit_Log.xlsx`, table `AuditLog`, 12 columns: Title, ProcessedAt,
  OriginalFileName, DocumentType, Borrower, ContractNumber, Agent, Confidence, Decision,
  DestinationPath, Reasoning, AgentResponseRaw.

Known traps: strip a trailing period from the borrower name before building the path (folder
names cannot end in a period); the chat interface returns formatted Markdown while the flow
needs raw JSON — test the flow output rather than assuming; Parse JSON needs a schema
generated from a real response.

Open decisions: confidence threshold, identity model for the flow, production SharePoint
location, confirmed email intake source, the document type list, and the real contract-number
format. Do not present any of these as settled.

## Rules

- Extract from the notice, never infer a rate or date that is not printed on it.
- Global and Nicola amounts are different numbers — keep them in their own columns.
- A repricing notice with no rates is incomplete by design; wait for the Rate Set.
