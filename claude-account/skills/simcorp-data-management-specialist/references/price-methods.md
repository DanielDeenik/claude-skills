# Price method domain (Domain-67), catalogue by family

Names for values 9 to 74 captured from the help portal on 2026-08-28; codes 2, 11, 12, 18, 31, 44, 60, 68 and 69 also confirmed by the TEST CEI code map. Full per method table with explanations, validity and NWM usage: PriceMethod_Explained sheet of the lineage workbook. Never hardcode these codes into logic; refresh from Show Values or the captured catalogue.

## Codes 1 to 8, partially resolved

2 is Quoted price. The other names were not visible in the capture. Three ladder methods MUST occupy three of the remaining slots because their names are absent from the 9 to 74 list: Theoretical price, Repo yield + quoted U lying, Quoted price + quoted U lying. One capture of the top of the value list closes the numbering. Until then, refer to these three by name only.

## Lookup family (reads something stored)

- 2 Quoted price: stored price from the Prices window by security, type, date. Behind almost every ladder step.
- 44 Quoted value: a stored amount for the position rather than a per unit price. Amount valued alts and direct real estate.
- 31 Position price: prices tied to a specific portfolio, from the Position Prices window. Same security, different price per portfolio.
- 53 Quoted value, position: the value analogue of 31.
- 73 Explicit quoted price: the explicitly registered price for the holding.
- 58 Trade level price: the price carried on the trade.
- 15 From key ratio calculation, 62 From pricing and key ratio calculation: reuse figures a key ratios calculation already stored (View Key Ratios and the Pricing and Key Ratios Calculations window).
- 51 From portfolio calculation: reuses the portfolio calculation result. The single step behind the ALTS_AM definition for alternative investments; ties AM alt values to the PFC chain.

## Cash adjusted alternatives family (commitment funds)

Per the Alternative Investments manual, these take calls and distributions into account between GP statements: 60 Quoted value cash adjusted, 65 Quoted price cash adjusted, 68 Explicit quoted value cash adjusted, 69 Explicit quoted price cash adjusted. NWM carries them in FUNDS_ALT_AMOUNT, FUNDS_ALT_UNIT and the ALTS GE_VAL_ALTS_BOND and GE_VAL_ALTS_EQ definitions, mostly against the GP price type.

## Theoretical family (computes)

- Theoretical price (code 1 to 8) and variants: 21 structured products, 55 preemptives, 67 collateral CTD (finds the cheapest to deliver collateral currency via the collateral discount curve mapping), 70 NDS, 71 convertible bonds.
- Black 76 option pricing: 16 Quoted price + repo yield + quoted U lying (options, incl. options on CTD futures needing all deliverable bond data).
- FX family: 17 Spot + both interest rates (results on the price currency leg; bank accounts, cash buckets, FX spots, forwards, swaps), 30 base currency variant, 18 Spot + tics + Int. price Ccy, 54 base currency variant, 45, 46, 49, 50 FX forward P and L variants.
- Curves and spreads: 26 Quoted price + yield curve, 19 zero coupon, 28 and 61 repo yield curves, 25 vol curve, 32 corporate bond yield spread, 33 and 35 combined curve methods, 29 Discounted margin (floating rate debt only, interest types Floating, Rev. floating, Super floating), 10 Quoted price + margin rate, 47 STIBOR FRN, 34 Australian yield, 48 basis swap, 23 Reference rate.
- Models and interfaces: 38 XpressInstrument (pricing model definition applied to modelled underlyings; swaptions, ILS), 63 quote first then XpressInstrument, 37 External calculation, 43 FINCAD convertible bonds, 74 Yield Book, 56 ISDA converter, 39 Credit derivatives.
- Underlying based: 36 Quoted Underlying, 40 Quoted Ultimate Underlying, 59 CTD futures quality option, 22 Quoted price drawn bonds, 24 Nominal price dual Ccy bonds, 64 and 72 convertible variants, 20 and 57 structured product quote variants (structured or convertible instruments only), 27 Fund components + fund (required on the definition used by look through portfolio calculations), 41 basket analogue, 66 Fund components + quoted fund, 52 Fund legal reporting value.

## Terminal family (guarantees a value)

- 11 Booked price: from booked value QC and nominal. NOT supported for Asset Manager and Compliance Manager (finding F16). Terminates most NWM ladders; fine for NAV consumers, invisible to the AM.
- 12 Cost price: holds the position at cost (FUNDS_AT_COST).
- 9 Maturity price: matured paper at redemption value (MORTGAGES ladder).
- 42 No discount: straight repos with the discount rate at zero.

## The 24 methods in live NWM use

Quoted price, Booked price, Cost price, Position price, Quoted value, Quoted value position, Quoted value cash adjusted, Quoted price cash adjusted, Explicit quoted value cash adjusted, Explicit quoted price cash adjusted, Theoretical price, Theoretical price preemptives, Maturity price, Quoted price drawn bonds, Quoted price + yield curve, Reference rate, CTD futures quality option, Quoted price + quoted U lying, Quoted price + repo yield + quoted U lying, Repo yield + quoted U lying, Spot + both interest rates, Spot + tics + Int. price Ccy, Fund components + fund, From portfolio calculation. Everything else in the domain is available but unused at NWM.
