---
name: data-analyst-solution-architect
description: Hard-gated data-analysis workflow for any tabular deliverable (data dictionary, mapping workbook, field summary, lineage matrix, audit cross-reference). Enforces a 16-field upfront intake form, presence + LLM review validation, 11 sequenced checkpoints with Dan-approval gates at Schema and v0.1 Slice, and 10 anti-shortcut rules learned from the Nicola Privates Data Dictionary v1→v11.1 iteration loop (2026-05-18). Profile-switched — `simcorp` profile bakes in v22-ENRICHED backbone, S-templates, AMCM, FK conventions, 8 SME personas; `generic` profile for any other client. Trigger on: "data dictionary", "data analysis", "build a dictionary", "mapping workbook", "field summary", "lineage matrix", "audit cross-reference", "/data-analyst", or any tabular consulting deliverable spanning multiple source files.
---

# Data-Analyst Solution-Architect Skill

> Built 2026-05-18 from the Nicola Privates Data Dictionary post-mortem.
> The Nicola build went through 11 versions because there was no intake contract.
> This skill exists so version 2 next time is the deliverable, not version 12.

---

## STAGE 0 — HARD HALT GATE (do this BEFORE anything else)

The moment this skill is triggered, before reading any source file, before writing any cell, before calling any tool other than the validator:

```bash
python "$SKILL_DIR/scripts/intake_validator.py" "$INTAKE_PATH"
```

Where:
- `$SKILL_DIR` = this skill's directory (resolve at runtime; symlinked at `~/.claude/skills/data-analyst-solution-architect/`).
- `$INTAKE_PATH` = path to the filled INTAKE.md the user is providing for this engagement.

**If validator exits non-zero — STOP.** Print the validator output to chat verbatim. Do not propose substitutes. Do not "fill in reasonable defaults". Ask Dan to complete the missing/thin fields. Re-run validator. Only proceed to STAGE 1 after exit 0.

If Dan has not yet provided an INTAKE path, render the in-chat elicitation widget from `templates/intake_elicitation_widget.html`. If he prefers a different format, hand him `templates/INTAKE_TEMPLATE.md`, `templates/INTAKE_TEMPLATE.docx`, or the Notion template structure from `templates/INTAKE_TEMPLATE_notion.md`.

No override flag exists. There is no `--force`. The halt is the point.

---

## STAGE 1 — Establish the 11 checkpoints + 10 rules

After the validator passes, IMMEDIATELY do all three:

### (a) Create the 11 checkpoint tasks via TaskCreate

```
0. Intake form complete (validator passed)
1. Source inventory + scope confirmed
2. Source-of-truth map (column → file + locator)
3. Schema design — Dan approves columns (BLOCKING)
4. v0.1 slice — 1 vertical, 5 fields
5. Dan reviews v0.1 (BLOCKING)
6. Full build
7. Verification (counts + cite audit + gap audit)
8. Companion DOCX
9. Notion push §18.x
10. Post-validation cleanup
```

Mark checkpoint 0 completed immediately (validator passed = intake done). Mark checkpoint 1 in_progress.

### (b) Create 10 anti-shortcut TodoWrite items (reminder track)

Copy the 10 rules from `references/anti_shortcut_rules.md` verbatim into TodoWrite. These remain pending throughout the engagement as a visible track. Each rule cites the Nicola version that triggered it.

### (c) Load the profile

If INTAKE field `profile = simcorp` → Read `references/profile_simcorp.md`.
Else → Read `references/profile_generic.md`.

---

## STAGE 2 — Walk the 11 checkpoints

Each checkpoint has a dedicated reference doc with a strict completion rubric. Do not advance past a checkpoint until its rubric is satisfied.

| # | Checkpoint | Reference | Blocking? |
|---|---|---|---|
| 0 | Intake | (validator) | done at validator pass |
| 1 | Source inventory | `references/01_inventory.md` | no |
| 2 | Source-of-truth map | `references/02_source_truth_map.md` | no |
| 3 | Schema design | `references/03_schema_design.md` | **DAN APPROVES** |
| 4 | v0.1 slice | `references/04_v01_slice.md` | no |
| 5 | Dan reviews v0.1 | `references/04_v01_slice.md` | **DAN APPROVES** |
| 6 | Full build | `references/05_full_build.md` | no |
| 7 | Verification | `references/06_verification.md` | no |
| 8 | DOCX companion | `references/07_docx_companion.md` | no |
| 9 | Notion push | `references/08_notion_push.md` | no |
| 10 | Cleanup | `references/09_cleanup.md` | no |

Blocking checkpoints (3 and 5) emit an `AskUserQuestion` "Approve to proceed?" before moving on. Never advance without an explicit "approve" from Dan.

---

## STAGE 3 — Hand off

After checkpoint 10:

- Deliverables list with `computer://` links posted to chat.
- Notion §18.x page URL surfaced.
- MEMORY.md entry written (`project_<engagement>_<date>.md`) covering: deliverable name, what's in it, where, what was decided, what's open.
- `post-validation-cleanup` skill invoked to stage prior versions for archive.

---

## Anti-shortcut rules (must be acknowledged before STAGE 1)

See `references/anti_shortcut_rules.md`. These are *blocking* — if Claude is about to write content that violates a rule, the rule fires and a `[GAP: <reason>]` marker goes in the cell instead. The source-trace audit (checkpoint 7) catches any unfilled gap markers.

The 10 rules in one line each:

1. **Never infer descriptions.** Blank cell beats invented text. (v1–v7 failure.)
2. **Atomic Y/N columns.** "Imported Y/N", "Calculated Y/N", "Derived Y/N" — never long descriptive prose. (v1–v5.)
3. **Strict NAME / DESCRIPTION column split.** "Import File" and "Import File Description" are two columns, never one. (v1–v9.)
4. **Per-vertical = only fields in extracts.** If PE extract has 19 fields, PE tab has 19 rows, not 154. (v1–v8.)
5. **Read every source file before writing any output cell.** No "draft from memory then fix". (Constant root cause.)
6. **SME Q&A inline in relevant tabs.** Banner panel at top of vertical tab + dedicated SME_QA_Full tab. Not buried in a separate DOCX. (v1–v10.)
7. **Every description carries verbatim citation.** `file + section/line/page`. Pricing Doc §3.1, FUND - Fund admin §3.3 FX, db2.sql line 49,198. (v1–v10.)
8. **Match existing column naming convention.** If v22 ENRICHED has "AM Field Name" + "AM Field Description", do not propose "AM_Display_Label". (v3, v5.)
9. **Never use long descriptions.** If you find yourself writing >150 chars in a cell, split into atomic columns. (v1–v5.)
10. **Show gaps honestly.** Empty SQL result proves only "empty for this query"; do NOT extrapolate. Verbatim quotes only; "[GAP: no source found]" for unfilled cells. (v2 wrong orphan count; v8 PROD-vs-TEST DB misdiagnosis.)

---

## Files in this skill

```
SKILL.md                                      ← you are here
references/
├── 00_intake_form_spec.md                    16-field intake contract
├── 01_inventory.md                           source inventory checklist
├── 02_source_truth_map.md                    column → file → locator table
├── 03_schema_design.md                       atomic Y/N + name-desc split rubric
├── 04_v01_slice.md                           1-vertical-5-fields slice rubric
├── 05_full_build.md                          re-runnable build pattern
├── 06_verification.md                        counts + cite audit + gap audit
├── 07_docx_companion.md                      narrative + verbatim sources
├── 08_notion_push.md                         §18.x hub + mermaid embed pattern
├── 09_cleanup.md                             post-validation-cleanup integration
├── anti_shortcut_rules.md                    the 10 rules + violation examples
├── profile_simcorp.md                        SimCorp domain knowledge
└── profile_generic.md                        generic data-engineering rubric
templates/
├── INTAKE_TEMPLATE.md                        primary intake format
├── INTAKE_TEMPLATE.docx                      Word-user intake
├── INTAKE_TEMPLATE_notion.md                 Notion-page structure
└── intake_elicitation_widget.html            in-chat fallback widget
scripts/
├── intake_validator.py                       hard-halt gate
├── source_trace_audit.py                     cell → source verifier
├── build_skeleton.py                         re-runnable .py skeleton generator
└── verification_report.py                    counts + fill rate + gap report
examples/
└── nicola_dictionary_v11_1/
    └── INTAKE_FILLED.md                      worked example
```

---

## Sister skills (route to these instead when appropriate)

- **simcorp-extraction** — for .dat / DEX / DFS / cross-table extraction design (not dictionaries).
- **simcorp-super-agent** — for SimCorp Q&A and Wiki page generation.
- **post-validation-cleanup** — invoked from checkpoint 10.
- **prompt-coach** — if Dan's intake message is itself underspecified.
