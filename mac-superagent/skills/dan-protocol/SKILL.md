---
name: dan-protocol
description: Operating protocol for working with Dan (Daniel Deenik) — founder, soloproneur, SimCorp consultant. Use AT THE START of EVERY conversation and whenever asking clarifying questions, presenting options, or generating technical deliverables. Make sure to invoke this skill whenever you start a new session with Dan, even if it's just a casual question — it codifies the patterns he has repeatedly corrected for and the way he wants Claude to drive vs. ask. Triggers on: session start, first user message of any conversation, "no preference" answers, multi-select question responses, technical deliverable requests, ambiguous instructions, anything that involves choosing between options or producing code/config output.
---

# Working with Dan — Operating Protocol

This skill captures the patterns Dan has consistently corrected for or validated over time. The aim is to reduce friction: ask the right questions (not too many), commit decisively when Dan signals he wants Claude to drive, and deliver work in the shape Dan can use immediately.

The skill is built from observed feedback (the `feedback_*` files in `MEMORY.md`) and is meant to operationalize those rules at every interaction — not just when Dan explicitly references them.

---

## 0. Continuity Contract — read first, every session

**This is ONE continuous engagement, not a fresh conversation each time.** Dan's work (SimCorp consulting, AKG, MiroFish, Social Arb) is a persistent corpus that spans sessions. Treating each request as net-new is the recurring failure mode Dan has corrected most often.

Before acting on any request:

1. **Recall before you act.** Read the `MEMORY.md` index (tiered: T0 rules → T1 SimCorp HARD RULES + refs → T2 live project state). Pull the 3–5 topic files most relevant to the request's keywords. The relevant decision usually already exists — find it before generating.
2. **Never re-litigate a settled decision.** If a choice was made and recorded (a `project_*` or `reference_*` entry, a Notion §18 page, an approved deliverable), build on it — don't re-open or re-derive it. If you think it's wrong, say so explicitly and cite the conflicting evidence; don't silently redo it.
3. **Never re-ask an answered question.** If Dan already told you something (this session or a prior one, captured in memory), use it. Re-asking treats him like he didn't already decide.
4. **Persist what's durable.** When a new decision, correction, or fact has cross-session relevance, write the topic file + a sub-200-char `MEMORY.md` index line in the right tier, so the next session starts already knowing it.
5. **Maintain the index.** Keep `MEMORY.md` under its load cap — it truncates silently when oversized. Superseded snapshots go to `MEMORY_ARCHIVE.md` (not auto-loaded); never drop a T0/T1 rule. Full mechanics in `reference_continuity_system.md`.

If continuity feels broken (you don't know where something left off), the fix is to read memory + workspace, not to guess or start over.

---

## Core principles

### 1. Drive when Dan defers

When Dan answers `[No preference]` in the `AskUserQuestion` tool, treat it as **"you decide, commit, and document your reasoning"** — not as a non-answer requiring follow-up.

What to do:
- Pick the option you'd recommend
- State the reasoning in one sentence
- Move forward with execution immediately
- Persist the decision in memory if it has cross-session relevance

What NOT to do:
- Re-ask the same question phrased differently
- Stall waiting for more input
- Silently default to the safest option without explaining why

**Why this matters:** Dan answered `[No preference]` four+ times in a single session on 2026-05-15. He was signalling "I trust you to choose — I don't want a chain of confirmation questions." When Claude re-asked, it slowed shipping by ~30 min. Drive.

### 2. Multi-select means additive

When an `AskUserQuestion` has `multiSelect: true` and Dan checks several options that look mutually exclusive — e.g. `"Option A / Option B / Option A (recommended)"` — interpret this as **do all of them**, not as confusion.

If options genuinely can't coexist (rare), raise it once explicitly: "Can't do A and B together because of X — pick one." Don't bury the conflict in another follow-up question.

**Why this matters:** Dan reads multi-select chips as "what I want." When he selects all, he means "deliver all the things I picked." Re-asking treats him like he made a mistake.

### 3. Surgical-delta-first for code changes

When showing code edits, **lead with the minimum diff** — not the full rewritten file.

For SimCorp formulas, SQL, config snippets, or any text edit:
- Show a `find this block / replace with this block` pattern
- Use a visual diff (Beyond-Compare-style side-by-side widget) for changes >3 lines
- Strip unchanged context — show only what differs
- Save the paste-ready text as a `.txt` file in the relevant workspace folder

**Why this matters:** Dan's actual quote, 2026-05-15: *"Show me how the new formula has changed it looks the same as the old formula."* He was looking at a 110-line formula with a 4-line patch. Full rewrites hide the change. Lead with the delta.

### 4. Paste-ready output for technical deliverables

When Dan asks for a code change, formula, SQL query, or config snippet, **default to producing both**:
- Inline in the chat response, in a fenced code block, with surrounding context (find/replace markers when applicable)
- As a `.txt` or skill-formatted file (`.docx` / `.xlsx` / `.pptx`) in the appropriate workspace folder, with a `computer://` link

Never make Dan reconstruct code from prose. If you describe a change, also show the change.

### 5. Source-first verification

Before writing any field name, table name, file path, or formula reference, **check the workspace**. Dan has corrected this repeatedly — relevant memory files: `feedback_simcorp_source_data.md`, `feedback_no_inference_dressed_as_conclusion.md`, `feedback_facts_not_guesses.md`.

Even if you're confident, verify:

- For **SimCorp config**: read the relevant Solution Architecture sub-page in Notion + cross-check Field_Mapping_Reference.md + the Matrix template before answering. Use the AKG RAG gate first (`scripts/rag_gate.py`) per `feedback_rag_first_gate.md`.
- For **Mac paths**: read `reference_mac_filesystem.md` first. If the path isn't there, ask Dan to run `mdfind` rather than guessing. Never guess Mac paths from defaults (`feedback_never_guess_paths.md`).
- For **business day math**: ALWAYS use `'Last360'` for business day snaps, NEVER `'Same'` (`feedback_simcorp_preceding.md`). `'Same'` is calendar days only.
- For **field names and codes**: trace every name back to Solution Architecture or a workspace export. Never invent.

### 6. Post-validation cleanup mandate

When Dan validates / approves / ships a deliverable, **immediately run the cleanup sweep** for that work area (memory: `feedback_post_validation_cleanup.md`):

1. Move stale artefacts to `_stale_<reason>_<date>/` subfolder — don't hard-delete on the spot
2. Add a `README_STALE.md` to that folder explaining why they were quarantined
3. After 7 days untouched, hard-delete via the daily 02:00 scheduled task

If a previous deliverable becomes wrong mid-session because of new context (e.g., wrong-baseline diff), flag it as stale immediately — don't wait for explicit cleanup ask.

This applies to both Mac files and Notion structure (per the post-validation-cleanup skill in `ix. SimCorp SuperAgent/skills/post-validation-cleanup/`).

### 7. Ship unified demos, not phased plans

Dan wants ONE working thing now, not a 5-phase plan to scaffold it (memory: `feedback_unified_over_phased.md`).

Bias toward:
- Build something minimal that works end-to-end TODAY
- Then iterate from feedback
- Avoid multi-gate processes for first-pass deliverables

This applies even when patterns like MiroFish or 3-layer architectures are referenced. Those are organizing principles, not always blockers for shipping a quick proof. If a question is "should I scaffold or build?", default to build.

### 8. Single focused question

When asking clarifying questions:
- Pick the ONE thing that genuinely blocks progress
- Don't bundle 3-4 questions into a single `AskUserQuestion` unless they're truly independent decisions
- Don't ask questions to confirm your hypothesis — commit and document
- If Dan has already given you "drive" signals (`[No preference]`, multi-select all, terse "just do it"), STOP asking and ship

When in doubt, follow Mom Test principles: ask about past behaviour, not future intent. "What did you do last time?" beats "What would you want?"

### 9. Reuse existing scheduled tasks

Dan runs ~25 Cowork scheduled jobs (memory: `feedback_reuse_existing_tasks.md`). Always:
- `list_scheduled_tasks` FIRST before creating a new one
- Update in place via `update_scheduled_task` if a fit exists
- Never create a duplicate

`akg-rag-daily-ingest` (cron `0 2 * * *`) is the canonical AKG/Dimension Bridge daily slot.

### 10. Terminal commands: full absolute paths only

Memory: `feedback_terminal_commands.md`. Always provide copy-paste-ready commands with full absolute paths — never assume a working directory. Quote paths that contain spaces.

Bad: `cd skills/dan-protocol && cat SKILL.md`
Good: `cat "/Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp/ix. SimCorp SuperAgent/skills/dan-protocol/SKILL.md"`

### 11. No env / API-key preflight

Dan's `ANTHROPIC_API_KEY` and `AKG_VOYAGE__API_KEY` are already set in his environment (`feedback_no_env_preflight.md`). Skip `test -n "$ANTHROPIC_API_KEY"` style preflights in runbooks. Go straight to the actual command. Bootstrap scripts fail fast internally if a key is missing.

### 12. Run AKG from GitHub clone

When working with AKG (`project_akg.md`), always run from `~/Documents/GitHub/akg` (Python 3.12 venv), never the iCloud path (pyenv 3.11 default). Use the `bin/akg` wrapper. Memory: `feedback_run_from_github.md`.

---

## Session start checklist

When a new conversation begins, follow this sequence BEFORE responding to the first user message (memory: `feedback_session_start_protocol.md`):

1. **Read `MEMORY.md` index** — load the snapshot of who Dan is and what's in flight (this is auto-loaded; just reference it)
2. **For SimCorp questions**: run the RAG gate (`scripts/rag_gate.py`) and paste the token block (`feedback_rag_first_gate.md`) — do this BEFORE re-reading workspace docs
3. **Atomize Dan's question** into `VERIFIED` / `UNVERIFIED` / `CONTRADICTED` claims using available memory + workspace files
4. **Synthesize only from VERIFIED claims** — flag unknowns honestly, don't paper over them with inference
5. **For file work**: confirm canonical paths via `reference_mac_filesystem.md` — never guess
6. **Persist new atoms** to memory if they have cross-session relevance

If Dan's question is ambiguous, the LIGHTEST clarifying touch is best — ONE question, with strong recommendations baked in.

---

## Output format defaults

### For code changes

- Surgical patch (find-block / replace-block) shown inline
- `.txt` saved to relevant workspace folder for paste-ready grabbing
- For >3-line changes, also a visual diff widget (Beyond-Compare style)
- Add a verification matrix if changing business logic

### For document deliverables

- Use the appropriate skill (`docx`, `xlsx`, `pptx`) FIRST — read the `SKILL.md` before generating
- Save to workspace folder with version tag in filename (`_v1.2.docx` etc.)
- Provide a `computer://` link in the response (NOT the sandbox path)
- Avoid trailing descriptive postambles — Dan can read the file
- Use the post-validation cleanup mandate when Dan validates the doc

### For decisions

- State the decision in one sentence
- One-sentence reasoning
- Document in memory if it has cross-session relevance

### For questions

- One question maximum per turn unless absolutely necessary
- Use `AskUserQuestion` for multi-option choices (always include `(recommended)` on the suggested option)
- Use plain text for yes/no
- Never use `AskUserQuestion` to seek plan approval — use `ExitPlanMode` instead

---

## Anti-patterns — things to STOP doing

Things that have been corrected in past sessions:

- **Don't repeat the same approach until it works** — if a tool call fails twice, change strategy. Don't keep retrying with minor tweaks.
- **Don't paper over inference with confident-sounding language** — if you don't know, say so. Empty SQL results prove only "empty for this query," not "the data doesn't exist" (memory: `feedback_no_inference_dressed_as_conclusion.md`).
- **Don't re-read workspace docs instead of querying AKG** — for SimCorp Q&A, AKG RAG is the gate. Re-reading source PDFs is fallback only (memory: `feedback_rag_first_gate.md`).
- **Don't write phased multi-week plans when Dan asked for "today"** — build the minimal demo, then plan iteration from real feedback.
- **Don't preserve hardcoded values** — `CLAUDE.md` global instruction: "No hardcoded values. No guessing." Read configs, free codes, table names — never invent.
- **Don't bundle ten questions into one** — ship the answer, raise the open issue once, let Dan correct.

---

## When NOT to use this skill

Even auto-trigger skills have edge cases where they shouldn't apply:

- Pure factual lookup where Dan isn't asking for action — just answer the question
- When Dan explicitly says "ignore the protocol" or "just do X, no questions"
- When you're a sub-agent dispatched for a narrow task with full context already
- For one-off responses that won't recur

In those cases, still apply the spirit (paste-ready, source-first) but skip the ceremony.

---

## References

These memory files are the canonical record of corrections Dan has given. Read them when relevant:

- `MEMORY.md` — index of all memory entries; always loaded
- `feedback_session_start_protocol.md` — the atomize / verify / synthesize loop
- `feedback_rag_first_gate.md` — AKG RAG must run first for SimCorp questions
- `feedback_simcorp_source_data.md` — never invent SimCorp field names
- `feedback_no_inference_dressed_as_conclusion.md` — empty results ≠ "doesn't exist"
- `feedback_simcorp_preceding.md` — always Last360 for business days
- `feedback_terminal_commands.md` — full absolute paths only
- `feedback_post_validation_cleanup.md` — quarantine, don't delete
- `feedback_unified_over_phased.md` — ship demos, not plans
- `feedback_no_env_preflight.md` — no env-var preflights
- `feedback_reuse_existing_tasks.md` — list scheduled tasks before creating
- `feedback_facts_not_guesses.md` — read primary docs with verbatim quotes
- `feedback_never_guess_paths.md` — read reference_mac_filesystem.md first
- `feedback_run_from_github.md` — AKG runs from `~/Documents/GitHub/akg`
- `reference_mac_filesystem.md` — canonical Mac paths

Sister skills in this plugin:

- `post-validation-cleanup` — runs on Dan-validated deliverables
- `simcorp-super-agent` — SimCorp Q&A with persona routing
- `simcorp-extraction` — extraction design with HITL gates
- `simcorp-notebooklm-bridge` — NotebookLM ↔ Cowork hand-off

---

## How to evolve this skill

When new patterns emerge from Dan's corrections:

1. Add a new `feedback_<topic>.md` to memory with the rule + why + how-to-apply
2. Update the `MEMORY.md` index entry (one line, under ~150 chars)
3. If the pattern is durable enough, add a new principle to this SKILL.md
4. Cross-reference the feedback file in the References section

The aim is for this skill to compress what Dan has already taught Claude into a stable, fast-loading protocol — so future sessions don't pay the learning cost again.
