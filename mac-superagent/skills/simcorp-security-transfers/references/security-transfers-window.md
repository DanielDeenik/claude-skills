# Security Transfers window family

Grounding: F1 help captured live in the client TEST environment on 12 August 2026, including
the Multi In and Multi Out pages, plus traproc.pdf, the Transaction Process manual of
September 2025, local at `ii. Manuals & Documentation/PDFs/traproc.pdf`. This window family is
the transfer half of the skill: it moves a security between a customer portfolio and a
portfolio in an external custody, whereas the reallocation windows move a holding across the
holding key inside the books.

## Purpose and preconditions

The F1 help states verbatim: Use the Security Transfers window to transfer a security to or
from a customer portfolio to a portfolio in an external custody and vice versa. Not all
instrument types are supported; check via Help then Show Transactions Properties. If the
portfolio group type is OWN, the setting Allow use of own portfolios in security transfer must
first be ticked on the Options 3 tab of the Transaction Options window.

## Fields on the single transfer window

As captured in the TEST environment: an Instrument section with Security ID and No.; a
Position section with Portfolio group and ID, Nominal and Price, Nominal ex, Trade, Days and
Pay dates, Trans. code and Yield; a Settlement information section with Custodian, Custody,
Bank and Account; a Quotation and portfolio values section with Currencies and Rate, Current
value, Accrued interest, Cost and tax, and Payment amount; and a Main status section with
Request, Actual, Trans. No. and Trans. flag.

## Direction codes, confirmed from both help pages

Transfers into a customer portfolio from custody use Add-C. or Add-C-Cdy, and the
reinvestment variant C-Reinv. which ties to Add-C. Transfers out of a customer portfolio into
custody use Remove-C or Rem-C-Cdy. Bulk entry runs through the Multi Security Transfer In and
Multi Security Transfer Out windows, which offer grid entry. Multi Out additionally has a
Search position function, reached via Functions then Select portfolios, to bulk select an
entire portfolio's holdings for transfer out.

## Booking and status, from traproc.pdf sections 3.2 to 3.4

The user picks the target status level in the Request field, saves with File then Save, and
the Actual field then shows what was actually saved. Actual matches Request when the user is
authorised and the transaction is valid, and can differ otherwise. The standard ladder runs
Entry, which is a draft with zero position impact, then Position or Free deal, where the
transaction is temporarily booked and affects positions without being final, then Fin calc,
where it is finally booked and profit and loss is calculated, then Trade GL and Settle GL,
where finance transactions go to the general ledger. Clients can configure custom intermediate
levels, for example Under Settlement, Free Payment or Settled and Paid, so always read the
actual ladder from the environment.

## The holding key lock, from traproc.pdf sections 3.2, 3.3 and 4.3

Every transaction carries a holding key, the combination of dimension fields such as
Portfolio, Security and, where custody is split, Custody. The holding key locks the moment the
transaction is saved at Position status level or higher, and that is the exact moment its
quantity starts aggregating into the real position. Trace a position back to its transactions
via View Positions, right click, then View Holdings or View Holding Keys. This is why a wrong
portfolio or custody on a transfer must be caught at Entry: from Position level onward the
holding key is fixed and correction means a new transaction, not an edit.

## Back office route context

Per traproc.pdf section 2.5, the back office transfer route runs directly through these
windows and the reallocation windows with no Order object involved. Quotes gathered outside
the system have no audit trail inside it, which is worth saying out loud when demonstrating
the window to users who are used to the order path.

## Open gap

The exact holding key field set specifically for the Security Transfers window is not
confirmed; traproc.pdf gives the general concept and one example. See `gap-register.md`.
