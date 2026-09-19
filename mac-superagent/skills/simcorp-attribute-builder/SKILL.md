---
name: simcorp-attribute-builder
description: >
  Build a SimCorp Dimension Custom Field / Attribute (Custom Field Configuration
  dialog) by constructing the table-lookup key chain correctly — grounded in the
  client's foreign-key catalog, never guessed. Use when creating, editing, or
  specifying a custom field that reads a value from a result/data table and must
  resolve which row via a recursive key lookup, and when linking such a field to a
  security, holding, or component. Teaches: start from the value, supply EVERY part
  of a compound key, resolve each key by walking real FKs (export 3.sql), cross-check
  the builder dropdown against the FK catalog, and anchor at a real context attribute.
  Trigger: "custom field", "attribute configuration", "custom field configuration",
  "build attribute", "map a field", "link to a security", "decomposition custom field",
  "DECOMPCALRESULTS", "lookup chain", "table group", "With key", "Component ID (IK)".
  Sister to simcorp-dex-builder (extractions), simcorp-netformula (formulas).
---

# SimCorp Dimension — Custom Field / Attribute Builder

A **Custom Field Configuration** (a.k.a. Attribute) returns one value read from a table
and resolves *which row* to read via a recursive key-lookup chain. You do not write SQL.
You assemble the chain in the dialog, and each hop must be justified by a real foreign
key or a value visible on the actual UI dropdown — never by a guessed column name.

## 1. The dialog, field by field

Top of the dialog (the value definition):
- **Type** — Numeric / Text / Date / … (the datatype the field returns).
- **Attribute** — the field's display name. **Description** — free text.
- **From table group** — the functional grouping (e.g. `Portfolio calculation`).
- **Table** — the internal table name (e.g. `DECOMPCALRESULTS`) with a friendly
  **Table name** (e.g. `Stored Decomposition Results`).
- **ID** — the column whose value the field returns (e.g. `Dirty value QC`).
- **As unit** — checkbox: return the per-unit value vs. the total.

The key chain (repeats, one block per hop):
- **Using `<field>`** — the key column used to pick the row in the current table.
- **from ( ) Attribute  ( ) Table** — where that key's value comes from:
  - **Attribute** = a field already present on the current evaluation row (the anchor).
  - **Table** = a nested lookup into another table — one more join hop.
- Each nested block adds: **Table** (the target), **With key** (the match/join column in
  that target table), **Using** (what that target returns), and again **from
  Attribute/Table** to recurse. The chain MUST bottom out at a **from Attribute** anchor.

## 2. How to read the chain

Read it **top-down**: *"return THIS value (ID); to know which row, here is the KEY
(Using); here is where the key comes FROM (Attribute or a nested Table)."*
- **Top = the return value.**
- **Bottom = the anchor** — the innermost `from Attribute` is the seed on the current
  evaluation-context row (e.g. the security, holding, or position being evaluated).
- Every `Table` hop in between is a bridge that translates one key into the next.

## 3. The method (the core of this skill)

1. **Start from the value.** Pick the table + ID column that physically holds the number
   or text you want. That fixes the top of the chain.
2. **Identify the target table's key(s) — including COMPOUND keys.** Many result tables
   need MORE THAN ONE key to identify a row. Example: `DECOMPCALRESULTS` is keyed by BOTH
   `Component ID (IK)` AND `Decomposition calculation set`. Matching only one part returns
   an arbitrary/non-deterministic row. **Supply every key part.**
3. **Resolve each key by walking foreign keys — never by guessing.** The authoritative
   source is the client's FK catalog: `ii. Manuals & Documentation/export 3.sql`. Grep it
   for a table to see exactly which child column joins to which parent
   table.column (see `references/fk-catalog-method.md`). Row counts (to confirm a table
   is actually populated) are in `export 2.sql`.
4. **Respect the UI's offered subset.** At each nested node the builder offers only a
   FILTERED list of tables (e.g. ~13 tables keyed by `Component ID (IK)`), NOT every table
   the data model could theoretically join. So the correct bridge must be BOTH
   (a) present in the dropdown the user actually sees, AND (b) confirmed by the FK catalog
   to carry the needed key. Read the dropdown / screenshot as source of truth, and match
   it against the FK catalog. "The data model has this FK" is NOT the same as "the builder
   offers this table here" — verify both.
5. **Flag one-to-many hazards.** If a key maps to many rows (e.g. one security is a
   component under many parents or many calc runs), the field is non-deterministic unless
   constrained (by calc set, and optionally by parent via a relations table). If it can't
   be constrained cleanly, note that the field may need to be evaluated at a finer
   granularity instead.
6. **Anchor at a real attribute.** Set the innermost `from Attribute` to a field that
   actually exists on the evaluation-context row.

## 4. HARD RULES

- **Never invent field/column names.** Every join column must come from the FK catalog
  (`export 3.sql`) or be read off the actual UI dropdown/screenshot. If neither is
  available, **STOP and say so** — do not guess.
- **No hardcoding.**
- **The UI screenshot / dropdown is the source of truth** for what is actually selectable
  at each node.
- **Distinguish** "the data model has this FK" from "the builder offers this table here" —
  verify BOTH before choosing a bridge.
- **State compound keys explicitly** and require every part to be supplied.
- **Call out one-to-many** hazards; a chain that can resolve to multiple rows is broken.

## 5. Worked example (condensed)

Goal: Numeric field **"Decomp Dirty Value"** returning `Dirty value QC` from
`DECOMPCALRESULTS` ("Stored Decomposition Results", group "Portfolio calculation"),
linked to a **security**.

Two wrong attempts, then the fix:
- **COMPPOSDEFS** — offered, but its only FK to a security path is `COMPIDIK → COMPIDS`;
  it carries **no security**, so its `Using` dropdown only offers `Component ID (IK)`.
  Dead end for reaching a security.
- **COMPIDS** — DOES carry the security (`SECIK → SECURITIES`, plus `INDIRECTSEC`), but is
  **not offered** by the builder dropdown at the component-key node. Can't select it.
- **COMPIDINSTGEN** ("Virtual Instrument Generation Information") — IS offered AND, per the
  FK catalog, carries a direct security FK (`SECIK → SECURITIES`) while keyed by
  `COMPIDIK → COMPIDS`. **This is the correct bridge.** (`PRIKEYS`, "Pricing & Key Ratio
  Keys", is the pricing-oriented alternative — also offered, also carries `SECIK`.)

Correct configuration (anchored on a security/holding row):
```
[Return] Table: DECOMPCALRESULTS ; ID: Dirty value QC ; Using: Component ID (IK) ; from: Table ↓
   Table: COMPIDINSTGEN ; With key: Security (IK)=SECIK ; Using: Component ID (IK)=COMPIDIK ; from: Attribute ↓
      Attribute: Security (IK)          (context security)
   + second key on DECOMPCALRESULTS: Decomposition calculation set
        (from Attribute, or pin via DECOMPCALEXECS "Decomposition Calculation Executions")
```
The lesson: only by grepping the FK catalog for the exact tables the dropdown actually
offered did `COMPIDINSTGEN` surface. **Cross-check the FK catalog against the real
dropdown; never guess.** Full walkthrough with cited FK names:
`references/worked-example-decomp-to-security.md`. FK-catalog procedure and commands:
`references/fk-catalog-method.md`.

> Populated-data caveat: always confirm the chosen table has rows (`export 2.sql`). In the
> current client DB `COMPIDINSTGEN` shows `NUM_ROWS=0` — the FK path is correct, but if the
> table is empty at runtime the field returns nothing, so validate against live data or use
> the populated alternative.

## 6. Pre-Save checklist

- [ ] **Value fixed** — correct Table + ID column for the number you want; `As unit` set
      correctly (per-unit vs total)?
- [ ] **All key parts supplied** — every part of a compound key present (e.g. Component ID
      (IK) *and* Decomposition calculation set)?
- [ ] **Every column verified** — each `Using` / `With key` column confirmed in the FK
      catalog (`export 3.sql`) or read off the actual dropdown/screenshot; nothing guessed?
- [ ] **Bridge is offered AND correct** — the chosen nested table is in the real dropdown
      AND the FK catalog confirms it carries the needed key?
- [ ] **Anchor set** — innermost `from Attribute` is a field that exists on the evaluation
      row?
- [ ] **One-to-many constrained** — the chain resolves to exactly one row; otherwise flag
      and reconsider granularity?
- [ ] **Populated** — target tables have rows (`export 2.sql`)?
