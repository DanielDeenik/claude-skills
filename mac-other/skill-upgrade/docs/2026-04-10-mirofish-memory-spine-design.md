# MiroFish Memory Spine — Design Document

**Date:** 2026-04-10
**Author:** Dan (with Claude in Cowork)
**Status:** Draft, awaiting review
**Project:** SimCorp Consulting → SuperAgent Architecture

---

## 1. Context

Dan runs SimCorp Dimension consulting work. He has built (or partially built) a knowledge stack including the Notion Solution Architecture (12 module sub-pages + master), the Notion Wiki, the Q&A Log, and a local SuperAgent RAG (`~/Documents/GitHub/Superagent_Consulting`) using ChromaDB + KuzuDB + LightRAG (Postgres + pgvector). Three skills currently route SimCorp work in Cowork: `simcorp-super-agent` (Q&A core), `simcorp-extraction` (data extraction designer), and the now-deleted `simcorp-notebooklm-bridge`.

The current setup answers questions and designs extractions, but it does not:
1. Preserve full reasoning traces across sessions
2. Version solutions when new information arrives
3. Detect when knowledge changes invalidate prior solutions
4. Improve itself from human feedback in a structured way
5. Manage memory bloat as the knowledge base grows
6. Auto-load project context at session start so Dan does not have to re-explain
7. Capture critical decisions before a chat is cleaned or compacted

This document specifies the **MiroFish Memory Spine**: a Cowork-native substrate that adds these capabilities by composing existing Cowork primitives (skills, MCPs, the schedule MCP, the workspace mount, Notion as system of record) with a small set of new Notion databases and four new automation scripts.

---

## 2. Goals and Non-Goals

### Goals

- **G1.** Solutions are versioned (branch-and-version model). Original reasoning is never lost.
- **G2.** When new information arrives, affected solutions are automatically flagged stale, and a new branch can be derived without losing the prior context.
- **G3.** Memory bloat is managed automatically via Ebbinghaus decay and tiered storage. Nothing is ever deleted; cold items move to cheaper storage.
- **G4.** Conversation context auto-loads at session start so Dan does not re-explain. Critical decisions are captured before any chat cleanup.
- **G5.** Different projects have isolated context. Switching projects loads a different bundle.
- **G6.** Personas in the agent network learn from human feedback. Skill files can be upgraded behind a human-in-the-loop gate.
- **G7.** Everything runs Cowork-native. Mac is used only for heavy LightRAG indexing in Phase 1. GCP migration is Phase 2.
- **G8.** Notion remains the single human-reviewable surface. No knowledge lives only in vector stores or external SaaS.

### Non-Goals

- **NG1.** No new external SaaS dependencies (Mem0, Zep, LangGraph, etc.). The research showed they would force a parallel knowledge store and add operational complexity.
- **NG2.** No NotebookLM bridge. The user explicitly removed it.
- **NG3.** Not a real-time system. Decay sweeps and delta detection run nightly, not on every edit.
- **NG4.** Not a full CMS replacement for Notion. We use Notion's native primitives (databases, relations, page versioning).
- **NG5.** No automatic skill file changes. Every skill upgrade requires Dan's explicit approval through the Pending Skill Updates database.
- **NG6.** No deletion of any artifact, ever. Demotion only.

### Success Criteria

- **SC1.** Dan can ask a SimCorp question in a fresh Cowork session and receive an answer that incorporates last week's decisions without re-explaining anything.
- **SC2.** When Dan updates a Wiki page, the Delta Detector identifies which Solutions reference that page within 24 hours and posts them to the morning brief.
- **SC3.** A solution generated three months ago is still recoverable in full reasoning detail, even if its decay score has dropped to "cold archive."
- **SC4.** A persona (e.g., Anti-Pattern Auditor) measurably improves over a quarter: Dan's correction rate on its outputs decreases.
- **SC5.** Switching from SimCorp to Social Arb work loads a different `bundle.md` and zero SimCorp context bleeds in.
- **SC6.** No critical decision from a session is lost when Dan runs `/clear` or context is auto-compacted.

---

## 3. Architecture Overview

The Memory Spine is composed of **six components** running on **four memory tiers**, all coordinated through Cowork's existing primitives.

### 3.1 The Six Components

1. **Project Context Layer** — boot/shutdown protocols, per-project bundles, cross-session continuity
2. **Versioned Solutions Database** — every solution is an immutable branch with parent lineage
3. **Reasoning Trace Database** — every persona statement in every debate, queryable
4. **Anti-Pattern Library** — proven failures with workarounds, queried before any solution ships
5. **Delta Detector + Decay Sweeper** — nightly automation maintaining freshness and bloat control
6. **Reflection Loop + Skill Upgrade Gate** — captures lessons from human feedback, proposes skill improvements

### 3.2 The Four Memory Tiers

| Tier | Name | Storage | Cost | Loaded When |
|------|------|---------|------|-------------|
| **0** | Global | `~/.auto-memory/MEMORY.md` | ~150 lines, free | Every session start |
| **1** | Project | `[project]/.context/bundle.md` | ~150 lines, free | Active project session start |
| **2** | Decisions | `[project]/.context/decisions.jsonl` | append-only, free | Last 10 entries on session start |
| **3** | Artifacts | Notion DBs + LightRAG/pgvector + KuzuDB | metered, queried on demand | When the agent needs them |

Tiers 0–2 load at session start (~3k tokens total). Tier 3 is queried via Notion MCP and LightRAG only when a workflow needs it.

### 3.3 Component Map

```
                  ┌────────────────────── Cowork ─────────────────────┐
                  │                                                   │
   Session       ─►│  BOOT SEQUENCE (project-context-loader skill):  │
   start         │  1. Load MEMORY.md  (Tier 0)                       │
                  │  2. Detect active project (cwd or declaration)    │
                  │  3. Load project bundle.md  (Tier 1)              │
                  │  4. Load last 10 decisions  (Tier 2)              │
                  │  5. Surface "Ready: [project]. Last decision: ..."│
                  │                                                   │
   Your turn    ─►│  Skills:                                          │
                  │   simcorp-super-agent (Q&A)                       │
                  │   simcorp-solution-architect [NEW] (debate)       │
                  │   simcorp-extraction (extraction design)          │
                  │   project-context-loader [NEW] (boot/shutdown)    │
                  │   knowledge-graph-coworker (substrate patterns)   │
                  │   lightrag-developer (retrieval)                  │
                  │                                                   │
                  │  All work writes to:                              │
                  │   - decisions.jsonl  (each decision, immediately) │
                  │   - bundle.md  (current state, after each turn)   │
                  │   - Notion DBs  (artifact memory, MCP)            │
                  │                                                   │
   Session     ──►│  END-OF-SESSION PROTOCOL:                         │
   wrap          │   - distill decisions → decisions.jsonl            │
                  │   - update bundle.md                              │
                  │   - extract generalizable lessons → MEMORY.md     │
                  │   - update Notion Project row (last activity)     │
                  └───────────────────────────────────────────────────┘
                                          │
                                          ▼
              ┌──────────────────────────────────────────────────────┐
              │  Notion (system of record)                           │
              │   Existing: Solution Architecture (RO),              │
              │             Wiki (RW), Q&A Log (RW)                  │
              │   NEW:      Projects, Solutions, Reasoning Trace,    │
              │             Anti-Pattern Library, Pending Skill      │
              │             Updates                                  │
              └──────────────────────────────────────────────────────┘
                                          │
                                          ▼
              ┌──────────────────────────────────────────────────────┐
              │  Mac (Phase 1 indexer) — migrates to GCP in Phase 2  │
              │   LightRAG + Postgres + pgvector                     │
              │   KuzuDB (entity graph)                              │
              │   ChromaDB (legacy, retained until LightRAG full)    │
              │   Bulk ingest scripts                                │
              └──────────────────────────────────────────────────────┘
```

---

## 4. Data Model

### 4.1 New Notion Databases

#### 4.1.1 Projects Database

The index of all active work streams. One row per project.

| Field | Type | Purpose |
|-------|------|---------|
| Name | Title | e.g., "SimCorp Consulting", "Social Arb", "Memory Spine Build" |
| Status | Select | Active / Paused / Archived |
| Current Goal | Rich text | One-sentence north star |
| Last Decision | Rich text | Mirror of latest decisions.jsonl entry |
| Last Activity | Date | When this project was last touched |
| Bundle Path | URL | Path to `[project]/.context/bundle.md` in workspace |
| Workspace Folder | URL | Root folder for this project |
| Related Notion Pages | Relation | Links to Wiki, Solution Architecture, Q&A Log |
| Owner | Person | Always Dan for now |

#### 4.1.2 Solutions Database (versioned)

| Field | Type | Purpose |
|-------|------|---------|
| Title | Title | Human-readable name |
| Domain | Select | DB+CS / DEX / DFS / FIX / Alternatives / Cross |
| Status | Select | Draft / Active / Superseded / Stale / Archived |
| Branch ID | Text | e.g., `alts-pelp-v3` |
| Parent Solution | Relation (self) | Links to the previous version in the lineage |
| Source Knowledge Hash | Text | SHA256 of all cited Wiki/SA/Anti-Pattern page versions at generation |
| Importance Score | Number (1–10) | Auto-decayed nightly |
| Importance Band | Select | Critical / Standard / Exploration (sets decay half-life) |
| Last Accessed | Date | Decay input |
| Access Count | Number | Decay input |
| Reasoning Trace | Relation | Links to Reasoning Trace Database |
| Anti-Patterns Cited | Relation | Links to Anti-Pattern Library |
| Customizations Applied | Rich text | What was bent and why |
| Risk Register | Rich text | Output of Sandbox layer |
| Generated At | Date | Audit |
| Rendered Artifacts | URL | Links to .docx / .pptx in workspace |
| Project | Relation | Links to Projects |

#### 4.1.3 Reasoning Trace Database

One row per persona statement in every debate.

| Field | Type | Purpose |
|-------|------|---------|
| Solution Branch | Relation | Which solution this belongs to |
| Step Number | Number | Order in the debate |
| Persona | Select | Architect / AntiPattern / Integration / Customization / Performance |
| Statement Summary | Rich text | ~500 char human-readable |
| Full Statement Vector ID | Text | Pointer into pgvector for the full content |
| Citations | Relation | Links to Wiki / Solution Architecture / Anti-Pattern entries |
| Vote | Select | Concur / Dissent / Abstain |
| Timestamp | Date | Audit |

The full statement (potentially long) is stored in pgvector via LightRAG. Notion holds the queryable summary plus the pointer.

#### 4.1.4 Anti-Pattern Library

The "proven not to work" knowledge base. Queried by the Anti-Pattern Auditor persona on every debate.

| Field | Type | Purpose |
|-------|------|---------|
| Title | Title | Short name |
| Domain | Select | DB+CS / DEX / DFS / FIX / Alt / Cross |
| Seductive Logic | Rich text | Why someone would think this works |
| What Was Tried | Rich text | The actual implementation attempted |
| What Broke | Rich text | The symptom |
| Root Cause | Rich text | Why it broke |
| Verified At | Rich text | Clients/dates, anonymized |
| Severity | Select | One-off fluke / Systemic blocker / Version-specific |
| Workaround | Rich text | The customization that actually works |
| Status | Select | Active warning / Superseded by SimCorp upgrade / Resolved |
| Sources | Relation | Wiki pages, postmortems, support tickets |

#### 4.1.5 Pending Skill Updates

The HITL gate for self-improvement. Reflection Loop writes proposed updates here. Dan reviews and approves.

| Field | Type | Purpose |
|-------|------|---------|
| Title | Title | "Update Anti-Pattern Auditor with PE asset class lesson" |
| Target Skill | Select | simcorp-super-agent / simcorp-solution-architect / simcorp-extraction / project-context-loader |
| Target Persona | Select | (For solution-architect) which persona's memory file |
| Proposed Change | Rich text | The exact diff |
| Rationale | Rich text | Why this change is being proposed (cite the solutions/feedback) |
| Status | Select | Proposed / Approved / Rejected / Deployed |
| Proposed At | Date | Audit |
| Reviewed At | Date | Audit |

### 4.2 Workspace Filesystem Conventions

Each project gets a `.context/` folder under its workspace root:

```
[project]/
├── .context/
│   ├── bundle.md           # ~150 lines, current state, loaded on session start
│   ├── decisions.jsonl     # append-only chronological decision log
│   ├── open_questions.md   # what's blocking, what needs Dan's input
│   └── meta.json           # {project_name, notion_project_id, last_synced}
└── [normal project files]
```

For SimCorp specifically:
```
a. Consulting - SimCorp/
└── .context/
    ├── bundle.md
    ├── decisions.jsonl
    ├── open_questions.md
    └── meta.json
```

The bundle is a markdown file with sections: Current Goal, Last 5 Decisions, Open Todos, Key Files, Blockers. The decisions log is JSON Lines:

```json
{"ts":"2026-04-10T15:30:00Z","decision":"Picked branch-and-version for solution adaptation","why":"Audit defensibility","alternatives":["delta-patching","re-derive"],"confidence":"high","supersedes":null}
```

---

## 5. Workflows

### 5.1 Session Boot Sequence

**Trigger:** Dan opens Cowork, the `project-context-loader` skill detects the active project (via cwd or explicit `/project [name]` declaration).

**Steps:**
1. Read `~/.auto-memory/MEMORY.md` (Tier 0, already automatic)
2. Detect active project from cwd or last-active in Notion Projects DB
3. Read `[project]/.context/bundle.md` (Tier 1)
4. Read last 10 lines of `[project]/.context/decisions.jsonl` (Tier 2)
5. Surface to Dan: `"Ready on [project]. Goal: [goal]. Last decision: [decision]. Open questions: [count]."`
6. Update Notion Projects row `Last Activity` field

**Total cost:** ~3k tokens, executes silently before Dan's first message renders.

### 5.2 Solution Generation (uses simcorp-solution-architect)

**Trigger:** Dan asks for a solution design (e.g., "design a Bloomberg DFS feed for fixed income with FIX order routing").

**Steps:**
1. Decomposition: break the request into sub-problems by domain (DB+CS, DEX, DFS, FIX, Alts)
2. GraphRAG (Layer 1): query Notion Solution Architecture sub-pages, Wiki, and Anti-Pattern Library for relevant context
3. 5-Persona Debate (Layer 2): Architect → Anti-Pattern Auditor → Integration → Customization → Performance, looped until 4-of-5 concur, dissent logged
4. Sandbox (Layer 3): run failure-mode checks (empty result, cardinality blow-up, schema drift, code table mismatch, CS overflow, batch window overrun, upgrade-break risk)
5. Write outputs:
   - New row in Solutions DB with Branch ID `[topic]-v1`, Parent NULL, Source Knowledge Hash computed
   - Rows in Reasoning Trace DB for every persona statement
   - Risk Register and Customizations populated
   - Wiki page draft (optional)
   - Solution document (.docx) generated to workspace if Domain is escalation-worthy
6. Update Project bundle and decisions log

### 5.3 New Information → New Branch

**Trigger:** Dan adds new information (a Wiki edit, a new Anti-Pattern Library entry, a SimCorp version note).

**Steps:**
1. Delta Detector (nightly) identifies affected Solutions by comparing current Source Knowledge Hash against stored hashes
2. Marks affected Solutions `Status = Stale`, posts to morning brief
3. Dan reviews and decides: regenerate or accept staleness
4. On regenerate: create new Solutions row with Branch ID `[topic]-v(N+1)`, Parent = previous version, run full debate against augmented knowledge
5. Old version stays immutable, new version becomes Active, old marked Superseded
6. Reasoning Trace for new version is independent (full re-derivation, not patch)

### 5.4 Decay Sweeper (nightly)

**Trigger:** `schedule` MCP fires nightly Cowork session.

**Steps:**
1. For each Active solution, compute:
   ```
   score(t) = base_importance × exp(-λ × days_since_access) × (1 + 0.2 × access_count)
   ```
   where λ depends on Importance Band:
   - Critical: half-life 365 days (λ = ln(2)/365)
   - Standard: half-life 90 days
   - Exploration: half-life 30 days
2. Update Importance Score in Solutions DB
3. Apply tier transitions:
   - score > 7: keep hot (full content in Notion)
   - 4 ≤ score ≤ 7: summarize Reasoning Trace via RAPTOR-style hierarchical compression, keep summary in Notion
   - 1 ≤ score < 4: cold archive — move full trace to GCS (or workspace `cold-archive/` in Phase 1), keep Notion stub
   - score < 1: long-term cold — Notion archived flag set
4. Never deletes. All transitions reversible by re-accessing.

### 5.5 End-of-Session Protocol

**Triggers (any of):**
- Explicit "/save" or "wrap up" intent from Dan
- Token usage above 70% of context window
- `/clear` or `/compact` intent detected
- Inactivity > 30 minutes (only fires if there were tool calls in this session)

**Steps:**
1. Scan the conversation for decisions (heuristic: messages where Dan picked an option, approved a plan, set a constraint, or said "do X")
2. For each decision, append a row to `decisions.jsonl`:
   ```json
   {"ts": "...", "decision": "...", "why": "...", "alternatives": [...], "confidence": "...", "supersedes": null}
   ```
3. Update `bundle.md` Current Goal, Last 5 Decisions, Open Todos, Blockers
4. Extract any generalizable lesson and write to `~/.auto-memory/MEMORY.md` as a new memory file (per the existing auto-memory protocol)
5. Update Notion Projects row Last Activity, Last Decision
6. Surface to Dan: `"Saved [N] decisions to [project]/.context/decisions.jsonl. Bundle updated. Safe to /clear."`

### 5.6 Reflection Loop (weekly)

**Trigger:** `schedule` MCP fires weekly Cowork session.

**Steps:**
1. Sweep last week's Solutions where Dan provided feedback (corrections, edits, approvals with comments)
2. For each piece of feedback, identify which persona was responsible (via Reasoning Trace persona attribution)
3. Draft a 1–3 sentence "lesson" per persona
4. Group lessons by persona, propose actual edits to:
   - The persona's memory file (`specialists/[persona].md`)
   - The skill's SKILL.md trigger set (if a new domain or term emerged)
5. Write proposed edits to the Pending Skill Updates Notion DB with Status = Proposed
6. Post to morning brief: "[N] skill upgrades pending review"

Dan reviews. On approval, the proposed change is committed to the skill files in `~/.claude/skills/[skill]/` (which is the iCloud-synced location after centralization).

### 5.7 Skill Upgrade HITL Gate

**Trigger:** Dan reviews an entry in Pending Skill Updates DB.

**Outcomes:**
- **Approved:** Claude commits the change to the skill file in `~/.claude/skills/[skill]/`, sets Status = Deployed, logs to git history.
- **Rejected:** Status = Rejected, lesson is discarded but linked feedback remains in Solutions DB for future reference.
- **Deferred:** Stays in Proposed state, surfaces in next morning brief.

---

## 6. Phasing

### Phase 1 (this work, ~2 weekends)

**In Cowork (this session and the next):**
- Create the 5 new Notion databases via Notion MCP
- Write `simcorp-solution-architect` skill into workspace `skill-upgrade/`
- Write `project-context-loader` skill into workspace `skill-upgrade/`
- Update `simcorp-super-agent` to reference the Memory Spine
- Create `.context/` folder for SimCorp project, seed initial bundle.md from MEMORY.md and conversation history
- Create 3 scheduled tasks: delta_detector, decay_sweeper, reflection_collector (all run inside Cowork via the schedule MCP)
- Create the Projects DB row for SimCorp Consulting

**On Mac (Dan's manual steps):**
- Centralize `.claude/` to iCloud + git per Section 3.1 of this doc
- Copy new skill folders from workspace `skill-upgrade/` to `~/.claude/skills/`
- Run one-time LightRAG bulk ingest of the SimCorp source corpus
- Verify scheduled tasks fire as expected

### Phase 2 (later, ~2 weekends, optional)

Migrate the indexer from Mac to GCP using the `knowledge-graph-coworker` skill's deployment patterns:
- LightRAG + Postgres + pgvector → Cloud Run + Cloud SQL
- KuzuDB → Cloud Run with persistent disk or migrate to a graph DB on GCP
- Cowork talks to GCP via HTTPS
- Mac dependency retired

---

## 7. Open Questions

- **OQ1.** Should Reasoning Trace summaries be capped at 500 chars (Notion-friendly) or longer (richer)? Trade-off: searchability vs richness.
- **OQ2.** When the Decay Sweeper compresses a Reasoning Trace, should it use a separate small LLM or call back to Claude in Cowork? Cost vs quality.
- **OQ3.** Should `/save` be a literal slash command pattern, or detected from natural language ("wrap up", "let's stop here", "save what we have")? Likely both.
- **OQ4.** What is the Importance Band default at solution generation time? Probably "Standard" with promotion to "Critical" on Dan's explicit flag, demotion to "Exploration" if it's clearly experimental.
- **OQ5.** Should the Anti-Pattern Library be seeded from existing artifacts (postmortems, lessons learned, support tickets) or grown only organically? If seeded, where do those source artifacts live today?
- **OQ6.** How do we detect "active project" if Dan opens Cowork without an explicit declaration? Options: (a) most recent activity in Projects DB, (b) cwd inspection, (c) ask Dan once per session.

---

## 8. Risks

- **R1.** Notion DB query performance at scale. Mitigation: cap Reasoning Trace summaries, use Notion filter views, archive cold tier to GCS.
- **R2.** Schedule MCP failures going unnoticed. Mitigation: every scheduled task writes a heartbeat to a Notion "Sweeper Health" page; morning brief surfaces missed runs.
- **R3.** Skill upgrade proposals being noisy and Dan ignoring the queue. Mitigation: cap weekly proposals at 5 per skill, group similar lessons, surface only highest-confidence changes.
- **R4.** Source Knowledge Hash producing false positives (innocuous edits flagging solutions stale). Mitigation: hash only the Detail and Sources sections of cited pages, ignore Tags/History/typo edits.
- **R5.** End-of-session protocol misfiring (cleanup before user is actually done). Mitigation: require either explicit /save or token threshold > 70% before firing; never fire on inactivity alone if there are unsaved decisions.
- **R6.** iCloud sync conflicts on `.claude/` if Dan edits skills from two devices simultaneously. Mitigation: git as conflict layer, daily commits.

---

## 9. Next Steps

Pending Dan's approval of this design doc:

1. Spec review loop (dispatch reviewer subagent)
2. Dan reviews and signs off on the spec
3. Invoke `superpowers:writing-plans` to create implementation plan
4. Implementation in this Cowork session: create Notion DBs, write skills, set up scheduled tasks
5. Dan completes Mac-side steps (centralize iCloud, copy skills, run bulk ingest)
6. Phase 1 live, then iterate
