---
name: knowledge-graph-coworker
description: >
  Knowledge-graph AI coworker + GCP deployment specialist. Turns research signals into a
  persistent queryable graph (Rowboat-inspired Obsidian vault + agent runtime + event bus).
  Also provides step-by-step GCP Cloud Run optimization: Litestream SQLite replication,
  multi-stage Docker builds, CI/CD pipelines, cost optimization, security hardening, and
  monitoring setup. TDD, HITL gates, zero hardcoded values. Notion ticket tracking.
  Trigger on: "knowledge graph", "coworker agent", "AI coworker", "Rowboat", "vault",
  "GCP", "Cloud Run", "deployment", "Litestream", "Docker optimize", or "infrastructure".
---

# Knowledge Graph Coworker Skill

Build a standalone AI coworker that turns unstructured research into a persistent knowledge
graph and acts on it — privately, locally, with full human control.

---

## Why This Skill Exists

Research signals are ephemeral. You read an email, catch a trend, hear something in a
meeting — and it's gone. The knowledge graph coworker captures everything into a persistent,
queryable graph that gets smarter over time. Agents then use that accumulated context to
prep you for decisions, surface connections you'd miss, and automate recurring research.

This is Rowboat's architecture adapted for information arbitrage: Obsidian-compatible
markdown vault + modular agent runtime + event-driven coordination + Bloomberg terminal UI.

---

## Core Architecture (from Rowboat analysis)

### Three Pillars

1. **Knowledge Graph** — Persistent entity-relationship graph stored as markdown
2. **Agent Runtime** — Modular agents that query the graph and act on it
3. **Event Bus** — Pub-sub coordination between agents, graph, and UI

### Data Flow
```
Signals (API/email/voice/manual)
  → Entity Extraction (LLM-powered)
  → Knowledge Vault (markdown + backlinks)
  → Graph Index (runtime memory, rebuilt incrementally)
  → Agent Context (index formatted in LLM prompt)
  → Agent Actions (tools, HITL gates, artifact generation)
  → Feedback Loop (prediction errors → graph updates)
```

---

## Workflow: 6 Phases

### Phase 0: SCOPE — Review Notion Backlog

Before building anything, check the existing Product Backlog in Notion:

1. Search Notion for "Social Arb — Product Backlog"
2. Query existing tickets to avoid duplicate work
3. Identify which backlog items this request maps to
4. If the request is new, create a Notion ticket BEFORE coding

This ensures the project evolution is tracked and no work happens outside the backlog.

### Phase 1: SOLUTION DESIGN

Create `docs/SOLUTION_<feature-name>.md` before any code. Template sections:

1. **Problem Statement** — What knowledge gap are we filling?
2. **Entity Model** — What entities, relationships, and properties?
3. **Data Sources** — What feeds into the graph? (API, email, voice, manual)
4. **Agent Architecture** — What agents operate on the graph?
5. **UI Specification** — Bloomberg terminal layout for graph interaction
6. **Test Plan** — pytest + vitest files and what they cover
7. **Config Contract** — Every configurable value with defaults and sources
8. **Notion Ticket Mapping** — Which backlog items does this implement?

**HITL Gate 1:** Present solution doc. Do NOT proceed until approved.

### Phase 2: TDD — Tests First

Write tests BEFORE implementation:

**Backend (pytest):**
```
tests/test_entity_extraction.py    — LLM entity extraction accuracy
tests/test_graph_index.py          — Index build, query, incremental update
tests/test_change_detection.py     — mtime + hash hybrid detection
tests/test_agent_runtime.py        — Agent loading, tool execution, abort
tests/test_config.py               — Zero hardcoded values verification
```

**Frontend (vitest):**
```
ui/src/__tests__/GraphViewer.test.jsx    — Graph visualization
ui/src/__tests__/LiveNotes.test.jsx      — Auto-updating trackers
ui/src/__tests__/AgentPanel.test.jsx     — Agent execution UI
```

**HITL Gate 2:** Show test structure. Ask: "Missing any test cases?"

### Phase 3: IMPLEMENT — Red-Green-Refactor

Build in this order:
1. **Config/constants** — the contract
2. **Entity model + vault** — markdown storage with frontmatter
3. **Graph index** — runtime memory index with incremental rebuild
4. **Change detection** — hybrid mtime + SHA256
5. **Entity extraction** — LLM-powered extraction pipeline
6. **Agent runtime** — YAML agent definitions + tool execution
7. **Event bus** — typed pub-sub for coordination
8. **UI components** — Bloomberg terminal graph viewer

### Phase 4: INTEGRATE — Wire Into Existing Systems

- New features extend existing modules (NEVER rewrite)
- New API routes go in existing route files where possible
- New UI pages wired into App.jsx + sidebar
- New Notion tickets created for any follow-up work
- All new DB tables through existing init_db()

### Phase 5: VERIFY — Quality Gate

1. All tests pass (pytest + vitest)
2. Zero hardcoded values (grep verified)
3. Extension integrity (no orphaned code)
4. Notion tickets updated with status
5. Config contract matches solution doc

**HITL Gate 3 (final):** Present verification results.

---

## Knowledge Graph Schema

### Entity Types (all stored as markdown with YAML frontmatter)

**People** (`knowledge/People/{name}.md`)
```yaml
---
type: person
name: Full Name
role: Analyst | Executive | Insider
organization: "[[Companies/OrgName]]"
email: email@example.com
aliases: [nickname, abbreviation]
first_seen: 2026-04-09
source: signal | email | manual
---
## Notes
Key observations about this person.

## Signals
- [[Signals/signal-id]] — context
```

**Companies** (`knowledge/Companies/{name}.md`)
```yaml
---
type: company
name: Company Name
class: public | private | crypto
ticker: SYMBOL (if public)
sector: "[[Sectors/SectorName]]"
market_cap: number (if public)
stage: seed | series-a | series-b | public (if private)
aliases: [abbreviations]
---
## Thesis
Current investment thesis summary.

## Signals
- [[Signals/signal-id]] — context
```

**Sectors**, **Topics**, **Signals**, **Theses** follow similar patterns.

### Relationships (via backlinks)
- Company → Sector: `sector: "[[Sectors/AI Infrastructure]]"`
- Signal → Company: `companies: ["[[Companies/NVDA]]", "[[Companies/Anthropic]]"]`
- Person → Company: `organization: "[[Companies/Palantir]]"`
- Thesis → Signals: `fragments: ["[[Signals/sig-001]]", "[[Signals/sig-002]]"]`

### Indexing
Runtime memory index rebuilt incrementally:
```python
{
  "people": [{"file": "People/Alex.md", "name": "Alex Karp", "org": "Palantir", ...}],
  "companies": [{"file": "Companies/NVDA.md", "ticker": "NVDA", "sector": "Semiconductors", ...}],
  "sectors": [...],
  "topics": [...],
}
```

Index is formatted as markdown and passed in LLM prompt as context.

---

## Agent Runtime Architecture

### Agent Definition (YAML + markdown)
```yaml
---
name: divergence-scanner
model: claude-sonnet-4-6  # from config, not hardcoded
schedule: "*/30 * * * *"  # from config
tools:
  workspace-readFile: { type: builtin }
  workspace-writeFile: { type: builtin }
  web-search: { type: mcp, serverName: exa }
  notion: { type: mcp, serverName: notion }
---
# Instructions
You are a divergence scanner. Query the knowledge graph for tracked companies,
run arbitrage scoring, and flag any with Signal Strength > {config.flag_threshold}.
```

### Execution Flow
```
User/Schedule → MessageQueue → AgentRuntime.trigger()
  → Load agent YAML + skills
  → Build prompt: system + knowledge index + history + tools
  → LLM call (streaming via event bus)
  → Tool calls? → Execute → Feed results back
  → Final response + run event log
  → Persist run as JSON
```

### Built-in Tools
- `vault-read`: Read entity from knowledge vault
- `vault-write`: Create/update entity in vault
- `vault-search`: Full-text search across vault
- `graph-query`: Query the runtime index
- `ask-human`: Pause for HITL input
- `run-pipeline`: Trigger Social Arb signal pipeline

---

## Notion Integration Requirements

Every feature built with this skill must:

1. **Check backlog first** — Search Notion for related tickets before starting
2. **Create ticket if new** — Any new feature gets a Notion ticket with:
   - Feature name, Layer, Category, Priority, Sprint, Effort, Status
   - Detailed description with acceptance criteria
3. **Update on completion** — Mark tickets as "Done" when implemented
4. **Cross-reference** — Solution docs reference Notion ticket IDs

This creates a living audit trail of the project's evolution.

---

## GCP Cloud Run Deployment Specialist

This skill also covers end-to-end GCP deployment optimization. When triggered for
infrastructure work, follow these steps:

### Deployment Workflow

1. **DIAGNOSE** — Read existing Dockerfile, deploy.sh, entrypoint.sh, Makefile, litestream.yml
2. **OPTIMIZE** — Apply multi-stage Docker builds, right-size Cloud Run config, fix cold starts
3. **SECURE** — Workload Identity Federation, Secret Manager, least-privilege IAM
4. **AUTOMATE** — GitHub Actions CI/CD pipeline with automated deploys
5. **MONITOR** — Cloud Run metrics, Litestream health checks, billing alerts

### Key Constraints (Litestream + Cloud Run)
- `--max-instances 1` is **required** (Litestream single-instance)
- Entrypoint must: restore → replicate → serve (in that order)
- All config via env vars or Secret Manager (zero hardcoded values)
- Use `-if-db-not-exists -if-replica-exists` flags for first deploy safety

### Docker Multi-Stage Pattern
Two stages: (1) Node alpine for React build, (2) Python slim for backend + Litestream.
Typical reduction: 1.3GB → 250MB. Copy dependency manifests before source code for
layer caching.

### Cost Optimization Quick Wins
- `--min-instances 0` for dev/staging (scale to zero)
- CPU allocation = "request" for bursty workloads
- Artifact Registry over Container Registry
- Litestream retention 24h (dev) / 72h (prod)
- Billing alerts at $10, $25, $50/month

### Reference Repos (curated)
- `steren/litestream-cloud-run-example` — exact pattern for SQLite on Cloud Run
- `GoogleCloudPlatform/gcp-hardening-toolkit` — security hardening IaC
- `google-github-actions/deploy-cloudrun` — official GitHub Action
- `GoogleCloudPlatform/terraform-google-secure-cicd` — pipeline as code
- `hystax/optscale` — FinOps cost optimization

Read `references/gcp-deployment-guide.md` for the full guide with code templates,
CI/CD workflows, troubleshooting playbook, and monitoring setup.

---

## Reference Files

- `references/rowboat-architecture.md` — Complete Rowboat codebase analysis: entity model,
  agent runtime, event bus, integrations, tech stack, design decisions
- `references/entity-templates.md` — Markdown templates for all entity types with
  frontmatter schemas
- `references/gcp-deployment-guide.md` — GCP Cloud Run deployment specialist: Litestream
  patterns, Docker optimization, CI/CD pipelines, security hardening, cost optimization,
  monitoring setup, troubleshooting playbook

Read these when you need deeper implementation detail.

---

## Checklist

- [ ] Notion backlog checked for existing related tickets
- [ ] New Notion ticket created (if new feature)
- [ ] Solution doc created and approved
- [ ] Tests written BEFORE implementation
- [ ] All tests passing
- [ ] Zero hardcoded values
- [ ] Extends existing modules (no rewrites)
- [ ] Knowledge vault uses markdown + YAML frontmatter
- [ ] Graph index rebuilds incrementally
- [ ] Agent definitions are YAML-driven
- [ ] Event bus coordinates all systems
- [ ] Bloomberg terminal UI aesthetic
- [ ] Notion ticket updated to "Done"

### GCP Deployment (when infrastructure triggered)
- [ ] Dockerfile uses multi-stage build (Node → Python slim)
- [ ] Litestream entrypoint: restore → replicate → serve
- [ ] `--max-instances 1` set (Litestream constraint)
- [ ] All config via env vars / Secret Manager (zero hardcoded)
- [ ] CI/CD pipeline uses Workload Identity Federation (no JSON keys)
- [ ] Billing alerts configured
- [ ] Health check endpoint validates DB + replication
- [ ] Container image scanned for vulnerabilities
