---
name: prompt-coach
description: Enforce Anthropic's 9 prompt-engineering pillars on non-trivial tasks. Auto-detects underspecified prompts (Dan's user prompts AND Claude's subagent/Task prompts) and runs a pillar-by-pillar checklist. For Dan's prompts → HALT and present diagnostic, force Dan to rewrite himself (coaching, not rewriting). For Claude's subagent prompts → silently auto-fix before dispatching the subagent. Triggers when a prompt involves files, deliverables, multi-step work, or ≥3 likely tool calls AND is missing ≥3 of the 9 pillars. Skip for pure conversational Q&A. Pillars are sourced from Anthropic's official prompt engineering canon (docs.anthropic.com/en/docs/build-with-claude/prompt-engineering). Use when: starting any non-trivial task, before invoking the Task/Agent tool with a subagent prompt, when Dan's prompt is vague or missing structure, when about to spend >5 tool calls on a single user request.
---

# Prompt Coach — Enforce Anthropic's 9 Pillars

This skill exists because most prompts (Dan's and Claude's) are missing structure that would make the output 2-3x better at zero marginal cost. It runs a fixed 9-pillar diagnostic, sourced from Anthropic's official prompt engineering docs, and forces a rewrite when too much is missing.

**The pillars come from Anthropic, not opinion.** Order matches Anthropic's stated importance ranking in their overview doc.

---

## When to run this skill

**ALWAYS run** when ANY of these are true:
- Dan's prompt names a deliverable (file, doc, deck, sheet, report, skill, code, config)
- Dan's prompt implies ≥3 tool calls (research + write + verify; or multi-file edits)
- You're about to call the `Task` / `Agent` tool to dispatch a subagent
- Dan's prompt is one short sentence on a non-trivial topic ("build me X", "fix Y", "research Z")

**SKIP** when:
- Pure conversational question ("what's the capital of France?", "what time is it in Tokyo?")
- Dan is replying to a clarifying question (the prompt context is the prior turn)
- Dan explicitly says "skip the coach" / "no coaching" / "just do it"

---

## The 9 pillars (Anthropic canon, ordered by importance)

| # | Pillar | Look for | Source |
|---|---|---|---|
| 1 | **Clear & direct task** | Explicit verb + object. NOT "help with X" — YES "build a 3-tab XLSX with X/Y/Z columns" | [be-clear-and-direct](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct) |
| 2 | **Examples (multishot)** | At least 1 input→output example for non-trivial format work | [multishot-prompting](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting) |
| 3 | **Chain of thought** | "Think step by step" / `<thinking>` tags / "show your reasoning before answering" | [chain-of-thought](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought) |
| 4 | **XML tag structure** | `<context>`, `<task>`, `<examples>`, `<format>`, `<constraints>` — NOT flat prose | [use-xml-tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) |
| 5 | **Role / system context** | "You are a SimCorp consultant" / "act as a senior PM" — sets behavior + tone | [system-prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts) |
| 6 | **Prefill** | First word(s) of expected output to constrain format. *Deprecated for Claude 4.6+ — skip unless on Claude 3.x* | [prefill](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response) |
| 7 | **Chain prompts** | Multi-step work broken into sequential prompts vs one monster prompt | [chain-prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts) |
| 8 | **Output format** | "Return as DOCX", "JSON with these keys", "3-column markdown table" — explicit | overview |
| 9 | **Success criteria + constraints** | Definition of done + what NOT to do ("no hardcoding", "cite sources verbatim") | overview |

**Grounding** is treated as a sub-pillar of #9 (a constraint: "read source X first; if not found, ask, don't guess"). It's Dan's #1 standing rule per CLAUDE.md.

---

## Trigger threshold

A prompt is **underspecified** if:
- It's missing **3 or more** of pillars 1–5, 8, 9 (skip 6 prefill / 7 chain — context-dependent)

AND

- It involves a deliverable, files, or ≥3 tool calls

If both conditions met → coach. Otherwise → proceed.

---

## What to do: TWO modes by scope

### Mode A — Dan's prompts to Claude (HALT and coach)

If Dan's prompt fails the threshold, **do not start work**. Respond with this exact-format block and stop:

```
PROMPT COACH — your prompt is missing N/9 pillars.

✗ 1. Clear task — [what's vague: e.g. "research" with no scope]
✓ 2. Examples — [or ✗ with what's missing]
✗ 3. Chain of thought — no "think step by step" / no <thinking>
✗ 4. XML structure — flat prose, no <context>/<task>/<format>
✗ 5. Role — no actor specified
— 6. Prefill — N/A (Claude 4.6+)
— 7. Chain prompts — N/A (single-step task)
✗ 8. Output format — unspecified (file type? structure? length?)
✗ 9. Success criteria — no DoD, no constraints

Suggested rewrite template:
<role>You are a [X]</role>
<context>[background, files to read first, prior decisions]</context>
<task>[verb + object + scope]</task>
<examples>[1 input→output sample]</examples>
<output_format>[file type, structure, length]</output_format>
<success_criteria>[done when X, Y, Z]</success_criteria>
<constraints>[no hardcoding, cite source §, ask if unsure]</constraints>

Rewrite and resend. Or reply "skip coach" to proceed as-is.
```

Then **wait**. Do not start work. Do not offer to do it for him. The point is to train the prompting muscle.

### Mode B — Claude's subagent prompts (silent auto-fix)

Before invoking `Task` / `Agent` tool, run the same checklist on the prompt YOU are about to send. If it fails the threshold, **rewrite it silently** using the template above, THEN dispatch the subagent. No halt, no announcement to Dan — coaching subagent prompts wastes nobody's time, so just fix and proceed.

This is asymmetric on purpose: Dan wants to learn; subagents just need a better prompt.

---

## Bypass

Dan can bypass with any of: "skip coach", "no coaching", "just do it", "as-is". Honor immediately and proceed.

---

## Self-application

This skill applies to ITSELF: if you're about to invoke `prompt-coach` and the user's prompt is genuinely conversational ("hey what's up"), don't run it. The threshold check (deliverable / files / ≥3 tool calls) is the gate.

---

## Sources (Anthropic canon)

- [Prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Prompting best practices (Claude 4)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Be clear and direct](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct)
- [Multishot prompting](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting)
- [Chain of thought](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought)
- [Use XML tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)
- [System prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts)
- [Prefill (deprecated 4.6+)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response)
- [Chain complex prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)
