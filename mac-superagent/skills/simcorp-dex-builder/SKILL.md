---
name: simcorp-dex-builder
description: >
  Build a SimCorp Dimension Data Extraction (DEX) the way it is actually configured in
  the Extraction Definitions window — NOT as Oracle table.column SQL. Use when creating,
  editing, or specifying a data extract / .dat export / cross-table pull in SimCorp.
  Grounded in the real Extraction Definitions window, the "201 Module 8 — Data Extractor"
  training exercise, and the 2510 Tools manual (Segments + Formulas). Produces a buildable
  spec mapped 1:1 to the window tabs. Trigger: "data extraction", "DEX", "extraction
  definition", "extraction setup", "extracts exporter", "extract to .dat", "build an
  extract", "U_ table", "data extractor". Sister to simcorp-extraction (conceptual design)
  and simcorp-netformula (formulas).
---

# SimCorp Dimension — Data Extractor (DEX) Builder

A DEX is built in the UI by selecting **functional fields** from logical tables and the
system generates the SQL. You never hand-write SQL, and you never reference Oracle
physical names (`TRANSMAIN`, `TRCBUSNO`) in the definition.

> HARD RULES (each one a mistake that has been made and corrected):
> 1. **Functional field names only** — pick from the field picker (e.g. "Business transaction code", "Trade date", "Payment amount QC", "Transaction cancellation flag"). Oracle column names belong to the DB schema, not the Data Extractor.
> 2. **Never hand-write the SQL / master statement.** The Source tab (Tables + Joins + Conditions) generates it. Use **Preview** / **Count records** to verify — do not assert a row count you have not previewed.
> 3. **A UI screenshot is the source of truth** for tab and field names. Read them off the screenshot; do not substitute from the schema or memory.
> 4. **Never invent a Definition type, field, table, or segment name.** If the live window shows a dropdown you can't enumerate (e.g. **Definition type**), say so and ask — don't guess.
> 5. **Segments read ONE table** and are referenced by ID. The Table-Group taxonomy (transactions / portfolios / instruments / …) belongs to SEGMENTS, not to "the DEX type".
> 6. `Last360` for any business-day as-at; **code-table joins fail loud** (never silent NULL).

---

## The Extraction Definitions window (verified structure)

**Header:** `ID` · `Name` · `Definition no.` · `Definition type` (dropdown — confirm options from the live window) · `Incomplete definition` (checkbox — tick while building).

**Upper tabs:** `Source` · `Destination Fields` · `Formulas` · `Plug-ins` · `Settings`.

**Source tab** = a **Statement hierarchy** tree (buttons: New, Edit, Delete, **Preview**, **Count records**) plus lower sub-tabs:

| Sub-tab | What goes here |
|---|---|
| **Tables** | columns: `Table` · `Inline view` · `Table alias` · `Type` · `Full view`. Add the logical tables (main + linked). |
| **Fields** | the source fields selected (functional names). |
| **Sorts** | sort order of the output. |
| **Joins** | how the added tables link (alias.field = alias.field). |
| **Conditions** | filters on fields (operator + value; can reference a Variable). |
| **Segments** | attach a Tools segment to scope (one table, by ID). |
| **Variables** | runtime-prompted values (e.g. a `:FROM` date). |
| **Extra** | misc. |

**Destination Fields** = the output columns and their order/format (what lands in the `U_` table or file).

---

## Build workflow (Definition → Setup → Exporter)

### 1. Extraction Definition (`Data Extraction > Extraction Definitions`)
- Set `ID`, `Name`, `Definition type` (confirm), tick `Incomplete` while building.
- **Source > Tables**: add the main logical table + any linked tables (give each an alias).
- **Source > Joins**: link them on their key fields.
- **Source > Fields**: pick the functional fields to output.
- **Source > Conditions**: filters (e.g. `Transaction cancellation flag = Active`, `Trade date >= :FROM`).
- **Source > Variables**: define runtime variables (e.g. `:FROM` date).
- **Source > Sorts**: set sort order.
- **Destination Fields**: map/confirm output columns.
- **Preview** / **Count records** to validate before saving; untick `Incomplete`.

### 2. Extraction Setup (`Data Extraction > Extraction Setups`)
- Attach the definition (+ segment). Choose **Destination type**: a **user schema** (`SCDEX`) with an extracted table named `U_<name>` (the `U_` prefix is required), **or** `None` when the target is a file export.
- `Execution Plan` shows the generated SQL + duration; `Preview Data` confirms rows.

### 3. Extracts Exporter (`Data Extraction > Extracts Exporter Definitions`)
- Exporter type `New Extraction`, linked to the Setup.
- Create a **reference / export file** (Edit Table; path = installation `rep` directory).
- Separation type `<tab>`; select fields and set **positions** (output order).
- Add a **Standard Header**; set a **field format ID** for dates (e.g. `YYYYMMDD`).
- **Test** the export, then **Execute**. Inspect via **Extracts Viewer** (Functions > Show All; note the 5,000-row clipboard/paste limit).

### Derived columns
A computed column (e.g. a "Vertical" tag from Portfolio) is a **Formula** (`Tools > Formulas`), defined in **Extraction Formula Fields** with Usage = `Data Extractor` before it can be selected. Not SQL.

---

## Ground before you build (no guessing)
1. **Read the canonical procedure**: `iii. Training Modules/…201_Module_8_Exercise…Data_Extractor….pdf` (the worked exercise) and `ii. Manuals & Documentation/tools.pdf` (Segments §3, Formulas §2).
2. **Confirm field & table names** against the field picker (live UI screenshot) or, for the DB label, `_simcorp_overview/simcorp_overview.duckdb` (`db_columns`) and `_simcorp_help_extract/db2.sql`. The picker uses functional names; the DB label maps to them (e.g. `TRCBUS.TRCBUSNAME` = "Business transaction code name").
3. **Reuse an existing built extract** as a template where one exists (e.g. exported `dxddefs`, `AM_Extract_DEX_FieldMaps_v1.xlsx`, the verified PD / Infra extracts). Match Nicola's naming + conventions.

---

## Worked example — "transaction codes used across alternatives"
Goal: which business transaction codes are booked for PE / VC / Infra / PD, explained.

- **Tables**: Transactions (main) + Business transaction codes + Portfolios + Securities (outer).
- **Joins**: transaction → business code; → portfolio; → security.
- **Fields**: Portfolio, Business transaction code, Business transaction code name, Instrument type, Security ID, Security Name, Trade date, Payment amount QC, Transaction number.
- **Conditions**: Transaction cancellation flag = Active; Trade date >= :FROM (Variable).
- **Segment**: alts portfolios (PE NWM510/NWM700; Infra NWM520; VC NWM530⚠; PD NWM260/NWM407/PDDLSPV/PDSMAI/PDSMAISPV/NWM900⚠).
- **Setup**: user schema → `U_TRC_ALTS`, or None for file.
- **Exporter**: reference file, `<tab>`, positions, Standard Header, execute.
- **Post-step (combined view)**: distinct Business transaction code + vertical flags + counts, joined to `Nicola_Transaction_Codes_Readable.xlsx` for the plain-English explanation.

---

## Anti-patterns (do NOT do these — all corrected in real use)
- ❌ Writing `SELECT … FROM TRANSMAIN JOIN TRCBUS …` as the "spec". The window generates SQL; specify Tables/Joins/Fields/Conditions instead.
- ❌ Using Oracle column names (`TRCBUSNO`, `PORIK`, `SECIK`) in the definition. Use functional field names.
- ❌ Calling it a "Transaction-type DEX" from the bookkeeping-segment taxonomy. The DEX's actual type is the `Definition type` dropdown — confirm it; segments (not the DEX) carry the Table-Group taxonomy.
- ❌ Asserting row counts without **Preview** / **Count records**.

Related memory: [[reference_dex_build_method]] · [[feedback_ui_screenshots_are_source_of_truth]] · [[reference_simcorp_2510_manuals]].
