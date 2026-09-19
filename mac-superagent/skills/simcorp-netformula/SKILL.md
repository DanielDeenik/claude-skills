---
name: simcorp-netformula
description: >
  Write SimCorp Dimension ManagersWorkBench .NET formulas (Portfolio Sheet / custom
  columns) and classic Formula-Language formulas. Use when creating, editing, or
  debugging a SimCorp formula — Total Commitment, custom key ratios, exposure,
  moneyness, leverage, price/value columns. Grounded in Nicola's real exported
  formulas (NetFormulas.xlsx) and the 2510 help corpus. Trigger: ".net formula",
  "netformula", "portfolio sheet formula", "custom column", "GetConfigurableKeyRatio",
  "ManagersWorkBench formula", "create a formula" in SimCorp.
---

# SimCorp Dimension — .NET Formulas (ManagersWorkBench) + Formula Language

There are TWO formula engines in SimCorp Dimension. Identify which one you are in BEFORE writing — the syntax is different and not interchangeable.

| | **.NET formula** (this skill's primary) | **Classic Formula Language** |
|---|---|---|
| Editor | Formula name / Title / Category / **Argument** (a .NET type) / Groups / *Treat null as zero* checkbox | Possible fields + Functions and operators panels |
| Fields | **bare PascalCase properties** — `DirtyValuePC`, `InstrumentType` | **braced display titles** — `{Dirty value PC}`, `{Instrument type}` |
| Strings | **double quotes** `"Equity"` | single quotes `'Equity'` |
| Equality | `==` (and `!=`) | `=` |
| Source Type field | `Formula Language` (interpreted) or `C#` (compiled assembly) | n/a |

The editor's **Argument type** decides which properties exist. Most Portfolio-Sheet columns use
`SimCorp.IMS.PortfolioManagement.ManagersWorkBench.Formulas.IPortfolioSheetFormulaArguments`.
(Others seen: `IPortfolioManagementFormulaArgument`, StrategyBuilder `IExternalStrategy*Arguments`.)

> HARD RULE: never invent a property, function, enum value, or field code. Pick fields from the editor's field list and press **Check**. The property name = PascalCase of the view-field code (`DIRTY_VALUE_PC` → `DirtyValuePC`, `BAL_BOOK_VALUE_QC` → `BalanceBookValueQC`); **`QC`/`PC` stay uppercase** (it is `...QC`, NOT `...Qc`). If unsure, type the first letters in the field list and take what autocompletes.

---

## .NET formula syntax (verified from Nicola's NetFormulas.xlsx)

- **Header fields:** Kind=`Ordinary`; Owner=`ALL`; **Return Type** = `System.String` | `System.Nullable<Decimal>` | `System.Nullable<Double>`; **Source Type** = `Formula Language`; **Argument type** = `…IPortfolioSheetFormulaArguments`; **CaptionTest NullGuard** = `Checked` (treat null as zero) / `Unchecked`; Category = free text (e.g. `Nicola Custom`, `Custom`, `Options`).
- **Control flow:** `if <cond> then <X> else <Y>` (nestable). No `endif`.
- **Operators:** `== != > < >= <=`, `and`, `or`, arithmetic `+ - * /`.
- **Assignment & statements:** `name := expr;` then a final return expression. `//` and `/////` comments.
- **Enums (compare to a typed member, NOT a string):** `InstrumentType == InstrumentType.Option`, `OptionType == OptionType.Put`, `OptionType == OptionType.Call`. (Comparing an enum to text fails: `InstrumentType=="Equity"` → "operator Equal requires same type".)
- **Strings:** double-quoted `"OPTION"`, `"AT_COST"`, `"Cash"`.

### Real functions (each verified in a live Nicola formula)
- `GetConfigurableKeyRatio("CODE")` → Decimal — read a configured key ratio by code. Seen: `"Delta"`, `"OPTION_UNDERLYING_PRICE"`, `"EQ_DIVIDEND YIELD"`, `"EQPFOLLEVERAGE"`, `"OPTION_EXP_MONTH"`/`"_DAYS"`/`"_YEAR"`.
- `GetSecurityGroupCode("GroupName")` → String — read a Security Group Code value. Seen: `"Asset Class"` (returns `"Equity"`, `"Cash"`, `"Asset"` for alt-invest, …), `"PricingSource"` (e.g. `"AT_COST"`), `"Best TP"`.
- `GetSumGrandTotal(Property)` → Decimal — grand total of a column, e.g. `GetSumGrandTotal(DirtyValuePC)`.
- `Abs(x)`, `ToNumber(text)`, `ToString(x)`, `Concat(a; b)`.

### Common properties (Portfolio Sheet argument)
`DirtyPrice`, `DirtyValuePC`, `DirtyValueDistribution`, `DirtyValueDistributionPreSimulation`, `DirtyValueDistributionSimulation`, `CleanValueQC`, `BalanceBookValueQC`, `BalanceNominalNumber`, `FXRatePC`, `FXFactorPC`, `StrikePrice`, `Delta`, `LeverageExposureDistribution`, `SecurityGroup` (string, e.g. `"OPTION"`), `PositionScope` (string, e.g. `"Mp"`), `InstrumentType`/`OptionType` (enums), `KeyRatio3/5/10/11/14/17` (configured key-ratio slots).
For balances not listed (e.g. commitment), confirm the exact property name in the editor's field list — view-field codes incl. `BAL_CB_COMMITMENT_QC` (Total Commitment / Balance commitment QC), `BAL_UNPD_COMMIT_QC` (Unfunded), `DIRTY_VALUE_PC`.

### Verbatim real examples (copy these patterns)
```
// PositionScopeHeld  (String)
if PositionScope=="Mp" then "Not Held" else "Held"

// LoanMktValue  (Jeff Burton — SGC switch between two value fields)  ← TEMPLATE for Total Commitment
if GetSecurityGroupCode("PricingSource") == "AT_COST" then BalanceBookValueQC else CleanValueQC

// PriceBase / DirtyPricePC
DirtyPrice*FXFactorPC
DirtyPrice/FXRatePC

// EqLeverage  (enums + SGC + assignment + GetSumGrandTotal)
dCash := if GetSecurityGroupCode("Asset Class")=="Cash" then DirtyPrice else 0;
dPutOptionExposure := if (InstrumentType == InstrumentType.Option and OptionType == OptionType.Put) then StrikePrice*-1 else 0;
((dCash + dPutOptionExposure)*BalanceNominalNumber*FXFactorPC)/GetSumGrandTotal(DirtyValuePC)
```

---

## How to create a .NET formula
1. Open **Formulas** window → new. Set **Name** + **Title**, **Category**, **Argument type** (Portfolio Sheet column → `IPortfolioSheetFormulaArguments`), **Return Type**, **Source Type** = `Formula Language`, tick **Treat null as zero** if it's an arithmetic amount.
2. Write the body using **bare properties** picked from the field list, double-quoted strings, `==`, typed enum members.
3. **Check** (validates types — "then"/"else" branches must be the same type; unknown property → "Unknown field"; enum-vs-text → Equal-type error).
4. Add to the Portfolio Sheet / Key Ratio Mapping as a column.

## Classic Formula-Language (the other engine)
Braced fields, single quotes, `=`, `switch case … default`, `try…catch`, functions `getseckeyrat`, `getsecpkrkeyrat`, `getpfcval`, `getportfig`, `getnav`, `getstatictext`, `securitiesgetfield`. Example: `switch {Instrument type} case 'Bond' : 5 case 'Equity' : 8 default 0`. Full function reference: 435 `FormulaFunction-*.htm` pages in the 2510 help scrape.

---

## Reference: Total Commitment (alts) + equity user-defined key ratio
Goal: one column that = native Total Commitment (`Balance commitment QC`) on alt investments, and dirty value on equities (which have no commitment). Null-guard pattern (Jeff's `LoanMktValue` shape):
```
if BalanceCommitmentQC == 0 then DirtyValuePC else BalanceCommitmentQC
```
Return `System.Nullable<Decimal>`, NullGuard **Checked** (so alt commitment present → returned; equity commitment null→0 → returns DirtyValuePC). Confirm the exact spelling of the commitment property (`BalanceCommitmentQC`) from the field list — it errored before only because of wrong casing (`Qc`) / wrong base name. `DirtyValuePC` is verified real.
