---
name: prompt-template
description: Return a fillable, use-case-specific prompt template built on Anthropic's 9 prompt-engineering pillars. Companion to prompt-coach — template hands Dan the scaffold, coach diagnoses the filled draft. Detects use case (Claude Code engineering, research/analysis, subagent dispatch via Task/Agent tool, or general) from prompt cues and returns the matching XML scaffold with all 9 pillars as labeled slots. Triggers when Dan asks for "a template", "scaffold this", "structure for a prompt", "/template"; when his prompt is one vague sentence; when fewer than 2 of 9 pillars are present (too thin to diagnose); or before invoking Task/Agent tool with a thin briefing. Hands off to prompt-coach for the diagnostic check once Dan fills the template in. Pillars sourced from Anthropic's official prompt-engineering canon.
---

# Prompt Template — Fillable Scaffolds Built on Anthropic's 9 Pillars

This skill is the **companion to `prompt-coach`**. They're a pair:

| Skill | When | What it does |
|---|---|---|
| `prompt-template` (this one) | Dan asks for a template, OR prompt is so empty there's nothing to diagnose | Returns a labeled, fillable XML scaffold — Dan fills it in |
| `prompt-coach` | Dan has a draft prompt with some structure | Scores the draft against the 9 pillars, halts work until rewritten |

**Template first, diagnostic second.** If Dan hands over a blank request like "research X" or "build me Y", don't run prompt-coach's diagnostic on near-nothing — give him a template to fill in. Once he fills it in, prompt-coach takes over.

---

## When to run this skill

**ALWAYS run** when ANY of these are true:

- Dan explicitly asks: "give me a template", "scaffold this", "what should this prompt look like", "/template", "prompt template for X"
- Dan's prompt is severely underspecified — fewer than 2 of the 9 pillars are present
- Dan is about to dispatch a subagent with a 1-sentence brief
- Dan says "I want to start prompting Claude Code better" / "rewire how I prompt"

**SKIP** when:

- Dan already has a partial prompt with ≥3 pillars present → `prompt-coach` is the right tool (diagnostic, not scaffold)
- Pure conversational question
- Dan says "skip template" / "no template" / "just do it"

---

## Step 1 — Detect the use case

Read Dan's prompt and classify into ONE of four use cases. Use the cues below. If ambiguous, ask Dan to pick.

| Use case | Cues |
|---|---|
| **Coding (Claude Code)** | mentions code, file paths (`.ts`/`.py`/`.tsx`/etc.), repo, branch, function, bug, refactor, implement, test, lint, migration, PR |
| **Research / analysis** | mentions research, investigate, analyze, find, sources, market, competitor, due diligence, thesis, report |
| **Subagent dispatch** | mentions the Task/Agent tool, "delegate", "subagent", "parallel agents", "in parallel" |
| **General** | none of the above clearly applies — universal fallback |

---

## Step 2 — Return the matching template

Return the template inside a markdown code block so Dan can copy-paste. Add a one-line note at the top telling Dan which template was selected and why. **Do NOT start work** — wait for Dan to fill it in and resubmit.

### Template A — Coding (Claude Code)

```xml
<role>You are a senior [LANGUAGE] engineer working in [REPO/PROJECT]. [Optional: experience hint, e.g. "expert in Postgres migrations"].</role>

<context>
  <repo_state>
    [Current branch, what's in CLAUDE.md, what was last shipped]
  </repo_state>
  <files_to_read_first>
    - [path/to/file1.ts — why: for understanding X]
    - [path/to/file2.ts — why: this is the convention to follow]
  </files_to_read_first>
  <prior_decisions>
    [What the team already ruled out, agreed conventions, what NOT to revisit]
  </prior_decisions>
</context>

<task>
  [Explicit verb + object + scope. NOT "fix the bug" — YES "Add a retry-with-backoff wrapper around the SQS publish call in src/queue/publish.ts, max 3 attempts, exponential backoff 1s/2s/4s."]
</task>

<plan_first>
  Before editing any file: produce a 5-line plan listing the files you'll touch and the order. Wait for my OK before writing code.
</plan_first>

<examples>
  [1 input→output snippet of the pattern to follow, OR a pointer to a similar function in the codebase, e.g. "see src/queue/consume.ts for the retry pattern already in use"]
</examples>

<chain_of_thought>
  Before each file edit, state in 1 line WHY this edit is needed. Don't narrate the obvious.
</chain_of_thought>

<output_format>
  - Edit existing files; don't create new ones unless the task requires it
  - Match existing style ([2-space indent, ESLint config, Prettier])
  - Inline comments only where intent is non-obvious
  - End with a 3-line summary of files changed
</output_format>

<success_criteria>
  - All existing tests pass: `[TEST_CMD]`
  - New behavior is covered by ≥1 unit test
  - `[LINT_CMD]` and `[TYPECHECK_CMD]` are clean
  - No new dependencies added
</success_criteria>

<constraints>
  - NO hardcoded values — use env vars / config
  - Don't touch files outside the scope listed above
  - If you find a related bug, FLAG it — don't fix it (Karpathy guidelines)
  - If unsure about scope, ask before assuming
</constraints>
```

### Template B — Research / Analysis

```xml
<role>You are a [senior research analyst in DOMAIN | mosaic-theory practitioner | investigative journalist].</role>

<context>
  <topic>[Specific subject + time window, e.g. "$COMPANY's Q1 2026 churn jump"]</topic>
  <why_im_asking>[The decision this informs — investment, hire, product call]</why_im_asking>
  <prior_research>[What I already know, links I've read, what I've ruled out]</prior_research>
</context>

<task>
  [Verb + object + scope. e.g. "Build a 1-pager on why $COMPANY's Q1 churn jumped 40% — focus on pricing-change correlation, exclude macro factors."]
</task>

<sources_to_prioritize>
  - PRIMARY: [10-K, S-1, investor decks, primary documents]
  - SECONDARY: [earnings calls, press releases, official statements]
  - TERTIARY: [reputable analyst notes, structured sentiment]
  - AVOID: [marketing blog posts, vendor-sponsored research, anonymous forums]
</sources_to_prioritize>

<chain_of_thought>
  Show your reasoning before the conclusion. State what you ruled out and why. Flag any inference that goes beyond the source.
</chain_of_thought>

<examples>
  [1 example of a prior research output I liked, OR a sample of how I want a claim formatted with its citation]
</examples>

<output_format>
  - Length: [1-page markdown / 3-page report / Notion page]
  - Sections: TL;DR → Key finding → Evidence → Counterarguments → What I'd still want to know
  - Every load-bearing claim has inline citation [Title](URL)
</output_format>

<success_criteria>
  - Every load-bearing claim is sourced
  - At least 2 counterarguments addressed
  - Confidence level stated per claim (high/medium/low) with reasoning
  - End with 5 follow-up questions worth investigating next
</success_criteria>

<constraints>
  - No speculation beyond evidence — say "unknown" when unknown
  - Flag sources older than 18 months
  - Don't use general knowledge to fill gaps — search the web or ask
  - Cite verbatim where possible
</constraints>
```

### Template C — Subagent Dispatch (Task/Agent tool)

```xml
<agent_role>
  You're a [research / build / verify / audit] subagent.
  Parent context: [1-2 sentences on what the parent Claude is working on overall, so you understand WHY this task matters]
</agent_role>

<your_specific_task>
  [Verb + object + boundaries. Narrower than the parent task. e.g. "Find every place in this repo where the legacy `auth.middleware.old` is still imported. Report file paths and line numbers."]
</your_specific_task>

<what_you_should_know>
  [Background the parent has but you don't. e.g. "We're mid-migration to a new auth lib. /api/users/* is already migrated — don't re-report those files."]
</what_you_should_know>

<what_weve_ruled_out>
  [So you don't redo work. e.g. "We already grepped for `requireAuth` — that's the new lib, not what we're looking for. We want `authMiddleware.old` specifically."]
</what_weve_ruled_out>

<scope_boundaries>
  - DO: [grep, read, report findings]
  - DON'T: [edit files, run tests, fix the bug — just report]
</scope_boundaries>

<return_format>
  Report under [N] words. Format:
  - Punch list of file:line:context entries
  - Nothing else — no preamble, no summary, no "I hope this helps"
</return_format>

<success_criteria>
  - Every match has file:line:context
  - No false positives (commented-out code doesn't count)
  - If you find zero matches, say so plainly — don't speculate
</success_criteria>
```

### Template D — General / Universal (fallback)

```xml
<role>You are a [actor with expertise — e.g. "a senior product manager who has shipped 3 B2B SaaS products"]</role>

<context>
  [Background: who's asking, why, what's already been decided, files/docs to read first, prior decisions]
</context>

<task>
  [Explicit verb + object + scope. NOT "help with X" — YES "produce a 5-bullet brief on X covering Y and Z, max 200 words"]
</task>

<examples>
  [1 input→output example of the format / style I want]
</examples>

<chain_of_thought>
  Think step by step before answering. Show your reasoning in <thinking> tags before the final answer.
</chain_of_thought>

<output_format>
  [File type / structure / length / where to save it]
</output_format>

<success_criteria>
  [Definition of done: X must be true, Y must be present, Z must be cited]
</success_criteria>

<constraints>
  - No hardcoded values
  - Cite sources verbatim where used
  - If unsure, ask — don't guess
  - [Any project-specific rules from CLAUDE.md]
</constraints>
```

---

## Step 3 — Hand off to prompt-coach

After Dan fills in the template and resubmits, **`prompt-coach` runs the 9-pillar diagnostic on the filled-in version**. That's the verification step — does the filled template actually express all 9 pillars, or did Dan leave placeholders/skipped slots?

This handoff is automatic — Dan doesn't need to invoke it. Both skills should already be active in his Cowork session.

---

## The 9 pillars represented in each template

For audit / sanity: every template above maps to Anthropic's canon ordered by importance.

| # | Pillar | Where it lives in the templates |
|---|---|---|
| 1 | Clear & direct task | `<task>` slot in all four |
| 2 | Examples (multishot) | `<examples>` slot |
| 3 | Chain of thought | `<chain_of_thought>` slot (or `<plan_first>` in Coding) |
| 4 | XML tag structure | Entire template uses XML tags |
| 5 | Role / system context | `<role>` or `<agent_role>` slot |
| 6 | Prefill | N/A on Claude 4.6+ (omitted) |
| 7 | Chain prompts | The template-then-coach handoff IS a chain |
| 8 | Output format | `<output_format>` or `<return_format>` slot |
| 9 | Success criteria + constraints | `<success_criteria>` + `<constraints>` slots |

---

## Bypass

Dan can bypass with: "skip template", "no template", "just give me X". Honor immediately and proceed without the scaffold.

---

## Sources (Anthropic canon — same as prompt-coach)

- [Prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Prompting best practices (Claude 4)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Be clear and direct](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct)
- [Multishot prompting](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting)
- [Chain of thought](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought)
- [Use XML tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)
- [System prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts)
- [Chain complex prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)
