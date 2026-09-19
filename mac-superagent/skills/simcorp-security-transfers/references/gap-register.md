# Verified gap register

Everything listed here is known to be absent from the two grounding sources. When a user
question lands on a gap, state that the corpus does not cover it and name the retrieval route.
Never bridge a gap from general knowledge. Retrieval route for all help page gaps: the
simcorp-citrix-scraper skill against the 2510 help inside Citrix, or the consultant pastes the
help page text or a screenshot into the session, after which this register and the affected
reference files are updated together.

## Gaps on the Partial Portfolio and Custody Reallocation window

The help page for the window itself is not in `SimCorp_Help_Structured.csv`; no form number is
known, and a sweep of 13 manuals on 12 August 2026 found the window in none of them, so the
screenshot is the sole grounding. The expansion and definition of the RalocCdyPorSD transaction code are undocumented;
only its presence in the Trans. code dropdown is verified from the screenshot, and only the
naming pattern supports a reading. Whether the dropdown offers further codes is unknown
because the screenshot shows the closed control with one value. The behaviour of Settlement
days and Payment date in the Reallocation section is unknown. The precedence between
Nominal/lots and Percentage when both are filled is unknown. The purpose of Price, Collateral,
the New trade checkbox and the Trade ID dropdown in the Position to section is unknown for
this window. The role of the USI namespace, USI, Org. USI namespace, Org. USI and Party/Client
trade ID fields in a reallocation context is unknown. The Calculate via euro dropdown values
are unknown; the euro help entries suggest a relation to the Transactions Options window euro
tab, but that relation is documented there for the quotation currency window, not for this
one.

## Gaps elsewhere in the family

The business transaction code for the Reallocation Custodian window (Form 924) is not stated
in its corpus summary. The full purpose code list for Reallocation Purpose beyond
RalocPurPriced is not in the corpus. The field level listings for every window are absent: the
corpus summaries end where the help section named Fields on begins, so per field help such as
formats, defaults and validation is unavailable throughout. The Reallocation Values and
Reallocation Values (New Holding) entries (Forms 3716 and 3717) have empty descriptions in the
corpus. The Multiple Reallocation Transactions window is referenced by the security conversion
help but has no entry. The Create Reallocation, Quotation Currency entry (Form 3720) is a
field stub only. The status ladder in the Main status section is client configuration and must
be read from the client environment, not from any help page.

## Gaps on the Security Transfers window

The exact holding key field set specifically for the Security Transfers window is not
confirmed; traproc.pdf gives the general concept and one example. The next places to check
are Front Office Configurations.pdf and Front Office Operations.pdf in the local manuals
folder.

## Gaps on data semantics

The semantics of TRANSSUBLEDGER.TRANSRALOC, TRANSRALOCMOVED and TRANSRALOCNET and of the
IXRALOC columns on holding subledger tables are not documented in the corpus; only their
existence and foreign keys are verified from the FK catalogue export.

## Maintenance rule

When any gap is closed, move the fact into the proper reference file with its citation, delete
the gap line here, and keep this file truthful. A gap register that lists closed gaps is as
misleading as an invented fact.
