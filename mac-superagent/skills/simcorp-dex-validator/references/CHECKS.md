# What the validator checks (deterministic, against the SCDAT dump)

Ground truth = three exports, indexed once by `build_index.py`:
- **db.sql + db2.sql** — every table, column, data type, table comment, column comment (84k columns).
- **export_fk_catalog.sql** — every declared FK edge child.col → parent.col (~20k edges). This is the join oracle.
- **export_table_catalog.sql** — row count per table. Empty-result + cardinality.

## The checks
1. **Table exists** — resolves lowercase/CEI table names to the real SCDAT table; if missing, returns nearest candidates by name and by description. (Catches `seggen` → SEGDEFS/SEGCOND.)
2. **Field is on that table** — normalises CEI names (`pPRICEPROFIK` → `PRICEPROFIK`) and checks the column exists ON the declared table. If not, lists where the column actually lives. (Catches `PRICEDEFS.pPRIORITY` — not there.)
3. **Join is a real FK** — VERIFIED_FK if the edge is in the FK catalog; IK_MATCH if the column matches the parent's IK by name only (no declared FK — usable but flag it); UNVERIFIED otherwise (do not ship). (Confirms `PRIKEYDEFS.PRICEPROFIK → PRICEPROFS.PRICEPROFIK`.)
4. **Empty-result risk** — any table with 0 rows in the dump is flagged before you build.
5. **Cardinality** — row counts on both sides of every join expose fan-out before it blows up downstream.
6. **Coded-column decode** — NUMBER columns whose comment implies a code (type/quotation/…) are flagged as needing a decode table (use `resolve.py column` to find it). This is the silent-zero guard.
7. **Formula fields** — every alias a formula references must be a real column in scope.

## Principle
Completeness is a property of the extraction, not the operator. The index IS the Fields picker — nothing is ever "NEED PICKER" again; it is either resolved from the index or it genuinely does not exist. No field, table, join, or formula reaches a build sheet until it is green here.
