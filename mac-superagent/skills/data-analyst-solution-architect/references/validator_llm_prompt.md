# Validator LLM Review Prompt

Used by `scripts/intake_validator.py` after the presence check passes. The script serializes the filled INTAKE.md, embeds it inside this prompt, and asks Claude (Haiku in production, Sonnet in development) for structured findings.

## Prompt template

```
You are the LLM-review step of an intake validator for a data-analysis skill.
The user has filled out a 16-field intake form. Your job is to flag fields that
are thin, contradictory, implausibly short, or self-inconsistent — NOT to
suggest improvements.

CRITICAL: This is a halt-gate. Findings will block the engagement from
proceeding. Be precise. Surface real problems. Do NOT flag stylistic preferences.

INTAKE CONTENT:
---
{intake_content}
---

For each of the 16 fields, return a JSON object:

{
  "engagement":          { "ok": true|false, "reason": "" },
  "profile":             { "ok": true|false, "reason": "" },
  "deliverable_name":    { "ok": true|false, "reason": "" },
  "version":             { "ok": true|false, "reason": "" },
  "audience":            { "ok": true|false, "reason": "" },
  "output_formats":      { "ok": true|false, "reason": "" },
  "inputs":              { "ok": true|false, "reason": "" },
  "scope_in":            { "ok": true|false, "reason": "" },
  "scope_out":           { "ok": true|false, "reason": "" },
  "source_truth_map_stub": { "ok": true|false, "reason": "" },
  "proposed_schema":     { "ok": true|false, "reason": "" },
  "slicing_rule":        { "ok": true|false, "reason": "" },
  "sme_questions":       { "ok": true|false, "reason": "" },
  "citation_format":     { "ok": true|false, "reason": "" },
  "verification_criteria": { "ok": true|false, "reason": "" },
  "notion_target":       { "ok": true|false, "reason": "" }
}

Flag with ok=false when:
- audience contains a generic label like "the team" or one unnamed person
- inputs lists only 1-2 files for a deliverable that obviously needs more
- inputs has any path that doesn't look absolute
- scope_in and scope_out overlap or contradict
- proposed_schema has fewer than 3 columns (insufficient for atomic Y/N pattern)
- proposed_schema has any column over 30 chars (likely a description, not a name)
- sme_questions field promises items but lists none
- citation_format is missing a "{file}" or "{section}" placeholder
- verification_criteria says "looks good" or similarly vague
- notion_target doesn't match the pattern §NN.M or §NN
- profile=simcorp but inputs has no canonical SimCorp backbone file
  (NWM_AM_Field_Summary, PELP, SimCorp_Help_Structured, db2.sql, Field-*.htm)

Do NOT flag with ok=false when:
- a field is short but specific (e.g., audience = "Dan, Diana, Erhan" is fine)
- inputs list is long but reasonable
- a stylistic preference differs from your default

Return ONLY the JSON object. No prose.
```

## How the script uses the response

```python
findings = json.loads(claude_response)
thin = [k for k, v in findings.items() if not v["ok"]]
if thin:
    print("HALT — LLM review flagged thin fields:")
    for k in thin:
        print(f"  {k}: {findings[k]['reason']}")
    sys.exit(2)
```

## Tuning the prompt

If false positives become a problem (Dan sees the validator halt on fields he intentionally kept brief), edit the "Do NOT flag with ok=false when..." section. Do NOT loosen "Flag with ok=false when..." — those are the actual failure modes from the Nicola loop.
