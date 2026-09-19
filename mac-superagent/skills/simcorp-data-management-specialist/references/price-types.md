# NWM price types, feeds and consuming ladders

A price type labels a stored price row in the Prices window. Resolved codes come from the TEST CEI code map; the full PRICETYPE domain pull in production is still open (extraction X7). Never hardcode a code that is not in the resolved map.

## Resolved types and where they are used

- Manual Override (14). The trump card, step 1 of every definition at max age 0. Desk override for today only; beats every feed.
- Close (12). End of day market price from the feeds. The standard second step: FUNDS_PUBLIC (0 then 10 day retry), WEALTH_MAIN (1), mortgages, loan quotes (30), nearly every ALTS definition at 0 or 1.
- Mid (4). Mid market quote. FUNDS_PUBLIC step 3 at 0; heavily used in the ALTS template at max age 0 as the same day alternative before Close for futures, options, warrants, IRF, FX forwards and LFI bonds.
- BVAL Mid (25). Bloomberg BVAL evaluated bond price. Read only by FUNDS_BVAL step 2 at max age 1, serving Bond rows in the PR_BVAL segment.
- SS&C (18). Fund administrator price. Step 2 of all WEALTH definitions with cycle matched max ages (1, 7, 40, 120), FUNDS_NICOLA and the fund certificate catch all at 120, ALTS GE_VAL_FUNDS_CLOSE at 300.
- NBIN (19). Custodian price. Step 3 of every WEALTH definition, same cycle max ages. Wealth side fallback behind SS&C.
- FundServ (21). Retail fund price over the FundServ network. FUNDS_MUT_FD and GE_VAL_FUNDS_CLOSE at 0 to 1.
- Manual (20). Ordinary manually entered price, low in the ladder (FUNDS_AT_COST, FUNDS_HISA, FUNDS_MUT_FD). For instruments with no feed, keyed on a normal cadence.
- GP (27). General partner reported value. The alternatives workhorse: FUNDS_ALTS_DI, the fund certificate catch all, FUNDS_ALT_AMOUNT and FUNDS_ALT_UNIT, mostly through cash adjusted methods so calls and distributions between statements are respected.
- Impaired (28). Written down valuation. Step 2 of FUNDS_MRTG (0) and FUNDS_LOAN_FACILITY (30), deliberately above Servicer and Close so an impairment decision overrides routine pricing.
- Servicer (29). Loan servicer price. FUNDS_MRTG (60) and FUNDS_LOAN_FACILITY (30). Routine periodic valuation of mortgages and private debt facilities.
- Nicola (30). Internal valuation. FUNDS_ALTS_DI step 2, FUNDS_MRTG fallback at 60, and the FUNDS_NICOLA definition family.
- Par (code unresolved, finding F14). Only GE_VAL_LN_PAR reads it, loan facilities at par. Resolve the code with the domain pull before use.

## Known orphan

- ALTS_AM. Present on imported alternative prices in production, consumed by NO ladder step in MAIN or in the four traced profiles, so prices imported under it never reach a valuation (finding F02). Alternative rows value From portfolio calculation instead. Treat as an orphan: either the import is repointed to a consumed type, a ladder step is added deliberately, or the import is retired. The price import owner decides; blast radius comes from the binding review first.

## Max age conventions

Match max age to the valuation cycle of the source: 0 for same day only (overrides, same day mids), 1 daily, 7 weekly, 40 monthly, 120 quarterly, 300 annual style alternative funds, 30 to 60 for servicer and loan pricing. A max age wider than the source cadence hides staleness; narrower starves the ladder into its fallback.

## Feeds into PRICES

Bloomberg BVAL, SS&C, NBIN, FundServ, GP statements, servicer feeds, Nicola manual entry, and the alternative investment imports. Every feed writes SECIK, PRICETYPE, PRICEDATE, PRICE, QUOTATION plus source keys. The standing control: every imported type consumed somewhere, every consumed type fed by someone (the orphan and starvation cross join in the validation playbook).
