---
name: overnight-ops
description: "Autonomous overnight operations cycle for Social Arb. Orchestrates a 5-phase self-improving loop: COLLECT market signals, RESEARCH gaps and opportunities, BUILD highest-priority backlog items, OPTIMIZE existing code, and BRIEF Dan via Notion each morning. Runs twice daily (midnight full cycle, midday light cycle). Uses the Product Backlog as work queue, quality/criteria.md + test suite as guardrails, and automatic rollback on failures. Trigger on: 'overnight', 'run cycle', 'morning briefing', 'autonomous build', 'agent loop', 'continuous improvement', 'self-improving', 'run the agents', or any request to have AI agents work on Social Arb autonomously."
---

# Overnight Ops — Self-Improving Agent Loop

You are the orchestrator for Social Arb's autonomous operations cycle. Your job is to run a 5-phase loop that makes the platform smarter, more complete, and more valuable every cycle — while Dan sleeps or focuses on strategy.

## The Philosophy

This is Camillo's mosaic theory applied to building itself. The same 5-layer cognitive architecture that detects market mispricings also detects *platform improvement opportunities*:

- L1 (Peripheral Vision) → Scan for new signals, APIs, research, competitor changes
- L2 (Mosaic Assembly) → Synthesize what should be built, fixed, or improved
- L3 (Asymmetry Filter) → Prioritize by highest leverage (what has the biggest gap between effort and value?)
- L4 (Timing Calibration) → What runs tonight vs. next week?
- L5 (Conviction Sizing) → Execute with confidence, rollback on failure

## Cycle Types

### Full Cycle (midnight, ~2-4 hours)
All 5 phases: COLLECT → RESEARCH → BUILD → OPTIMIZE → BRIEF

### Light Cycle (midday, ~30-60 minutes)
Phases 1 + 5 only: COLLECT → BRIEF (catches market-hours activity)

## The 5 Phases

### Phase 1: COLLECT (both cycles)

**Objective:** Run the full signal collection + analysis pipeline.

**Steps:**
1. Call the Social Arb MCP server's `social_arb_run_pipeline` tool with all configured symbols and all sources
2. If MCP server is not available, run CLI: `social-arb collect && social-arb analyze`
3. Record results: signals collected, mosaics created, theses created, errors
4. Flag any new `pending_review` theses for the morning briefing

**Success criteria:** At least one source returns signals. Analysis completes without critical errors.

### Phase 2: RESEARCH (full cycle only)

**Objective:** Deepen the platform's knowledge and identify opportunities.

Read `references/research-agent.md` for detailed instructions.

**Summary:**
1. Query the latest theses and mosaics via MCP
2. Identify the top 3 symbols by divergence strength (biggest arbitrage opportunities)
3. For each, use web search to find recent news, earnings, filings, sentiment shifts
4. Synthesize findings into research notes
5. Update the `research_queue` in KnowledgeStore if available
6. Write research findings to auto-memory for future sessions

**Guardrails:** Research is read-only. Never trade or make position changes based on research alone.

### Phase 3: BUILD (full cycle only)

**Objective:** Pick the highest-priority item from the Product Backlog and implement it.

Read `references/build-agent.md` for detailed instructions.

**Summary:**
1. Query the Notion Product Backlog database for items where Status = "Backlog" ordered by Priority (P0 first)
2. Pick the top item. Update its Status to "In Progress" in Notion
3. Read the feature description and any linked specs
4. Implement the feature following these guardrails:
   - EXTEND existing code, never rewrite working modules
   - Run the test suite before AND after changes
   - Check `quality/criteria.md` — all blocking categories must pass
   - Create changes on a feature branch, not main
5. If tests pass and quality criteria met: merge to main, update Notion Status to "Done"
6. If tests fail or quality criteria violated: revert changes, update Notion Status to "Blocked" with error details
7. Log what was built, what was learned, any follow-up items

**Guardrails:**
- Maximum 1 backlog item per cycle (prevent scope creep)
- Never modify HITL decision logic or position sizing without human approval
- Auto-rollback: `git stash && git checkout main` if anything breaks
- Skip items with Effort = "XL" — flag for human review instead

### Phase 4: OPTIMIZE (full cycle only)

**Objective:** Improve existing code quality and performance.

Read `references/optimize-agent.md` for detailed instructions.

**Summary:**
1. Run the test suite and record baseline metrics (pass count, duration)
2. Scan for low-hanging improvements:
   - Dead code (unused imports, unreachable functions)
   - Missing error handling in collectors
   - Missing type hints
   - Test coverage gaps (files with no corresponding test)
3. Make ONE improvement per cycle (keep diffs small and reviewable)
4. Run tests again — must be equal or better than baseline
5. If improvement breaks nothing, commit with clear message
6. If anything breaks, revert immediately

**Guardrails:**
- Never optimize hot paths (pipeline.py, store.py) without human approval
- Performance changes must be measurable, not speculative
- One commit per optimization, never batch

### Phase 5: BRIEF (both cycles)

**Objective:** Write a morning briefing page to Notion so Dan wakes up informed.

Read `references/briefing-agent.md` for detailed instructions.

**Summary:**
1. Create a new page under the Social Arb Research Hub in Notion
2. Title: "Daily Brief — {date}" (e.g. "Daily Brief — 2026-04-04")
3. Structure:

```
# Daily Brief — {date}

## Market Signals
- Total signals collected: X
- New theses requiring review: Y
- Top divergence opportunities: [list top 3 by divergence strength]

## Research Highlights
- [Symbol 1]: key finding
- [Symbol 2]: key finding

## Build Log
- Feature completed: [name] (from backlog)
- Status: merged / rolled back / flagged
- What was learned: [brief]

## Optimization
- Improvement made: [description]
- Tests: X passing (before: Y)

## Attention Required
- [ ] Theses pending review: [list with IDs]
- [ ] Backlog items flagged for human review: [if any]
- [ ] Errors or failures: [if any]

## Platform Health
- DB: X signals, Y mosaics, Z theses
- Collectors: [status of each]
- Last successful pipeline run: [timestamp]
```

4. Link to the specific theses, mosaics, and backlog items mentioned

## Notion Integration Details

These IDs are stable and used across all phases:

- **Product Backlog DB:** `1fed676f-1cff-473c-b9c9-2c4c646fe529`
  - Data source: `collection://386c820d-dd57-4e50-9966-3930d1a81d15`
  - Columns: Feature (title), Category, Effort, Layer, Priority, Sprint, Status
  - Status values: Done, In Progress, Backlog, Blocked
  - Priority values: P0 Critical, P1 High, P2 Medium, P3 Low
- **Research Hub (parent for briefing pages):** `3127772f-a7ae-8164-a661-fb85c6dad3c9`
- **Founder OS root:** `2b37772f-a7ae-80ea-afc8-d7bdc7851472`
- **Product Roadmap:** `32d7772f-a7ae-81ec-892c-d27165425313`

## Git + Quality Guardrails

Before ANY code change:
1. `git checkout -b overnight/{date}-{feature-slug}` — always branch
2. Run `python -m pytest tests/ -v` — record baseline
3. Read and evaluate against `quality/criteria.md`:
   - Blocking (must pass): Extension Integrity, Data Contract Consistency, Agent Pipeline Coherence, Frontend-Backend Alignment, No Regression
   - Warning (log, defer): Memory & Context Persistence, Code Hygiene, Documentation Trail

After code change:
4. Run `python -m pytest tests/ -v` — must pass >= baseline
5. Re-check quality criteria
6. If pass: `git add <specific files> && git commit` → `git checkout main && git merge overnight/{branch}`
7. If fail: `git checkout main` (discard branch), log failure in briefing

## Memory Updates

After each cycle, update auto-memory with:
- New research findings (project type memories)
- Patterns learned from build/optimize (feedback type memories)
- New external references discovered (reference type memories)
- Never duplicate existing memories — check first

## Error Handling

- If a phase fails, log the error and continue to the next phase
- Never let one failure stop the entire cycle
- Always produce a briefing, even if it's just error reports
- If the DB is unreachable, skip COLLECT and flag in briefing
- If Notion is unreachable, write briefing to `docs/daily-briefs/{date}.md` as fallback
