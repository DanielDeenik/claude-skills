# Learning Loop — Continuous Knowledge Accumulation

How the SimCorp Super Agent gets smarter with every interaction. This is the feedback loop
from L4 Action back through L1 Memory and L0 Perception — the mechanism that turns a
static RAG system into a living knowledge base.

---

## The Three Learning Channels

### Channel 1: Specialist Memory (Local JSON)

**What it stores**: Question-answer pairs with metadata (confidence, source, specialist,
timestamp, human verdict).

**Where it lives**: `memory/specialists/{name}.json` on the SuperAgent host
(~/Documents/GitHub/Superagent_Consulting/memory/specialists/)

**When it fires**: After every answered question, regardless of confidence level.

**Format per entry**:
```json
{
  "id": "mem_20260409_001",
  "question": "How do I set up fund date formulas for daily NAV?",
  "answer": "Use SGC/DEX/COND_DEFAULT with D (daily) frequency...",
  "confidence": "High - Cited",
  "sources": ["Fund_Admin_Manual_Ch12.pdf", "Training_Module_FA03.pdf"],
  "specialist": "config_engineer",
  "keywords": ["fund date", "formula", "daily", "NAV", "SGC", "COND_DEFAULT"],
  "human_verdict": "approved",
  "corrections": null,
  "timestamp": "2026-04-09T14:30:00Z"
}
```

**Recall mechanism**: On new question, keyword-match against all entries for the activated
specialist. Top-K matches by keyword overlap + recency weighting get injected into the
specialist's context window as "prior knowledge."

### Channel 2: Knowledge Graph (KuzuDB)

**What it stores**: Entity-relationship triples extracted from answers and documents.

**Where it lives**: KuzuDB embedded database alongside ChromaDB in the SuperAgent.

**When it fires**: During ingestion (entity extraction from docs) AND after validated answers
(new relationships discovered during Q&A).

**Node types**:
- Module (e.g., "Fund Administration", "DEX/DFS", "Alternatives")
- Config (e.g., "SGC formula", "PELP dropdown", "S2 import format")
- Entity (e.g., "Nicola Wealth", "Bloomberg", "AISTAGES code table")
- Concept (e.g., "preceding convention", "lookthrough", "NAV calculation")

**Edge types**:
- `DEPENDS_ON`: Module A requires Module B
- `CONFIGURES`: Config X sets up Module Y
- `OVERRIDES`: Client-specific Config X overrides default Config Y
- `MAPS_TO`: PELP field maps to SimCorp dropdown
- `LEARNED_FROM`: Knowledge was derived from Source Z
- `VALIDATED_BY`: Human validated this relationship on Date D

**Query patterns**:
```cypher
// What configs does Fund Admin depend on?
MATCH (m:Module {name: 'Fund Administration'})-[:DEPENDS_ON]->(c:Config)
RETURN c.name, c.description

// What did we learn from Nicola Wealth engagement?
MATCH (e:Entity {name: 'Nicola Wealth'})<-[:LEARNED_FROM]-(k)
RETURN k.type, k.name, k.timestamp
```

### Channel 3: Notion Wiki Sync

**What it stores**: Validated, high-confidence knowledge promoted to the team-visible Wiki.

**Where it lives**: Notion Wiki database (ID: 93a436bb-099b-4680-b098-72dfeb554dcc)

**When it fires**: When a Q&A answer reaches "Validated" status (human-approved, high
confidence, at least 2 sources cited).

**Wiki page format**:
```
Title: [Domain] — [Topic]
Tags: [module], [sub-topic], [client if applicable]
Body:
  ## Summary
  [Concise answer — 2-3 sentences]

  ## Detail
  [Full answer with configuration steps, formulas, references]

  ## Sources
  [Links to manuals, training modules, or prior Q&A]

  ## Customizations
  [Client-specific overrides or special configurations, if any]

  ## Learned On
  [Date first learned + date last validated]
```

**Sync direction**: Bidirectional.
- Agent → Notion: validated answers promote to Wiki
- Notion → Agent: if someone edits a Wiki page, next ingestion picks up the change and
  updates the knowledge graph

---

## The Learning Cycle (Step by Step)

```
1. Question arrives (Notion Q&A Log or direct query)
       ↓
2. L0 PERCEPTION: Parse question, extract entities, classify domain
       ↓
3. L1 MEMORY: Recall relevant specialist memories + graph relationships
       ↓
4. L2 WORLD MODEL: Assemble context (RAG chunks + memory + graph)
       ↓
5. L3 PLANNING: Route to specialist(s), generate answer, score confidence
       ↓
6. L4 ACTION: Write answer to Notion Q&A Log
       ↓
7. HUMAN REVIEW: Dan reviews answer
       ↓
   ┌─── If APPROVED:
   │    → Store in specialist memory (Channel 1)
   │    → Extract new entities/relationships to KuzuDB (Channel 2)
   │    → If high confidence + 2+ sources: promote to Wiki (Channel 3)
   │    → Prediction error = 0 (model was correct)
   │
   ├─── If CORRECTED:
   │    → Store correction in specialist memory (Channel 1)
   │    → Update/create graph relationships with correction (Channel 2)
   │    → Do NOT promote to Wiki yet (needs re-validation)
   │    → Prediction error > 0 → update World Model weights
   │    → Flag source documents for re-review
   │
   └─── If REJECTED:
        → Store rejection with reasoning in specialist memory
        → Mark any graph relationships as "disputed"
        → Prediction error = max → significant World Model update
        → Trigger: "What went wrong?" analysis
```

---

## Customization Learning (The Key Differentiator)

SimCorp Dimension is configured differently for every client. The agent must learn and
track these customizations without confusing Client A's setup with Client B's.

**Client isolation**: Memory entries are tagged with a `client` field. When answering for
a specific client, memories from that client get priority weighting. Generic (no-client)
memories serve as defaults.

**Customization types the agent should learn**:
1. **Config overrides**: Client uses non-standard dropdown values, formula parameters
2. **Workflow variants**: Client's business process differs from default SimCorp workflow
3. **Integration specifics**: Client's data feeds, file formats, naming conventions
4. **Known issues**: Bugs or workarounds specific to client's environment version
5. **Preferences**: Client contact prefers certain report formats, terminology, detail level

**How to detect customizations**: When the agent's answer (based on generic knowledge)
gets corrected, the correction IS the customization. Store it with the client tag and
the reason it differs from the generic answer.

---

## Notion Database IDs (Reference)

- Q&A Log: `8c355a12-7b9e-4991-b497-619c9b345169`
- Wiki: `93a436bb-099b-4680-b098-72dfeb554dcc`
- Deliverables: `76fbcea1-5a5a-4e40-b0ec-20d51b0fb7d9`
- Decisions: `494ea923-1480-4308-b55c-344b8a59724e`
- Parent Page: `3337772f-a7ae-81bc-b7c8-d025e13f7a86`
