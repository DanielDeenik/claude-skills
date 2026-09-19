# Optimize Agent — Phase 4

## Objective
Make one small, measurable improvement to existing code per cycle. Accumulate these over time for significant quality gains.

## Critical Rules
1. **One improvement per cycle.** Small, clean diffs are better than sweeping refactors.
2. **Measure before and after.** Every optimization must have a measurable effect (test count, coverage, import count, lint warnings, etc.)
3. **Never optimize pipeline.py or store.py** without human approval — these are the hot paths.
4. **Dead code removal is always safe.** Start there if nothing else is obvious.
5. **Revert on any test failure.** Zero tolerance for regressions.

## Improvement Categories (in priority order)

### 1. Dead Code Removal
- Unused imports (use `pylint` or manual scan)
- Functions that are defined but never called
- Commented-out code blocks (>5 lines)
- The 18 unused API client methods in `api.js` (known issue)

### 2. Error Handling
- Collectors that catch generic `Exception` — make specific
- Missing error handling in API routes
- Silent failures (bare `except: pass`)

### 3. Type Hints
- Functions missing return type annotations
- Function parameters without type hints
- Especially in `collectors/` and `engine/` modules

### 4. Test Coverage
- Files with no corresponding test file
- Functions with >10 lines and no test
- Edge cases: empty inputs, None values, malformed data

### 5. Documentation
- Functions missing docstrings
- Module-level docstrings that are outdated
- README updates for new features added by build agent

## Process

1. Run baseline: `python -m pytest tests/ -v --tb=short`
2. Pick ONE category, ONE specific improvement
3. Make the change on branch: `git checkout -b overnight/{date}-optimize-{slug}`
4. Run tests again
5. If pass: commit, merge, log
6. If fail: `git checkout main`, log failure

## Commit Message Format
```
refactor({module}): {description}

Overnight optimization: {category}
Tests: {X}/{Y} passing (unchanged)
```
