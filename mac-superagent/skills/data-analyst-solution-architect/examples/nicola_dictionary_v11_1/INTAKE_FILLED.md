# INTAKE — NWM Privates Data Dictionary (worked example)

> Filled retroactively from the v11.1 build. This is what the INTAKE should
> have looked like at the START of the engagement on 2026-05-17. Had this
> existed up front, the engagement would have completed in 2–3 iterations
> instead of 11.

---

## 1. engagement
NWM Privates Data Dictionary

## 2. profile
simcorp

## 3. deliverable_name
Nicola_Privates_Data_Dictionary_v{N}_{YYYY_MM_DD}.xlsx

## 4. version
v12

## 5. audience
Erhan Yildirim (Migration), Diana Schinkel (Attribute Config), Chris Wong (PELP), Jeff Burton (Mortgages, SimCorp), Pamela Silva (NWM Mortgages PM), Sebastian Nicholson (NWM Infrastructure), Longco Ko (NWM Infrastructure Sr Analyst)

## 6. output_formats
XLSX primary, DOCX companion, Notion §18.32 sub-page, Mermaid lineage (8 diagrams), re-runnable build script (.py)

## 7. inputs

| path | role | description |
|---|---|---|
| /Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/NWM_AM_Field_Summary_by_Vertical_ENRICHED_v22.xlsx | canonical | 158 AM fields × 11 sheets (master + 5 verticals + 5 enrichment) |
| /Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/Nicola_PE_Mapping.xlsx | canonical | PELP 10-col canonical format (PE_Mapping) |
| /Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/_SimCorp_Help_Extraction/SimCorp_Help_Structured.csv | documentation | 2,866 SimCorp Help table+form descriptions |
| /Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/_SimCorp_Help_Extraction/Field-{NNN}.htm (72 files) | documentation | per-field SimCorp Help verbatim |
| /Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/_SimCorp_Help_Extraction/Pricing_Documentation.pdf | documentation | 70 formulas + 518 definitions |
| /Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/_SimCorp_Help_Extraction/db2.sql | documentation | 49,198 COMMENT ON COLUMN |
| /Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/Alternative_Templates_Matrix.xlsx | template | S-template structure (S2-S9, PD1, PD2) |
| /Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/SCD_Available_Mortgage_Fields_Reference.xlsx | canonical | 505 mortgage fields |
| /Users/danieldeenik/Library/Application Support/Claude/local-agent-mode-sessions/.../uploads/NWM510.txt | extract | wealth-mixed alts portfolio extract |
| /Users/danieldeenik/Library/Application Support/Claude/local-agent-mode-sessions/.../uploads/NWM520.txt | extract | INFRA-FUND + INFRA-DIRECT extract |
| /Users/danieldeenik/Library/Application Support/Claude/local-agent-mode-sessions/.../uploads/NWM530.txt | extract | VC pure extract |
| /Users/danieldeenik/Library/Application Support/Claude/local-agent-mode-sessions/.../uploads/NWM260.xlsx | extract | rich PD extract (WAL/Duration/YTM) |
| /Users/danieldeenik/Library/Application Support/Claude/local-agent-mode-sessions/.../uploads/CDMLP.txt | extract | mortgage extract |
| /Users/danieldeenik/Library/Application Support/Claude/local-agent-mode-sessions/.../uploads/USMFSP.txt | extract | mortgage extract |
| /Users/danieldeenik/Library/Application Support/Claude/local-agent-mode-sessions/.../uploads/USMFSMAI.txt | extract | mortgage extract |
| /Users/danieldeenik/Library/Application Support/Claude/local-agent-mode-sessions/.../uploads/NWM160.xlsx | extract | mortgage extract |
| /Users/danieldeenik/Library/Application Support/Claude/local-agent-mode-sessions/.../uploads/{NWM260,NWM407,PDDLSPV,PDSMAI,PDSMAISPV}.txt | extract | PD extracts (some duplicates: NWM290=NWM407, PDSMAI=PDDLSPV byte-identical) |

## 8. scope_in
Private Equity, Venture Capital, Private Debt, Infrastructure, Mortgages — Mar 31 2026 extracts only. Per-vertical AM-field rosters as actually displayed in extracts.

## 9. scope_out
Wealth-only portfolios except NWM510 (which is wealth-mixed and feeds PE+VC+Infra all). NW2 series. Real estate (not in NWM Privates). Loan-level (vs facility-level) detail.

## 10. source_truth_map_stub

| output_column | source_file | source_locator | role |
|---|---|---|---|
| AM Field Name | NWM_AM_Field_Summary_ENRICHED_v22.xlsx | sheet "Master", col A | canonical |
| AM Field Description | SimCorp_Help_Structured.csv | Forms sheet (2,210 rows), description matching field_name | canonical |
| Calculation Description | Pricing_Documentation.pdf | §3.1-§3.4 + §7.1-§7.4 formula definitions | canonical |
| Imported Y/N | derived | from "Import File" non-blank | derived |
| Import File | Alternative_Templates_Matrix.xlsx | S-template column (S2/S3/S4/S5/S6/S7/PD1/PD2) | canonical |
| In NWM510 Y/N (etc.) | NWM510 extract | column present + non-blank in extract | derived |
| AttrConfig Name | NWM_PE_Mapping.xlsx | AttrConfig sheet | canonical |
| Source | derived | concatenation of source file + locator | derived |

## 11. proposed_schema

```
Tab: Full_Data_Dictionary (master)
  Row = one AM field
  Cols (27):
    - AM Field Name
    - AM Field Description
    - Imported Y/N
    - Import File
    - Import File Description
    - Calculated Y/N
    - Calculation Description
    - Derived Y/N
    - Derivation Rule
    - AttrConfig Y/N
    - AttrConfig Name
    - AttrConfig Free Code Number
    - AttrConfig Description
    - In PE Y/N
    - In VC Y/N
    - In PD Y/N
    - In Infra Y/N
    - In MTG Y/N
    - Fill Rate (NWM510)
    - Fill Rate (NWM520)
    - Fill Rate (NWM530)
    - Fill Rate (NWM260)
    - Source File
    - Source Locator
    - Notes
    - SME Question ID (if any)
    - SME Resolution Status

Tab: Private_Equity (per-vertical)
  Row = one AM field with PE-portfolio fill rate > 0 (19 fields)
  Cols = same 26 minus "In X Y/N" pivots

Tab: Venture_Capital (29 fields, same shape)
Tab: Private_Debt (55 fields, same shape + WAL/Duration/YTM cols where present)
Tab: Infrastructure (29 fields, banner panel with 6 SQ-* items at top)
Tab: Mortgages (22 fields, banner panel with 4 PQ-* items at top)

Tab: SME_QA_Full (dedicated)
  Row = one SME question
  Cols (8): ID | From | Date | Question | SimCorp Answer | Status | Open Action | Owner
```

## 12. slicing_rule
Per-vertical tab contains the column union of AM fields across the extract files mapped to that vertical:
- PE = NWM510 (partial) + ad-hoc PE positions
- VC = NWM510 (partial) + NWM530 (pure VC)
- Infra = NWM510 (partial) + NWM520 (INFRA-FUND + INFRA-DIRECT)
- PD = NWM260 + NWM290/407 + PDDLSPV/PDSMAI + PDSMAISPV
- MTG = CDMLP + USMFSP + USMFSMAI + NWM160

NWM510 is wealth-mixed, contributes to PE+VC+Infra unconditionally (do NOT filter by its Asset Class column — values are generic Asset/Cash/Equity/FX, not vertical names).

## 13. sme_questions

Inline SME items embedded in Infrastructure (6 items) and Mortgages (4 items) tabs as banner panels + dedicated SME_QA_Full tab + full narrative in companion DOCX.

| ID | From | Date | Question | Status |
|---|---|---|---|---|
| SQ-1 | Longco Ko (Infra) | 2026-05-07 | Total Commitment FX methodology — why doesn't NWM520 reconcile to local commitments? | RESOLVED |
| SQ-2 | Sebastian Nicholson (Infra) | 2026-05-07 | KKR DCIF unfunded = -2 | RESOLVED (rounding artifact) |
| SQ-3 | NWM Infra team | 2026-05-08 | EagleCrest IC USD vs CAD translation | RESOLVED |
| SQ-4 | Longco | 2026-05-08 | 757Co Class B NDVS + Class A DVS — Equity treatment | RESOLVED |
| SQ-5 | Longco | 2026-05-08 | Attribute mismatches (Asset Type / Stage / Geography / Vintage) | PENDING (AMO Matthew Chan) |
| SQ-6 | Longco | 2026-05-08 | Column P/Q/R/S precise definitions | RESOLVED |
| PQ-1 | Pamela Silva (MTG) | 2026-05-09 | Security Name/ID — servicer prefix | OPEN |
| PQ-2 | Pamela | 2026-05-09 | NWM160 Cash (AVS CAD + DYN5006) sourcing | ACKNOWLEDGED |
| PQ-3 | Pamela | 2026-05-09 | NWM290 AREEIF notional balance | ACKNOWLEDGED |
| PQ-4 | Pamela | 2026-05-09 | CDMLP Row 31 Country correction | CONFIRMED |

## 14. citation_format
`{verbatim quote} ({source_file}, §{section} | line {N} | p.{page})`
Use `[GAP: no source found in {sources_searched}]` for missing.

## 15. verification_criteria

- All non-blank AM Field Description cells have a non-blank Source column (Rule 7).
- Every Y/N column contains only Y, N, or blank (Rule 2).
- Per-vertical tab row count matches column-union row count from inputs (Rule 4).
- Zero invented descriptions — every description is verbatim from SimCorp source (Rule 1).
- SME Q&A coverage: 10 items in SME_QA_Full tab, 6 in Infrastructure banner, 4 in Mortgages banner.
- Cell length ≤ 150 chars — flag any over (Rule 9).
- Gap audit count surfaced to Dan — not hidden (Rule 10).

## 16. notion_target
§18.32 — Nicola Ultimate Data Dictionary (existing page, update with v12+ link)

---

## 17. open_questions_for_dan

- Should NWM510 wealth-mixed extract count toward PE fill rate or only Infra/VC?
- Are AICOMPONENTS-table fields (AFC 103-142 IK-backed) in scope? Currently Portal-gated, would need Diana to share the DDL.
- Confirm v22-ENRICHED master sheet has all 158 fields, or use the "Master" tab only?
- Should we add a per-AM-field FX-methodology column to capture the PE-blended vs Infra-single-rate split documented in `reference_simcorp_fx_commitment_logic.md` and `reference_nwm_fx_method_sebastian.md`?
