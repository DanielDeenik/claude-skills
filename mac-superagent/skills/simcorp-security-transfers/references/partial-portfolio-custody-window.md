# Partial Portfolio and Custody Reallocation, field map

Grounding: this entire file is read from one client screenshot of the window supplied by the
consultant on 31 August 2026. The help page for this window is not in the local corpus, so no
field behaviour beyond what the screenshot shows may be asserted. Behavioural questions go to
`gap-register.md`. The screenshot shows example values for one client environment; they are
illustrations of format, never required entries.

## What the window is for

The window title is Partial Portfolio and Custody Reallocation. Its layout matches the shared
skeleton of the reallocation family: a Position from section, a Position to section, a
Reallocation section, a Main status section and a Balance section. The Trans. code field shows
RalocCdyPorSD, which by the verified naming of the family sits alongside RalocCdy, RalocCdySD,
RalocPort and RalocPortSD. The documented pattern is that Cdy refers to custody, Por to
portfolio and SD to start of day. Treat that reading as pattern consistent, not as confirmed
documentation, and say so if asked.

## Position from section

Fields visible: Security ID with Security No. beside it, Portfolio group with Portfolio ID
beside it, Custodian with Custody beside it, Counterparty, Leg No., Quotation currency as a
dropdown, Portfolio ccy/Rate as a pair of fields, USI namespace, USI, Org. USI namespace,
Org. USI, and Party/Client trade ID. In the screenshot the editable identifying fields carry
example values for the source position: a portfolio group with its portfolio, and a custodian
with its custody code. The USI and Party/Client trade ID fields are greyed in the screenshot.

## Position to section

Fields visible: Portfolio group with Portfolio ID, Custodian with Custody, Price, Collateral,
Portfolio ccy/Rate, Calculate via euro as a dropdown, a New trade checkbox, Trade ID as a
dropdown, USI namespace, USI, Org. USI namespace, Org. USI, and Party/Client trade ID. In the
screenshot these are empty or greyed, consistent with the standard skeleton where the user
fills the destination after selecting the source position.

## Reallocation section

Fields visible: Reallocation date, Settlement days, Payment date, Nominal/lots, Percentage,
and Trans. code showing RalocCdyPorSD in a dropdown. The presence of both Nominal/lots and
Percentage indicates the moved quantity can be given either way; which one takes precedence
when both are filled is not documented in the corpus and is a registered gap. Settlement days
and Payment date behaviour for this window is also a registered gap.

## Main status section

Fields visible: Request as a dropdown, Actual as a greyed display field, Trans. No., and
Trans. flag. This matches the family pattern where saved reallocation transactions are
searched into the window and saved again at a higher status level; the Request field is where
the target status is set and Actual shows the current one. The exact status ladder configured
for a client environment must be read from that environment, not assumed.

## Balance section

A From column and a To column with a Before row and an After row. In the family pattern the
Balance section displays how the original position splits into the old and the new positions
once the transaction is made.

## Window furniture

The screenshot shows the standard menu bar with File, Edit, View, Search, Functions, Options
and Help, the toolbar beneath it, and an SRCH indicator at bottom right, meaning the window
was captured in search mode. Position selection in this family runs through Functions then
Positions after the key fields are filled.

## How to demonstrate this window to users

Follow `user-walkthrough.md` for the sequence and use this file for what to point at on
screen. Name the section, name the field, state whether the user fills it or the system does,
and where behaviour is not in the corpus say that it will be confirmed from the help page
rather than improvising an answer.
