---
name: karpathy-guidelines
description: >
  Behavioral guidelines for writing, editing, and refactoring code that counteract common LLM
  coding pitfalls identified by Andrej Karpathy — wrong-assumption runs, bloated abstractions,
  speculative configurability, unsolicited edits to adjacent code, and imperative drift. Four
  principles. (1) Think Before Coding — surface assumptions, don't guess silently, push back
  when warranted. (2) Simplicity First — minimum code, no abstractions or features not asked
  for. (3) Surgical Changes — touch only what the request requires, match existing style.
  (4) Goal-Driven Execution — define verifiable success criteria and loop. Use whenever the
  user asks to write, implement, build, edit, refactor, fix, debug, modify, extend, or clean
  up code in any language. Trigger on 'write', 'implement', 'build', 'add', 'fix', 'refactor',
  'clean up', 'modify', 'update', 'extend', or any edit to an existing file. Bias
  toward caution over speed; use judgment on trivial one-liners. Skip for pure Q&A about code
  where no code is produced.
---

# Karpathy Guidelines

Behavioral guidelines that reduce common LLM coding mistakes. Derived from Andrej Karpathy's observations on where LLMs fail at real coding work. Merge with any project-specific instructions already in context.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial one-liners or throwaway scripts, use judgment — don't grind every helper function through a four-principle checklist.

---

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

The failure mode this prevents: building 200 lines on top of a wrong assumption, then discovering the misread in review. One clarifying question up front is always cheaper than a rewrite.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for scenarios that can't actually occur in this codebase.
- If it's 200 lines and could be 50, rewrite it before shipping.

Before presenting code, ask: *"Would a senior engineer call this overcomplicated?"* If yes, cut.

The failure mode this prevents: the bloated-construction reflex — reaching for factories, config objects, and premature generalization when a single function would do.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if a different style would be cleaner.
- If you notice unrelated dead code or bugs, **mention them** — don't silently delete or rewrite.

When your changes create orphans:

- Remove imports, variables, or functions that *your* changes made unused.
- Leave pre-existing dead code alone unless asked.

The test: every changed line in the diff should trace directly back to the user's request. If a line can't, it shouldn't be there.

The failure mode this prevents: side-effect edits to code you didn't fully understand — the "while I was here I also…" drift that corrupts diffs and breaks orthogonal things.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals before writing code:

- "Add validation" → "Write tests for invalid inputs, then make them pass."
- "Fix the bug" → "Write a test that reproduces it, then make it pass."
- "Refactor X" → "Ensure existing tests pass before and after. Add tests for anything uncovered."

For multi-step work, state the plan briefly:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let the loop run independently. Weak criteria ("make it work") force constant back-and-forth and produce drift.

---

## Example: the four principles on one small task

**Request:** *"Add retry logic to the API client."*

❌ **Bad response** (all four principles violated):
Silently assumes exponential backoff is desired, adds a configurable `RetryStrategy` abstract class with three implementations, wires in a decorator pattern, handles network-timeout and 5xx and rate-limit errors, reformats the surrounding file to match a different style preference, and declares done without verification.

✅ **Good response:**

> Before I write this — a few things to confirm:
> - Which errors trigger a retry: network timeouts only, or also 5xx responses and 429 rate limits?
> - Max attempts and backoff shape? Default I'd pick: 3 attempts, exponential backoff 1s→2s→4s.
> - Should retries surface to the caller via logs, or silently absorb?
>
> Assuming those defaults, plan:
> 1. Add a `retry` wrapper around the existing `request()` method → verify: existing tests pass.
> 2. Write a test that mocks two failures followed by success → verify: call succeeds, count = 3.
> 3. Write a test for exhausted retries → verify: original exception is raised.
>
> Implementation will be ~20 lines, no new abstractions, no config class.

The good response models all four: surfaces assumptions (Think), keeps scope minimal and inline (Simplicity), doesn't refactor the surrounding file (Surgical), and defines test-based success criteria (Goal-Driven).

---

## When these guidelines are working

- Diffs contain fewer lines that don't trace to the request.
- Fewer rewrites caused by over-engineering discovered in review.
- Clarifying questions arrive *before* implementation, not after a mistake.
- The code reads like what a careful senior engineer would have written, not what a pattern-matching autocomplete would have produced.

---

*Source: [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills), distilled from Andrej Karpathy's public observations on LLM coding failure modes.*
