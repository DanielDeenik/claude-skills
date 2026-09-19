# Security and portfolio conversion chains

Both chains generate reallocation transactions in bulk. The pattern is identical: define
principles, run a create window that combines the principles with a selection of portfolios or
segments, then manage the generated transactions in a monitor window where they can be seen,
deleted, recreated via Functions then Recreate Transaction, or raised in status. Grounding:
Forms 3362, 3482 and 3484 for securities and Forms 3542, 3563, 3566 and 3567 for portfolios,
from `SimCorp_Help_Structured.csv`. The help for these windows was written around the euro
introduction, so its examples speak of national currencies converting to euro; the mechanics
are what matters.

## Security conversion

Security Conversion Principles (Form 3362) defines how holdings in one security or a group of
securities are converted, without referring to any portfolio. Create Security Conversion
Transactions (Form 3482) combines the principles with a selection of portfolios or segments
and generates one reallocation transaction per nominal level holding, transferring all amounts
from the old holding to the new and converting quotation currency amounts in the process.
Security Conversion (Form 3484) is the monitor window.

The conversion transaction is a security number reallocation between two nominal level
holdings in the same portfolio but two different securities. The two securities must be of the
same instrument type; everything else may differ, including quotation currency. When the
quotation currencies differ, all quotation currency amounts of the old holding are converted
into the currency of the new security and added to the new holding; the new amounts are
converted back and the differences appear as profit or loss on the out leg of the
reallocation. To keep the nominal level sub holdings of the profit and loss level holding, one
conversion transaction is created per nominal level sub holding, booked values are distributed
proportionally by nominal and rounding residuals go to the largest sub holding. Different
security sizes can leave an odd lot in the new holding; odd lot handling and nominal rounding
are defined in the principles.

For equity like instruments the Reallocation Quotation Currency window is used instead. The
exception is equity like instruments not quoted per unit but in percent, per mille, points or
pips, where the security conversion route may be in place; the deciding setting is the Quote
type field in the Market Conventions static data subform. For a larger number of instruments
the Multiple Reallocation Transactions window can be employed; that window has no help entry
in the corpus and is a registered gap.

## Portfolio conversion

Create Portfolios (Form 3542) defines new post conversion portfolios from the existing pre
conversion portfolios, with naming rules for appended text and kept characters. The financial
accounting principles must be the same for the pre and post conversion portfolios, and the
help warns that consistent bookkeeping results are not guaranteed across a change of
accounting principles. Portfolio Conversion Principles (Form 3563) defines which old portfolio
matches which new portfolio and how to handle the case where the old portfolio currency
differs from the quotation currency while the new one equals it; when direct conversion leaves
differences, the principle chooses which set of values continues, and the differences appear
as profit or loss. Create Portfolio Conversion Transactions (Form 3566) generates the
transactions, one reallocation per nominal level holding, as a portfolio reallocation with
currency conversion of the values. Portfolio Conversion (Form 3567) is the monitor window.

The conversion transaction is a reallocation between two nominal level holdings of the same
security in two different portfolios. The portfolios must have the same or fully compatible
accounting principles, otherwise the holdings in the new portfolio become inconsistent at the
next transaction with realisation or regulation. With different portfolio currencies, amounts
convert into the new portfolio currency, and back conversion differences show as profit or
loss on the out leg. One transaction is created per nominal level holding so the nominal level
splits survive in the new holdings.

## Quotation currency reallocation

Covered in `window-catalogue.md` under currency moves. The single position window works one
nominal level holding at a time according to the splits in the Financial Accounting Principles
window; the bulk window is Create Reallocation, Quotation Currency (Form 3720), whose help
entry in the corpus is only a field stub. The choice between RalocQuoCur and RalocQuoCur(PC)
decides whether converted quotation currency values or existing portfolio currency values
prevail when the future quotation currency equals the portfolio currency.
