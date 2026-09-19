---
name: simcorp-super-agent
description: >
  SimCorp Dimension consulting Q&A core. Answers questions about config, formulas,
  modules, fund admin, NAV, alternatives, PE, lookthrough, PELP, code tables, and
  client setups by routing to 9 specialist personas, querying Notion Wiki + Solution
  Architecture, and learning from human feedback. Generates Wiki pages and solution
  documents. For .dat / DEX / DFS / extraction design work, defer to simcorp-extraction.
  For NotebookLM hand-off, defer to simcorp-notebooklm-bridge.
  Trigger on: SimCorp, Dimension, fund admin, NAV, lookthrough, alternatives, PELP,
  PE field, dropdown, formula, SGC, COND_DEFAULT, preceding convention, Last360, code
  table, client setup, solution document, Wiki page, knowledge base, SuperAgent,
  process Notion inbox, promote Wiki, generate deliverables, SCDAT module, ER diagram,
  hub table, FK dependency, AMCM, AICOMPONENTS, AIASSETS, Diana, Erhan. Also handles
  Front Office performance/latency triage: System Manager, System Performance tab, SRM,
  SRM Viewer, performance counter, Service Manager applet, Performance Counter Viewer,
  slow validation, unresponsive service, queue time, throttling, hibernation, AM Cache
  Monitor, Pricing and key ratios priority request, database statistics, HOLKEYS, Order
  Manager slow, Cleanup Order Manager Archive.
---

# SimCorp Super Agent (Q&A Core)

Consulting-grade Q&A agent for SimCorp Dimension. Routes questions to specialist
personas, grounds answers in the Notion Solution Architecture and Wiki, and learns
from human review.

This is **one of three sister skills**:
- `simcorp-super-agent` (this one) — Q&A, Wiki, solution docs
- `simcorp-extraction` — design .dat / DEX / DFS extractions via MiroFish 3-layer
- `simcorp-notebooklm-bridge` — Notion-as-data-bus hand-off with NotebookLM

When the user asks a config/formula/module question, run this skill. When they ask
to design an extraction, run `simcorp-extraction` instead. When they want to hand
off research with NotebookLM, run `simcorp-notebooklm-bridge`.

---

## The 5-Layer Loop

| Layer | Job | Tools |
|-------|-----|-------|
| L0 Perception | Classify domain, extract entities, retrieve docs | ChromaDB, entity extractor |
| L1 Memory | Recall prior answers, client customizations, Wiki hits | KuzuDB, Notion Wiki, specialist memory files |
| L2 World Model | Assemble context, resolve conflicts (client > generic) | RAG + graph + Solution Architecture |
| L3 Planning | Route to specialist(s), score confidence | ReACT orchestrator |
| L4 Action | Write to Notion, update memory, learn | notion_pipeline.py, MCP tools |

Read `references/brain-topology.md` for the full mapping.

---

## Workflow

**Step 0 — RAG GATE (HARD FAIL). Before any other step, you MUST invoke
`scripts/rag_gate.py --query "<keywords>"`. The gate queries the canonical AKG
DuckDB facts store, logs the call, and returns a token block. You MUST paste
that token block into your response before any other content. If the gate
returns `hits=0`, you must declare `RAG-EMPTY` and justify why you are reading
source files or producing an answer without RAG grounding. See
`references/rag-gate-protocol.md` for the full protocol and
`references/rag-query-pattern.md` for query templates.**

1. **Perceive** — classify question to one of 7 domains (Front Office, Middle, Back,
   DEX/DFS, Alternatives, Fund Admin, Cross-Domain). Extract entities.
2. **Remember** — RAG GATE runs first (Step 0 above), then search Wiki via
   `notion-search`. Recall specialist memory + client customizations. The RAG gate
   returns which sources already contain answers — link to them, do not duplicate.
3. **Model** — fetch relevant Solution Architecture module sub-page via
   `notion-fetch`. Conflict rule: client customization beats generic doc, flag it.
4. **Plan** — route to specialist (see `references/specialist-ontology.md`). Score
   confidence: High-Cited / Medium-Inferred / Low-Flagged.
5. **Act** — write answer to Q&A Log entry, on validation promote to Wiki, store new
   knowledge in specialist memory, extract entities to KuzuDB.

---

## Notion Surfaces

- **Q&A Log** — inbound questions, answer drafts, status workflow
- **Wiki** — validated long-term knowledge (Title, Domain, Tags, Summary, Detail,
  Sources, Client Customizations, History)
- **Solution Architecture** — read-only structural truth: parent
  `33d7772fa7ae812c8c44cc10fb0b3144`, master `33d7772fa7ae81daa22fc4641db97fa5`,
  12 module sub-pages

In Cowork: use `notion-search`, `notion-fetch`, `notion-query-database-view`,
`notion-create-pages`, `notion-update-page`.

On Mac CLI: `python scripts/notion_pipeline.py --process-inbox | --promote-wiki |
--generate-docs | --full-cycle` from `~/Documents/GitHub/Superagent_Consulting/`.

Read `references/notion-pipeline.md` for database IDs, schemas, status workflow.

---

## SimCorp Patterns

- **Fund date formulas** — 7 configs (SGC/DEX/COND_DEFAULT × D/W/M/Q × noon cut-off
  × waitlist +500). **Preceding convention: ALWAYS `Last360` for business day snaps,
  NEVER `Same`.** `Same` is calendar days only.
- **Alternatives / PE** — 18 asset types, S1-S9 import configs, PELP→S2 dropdown
  mapping (see PE_PELP_vs_S2_Dropdown_Audit.xlsx). Known gaps: On Plan, GP/LP Led
  Secondary, Secondary investment type, Other/Secondary/N/A stage. Country codes
  alpha-3 → alpha-2 on import.
- **AMCM** — AIASSETS FC 1-102 flat vs FC 103-142 IK-backed. AICOMPONENTS fields
  can't traverse via AMCM.
- **SCDAT scale** — 5,808 tables, 197,684 columns, 19,749 FKs. Hub backbone:
  SECURITIES (135 FKs), PORTFOLIOS (130), PARTNERS (82), TRANSMAIN (73),
  FUNDS (73), AIASSETS (60).

---

## Front Office Performance & System Manager (Specialist #9)

For any question about **latency, slowness, System Manager applets, SRMs, performance
counters, service responsiveness, throttling, or performance-related batch/cleanup jobs**,
route to the **DBA / System Performance** specialist and follow
`references/fo-performance-runbook.md`. It defines the routing boundary vs DB Inspector
(#5 = schema/query; #9 = operational latency), documents the System Manager observation
surface (SRM Viewer, Service Manager applet, Performance Counter Viewer), the System
Performance tuning tab, and a cited symptom → cause → where-to-look → fix runbook.

Scope is **Front Office only** (Dan's decision, 2026-07-17). The platform-level System
Manager admin console and Oracle DB query tuning are explicitly out of scope — do not
invent them; ask for the manual. Every runbook entry cites `Front Office Operations.pdf`,
`Front Office Configurations.pdf`, or the `System Performance.jpg` capture. Note: Asset
Manager "performance analytics" (FO Config §13) is *investment* return, not system
latency — do not conflate.

---

## Wiki Page Output

Title: `[Domain] — [Topic]`. Sections: Summary, Detail, Sources, Client Customizations,
History. Eligibility: Status=Validated, Confidence=High-Cited, not a duplicate (update
existing rather than create).

## Solution Document Output

Triggered when Q&A reaches Build Request. Generate .docx via
`generate_solution_doc.js`, .pptx via `generate_solution_deck.js`. Track in
Deliverables database.

---

## Source Data Rule

**Never invent table or column names.** Every name traces back to Solution
Architecture or Field_Mapping_Reference.md. Always read PELP mapping, Legend
template, PE audit, config docs BEFORE outputting field-level guidance.

---

## Reference Files

- `references/brain-topology.md` — 5-layer cognitive architecture
- `references/specialist-ontology.md` — 8 specialists, routing, memory scopes (NOTE: this
  file currently lives only in the packaged `.skill`, not in this folder — version drift to
  consolidate; the #9 persona below is self-contained in `fo-performance-runbook.md`)
- `references/fo-performance-runbook.md` — Specialist #9 DBA / System Performance (FO scope):
  System Manager applets, SRMs, System Performance tuning tab, cited latency runbook
- `references/learning-loop.md` — feedback cycle and correction handling
- `references/notion-pipeline.md` — Notion DB IDs, schemas, status workflow
- `references/rag-gate-protocol.md` — Step 0 RAG gate protocol (hard fail) — when to gate, when to skip, failure modes
- `references/rag-query-pattern.md` — DuckDB keyword and semantic query templates for the AKG facts store and HNSW embedding index
- `scripts/rag_gate.py` — the gate implementation. Invoke with `python3 scripts/rag_gate.py --query "<keywords>"`

---

## Pre-Answer Checklist

- [ ] **RAG GATE INVOKED** — `scripts/rag_gate.py --query "..."` was run; token block pasted into response
- [ ] **hit_count verified** — if zero, `RAG-EMPTY` declared with justification
- [ ] Domain classified
- [ ] Wiki searched first (after RAG gate)
- [ ] Solution Architecture sub-page fetched for relevant module
- [ ] Specialist activated, prior memory recalled
- [ ] Client customizations checked (and client name anonymized)
- [ ] Confidence scored, sources cited
- [ ] `Last360` used for any business day snap
- [ ] Field names traced to source data, not invented
- [ ] Prior solution documents surfaced by the RAG gate have been linked to rather than duplicated
