# Reallocation window catalogue

Every entry cites its SimCorp Dimension 2510 help form number from
`SimCorp_Help_Structured.csv`. The menu family is Back office, Transactions, Reallocations,
which the help itself names in the Registration/Assignment entry (Form 600). All windows
follow the shared skeleton in `user-walkthrough.md`; entries below list only what is specific
to each window. Codes in brackets are the verified business transaction codes.

## Core position moves

**Partial Portfolio and Custody Reallocation** (no help entry in the corpus). Moves a holding
to another portfolio and custody in one business transaction. Verified only from the client
screenshot; field map in `partial-portfolio-custody-window.md`. Trans. code observed:
RalocCdyPorSD. A sweep of 13 manuals on 12 August 2026 confirmed this window appears in none
of them, so the screenshot is the sole grounding. The code expansion is a gap, see
`gap-register.md`.

**Reallocation Portfolio** (Form 926) [RalocPort, RalocPortSD]. Moves a holding from one
portfolio into another. The Position to section takes the new Portfolio and portfolio Group.
RalocPortSD is the start of day variant where the nominal basis is yesterday's end of day
holding.

**Reallocation Custody** (Form 930) [RalocCdy, RalocCdySD]. Moves a holding from one custody
into another custody at the same custodian. The Position to section takes the new Custody.
Meaningful only when the financial accounting principle sets split on custody. Modify is
supported via File then Modify, then Functions then Positions again.

**Reallocation Custodian** (Form 924). Moves a holding from one custody into another custody
at another custodian. The help summary in the corpus stops before naming the business code, so
the code is a gap.

**Reallocation Security No.** (Form 927) [NewSecNo]. Moves a holding from one security into
another already defined security. The alternative of changing the identification in the data
windows loses history; this window keeps history and supports partial moves. The window does
not validate against moving between security segments with different accounting principles, so
check the principles yourself before advising it.

**Reallocation Model Portfolio** (Form 5845) [RalocModPf, RalocModPfSD, RalocModPfResti].
Moves a holding between model portfolios. RalocModPfResti moves all open expected restitution
balances linked to a zero balance nominal position; the target model portfolio is set in the
Model portfolio field of the Position to section.

## Holding key attribute moves

**Reallocation Special Holding Mark** (Form 929) [RalocSpcMk, RalocSpcMkSD]. Changes the
Special Instance Mark on part or all of a position. Meaningful only with split on special
instance mark in the financial accounting principle.

**Reallocation Free Codes** (Form 977) [RealFrCode]. Changes the free code set on a position.
Only free codes with split on in the financial accounting principle may be entered. The help
notes bonds may be reallocated between FAM lines with or without variable yield adjustment.

**Reallocation Compound** (Form 1112) [RalocCmpnd]. Moves part of an existing position into or
out of a Compound Code. Compound codes are normally set at transaction level; this window is
for existing positions. Holding key information can be added via Functions then Extra
Information.

**Reallocation Purpose** (Form 3808) [RalocPurPriced and other purpose codes]. Moves a holding
between accounting principles split by Purpose, for example trading, hedging, long term
investment or hold to maturity. Average and FIFO profit and loss methods are supported. The
priced variant carries elementary codes RalocPurPrOut and RalocPurPrIn and lets the user set
Price so book and cost value of the new holding are determined at the reallocation. Profit and
loss on old and new holdings are viewed via Functions then Profit/loss and Functions then
Profit/loss (New Holding). Split on purpose is always on profit and loss level.

**Reallocation Blocking** (Form 174) [Blocking]. Blocks a nominal amount of a position for a
purpose and period. Block types are user defined codes that must exist in the Blocking window
first. Block Date states the period. Removing a blocking is a new blocking reallocation on the
blocked position with Block Type and Date left empty. Requires split on blocking, and only
makes sense when short selling is prevented on the financial accounting principle.

## Currency moves

**Reallocation Quotation Currency** (Form 4094) [codes documented on the euro variant].
Reallocates a holding of equities to a new quotation currency. The new quotation currency must
first be added in the Quote Currencies window and the default quotation currency changed.

**Reallocation Quotation Currency, euro module** (Form 3638) [RalocQuoCur, RalocQuoCur(PC)].
Same purpose inside the euro module, one nominal level holding at a time per the splits in the
Financial Accounting Principles window. RalocQuoCur keeps the converted quotation currency
values; RalocQuoCur(PC) keeps the existing portfolio currency values and is relevant when the
portfolio conversion is part of the euro conversion. Bulk creation is Create Reallocation,
Quotation Currency (Form 3720). Details in `conversions.md`.

## Specialised reallocations

**Reallocation Collaterals** (Form 4515). Primarily updates individual reallocation collateral
transactions created by the Collateral Manager; can also create them. Modifiable depending on
transaction status. Confirmed on 13 August 2026 to be the Collateral Reallocation window
described in collmgr.pdf section 8.2.

**Hedge Reallocation, Inception** (Form 4806). One legged reallocation that initiates a hedge
relationship. Elements come from the Hedge Relationship Manager, never from this window.

**Hedge Reallocation, Termination** (Form 4821). Multi legged, one leg per holding in the
Hedge Relationship Manager. Discontinuing keeps accumulated hedge adjustments; reversing
removes them from the reversal date.

**Registration/Assignment** (Form 600). Issuers module. Registration of an owner is a
reallocation on holding level 2 where the client changes, normally with a custody change too.

## Related bulk chains

Security conversion (Forms 3362, 3482, 3484) and portfolio conversion (Forms 3542, 3563, 3566,
3567) generate reallocation transactions in bulk. See `conversions.md`.
