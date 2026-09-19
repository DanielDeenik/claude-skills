# INTAKE Template — Notion Page Structure

Use this spec to create a Notion page that serves as the INTAKE contract.

## Page properties

| Property | Type | Required |
|---|---|---|
| Engagement | Title | yes |
| Profile | Select (simcorp / generic) | yes |
| Status | Select (Draft / Locked / In-Build / Complete / Approved) | yes |
| Version | Text | yes |
| Owner | Person | yes (Dan) |
| Notion Target | URL or §-reference | yes |
| Date Created | Date | yes |

## Page body (in order)

Each H2 below maps to one of the 16 INTAKE fields. Notion DBs work better for `inputs`, `source_truth_map_stub`, `proposed_schema`, and `sme_questions` — convert those four sections into linked inline databases.

### H2 — Audience

Multi-select of named people. Reject "the team".

### H2 — Output Formats

Multi-select pills.

### H2 — Inputs (linked DB)

Database with columns: Path · Role · Description · File exists (formula).

### H2 — Scope In / Scope Out

Two paragraphs. Side-by-side toggle list.

### H2 — Source-of-Truth Map Stub (linked DB)

Database with columns: Output Column · Source File · Source Locator · Role.

### H2 — Proposed Schema (linked DB)

Database with columns: Tab · Column Name · Type (text/Y-N/numeric) · Source · Example · Max Length.

### H2 — Slicing Rule

Free text.

### H2 — SME Questions (linked DB)

Database with columns: ID · From · Date · Question · Status · Owner.

### H2 — Citation Format

Code block with the literal format template.

### H2 — Verification Criteria

Bulleted list of concrete checks.

### H2 — Open Questions for Dan

Toggle list. Each item with a checkbox.

## How Claude consumes a Notion INTAKE

The validator script accepts either a markdown file OR a Notion page URL. For Notion:

```bash
python scripts/intake_validator.py "https://www.notion.so/{page_id}"
```

The script calls `mcp__plugin_engineering_notion__notion-fetch` and serializes the page + linked DBs into the same 16-field structure the markdown form uses. Validation logic is identical from there.

## Why Notion as an option

Three engagement patterns:

1. **Quick one-off** → markdown template, version-controlled in workspace.
2. **Word user reviewing** → DOCX template, fills in Word, Claude reads back.
3. **Cross-team engagement with stakeholders** → Notion page, multiple people fill different sections, audit trail via Notion versioning.

All three end at the same validator and the same 11 checkpoints.
