# 02 How an order gets a bank account, and how it ends up without one

## The order default chain (foconfig September 2025, section 21.2, pages 262 to 263)

Order default types: Assign values, Order routing defaults, Order substitution
defaults, Order settlement defaults, Order simulation defaults, Exclude from
compliance defaults, Order aggregation defaults, Order Manager rules, Order
allocation defaults, Default values in the Portfolio Orders window.

"Those defaults that refer to a Portfolio Master are applied in preference to
those of the portfolio." When the same field is defaulted by several types
the order is: 1 Simulation defaults, 2 Substitution defaults, 3 Routing
defaults, 4 Settlement defaults. "If Use the first rule in order defaults in
the Order Options window is selected, then the rule with the lowest number
(1) in the Sort field in the Order Defaults window, and within the same order
default type, which matches the search criteria is used."

Order Options, Options 1 - Portfolio Master tab, Order defaults section
(foconfig section 17.4.1.6, page 198 to 199): "Use the first rule in order defaults" (no prompt,
first rule by Sort) and "Overwrite values with order defaults" (if cleared,
defaults fill empty fields only). Assign Values is not used for settlement
details such as bank accounts (Nicola Configuration Document D3, section 9,
on record in project memory).

## The bank account search and the option that blanks it

foconfig section 17.4.1.5 (Options tab), page 197: "Blank Dynamic Account unless in SC:
Select this check box to leave the Bank Account field empty if a Dynamic Bank
Account is not found in SC (Settlement Currency). The system skips the
default search order: SC, then QC (Quotation Currency), and finally PC
(Portfolio Currency). The default search priority is defined by the Default
settlement Ccy from quotation Ccy (else portfolio Ccy) option in System
Configuration, Currencies tab."

sysoptns, Currency options: "The Default settlement Ccy from quotation Ccy
(else portfolio Ccy) checkbox defines whether the default settlement currency
on transactions should be equal to the quotation currency (QC) or the
portfolio currency (PC)." "The Transaction's portfolio Ccy must equal the
bank account's portfolio Ccy checkbox determines whether the system should
check if the portfolio currency on the transaction is identical to the
currency in the bank account. This affects the validation of transactions,
setting of popups showing valid bank accounts and selection of valid
settlement default rules."

Three ways an order carries no bank account:
1. No Settlement Our Defaults row matches the portfolio plus settlement
   currency (for example NWM300_A plus CHF when no CHF account exists), and
   Blank Dynamic Account unless in SC is ticked so the QC and PC fallbacks are
   skipped.
2. Settlement defaults are applied at a status the order never reached.
   setdef section 3.7, page 12: Minimum required status for automatic
   settlement defaults and Maximum actual status for running settlement
   defaults on the Defaults tab of Transaction Options. Orders that stay
   pending or partly executed can sit below the minimum.
3. The account exists but is filtered out: cashman section 3.7, page 12:
   "In the Valid within section you may state a portfolio group, restricting
   the bank account only to be used for transactions in this portfolio
   group." A bank account valid within one portfolio is not offered to
   another portfolio's order.

## Settlement Our Defaults (setdef September 2025, section 3.1, page 8)

Window Settlement - Our Defaults. Default type: Back office, Security trade,
Money only. Optional Payment Clearinghouse and Delivery Clearinghouse.
Settlement - Our Defaults By Counterparty exists as the per counterparty
variant (section 3.2, page 9). Dynamic bank account IDs (section 3.5, page
10) let one rule resolve to different accounts through the Free Codes - Bank
Accounts window. Transaction Options, Defaults tab: "Use first rule in
settlement default when running in batch or on service" and "Search
settlement default rules via portfolio structure" (section 3.6, page 11).

## Simulations, OTC and the Default cash position flag

cashman section 3.5, page 11: "The Default cash position check box is used
for assigning bank accounts to simulated positions and orders in front office
holdings." Release Notes 26.04 section 3.13, page 19: for OTC simulations
of type Order "bank accounts are applied based on the order settlement
defaults. Note: If no bank accounts are specified in the order settlement
defaults, the Default cash position bank accounts are applied." Before 26.04
the Default cash position account won over settlement defaults for OTC.

amsim, Create simulation result list: "A cash balance is added to the Cash
Viewer for the payment date of the simulated trade for the default currency
bank account and/or cash bucket." A simulation therefore shows on a bank
account even when the later order does not.

## What a bare currency row means

The Cash Viewer lists one row per bank account (amcv section 3.1, page 11).
A row whose Security ID is the currency code itself, sitting beside the
named accounts under the same currency node, is a cash position booked on
the currency with no bank account. In the Nicola export of 9 September this
is the CAD row under NWM110_A carrying (739,625.00) on 9/10 and the USD row
under NWM240_A carrying (8,100,000.00) on 9/23. The Cash Balance Details of
the CAD row showed Security ID CAD, Payment security name CARGOJET INC,
Business transaction code Buy/Sell, Instrument type Bank account, Payment
type Cash effect, Order number 20260908000153, Payment nominal 9,700.00.

## The check list per affected order

1. Open the order (Order Outbox or Portfolio Orders). Read Bank account,
   Settlement currency, Expected trade date, Payment date, status, executed
   and remaining quantity.
2. Explain Order Defaults on the order: which settlement rule matched, or
   none.
3. Settlement - Our Defaults: load rows for the portfolio; check a row for
   the settlement currency exists and is valid within the portfolio.
4. Order Options: Blank Dynamic Account unless in SC on the Options tab,
   Use the first rule in order defaults on the Options 1 - Portfolio Master
   tab.
5. Transaction Options, Defaults tab: minimum and maximum status for
   automatic settlement defaults.
6. Bank Accounts window for the intended account: Valid within, Default cash
   position, Disable cash management.
Report the first failing step; that is the cause.
