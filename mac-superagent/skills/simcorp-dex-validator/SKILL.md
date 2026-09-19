---
name: simcorp-dex-validator
description: >
  Validate a SimCorp Dimension DEX / data-extraction design against the real SCDAT schema
  BEFORE anything is configured — deterministically, not by trial and error. Confirms every
  table exists, every field is on the right table, every join is a real foreign key, every
  coded column has a decode, and flags empty-result and cardinality risk from actual row
  counts. Replaces "NEED PICKER" guessing: the indexed schema IS the picker. Use whenever a
  DEX / extraction / .dat / lineage design names tables, fields, joins or formulas and you
  need to prove it will run. Trigger: validate extraction, validate DEX, check tables/joins,
  will this extract work, confirm field names, resolve SimCorp table/column, FK join check.
type: skill
---

# SimCorp DEX Validator

Turns "I think these are the tables/fields/joins" into a green/red report checked against the
database itself. Sisters: `simcorp-extraction` (design authoring), `simcorp-dex-builder`
(window mirror). This skill is the **validation gate** between design and build.

## Inputs (ground truth — already on disk)
Canonical schema exports (regenerate when the environment refreshes):
- `Reference/Db-Schema-<date>/Db/db.sql` and `db2.sql` — DDL + comments
- `ii. Manuals & Documentation/sc_model/source_uploads/export_fk_catalog.sql` — FK edges
- `…/export_table_catalog.sql` — row counts

## Workflow
1. **Index once** (rebuild only when the schema dump changes):
   `python scripts/build_index.py <db.sql> <db2.sql> <export_fk_catalog.sql> <export_table_catalog.sql> schema_index.json`
   → prints table / column / FK-edge counts and spot checks.
2. **Express the design** as JSON (see `templates/design_template.json`): per extraction, list
   `tables`, `fields` (table+field, CEI names OK), `joins` (child.col → parent.col), and any
   `blocked` items you have not confirmed.
3. **Validate**: `python scripts/validate_design.py schema_index.json my_design.json`
   → per-extraction report: TABLE OK / ????, FIELD OK / BAD (+ where it really lives),
   JOIN OK (VERIFIED_FK) / ~ok (IK_MATCH) / ???? (UNVERIFIED), EMPTY-RESULT RISK, BLOCKED→resolved.
4. **Resolve anything red** with the picker-replacement:
   - `python scripts/resolve.py table PRICEDEFS` — real columns + types + comments
   - `python scripts/resolve.py column "price date"` — which table.column carries it
   - `python scripts/resolve.py fk TRANSMAIN` — real join keys in/out
   - `python scripts/resolve.py find "segment"` — tables by description
5. **Only build what is green.** Fix the design JSON, re-run step 3 until zero ???? / BAD, then
   hand the confirmed tables/fields/joins to `simcorp-dex-builder`.

## Rules
- Never carry a CEI name onto a build sheet unresolved — the validator maps it or fails it.
- IK_MATCH is usable but must be logged as an assumed join (no declared FK).
- A 0-row table is a design smell (wrong table or wrong environment) — investigate before building.
- The index is per-environment. Re-run `build_index.py` after every refresh; schema drift shows
  up as newly-missing tables/fields.

See `references/CHECKS.md` for the full check list and the completeness principle.
