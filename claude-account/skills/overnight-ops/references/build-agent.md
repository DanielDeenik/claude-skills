# Build Agent — Phase 3

## Objective
Pick the highest-priority item from the Product Backlog, implement it fully, and ship it — or roll back cleanly if anything breaks.

## Critical Rules
1. **EXTEND, never rewrite.** Every change adds to existing modules. If you find yourself deleting more than 10 lines of working code, stop and reconsider.
2. **One item per cycle.** Do not pick up multiple items. Finish one cleanly.
3. **Branch always.** Never commit directly to main.
4. **Test before AND after.** Record baseline test results. Your changes must not reduce passing tests.
5. **Skip XL items.** If the top backlog item has Effort = "XL", skip it and flag for human review. Pick the next highest-priority item instead.
6. **Never touch HITL logic.** Decision gates, position sizing, and audit trail code are sacred. If a backlog item requires changes there, flag it for Dan and move on.

## Detailed Steps

### Step 1: Pick a Task
1. Query Notion Product Backlog: Status = "Backlog", sorted by Priority
   - Use `notion-query-database-view` with data source `collection://386c820d-dd57-4e50-9966-3930d1a81d15`
   - Filter: Status = "Backlog"
   - Sort: Priority ascending (P0 first)
2. Pick the first item that is NOT Effort = "XL"
3. Update its Status to "In Progress" via `notion-update-page`
4. Read the feature description and any linked pages for specs

### Step 2: Plan
Before writing any code:
1. Identify which files need to change
2. Check if there are existing tests for those files
3. Map the change to the Camillo topology layer (which agent/service does this touch?)
4. Write a brief implementation plan (3-5 steps max)

### Step 3: Implement
1. Create branch: `git checkout -b overnight/{date}-{slug}`
2. Run baseline tests: `python -m pytest tests/ -v 2>&1 | tee /tmp/test-baseline.txt`
3. Make the changes, following these patterns:
   - New collector? → Add to `social_arb/collectors/`, implement `BaseCollector`
   - New engine? → Add to `social_arb/engine/`, follow duck-typing pattern
   - New API route? → Add to `social_arb/api_server.py`, follow existing `_serve_*` pattern
   - New MCP tool? → Add to `social_arb/mcp_server.py`, add Pydantic model to `mcp_models.py`
   - Frontend? → Modify files in `social_arb/ui/`, ensure Tailwind CSS only
   - DB schema change? → Add migration to `db/schema.py`, ensure backward compatibility
4. Write tests for new code (at minimum, one test per new function)
5. Run tests again: `python -m pytest tests/ -v 2>&1 | tee /tmp/test-after.txt`

### Step 4: Quality Gate
1. Compare test results: after >= baseline (no regressions)
2. Check `quality/criteria.md`:
   - Extension Integrity: did you extend, not rewrite?
   - Data Contract Consistency: do all data flows still work?
   - Agent Pipeline Coherence: does the pipeline still run end-to-end?
   - Frontend-Backend Alignment: if you changed API, did you update frontend?
   - No Regression: tests pass, no broken imports
3. If ALL blocking criteria pass → proceed to merge
4. If ANY blocking criteria fail → rollback

### Step 5: Ship or Rollback

**Ship:**
```bash
git add <specific files>  # Never git add -A
git commit -m "feat({layer}): {description}

Built by overnight-ops agent. Backlog item: {feature name}
Quality criteria: all blocking passed
Tests: {X}/{Y} passing (baseline: {A}/{B})"
git checkout main
git merge overnight/{branch}
```
Then update Notion: Status = "Done"

**Rollback:**
```bash
git checkout main  # Discard the branch
```
Then update Notion: Status = "Blocked", add error details as a comment

### Step 6: Log
Record in the briefing data:
- What was built (feature name, backlog item link)
- Files changed (list)
- Tests added (count)
- Ship or rollback (and why)
- Follow-up items discovered during implementation
