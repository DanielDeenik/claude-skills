---
name: social-arb-context-arch
description: Context-aware plug-and-play architecture for Social Arb. Any AI agent (Claude, Cursor, custom MiroFish brains, overnight-ops worker) can register via MCP, introspect the live ontology, query the unified knowledge graph (episodic + semantic + structural memory), and write research findings back with HITL gates. Inspired by RushDB's three-memory model. Use when wiring a new research agent into Social Arb, designing context surfaces for agent consumption, extending the MCP gateway, debugging agent-KG interactions, building tickets in the Context-Aware Architecture scrum board, or running the 3-gate HITL review flow (Design / Mid-build / Pre-merge).
---

# Social Arb — Context-Aware Agent Architecture

Social Arb exposes a single **context surface** so any agent can plug in and do research without bespoke glue. Architecture is three stacked layers, RushDB-style.

## The three layers

**L0 Context Bus (Structural Memory) — live ontology.**
Exposes the schema of everything in the system: tickers, signals, theses, decisions, HITL gates, agents, repos. Any agent calls `GET /ontology` to discover what it can read and write. Zero hardcoded schemas in agent code.

**L1 Unified Knowledge Graph (Episodic + Semantic).**
One store, three query modes:
- **Episodic** — signal events, HITL decisions, overnight cycle outcomes, research reports (typed records with auto-relationships).
- **Semantic** — dense vector embeddings of theses, news, social posts, SEC filings; meaning-based retrieval.
- **Structural** — graph traversals: ticker → signals → thesis → decision → outcome.

Unified query API: one call can do `similar_theses(embed) + traverse(ticker→decisions) + filter(date_range)`.

**L2 MCP Gateway + Agent Registry.**
Agents register capabilities (`research`, `synthesize`, `critique`, `score`). Gateway routes queries, enforces rate limits, logs every read/write as episodic memory. Claude, Cursor, overnight-ops, MiroFish brains all consume the same interface.

## Repo map (in-scope for synthesis)

| Repo | Role in context-arch |
|------|---------------------|
| **Trader** | Core Social Arb. Hosts L0/L1/L2. |
| **nexus_live** | Frontend (Nexus Financial). Consumer of KG via MCP. |
| **LensIQ-DataIngestion-TrendRadar** | Signal collector → writes episodic memory. |
| **TrendSense** | Sustainability PE adapter → semantic+structural writes. |
| **Delphi** | Volume quant model → scoring agent via registry. |
| **mcp** (fork) | AWS MCP reference for gateway patterns. |
| **Freelance_Forecaster** | Forecast agent plugin. |
| **AiStrategyConsultant** | Strategy agent plugin. |
| **quant_dashboard / longshort / TradingAlgo / QuantLongShort / TradingJournal** | Legacy models → wrap as registered agents. |
| **trading-dashboard** | React reference for Nexus UI. |
| **AegisKYC** | Compliance gate for decisions. |
| **nexus_live + dtrack_updates** | Deploy targets. |

## The HITL 3-gate contract (every ticket)

Every story ships through three human gates. No gate = no merge.

**Gate 1 — Design approval** (before code).
Spec, ontology delta, KG schema delta, agent contract. Dan signs off in Notion.

**Gate 2 — Mid-build checkpoint** (~50% built).
Working slice on a feature branch + tests green. Dan reviews behaviour on `nexus_live` staging or CLI demo. Adjust scope before full build.

**Gate 3 — Pre-merge review**.
Full test suite + quality/criteria.md check + no hardcoded values + docs updated + memory note planned. Dan approves merge.

Gates are properties on every Notion ticket: `Gate 1 Status`, `Gate 2 Status`, `Gate 3 Status` ∈ {Pending, Approved, Changes Requested}.

## How an agent plugs in (the happy path)

1. Agent calls `register(agent_id, capabilities, version)` on MCP gateway.
2. Agent calls `GET /ontology` → gets live schema.
3. Agent queries KG: `query({ traverse: ticker→signals, similar_to: embed(thesis), filter: {date: last_7d} })`.
4. Agent writes findings: `append_episodic({type: research, ticker, thesis_id, evidence, confidence})`.
5. Writes are flagged for HITL if `confidence > threshold` OR `position_size > kelly_cap`.
6. Gate 1/2/3 workflow runs against Notion board.

## When to invoke this skill

- "Wire agent X into Social Arb"
- "Design a new signal collector / research agent / scoring model"
- "Extend MCP gateway"
- "Build tickets for Context-Aware Architecture epic"
- "Run HITL review on ticket XYZ"
- "What's the context surface for agent Y?"

## Non-negotiables (from CLAUDE.md)

- **Zero hardcoded values** — all schemas come from the ontology endpoint.
- **Extend, never rewrite** — new agents wrap legacy repos, don't replace them.
- **Check quality/criteria.md** before marking any task Done.
- **Memory-first** — every non-trivial finding must be saved with absolute dates.

## Notion backlog

All tickets live in the **Context-Aware Architecture** database under Social Arb Research Hub. Each has: Type (Epic/Story/Task/Spike), Layer (L0/L1/L2), Repo, Sprint, Points, 3 HITL gates, Acceptance Criteria.

Views: Sprint Kanban (by Status), Epic Board (by Epic), Sprint Timeline, HITL Queue (filter: any gate = Pending), Burndown (chart).
