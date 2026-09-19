# Context Assembler — Knowledge Graph Traversal Algorithm

How the orchestrator builds a context packet for any subagent by traversing the knowledge graph.

## Overview

The context packet is the bridge between the knowledge graph and a subagent's understanding. A well-assembled packet means the subagent acts like it's been on the project for months. A poorly assembled one means wasted cycles and bad code.

## The 4-Layer Search

### Layer 1: Tag Match (Broad Discovery)

Extract keywords from the task:
- Task title words (excluding stop words)
- Technology terms (e.g., "SQLAlchemy", "Redis", "React")
- Domain terms (e.g., "collector", "pipeline", "signal")

Search ALL entity types for matching tags:
```
For each keyword:
  → Find entities where tags[] contains keyword
  → Score: 1 point per tag match
  → Entities matching multiple keywords score higher
```

### Layer 2: Module Match (Structural)

Determine which MODULE entities the task will touch:
1. Parse task description for file paths, module names, class names
2. Check `memory/graph/entities/` for MODULE entities matching those references
3. If task says "collectors" → find all MODULE entities under collectors/

Then traverse FROM those modules:
```
For each matched MODULE:
  → MODULE --governed-by--> DECISION    (architectural constraints)
  → MODULE --uses--> PATTERN            (coding conventions)
  → CORRECTION --applies-to--> MODULE   (Dan's overrides)
  → FAILURE --occurred-in--> MODULE     (past problems)

Score: direct connection = 3 points, secondary = 2 points, tertiary = 1 point
```

### Layer 3: Always-Include (Non-Negotiable Context)

These entities are ALWAYS included regardless of relevance scoring:

1. **All CORRECTION entities from last 30 days**
   - Dan's recent corrections are always relevant
   - Priority: corrections tagged `blocking` come first

2. **All PATTERN entities tagged `universal`**
   - Project-wide conventions (no-hardcoding, logging, config approach)
   - These apply to every task

3. **Architecture summary** from MODULE entities
   - Top-level system description
   - How major components connect

4. **Any entity tagged `blocking`**
   - Hard rules that override everything

### Layer 4: Failure Prevention (Historical)

Search FAILURE entities specifically:
```
For each FAILURE entity:
  → Check if tags overlap with task keywords (Layer 1 match)
  → Check if FAILURE --occurred-in--> any MODULE the task touches (Layer 2 match)
  → Check if FAILURE was created in last 60 days (recency bonus)

Always include failures with > 0 match score
```

## Scoring and Ranking

After all 4 layers, each candidate entity has a composite score:

```
score = (tag_matches × 1)
      + (module_connection × 3 for direct, 2 for secondary, 1 for tertiary)
      + (always_include × 10)  // guaranteed inclusion
      + (recency_bonus)        // +2 if last 7 days, +1 if last 30 days
      + (priority_bonus)       // +5 if blocking, +2 if high
```

### Priority Override

Regardless of score, entities are grouped by type priority:
1. **CORRECTION** — always first in the packet
2. **FAILURE** (matching domain) — second
3. **DECISION** (direct match) — third
4. **PATTERN** (relevant) — fourth
5. **MODULE** (context) — fifth

Within each group, sort by score descending.

## Trimming to Budget

Target context packet size: **~2,500 words** (enough to be useful, small enough for subagent focus).

**Trimming strategy:**
1. Always-include entities are never trimmed
2. If over budget after always-includes: trim from lowest-scoring entities first
3. For entities being trimmed: generate a 1-line summary instead of full content
4. Never trim CORRECTION entities (Dan's word is law)
5. Never trim FAILURE entities that directly match the task domain

**If still over budget:**
1. Summarize MODULE context into a single paragraph
2. Merge similar PATTERN entities into a combined "conventions" section
3. Keep DECISION entities that directly govern the task, summarize others

## Context Packet Format

The assembled packet is structured for the subagent prompt:

```markdown
## Product Context (from Knowledge Graph)

### Architecture
[MODULE entity summaries — system overview, relevant module descriptions]

### Decisions That Govern This Work
[DECISION entities — what was decided, when, rationale]
[Sorted: most directly relevant first]

### Patterns You Must Follow
[PATTERN entities — conventions, examples, anti-patterns]
[Universal patterns first, then task-specific]

### Corrections (Dan's Overrides — Highest Priority)
[CORRECTION entities — what Dan corrected, what to do instead]
[ALWAYS complete, never summarized]

### Past Failures to Avoid
[FAILURE entities — what went wrong, why, prevention]
[Include: cause, module, what to do differently]
```

## Role-Specific Assembly

Different subagent roles get different subsets:

| Role | Emphasized Entities | De-emphasized |
|------|-------------------|---------------|
| **Implementer** | Everything — full context | None |
| **Spec Reviewer** | DECISIONs, CORRECTIONs, task spec | PATTERNs (less relevant) |
| **Quality Reviewer** | PATTERNs, CORRECTIONs, FAILUREs | MODULEs (less relevant) |
| **Architect Reviewer** | MODULE graph, DECISIONs, relationships | Individual PATTERNs |
| **Discovery Agent** | Full MODULE graph, FAILUREs, PATTERNs | Specific CORRECTIONs |

## Graph Update After Task

After a task completes (success or failure), the orchestrator updates the graph:

**On Success:**
- Update touched MODULE entities with new knowledge
- Create new PATTERN entities if conventions were established
- Create new DECISION entities if choices were made
- Create BACKLOG_ITEM → MODULE relationships
- Update relationship index

**On Failure:**
- Create FAILURE entity with cause, module, prevention
- Link FAILURE → MODULE
- If pattern violation caused it: strengthen PATTERN → FAILURE relationship
- If correction was missed: note in CORRECTION entity

**On Skipped (Needs Clarification):**
- Create a "pending question" note in the session log
- Do NOT create speculative entities
