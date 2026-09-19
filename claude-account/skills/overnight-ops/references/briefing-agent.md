# Briefing Agent — Phase 5

## Objective
Write a morning briefing page to Notion so Dan wakes up fully informed about what happened overnight. This is the most important phase — even if every other phase fails, the briefing must always be produced.

## Critical Rules
1. **Always produce a briefing.** Even if it's just error reports. No silent failures.
2. **Write to Notion first, fallback to markdown.** If Notion is unreachable, write to `docs/daily-briefs/{date}.md`.
3. **Link, don't duplicate.** Reference Notion page IDs and git commits, don't paste full content.
4. **Flag actions clearly.** Anything requiring Dan's attention goes in "Attention Required" with checkboxes.
5. **Timestamp everything.** Use ISO 8601 with timezone for all timestamps.

## Notion Details

- **Parent page (Research Hub):** `3127772f-a7ae-8164-a661-fb85c6dad3c9`
- **Tool:** `notion-create-pages` with parent = Research Hub page ID
- **Title format:** `Daily Brief — YYYY-MM-DD`

## Briefing Structure

```markdown
# Daily Brief — {date}

## Cycle Summary
- **Type:** Full / Light
- **Started:** {ISO timestamp}
- **Completed:** {ISO timestamp}
- **Phases run:** {list}
- **Phases skipped/failed:** {list with reasons}

## Market Signals (Phase 1: COLLECT)
- **Signals collected:** {count} across {source_count} sources
- **New mosaics assembled:** {count}
- **New theses generated:** {count}
- **Source breakdown:**
  | Source | Signals | Status |
  |--------|---------|--------|
  | yfinance | X | ✓/✗ |
  | Reddit | X | ✓/✗ |
  | Google Trends | X | ✓/✗ |
  | SEC EDGAR | X | ✓/✗ |
  | CoinGecko | X | ✓/✗ |
  | DeFi Llama | X | ✓/✗ |
  | GitHub | X | ✓/✗ |

## Top Opportunities
| Symbol | Divergence | Coherence | Lifecycle | Thesis Status |
|--------|-----------|-----------|-----------|---------------|
| {sym1} | {score} | {score} | {stage} | pending/approved |
| {sym2} | {score} | {score} | {stage} | pending/approved |
| {sym3} | {score} | {score} | {stage} | pending/approved |

## Research Highlights (Phase 2: RESEARCH)
### {Symbol 1}
- **Key finding:** {one-liner}
- **Thesis implication:** strengthens/weakens/neutral
- **Source:** {URL or reference}

### {Symbol 2}
- ...

## Build Log (Phase 3: BUILD)
- **Backlog item:** {feature name} (Priority: {P0-P3})
- **Status:** ✅ Merged / ❌ Rolled back / ⏸ Skipped
- **Branch:** `overnight/{date}-{slug}`
- **Files changed:** {count} ({list})
- **Tests added:** {count}
- **Reason (if rolled back):** {error details}
- **Follow-ups discovered:** {list}

## Optimization (Phase 4: OPTIMIZE)
- **Category:** {dead code / error handling / type hints / test coverage / docs}
- **Improvement:** {description}
- **Status:** ✅ Committed / ❌ Reverted
- **Tests:** {X} passing (before: {Y})
- **Diff size:** +{added} / -{removed} lines

## ⚠️ Attention Required
- [ ] **Theses pending review:** {list with IDs — these need HITL approval}
- [ ] **XL backlog items skipped:** {list — too large for autonomous build}
- [ ] **Build failures:** {details if any phase rolled back}
- [ ] **Collector errors:** {any sources that failed to return data}
- [ ] **Quality warnings:** {non-blocking criteria that fired}

## Platform Health
- **Database:** {X} signals, {Y} mosaics, {Z} theses, {W} decisions
- **Last pipeline run:** {ISO timestamp}
- **Test suite:** {X}/{Y} passing
- **Git:** main branch, {N} commits ahead of last tag
```

## Process

### Step 1: Gather Data
Collect results from all preceding phases. Each phase should have logged:
- Phase 1 (COLLECT): signal counts, source statuses, new thesis IDs
- Phase 2 (RESEARCH): research notes per symbol, thesis implications
- Phase 3 (BUILD): feature name, branch, merge/rollback status, files changed, test counts
- Phase 4 (OPTIMIZE): category, description, commit/revert status, test counts

If a phase was skipped or failed, record that fact with the error message.

### Step 2: Query Platform State
1. Call `social_arb_get_summary` to get current DB stats
2. Call `social_arb_get_theses` with status="pending_review" to list theses needing HITL
3. Call `social_arb_get_mosaics` with action="build_thesis" to get top opportunities

### Step 3: Write to Notion
1. Use `notion-create-pages` with:
   - Parent: `3127772f-a7ae-8164-a661-fb85c6dad3c9` (Research Hub)
   - Title: `Daily Brief — {YYYY-MM-DD}`
   - Content: formatted briefing using the structure above
2. If Notion fails, write the same content to `docs/daily-briefs/{date}.md` as fallback

### Step 4: Link Related Items
In the Notion briefing page:
- Link to specific thesis pages if available
- Link to the Product Backlog item that was built
- Link to the git commit (GitHub URL if repo is public)

## Light Cycle Briefing

For midday light cycles, use a shorter format:

```markdown
# Midday Update — {date}

## Market Signals
- Signals collected: {count}
- New theses: {count}
- Top movers: {list top 3 by divergence change since morning}

## ⚠️ Attention Required
- [ ] New pending theses: {list}
- [ ] Collector issues: {if any}
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Notion unreachable | Write to `docs/daily-briefs/{date}.md` |
| MCP server unreachable | Report "Platform offline" in briefing, skip DB stats |
| No data from any phase | Still produce briefing with "No data collected" |
| Phase errors | Include error messages verbatim in Attention Required |
