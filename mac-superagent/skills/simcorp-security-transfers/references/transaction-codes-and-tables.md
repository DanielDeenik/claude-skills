# Transaction codes and database tables behind reallocations

Grounding: help entries for the Transaction Codes window (Form 3162) and database tables
TRANSMAIN (Table 120), TRCELM (Table 201) and TRCBUS (Table 202), all from
`SimCorp_Help_Structured.csv`, plus foreign key rows from the client FK catalogue export.

## Business versus elementary codes

SimCorp Dimension has two kinds of transaction codes. Business transaction codes are what the
user sees and selects in the transaction windows; they describe the type of business.
Elementary transaction codes identify the physical records in the transaction file. The
relationship is not one to one. The help uses the custody reallocation as its own example: one
business processed in the window corresponds to two elementary transactions, one booking an
amount out of the old holding and one booking the same amount into the new holding. The
physical records are the basic building blocks of all computations and of the transfer to the
general ledger system. The business code exists for the convenience of the user in the input
phase.

## The tables

TRCBUS describes the business transaction codes and the external numbering follows them.
TRCELM describes the elementary transaction codes; each elementary transaction has a record in
the transactions table. TRANSMAIN is the main transaction table with one record per
transaction, all instruments included, optimised for purchase and sell transactions, with
special information pushed to sub tables. The sub table relevant here is TRANSVMT, which the
help describes as figures used by position reallocations, in a one to one relation to
TRANSMAIN. Settlement information sits in TRANSSETTLEMENT, instructions in TRANSINSTRUC, the
log in TRANSLOG, costs and tax in TRANSCOSTTAX and booked figures in TRANSGAINLOSS.

The client FK catalogue export additionally verifies reallocation linkage columns on the
subledger: TRANSSUBLEDGER carries TRANSRALOC, TRANSRALOCMOVED and TRANSRALOCNET, each a
foreign key to TRANSMAIN.TRANSIK, and the holding side tables HOLDSUBLEDGER and HOLDSUBLRPH
carry an IXRALOC column. These columns exist; their exact semantics are not documented in the
corpus and belong to the gap register if asked.

## Verified business transaction codes in the reallocation family

The following codes are stated in the 2510 help summaries. Cite them as documented.

RalocPort and RalocPortSD for the portfolio window; the SD variant takes yesterday's end of
day holding as the nominal basis. RalocCdy and RalocCdySD for the custody window. NewSecNo for
the security number window. RalocSpcMk and RalocSpcMkSD for the special holding mark window.
RealFrCode for the free codes window. RalocCmpnd for the compound window. RalocPurPriced for
the priced purpose reallocation, covering elementary codes RalocPurPrOut and RalocPurPrIn.
RalocQuoCur and RalocQuoCur(PC) for the quotation currency reallocation in the euro module.
RalocModPf, RalocModPfSD and RalocModPfResti for the model portfolio window. Blocking for the
blocking window, where the help gives the long name as Reallocation, Blocking.

RalocCdyPorSD is additionally verified as an observable value of the Trans. code field in the
Partial Portfolio and Custody Reallocation window, from the client screenshot only. Its help
definition is not in the corpus.

## Naming pattern

Across the documented codes, Raloc opens a reallocation code, Port refers to portfolio, Cdy to
custody, SpcMk to special instance mark, Cmpnd to compound, ModPf to model portfolio, QuoCur
to quotation currency, Pur to purpose, and a trailing SD marks a start of day variant. Use the
pattern to read an unfamiliar code aloud, and always label such a reading as pattern based
until the help page for that code is retrieved.

## What this means when supporting users

A user reporting one reallocation will always generate two records downstream, so counts that
look doubled in extracts keyed on elementary transactions are expected. Anything that consumes
TRANSMAIN, for example reconciliation or ledger extracts, sees both legs. When tracing a
reallocation in data, start from TRANSMAIN and pull TRANSVMT for the reallocation figures.
