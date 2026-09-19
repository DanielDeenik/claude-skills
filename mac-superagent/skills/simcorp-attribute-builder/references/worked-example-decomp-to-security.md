# Worked Example — Decomposition value linked to a Security

**Goal:** build a Numeric custom field **"Decomp Dirty Value"** that returns `Dirty value QC`
from `DECOMPCALRESULTS` (friendly name "Stored Decomposition Results", table group
"Portfolio calculation") and links it to a **security**.

All FK facts below are verified against the client's FK catalog
`ii. Manuals & Documentation/export 3.sql`; FK names are cited so they can be re-checked.

## Verified facts from the FK catalog

- **`DECOMPCALRESULTS` has NO declared FKs.** It is a results table. It is joined
  *logically* on `Component ID (IK)` (internal column `COMPIDIK`) and is additionally keyed
  by `Decomposition calculation set`. Because there are no FK rows, you cannot discover its
  keys from `export 3.sql` — read them off the dialog and resolve the *bridge* table's FKs.

- **`COMPPOSDEFS.COMPIDIK → COMPIDS.COMPIDIK`** (`R_COMPPOSDEFS_COMPIDIK`).
  COMPPOSDEFS carries **no security** — only a component id. This is why picking
  COMPPOSDEFS to reach a security fails, and why its `Using` dropdown only offers
  `Component ID (IK)`.

- **`COMPIDS.SECIK → SECURITIES.SECIK`** (`R_COMPIDS_SECIK`) and
  **`COMPIDS.INDIRECTSEC → SECURITIES.SECIK`** (`R_COMPIDS_INDIRECTSEC`).
  COMPIDS DOES carry the security in the data model — **BUT COMPIDS is not always offered
  in the builder dropdown**, so you may be unable to select it at the component-key node.

- In the actual builder dropdown at the component-key node (**13 tables offered**), the two
  tables that carry a DIRECT security FK are:
  - **`COMPIDINSTGEN.SECIK → SECURITIES.SECIK`** (`R_COMPIDINSTGEN_SECIK`) and
    **`COMPIDINSTGEN.COMPIDIK → COMPIDS.COMPIDIK`** (`R_COMPIDINSTGEN_COMPIDIK`) —
    "Virtual Instrument Generation Information". **THIS is the correct bridge**: keyed by
    `Component ID (IK)` and carrying `SECIK`.
  - **`PRIKEYS.SECIK → SECURITIES.SECIK`** (`R_PRIKEYS_SECIK`), also
    `PRIKEYS.COMPIDIK → COMPIDS.COMPIDIK` (`R_PRIKEYS_COMPIDIK`) —
    "Pricing & Key Ratio Keys" — a pricing-key oriented alternative.

## The two wrong attempts (why they failed)

1. **COMPPOSDEFS** — natural first guess (it's the component-position table), and it IS
   offered. But it holds no security; its only outward path is `COMPIDIK → COMPIDS`. Its
   `Using` dropdown only offers `Component ID (IK)`. You cannot reach a security through it.
2. **COMPIDS** — the correct data-model home of the security (`SECIK`, `INDIRECTSEC`). But
   the builder did **not** offer COMPIDS at that node, so it was not selectable. Knowing the
   FK exists is useless if the dialog won't let you pick the table.

Only by grepping the FK catalog for the *exact tables the dropdown offered* (all 13) did
`COMPIDINSTGEN` surface as a table that is both **offered** and **carries `SECIK`**.
**This is the whole reason the skill exists: cross-check the FK catalog against the actual
dropdown; never guess.**

## Correct configuration (field anchored on a security/holding row)

```
[Return]  Table: DECOMPCALRESULTS ; ID: Dirty value QC ; Using: Component ID (IK) ; from: Table ↓
   Table: COMPIDINSTGEN ; With key: Security (IK)=SECIK ; Using: Component ID (IK)=COMPIDIK ; from: Attribute ↓
      Attribute: Security (IK)   (context security)
   + second key on DECOMPCALRESULTS: Decomposition calculation set
        (from Attribute, or pin via DECOMPCALEXECS "Decomposition Calculation Executions")
```

Read top-down: return `Dirty value QC`; to pick the row, use `Component ID (IK)`; that
component id comes from `COMPIDINSTGEN`, matched by `Security (IK)` = the context security's
`SECIK`. The chain bottoms out at the `Security (IK)` attribute on the evaluation row.

## Compound key — do not forget the second part

`DECOMPCALRESULTS` is keyed by **both** `Component ID (IK)` **and** `Decomposition
calculation set`. Supplying only the component id returns an arbitrary result row (a
security decomposed under many runs → one-to-many). Pin the calc set as a second key, from
an attribute or via `DECOMPCALEXECS` ("Decomposition Calculation Executions").

## One-to-many hazard

One security can be a component under many parents / many calc runs. Without the calc-set
constraint (and optionally a parent constraint via a relations table) the field is
non-deterministic. If it cannot be constrained to exactly one row, the field should instead
be evaluated at the finer (component-level) granularity.

## Populated-data caveat

Verify the bridge table has rows before relying on it (`export 2.sql`). In the current
client DB, `COMPIDINSTGEN` shows `NUM_ROWS=0` (last analyzed 29-NOV-25) while `COMPIDS`
(4,134) and `PRIKEYS` (62,766) are populated. The `COMPIDINSTGEN` FK path is correct, but
if it is empty at runtime the field returns nothing — validate against live data, or use
the populated `PRIKEYS` alternative if it fits the intended semantics.
