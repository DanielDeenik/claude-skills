# Generic Profile

Loaded when INTAKE field `profile = generic`. No domain-specific knowledge. The 10 anti-shortcut rules and 11 checkpoints still apply identically.

## What changes vs SimCorp profile

- No canonical backbone files declared — Dan's INTAKE must list everything.
- No citation search order — declared per-engagement in source-of-truth map.
- No FK prefix conventions or batch IDs.
- No SME persona routing — INTAKE field 13 declares the personas directly.
- Notion target = INTAKE field 16 (no default hub).

## What stays the same

- 16-field INTAKE.
- Validator presence + LLM review.
- 11 checkpoints with Dan-approval gates at #3 and #5.
- 10 anti-shortcut rules (verbatim from `anti_shortcut_rules.md`).
- All 7 mandatory deliverables (XLSX, DOCX, Notion, verification, source-trace, mermaid, build script).

## When to use this profile

- Other consulting engagements (non-SimCorp).
- Personal projects (Social Arb dashboards, MiroFish research artifacts).
- One-off data cleans where the source documentation isn't a known canon.

## Adapting to a new domain

Three steps to make the generic profile work for a new client:

1. **Declare the citation corpus in INTAKE field 7** — every source file with `role` (canonical / supplementary / documentation).
2. **Declare the citation search order in INTAKE field 14** — for descriptions, look in X first, fall back to Y, then Z.
3. **Declare the schema backbone in INTAKE field 11** — column names match an existing convention (per Rule 8) OR are NEW with explicit sign-off requirement.

If a new client engagement runs through this skill twice, consider creating a `profile_{client}.md` and adding a third profile option to INTAKE field 2.
