# FK-Catalog Method — resolving key chains without guessing

The authoritative sources live in the client workspace under
`ii. Manuals & Documentation/`. Both are Oracle `INSERT` dumps into an `EXPORT_TABLE`.

- **`export 3.sql`** — the foreign-key catalog. Each row:
  `INSERT ... values ('CHILD_TABLE','CHILD_COLUMN','PARENT_TABLE','PARENT_COLUMN','FK_NAME')`.
  This is the ONLY authority for which column joins to which parent.
- **`export 2.sql`** — table row counts. Each row:
  `INSERT ... values ('TABLE_NAME',NUM_ROWS,LAST_ANALYZED)`. Use it to confirm a table is
  actually populated before relying on it.

Quote the path — it contains spaces.

## Find a table's OUTBOUND foreign keys (which columns leave this table)

```bash
cd "/sessions/epic-confident-mayer/mnt/a. Consulting - SimCorp/ii. Manuals & Documentation"
grep -iE "values \('TABLENAME'," "export 3.sql"
```
Reads as `CHILD_COLUMN → PARENT_TABLE.PARENT_COLUMN` (with the FK name to cite). Example:
```bash
grep -iE "values \('COMPIDS'," "export 3.sql"
# COMPIDS.SECIK        → SECURITIES.SECIK   (R_COMPIDS_SECIK)
# COMPIDS.INDIRECTSEC  → SECURITIES.SECIK   (R_COMPIDS_INDIRECTSEC)
```

## Find who REFERENCES a given parent (who can reach SECURITIES)

```bash
grep -iE "'SECURITIES','SECIK'" "export 3.sql"
```
Returns every child table + column that has a declared FK to `SECURITIES.SECIK`. This is
how you discover candidate bridge tables that carry a security. Then intersect that list
with the tables the builder actually offers at the current node.

## Confirm a table is populated

```bash
grep -iE "'TABLENAME'," "export 2.sql"
# ('COMPIDS',4134,...)  ('COMPIDINSTGEN',0,...)  ('PRIKEYS',62766,...)
```
`NUM_ROWS = 0` (or the table absent from `export 2.sql`) means the FK path may be logically
correct but empty at runtime — validate against live data or pick a populated alternative.

## Reading the internal-key convention

- **`(IK)` = Internal Key** — SimCorp's surrogate primary key. UI labels map to internal
  columns: `Component ID (IK)` → `COMPIDIK`, `Security (IK)` → `SECIK`.
- The dialog shows **friendly labels**; the FK catalog shows **internal column names**.
  Translate between them when matching a dropdown entry to a catalog row.
- A table with **no rows in `export 3.sql`** (like `DECOMPCALRESULTS`) has **no declared
  FKs** — it is a results table joined *logically* on its key columns, not by a database
  constraint. You still supply the keys in the dialog; you just won't find them as FK rows,
  so read them off the dialog/screenshot and confirm the *bridge* table's FKs instead.

## The non-negotiable rule

If a column is not confirmed by `export 3.sql` **and** not visible on the actual UI
dropdown/screenshot, **do not use it**. Stop and flag the gap rather than guessing a name.
