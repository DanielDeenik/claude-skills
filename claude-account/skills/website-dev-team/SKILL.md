---
name: website-dev-team
description: >
  Deploys a 7-agent website development team using MiroFish swarm-intelligence architecture:
  Orchestrator (ReportAgent), PM, Architect, Designer, Frontend Dev, Backend Dev, QA/Launch.
  Each agent has a defined ontology, reads from a shared GraphRAG knowledge graph
  (decisions.md), and activates on a temporal phase schedule with mandatory HITL gates.

  Use whenever the user wants to build a website, web app, SaaS, landing page, or coordinate
  an AI dev team front to back. Trigger on: "build a website", "web app", "landing page",
  "SaaS build", "dev team", "agent team", "front to back", "full stack build", "agentic dev
  team", or "MiroFish architecture". Seven agents, five HITL gates, one shared knowledge graph,
  always-clean git, and a live Notion PM journey doc with mermaid architecture diagrams.
---

# Website Dev Team — MiroFish Architecture

## Architecture Overview

MiroFish maps onto website development as follows:

| MiroFish Concept     | Website Dev Team Equivalent                        |
|----------------------|----------------------------------------------------|
| Seed Material        | Project brief from human                           |
| Ontology Generation  | Agent role definitions + relationship graph        |
| GraphRAG Build       | `decisions.md` + `project-context.md`             |
| Environment Setup    | Repo scaffold, tool config, dev environment        |
| Simulation Run       | Parallel agent execution across phases             |
| Report Generation    | Orchestrator HITL gate reports                     |
| Deep Interaction     | Human can query any agent directly at any phase    |
| ReportAgent          | Orchestrator agent                                 |
| Swarm Emergence      | The website that emerges from agent interactions   |
| Persistence Layer    | Git (always clean) + Notion (live PM journey)      |

## How to Run

### Phase 0 — Repo + Notion Bootstrap (NEW, MANDATORY)
The Orchestrator MUST complete Phase 0 BEFORE Phase 1. No exceptions.

0. **No sandbox isolation — repo MUST live in a mounted workspace folder.**
   - The Orchestrator HALTS if `project.repo_path` is not inside the user's
     mounted Cowork folder (e.g., resolves under the workspace mount, NOT
     under `/sessions/<id>/` scratch).
   - The Orchestrator HALTS if no `.git` directory exists at `repo_path`.
     If the user is starting a brand-new project, the Orchestrator instructs
     them to: (a) create an empty repo on their machine, (b) add a remote,
     (c) mount the folder into Cowork, then re-trigger the skill. The
     Orchestrator does NOT auto-`git init` and does NOT scaffold code in
     the sandbox "for now".
   - All specialist agents (PM, Architect, Designer, Frontend, Backend, QA)
     write their code-bearing artifacts ONLY to paths under `repo_path`.
     Writing to `/sessions/<id>/` for code is a protocol violation.
1. **Git readiness check** — fail loud if any of these are wrong:
   - `repo_path` is inside a mounted workspace folder (Phase 0 step 0)
   - `.git` exists at `repo_path` AND `git remote get-url origin` succeeds
   - Working tree is clean (`git status --porcelain` returns empty), OR
     existing changes are explicitly approved by human and committed first
   - Local branch is in sync with `origin/<branch>` (no behind/ahead drift)
   - A dedicated build branch is created: `build/<project-slug>-<YYYYMMDD>`
2. **Notion bootstrap** — under the parent page configured in
   `references/git-and-notion-protocol.md` (default: Nexus Decision workspace),
   create:
   - Build hub page: `Build — <Project Name> — <YYYYMMDD>`
   - Child page: `PM Journey — <Project Name>` (LIVE doc, updated each gate)
   - Child page: `Solution Architecture — <Project Name>` (mermaid diagrams)
   - Child page: `Decision Log — <Project Name>` (mirrors decisions.md)
   - Child page: `Gate Reports — <Project Name>` (one section per gate)
3. **Seed both layers** — write the project brief to `project-context.md` AND
   to the Notion Build hub page. The two must stay in sync until Gate 5.

### Step 1 — Seed the Knowledge Graph
```
Human provides: project brief (1-3 paragraphs minimum)
Orchestrator creates: /project-context.md and /decisions.md
All agents READ from these files before acting
```

### Step 2 — Activate Agents by Phase
```
Phase 1: PM Agent          → Gate 1 → Human approves PRD
Phase 2: Architect Agent   → Gate 2 → Human approves tech stack
Phase 3: Designer Agent    → Gate 3 → Human approves design system
Phase 4: Frontend + Backend (PARALLEL) → Gate 4 → Human approves integrated app
Phase 5: QA Agent          → Gate 5 → Human approves launch
```

### Step 3 — HITL Gate Protocol (UPGRADED)
At EVERY gate, the Orchestrator runs the **Gate Closeout Sequence** in this exact
order. Skipping any step is a protocol violation:

1. **Synthesize** agent output into `decisions.md` and `project-context.md`
2. **Update Notion**:
   - Append decisions to `Decision Log` page
   - Update `PM Journey` page with phase narrative, risks, what changed, why
   - Update `Solution Architecture` page mermaid diagrams (see protocol ref)
   - Post the Gate Report to `Gate Reports` page as a new toggle
3. **Git closeout**:
   - `git add -A` only the files this phase touched (named explicitly, never `.`)
   - Commit with message format: `feat(<phase>): gate <N> — <summary>`
   - Push to `origin/build/<project-slug>-<date>`
   - Verify `git status --porcelain` is empty AFTER push
   - Verify `git rev-parse HEAD` matches `origin/<branch>` HEAD
4. **Present** the Gate Report to the human with explicit APPROVE / REJECT prompt
5. **On APPROVE**: tag the commit `gate-<N>-approved`, push tag, activate next phase
6. **On REJECT**: append `[GATE-N-REJECTION]` to decisions.md AND Notion, route
   back to responsible agent — DO NOT roll back the commit, create a new commit
   on top with the revision

Rejection routes back to the responsible agent with human feedback appended to
decisions.md AND the Notion PM Journey page (so the journey reflects reality).

### Step 4 — Continuous Invariants (checked at every gate)
- All code-bearing files written this phase are under `repo_path` (no sandbox stragglers)
- `git status --porcelain` is empty
- Local HEAD == `origin/<branch>` HEAD
- Notion `PM Journey` last-updated timestamp == today
- Notion `Solution Architecture` page contains a current mermaid diagram for
  every approved component
- `decisions.md` line count matches what Notion `Decision Log` shows

**Sandbox-vs-repo audit at every gate.** The Orchestrator runs:
`find /sessions/*/[^.]* -newer <last-gate-timestamp> -type f 2>/dev/null` (or
equivalent) and HALTS if any code-bearing file (`.ts`, `.tsx`, `.js`, `.jsx`,
`.py`, `.go`, `.rs`, `.html`, `.css`, `.sql`, `.sh`, etc.) was created or
modified outside `repo_path`. Sandbox is for scratch notes and tool output
only — never for shipped code.

If any invariant fails, the Orchestrator MUST halt and report the drift to the
human before proceeding.

---

## Agent Ontology Map

```
ORCHESTRATOR (ReportAgent)
  ├── reads:  all agent outputs, decisions.md, project-context.md, git state, Notion pages
  ├── writes: decisions.md (append only), gate reports, Notion live docs, git commits/tags
  └── relationships: supervisor of all agents; interface to human; sole owner of git + Notion

PM AGENT
  ├── reads:  project-context.md, seed brief
  ├── writes: PRD, sitemap, personas, KPIs → decisions.md
  └── relationships: feeds ARCHITECT, DESIGNER

ARCHITECT AGENT
  ├── reads:  PRD from decisions.md
  ├── writes: tech stack, schema, API contract, ADRs, mermaid diagrams → decisions.md
  └── relationships: feeds FRONTEND, BACKEND, DESIGNER

DESIGNER AGENT
  ├── reads:  PRD + architecture from decisions.md
  ├── writes: design system, component specs, wireframes → decisions.md
  └── relationships: feeds FRONTEND

FRONTEND AGENT
  ├── reads:  design system, architecture from decisions.md
  ├── writes: scaffold, components, pages → code files
  └── relationships: integrates with BACKEND API contract

BACKEND AGENT
  ├── reads:  API contract, schema from decisions.md
  ├── writes: server, DB, auth, tests → code files
  └── relationships: contracts consumed by FRONTEND

QA AGENT
  ├── reads:  all deliverables, decisions.md, code files
  ├── writes: test reports, launch checklist → decisions.md
  └── relationships: final gate before production deploy
```

---

## Knowledge Graph Files

All agents read and write to two shared files:

### `/decisions.md` — Append-only decision log
Format: see `references/decisions-schema.md`

### `/project-context.md` — Evolving project state
Contains: current phase, approved decisions, open risks, human feedback

### Notion mirror (NEW)
Both files MUST be mirrored into Notion at every gate. The Orchestrator owns the
sync. See `references/git-and-notion-protocol.md` for the page layout, naming
convention, parent-page configuration, and mermaid diagram standards.

---

## Agent Reference Files

Load only the agent relevant to the current phase:

- `agents/orchestrator.md` — Orchestrator / ReportAgent system prompt
- `agents/pm.md` — Product Manager system prompt
- `agents/architect.md` — System Architect system prompt
- `agents/designer.md` — UX/UI Designer system prompt
- `agents/frontend.md` — Frontend Developer system prompt
- `agents/backend.md` — Backend Developer system prompt
- `agents/qa.md` — QA / Launch Engineer system prompt

## Reference Files

- `references/mirofish-patterns.md` — MiroFish architecture patterns applied to dev teams
- `references/hitl-gates.md` — Full HITL gate protocol + templates (includes git + Notion checkpoints)
- `references/decisions-schema.md` — decisions.md schema + examples
- `references/git-and-notion-protocol.md` — Always-clean git + live Notion PM journey + mermaid standards

## Initialization Script

Run `scripts/init-project.sh <project-name>` to scaffold the knowledge graph files,
decisions.md, and agent workspace for a new project. The script also runs the
Phase 0 git readiness check and prints the Notion bootstrap instructions.

## No Hardcoded Values
Project name, branch name, Notion parent page ID, repo path, and human approver
identity are ALL passed in as arguments or read from `project-context.md` —
never hardcoded into agent prompts or scripts.
