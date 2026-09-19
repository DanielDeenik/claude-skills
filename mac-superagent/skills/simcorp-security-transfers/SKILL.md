---
name: simcorp-security-transfers
description: >
  Security transfers and reallocations in SimCorp Dimension. Covers the Security Transfers
  window family with its direction codes Add-C., Add-C-Cdy, C-Reinv., Remove-C and Rem-C-Cdy
  and the Multi Security Transfer In and Out windows, plus the full reallocation window family
  under Back office, Transactions, Reallocations, from Partial Portfolio and Custody
  Reallocation through Portfolio, Custody, Security No., Free Codes, Purpose and Blocking to
  the hedge reallocations and the conversion chains. Explains the two leg
  transaction model, the holding key precondition and lock, the Request and Actual status
  ladder from the Transaction Process manual, and verified codes such as RalocPort, RalocCdy,
  NewSecNo, RealFrCode, RalocCmpnd and RalocCdyPorSD. Use whenever the user asks how to
  transfer a security, move a holding between portfolios, custodies or custodians, rebook or
  split a position, explain a Raloc code, or walk an end user through any of these windows.
---

# SimCorp Security Transfers and Reallocations

This skill owns two window families that move existing holdings without a market trade: the
Security Transfers windows, which move a security between a customer portfolio and a portfolio
in an external custody, and the reallocation windows, which move a holding across one
dimension of the holding key inside the books. It is the skill to load when a user asks how to
transfer a security, what a Raloc transaction code means, or how to fill in any of these
windows. Sisters: `simcorp-recon-breaks` for breaks a missing or wrong transfer causes,
`simcorp-pd-lifecycle` for private debt events, `simcorp-dashboards` for monitoring views.

## Sources and their limits

Everything here is grounded in these sources and nothing else.

1. `SimCorp_Help_Structured.csv` in `ii. Manuals & Documentation`, the SimCorp Dimension 2510
   help summaries for the reallocation forms and related database tables. Catalogue entries
   cite Form numbers from it.
2. A user supplied screenshot of the Partial Portfolio and Custody Reallocation window from
   the client environment, grounding `references/partial-portfolio-custody-window.md`.
3. traproc.pdf, the Transaction Process manual of September 2025, local in
   `ii. Manuals & Documentation/PDFs`, for the status ladder, the holding key lock and the
   back office route, as verified in the 12 August 2026 session.
4. F1 help captured live in the client TEST environment on 12 August 2026 for the Security
   Transfers window family, and collmgr.pdf section 8.2 for the collateral reallocation.

The help summaries end where the per field listings begin, so field level help for most
windows is not in the corpus, and a 13 manual sweep on 12 August 2026 confirmed the Partial
Portfolio and Custody Reallocation window appears in none of them. Everything not covered is
in `references/gap-register.md` and must be answered with a statement that it is not in the
corpus plus the retrieval route, never from general knowledge. Never guess SimCorp UI or
configuration.

## Rule 1. One business, two legs

A reallocation is one business transaction booked as two elementary transactions: an outgoing
leg from the original position, the From position, and an ingoing leg into the new position,
the To position. The business code is what the user picks; the elementary codes are the
physical records that every computation and general ledger transfer is built from. Business
codes live in TRCBUS, elementary codes in TRCELM, booked records in TRANSMAIN with
reallocation figures in TRANSVMT. See `references/transaction-codes-and-tables.md`.

## Rule 2. The holding key decides whether a reallocation is meaningful, and it locks

Every reallocation window moves a holding across one dimension of the holding key. The help
states repeatedly that this makes no sense unless the Financial Accounting Principle for the
security sets split on that dimension; check the split before advising a reallocation. The
holding key also locks the moment a transaction is saved at Position status or higher, which
is when its quantity starts aggregating into the real position, so errors must be caught at
Entry. See `references/security-transfers-window.md` for the lock mechanics.

## Rule 3. Every window follows the same operating skeleton

Fill key fields in the Positions from section. Choose Functions then Positions and pick the
position from the list. Fill the Position to section with the new value of the changing
dimension. Fill the Reallocation section with Date and Nominal. Confirm the Trans. code. Save,
then read the Balance section, which shows how the original position splits into old and new.
Status is raised by setting the Request field and saving; Actual shows what was saved. Modify
is File then Modify, after which Functions then Positions must be chosen again. The end user
version is `references/user-walkthrough.md`.

## Rule 4. Codes are read from the catalogue, never invented

Verified codes per window are in `references/window-catalogue.md`, and the transfer direction
codes in `references/security-transfers-window.md`. Codes ending in SD are start of day
variants where documented; for RalocPortSD the nominal basis is yesterday's end of day
holding. RalocCdyPorSD is verified as present in the Partial Portfolio and Custody
Reallocation window from the screenshot only; its help definition is a registered gap, so
present the code as fact and its expansion as pattern based until retrieved.

## Rule 5. Conversions are reallocations with a factory in front

Security and portfolio conversions generate reallocation transactions in bulk: principles
first, then the create window, then the monitor window for status raising, deletion and
recreation. Currency conversion differences land as profit or loss on the out leg. See
`references/conversions.md`.

## Rule 6. Transfers are not reallocations

A Security Transfer crosses the boundary between a customer portfolio and external custody
and has its own direction codes and settlement fields. A reallocation stays inside the books
and moves a holding across the holding key. Both run on the back office route with no Order
object, per traproc.pdf section 2.5. Classify the user's ask first and route accordingly.

## How to answer a user question

Classify the ask: transfer across the custody boundary, or reallocation across a holding key
dimension, and if the latter, which dimension. Quote the window name, its location, the code
and the skeleton adapted to that window. Portfolio and custody values differ per client and
environment, so never present example values as required entries. If the ask lands on a gap,
say so and offer the retrieval route instead of improvising.

## Reference map

`references/security-transfers-window.md` holds the transfer family, codes, status ladder.
`references/window-catalogue.md` holds every reallocation window, purpose, codes, Form number.
`references/partial-portfolio-custody-window.md` holds the screenshot grounded field map.
`references/user-walkthrough.md` holds the end user procedure in show and tell order.
`references/transaction-codes-and-tables.md` holds the code model and database tables.
`references/conversions.md` holds the security and portfolio conversion chains.
`references/gap-register.md` holds what is not in the corpus and how to fetch it.
