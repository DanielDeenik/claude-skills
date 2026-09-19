# SimCorp Profile

Loaded when INTAKE field `profile = simcorp`. Contains SimCorp Dimension domain knowledge that Claude needs before checkpoint 1 (inventory).

## Canonical backbone files

These are the files almost every SimCorp data deliverable starts from. If they're not in INTAKE field 7 (inputs), ask Dan whether to add them:

| File | Role | Path pattern |
|---|---|---|
| `NWM_AM_Field_Summary_ENRICHED_v22.xlsx` | canonical AM field roster (158 fields) | workspace root |
| `Nicola_PE_Mapping.xlsx` | PELP canonical 10-col format | workspace root |
| `SimCorp_Help_Structured.csv` | 2,866 SimCorp Help table/form descriptions | `_SimCorp_Help_Extraction/` |
| `db2.sql` COMMENT ON COLUMN | 49,198 DB column descriptions | `_SimCorp_Help_Extraction/` |
| `Field-*.htm` (72 files) | per-field SimCorp Help pages | `_SimCorp_Help_Extraction/` |
| `Pricing_Documentation.pdf` | 70 formulas + 518 definitions | `_SimCorp_Help_Extraction/` |
| `SCD_Available_Mortgage_Fields_Reference.xlsx` | 505 mortgage fields | workspace root |
| `Alternative_Templates_Matrix.xlsx` | S1–S9 template definitions | workspace root |

## Citation search order (Rule 1, Rule 7)

When looking up a description for an AM field, search in this priority:

1. `Field-{NNN}.htm` — verbatim field-level help
2. `SimCorp_Help_Structured.csv` (Forms 2,210 rows) — form-level descriptions
3. `SimCorp_Help_Structured.csv` (Tables 656 rows) — table-level descriptions
4. `Table-*.htm` — verbatim table help
5. `Command-*.htm` — command/job descriptions
6. `Pricing_Documentation.pdf` — formula definitions (boost: calculat/formula/compute/derive/=/accru/yield/duration)
7. `db2.sql` COMMENT ON COLUMN — DB-level description

First hit wins. Record the hit's locator in the Source column.

## S-template structure

Per memory `feedback_simcorp_s_numbering.md`:

| Template | Object |
|---|---|
| S2 | Assets (TAIASSETS) |
| S3 | Investment Links (AIINVESTLINKS) |
| S4 | Alt Investments (TSEC ALT_FD subset) |
| S5 | Equities (TSEC ALT_EQUITY) |
| S6 | Bonds / Mortgages (TSEC variants) |
| S7 | Call Money (TSEC CALL_MONEY) |
| S8 | Leverage Link |
| S9 | (reserved) |
| PD1 | Loan Facilities (LOANFACILITIES) |
| PD2 | Loan Contracts (LOANCONTRACTS) |

Template numbering is *template-tab numbered*, NOT object-oriented. Cross-check Notion against the Matrix file.

## FK prefix conventions

Alts portfolio codes: 130, 140, 160, 220, 260, 280, 290, 407, 510, 520, 530, 700, 900.
Mortgage lender codes: NAC, SP, PCC, IMC, CMLS, PHC, MCAP, PQ, FN, LFC, JPM.

## AttrConfig Free Code families

- AFC — AIASSETS 1–142 (103+ are IK-backed)
- SFC — Security
- TFC — Transaction
- PFC — Portfolio
- EFC — Equity

AICOMPONENTS fields cannot traverse via AMCM (memory: `project_amcm_architecture.md`).

## Batch IDs

| ID | Purpose |
|---|---|
| `FO_DECOMP_DAILY` | 8-step decomposition chain |
| `UPDATE_DATES` | on GE_FUNDCERT |
| `FO_FND_MP_COMP_UPD` | (not CLI_UPD) |
| `FO_TAA_UPD` | TAA recalc |
| `FO_FND_FOH_UPD` | FOH update |
| `LF_DRAW_PAYD`, `LF_FEE`, `LF_SPREAD_CHANGE`, `LF_REPRICE` | Loan facility events |

## 8 SME personas (route inline SME questions to these)

| Persona | Domain | When to route |
|---|---|---|
| Yann | IBOR | IBOR/SCD/data extracts |
| Giorgio | ABOR | NAV/fund accounting |
| Diana Schinkel | Attribute Config | Free Codes, AttrConfig, native-vs-attribute |
| Erhan Yildirim | Migration | Field mapping, migration overlay |
| Chris Wong | PELP | PE/Alt asset structure, PE_Mapping |
| Jeff Burton | Mortgages | Mortgage product, FX/commitment logic |
| Miguel | PD | Private Debt, LOANFACILITIES |
| Lotte | Look-through | PELP lookthrough, segment hierarchy |

Inline SME questions in INTAKE field 13 carry the persona; the SME Q&A banner panel cites them.

## SimCorp formulas reference

Per memory `project_simcorp_formulas.md`: 7 fund date formulas (SGC/DEX/COND_DEFAULT, D/W/M/Q, noon cut-off, waitlist +500, preceding convention). Preceding convention: ALWAYS use `Last360` for business day snaps, never `Same` (memory `feedback_simcorp_preceding.md`).

## Notion §18 hub

SimCorp Solution Architecture lives at §18. New deliverables get the next available §18.{N} sub-page. Check existing pages first:

- §18.7, §18.7.1, §18.7.2 — Forecast Model
- §18.10, §18.11 — Nicola alts architecture
- §18.16 — MiroFish SME team
- §18.17 — AM Mapping Clean
- §18.18 — PD Testing
- §18.27 — NWM520 Infra Review
- §18.29.5 — Internal FoF Decomposition
- §18.30 — NWM S-Template Review
- §18.31 — NWM Privates Unified Solution
- §18.32 — Nicola Ultimate Data Dictionary
- §18.33 — Nicola Privates PROFESSIONAL Dict v3
