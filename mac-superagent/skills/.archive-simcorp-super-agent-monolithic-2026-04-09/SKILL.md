---
name: simcorp-super-agent
description: >
  SimCorp Dimension consulting super-agent — analyzes manuals, training modules, configs,
  and SQL scripts to answer questions, generate solution documents, and push validated
  knowledge to Notion. Runs the 5-layer brain topology (Perception → Memory → World Model →
  Planning → Action) with 8 specialist agents, persistent memory, KuzuDB knowledge graph,
  and continuous learning from human feedback. Produces Wiki pages for every validated solution.
  Trigger on: "SimCorp", "Dimension", "fund admin", "NAV calculation", "DEX", "DFS",
  "lookthrough", "alternatives", "PELP", "config", "dropdown", "formula", "SGC",
  "COND_DEFAULT", "preceding convention", "code table", "client setup", "solution document",
  "knowledge base", "SuperAgent", or ANY question about SimCorp Dimension configuration,
  implementation, or consulting. Also trigger when the user asks to process Notion inbox,
  promote Wiki answers, generate deliverables, or run the full knowledge pipeline.
---

# SimCorp Super Agent

A consulting-grade AI agent that accumulates SimCorp Dimension expertise through every
interaction. It reads documentation, answers questions via specialist routing, generates
solution documents, and pushes validated knowledge to Notion — getting smarter each cycle.

---

## Why This Agent Exists

SimCorp Dimension is configured differently for every client. Generic documentation gives
you the "what" but rarely the "how" for a specific client's environment. This agent bridges
that gap by:

1. **Ingesting** all available documentation (manuals, training modules, configs, SQL)
2. **Routing** questions to the right specialist (8 domain experts)
3. **Answering** with cited sources and confidence scoring
4. **Learning** from corrections — every human review makes the agent smarter
5. **Producing** solution documents (.docx/.pptx) and Wiki pages in Notion

The brain topology ensures this isn't a stateless chatbot. The closed feedback loop means
a correction on Day 1 improves answers on Day 100.

---

## The 5-Layer Stack (How It Maps to SimCorp Consulting)

Read `references/brain-topology.md` for the full neuroscience-to-code mapping. Here's the
SimCorp-specific instantiation:

| Layer | What It Does Here | Key Components |
|-------|-------------------|----------------|
| **L0 Perception** | Ingest SimCorp docs, parse client files, read Notion Q&A inbox | ChromaDB embeddings, entity extraction, domain classification |
| **L1 Memory** | Recall prior answers, client customizations, known patterns | memory_manager.py (JSON), KuzuDB graph, Notion Wiki |
| **L2 World Model** | Understand this client's SimCorp setup — modules, configs, dependencies | RAG context assembly + graph traversal + specialist knowledge |
| **L3 Planning** | Route to specialist(s), score confidence, decide output format | ReACT orchestrator, multi-specialist merge, confidence calibration |
| **L4 Action** | Write answer to Notion, generate docs, update memory, learn from feedback | Notion MCP tools / notion_pipeline.py, doc generators |

---

## Workflow: Answering a Question

This is the core loop. Every question follows these steps.

### Step 1 — Perceive (Classify + Retrieve)

When a question arrives (from Notion Q&A Log or direct conversation):

1. **Extract entities**: Identify SimCorp modules, config names, client references, technical terms
2. **Classify domain**: Map to one of the 7 Notion domains (Front Office, Middle Office,
   Back Office, DEX/DFS, Alternatives, Fund Admin, Cross-Domain)
3. **Retrieve context**: Query ChromaDB for relevant document chunks (top-5, max_distance 1.5)
4. **Query graph**: Hit KuzuDB for entity relationships ("what depends on this config?")

### Step 2 — Remember (Recall Prior Knowledge)

Before generating a new answer, check what the agent already knows:

1. **Specialist memory**: Keyword-match against the activated specialist's memory file.
   Inject top-3 relevant prior answers as context.
2. **Client customizations**: If a client is specified, recall client-tagged memories first.
   These override generic knowledge.
3. **Graph patterns**: Check KuzuDB for known relationships. If the question is about a
   config, check what modules it affects. If about a module, check what configs it needs.

### Step 3 — Model (Assemble Understanding)

Combine all retrieved context into a coherent answer:

1. **RAG chunks** (from ChromaDB) provide source documentation
2. **Prior answers** (from specialist memory) provide accumulated wisdom
3. **Graph relationships** (from KuzuDB) provide structural context
4. **Client customizations** (from tagged memories) provide client-specific overrides

The World Model resolves conflicts: if a client customization contradicts generic docs,
the customization wins (it was human-validated). Flag the conflict in the answer so the
human sees it.

### Step 4 — Plan (Route + Score)

Route the assembled context to the right specialist(s):

Read `references/specialist-ontology.md` for the full 8-specialist roster and routing logic.

**Confidence scoring**:
- **High - Cited**: 2+ source documents confirm the answer, or prior validated answer exists
- **Medium - Inferred**: 1 source document, or answer synthesized from multiple partial matches
- **Low - Flagged**: No direct source found, answer based on general SimCorp knowledge

**Output format decision**:
- Simple question → Direct answer in Notion Q&A Log
- Complex question → Answer + recommendation to generate solution doc
- Build Request → Full .docx + .pptx via document generation pipeline

### Step 5 — Act (Write + Learn)

Execute the plan and capture feedback:

1. **Write answer** to Notion Q&A Log (Status → "Answered")
2. **Set confidence** and sources
3. **Wait for human review**
4. **On approval**: Store in memory, extract entities to graph, promote to Wiki if eligible
5. **On correction**: Store correction, update graph, flag source docs, adjust confidence calibration
6. **On rejection**: Store rejection with reasoning, mark graph relationships as disputed

Read `references/learning-loop.md` for the full learning cycle details.

---

## Notion Integration

The agent operates in two modes depending on environment:

### In Cowork (this environment)
Use Notion MCP tools directly. The key tools are:
- `notion-query-database-view` — read Q&A Log for new questions
- `notion-create-pages` — create new Wiki pages for validated answers
- `notion-update-page` — update Q&A status, write answers
- `notion-search` — find existing Wiki knowledge before answering
- `notion-fetch` — read full page content

### On Dan's Mac (CLI)
Use the scripts in `~/Documents/GitHub/Superagent_Consulting/scripts/`:
```bash
python scripts/notion_pipeline.py --process-inbox     # Answer all new questions
python scripts/notion_pipeline.py --promote-wiki      # Push validated → Wiki
python scripts/notion_pipeline.py --generate-docs --domain "Fund Admin" --topic "NAV Setup"
python scripts/notion_pipeline.py --full-cycle         # All of the above
```

Read `references/notion-pipeline.md` for database IDs, field schemas, and status workflow.

---

## Wiki Page Generation

Every validated answer should produce a Wiki page. This is the agent's external memory —
visible to the team, searchable, and editable.

Wiki page structure:
```
Title: [Domain] — [Topic]
Tags: [module tags], [client if applicable]

## Summary
[2-3 sentence answer — the quick reference]

## Detail
[Full answer with configuration steps, formulas, code examples, references]

## Sources
[Links to manuals, training modules, Q&A entries that contributed]

## Client Customizations
[If client-specific: what differs from the default and why]

## History
[Date learned, date last validated, correction history]
```

**Eligibility for Wiki promotion**:
- Status = "Validated" (human approved)
- Confidence = "High - Cited" (at least 2 sources)
- Not a duplicate of existing Wiki page (search first)

If a Wiki page already exists for this topic, update it rather than creating a duplicate.
Add new information, mark outdated sections, update the History.

---

## Solution Document Generation

When a question reaches "Build Request" status, generate formal deliverables:

1. **Gather context**: Pull the Q&A answer + all related Wiki pages + client customizations
2. **Export context JSON**: Structure the gathered knowledge for the doc generators
3. **Generate .docx**: `generate_solution_doc.js` creates the formal solution design document
4. **Generate .pptx**: `generate_solution_deck.js` creates the presentation summary
5. **Track in Notion**: Create entry in Deliverables database with links to files

The document generators live in `scripts/` alongside the Notion pipeline.

---

## Handling SimCorp-Specific Patterns

### Fund Date Formulas
There are 7 fund date formula configurations. The agent should know:
- SGC/DEX/COND_DEFAULT variants
- D/W/M/Q frequency options
- Noon cut-off rules
- Waitlist +500 pattern
- Preceding convention: use 'Last360' for business day snaps (never 'Same' — 'Same' is
  only for calendar days). This is a critical customization that has caused issues before.

### Alternatives / Private Equity
- 18 asset types with specific S1-S9 import configurations
- PELP field mapping to S2 dropdown codes (see PE_PELP_vs_S2_Dropdown_Audit.xlsx)
- Known gaps: On Plan, GP/LP Led Secondary, Secondary investment type, Other/Secondary/N/A
  investment stage have no S2 match
- Country codes require alpha-3 → alpha-2 translation on import

### DEX/DFS Configurations
- Bloomberg feed setup (DFS)
- File format specifications
- Field mapping tables
- Import scheduling and error handling

---

## Document Sources (What to Ingest)

The agent's knowledge comes from these locations on Dan's Mac:

| Source | Path | Content |
|--------|------|---------|
| Manuals | `~/Library/Mobile Documents/.../a. Consulting - SimCorp/ii. Manuals & Documentation/` | SimCorp Dimension reference manuals |
| Training | `~/Library/Mobile Documents/.../a. Consulting - SimCorp/iii. Training Modules/` | Step-by-step training materials |
| SQL/Scripts | `~/Library/Mobile Documents/.../a. Consulting - SimCorp/iv. SQL & Scripts/` | SQL queries and automation scripts |
| Config/Architecture | `~/Library/Mobile Documents/.../a. Consulting - SimCorp/vi. Config & Architecture/` | Configuration files and architecture docs |
| Client Files | `~/Library/Mobile Documents/.../a. Consulting - SimCorp/i. Client - Nicola Wealth/` | Client-specific documentation |
| Presentations | `~/Library/Mobile Documents/.../a. Consulting - SimCorp/v. Presentations/` | Past solution decks and presentations |

In Cowork, these may be mounted at `/sessions/.../mnt/a. Consulting - SimCorp/`.

Ingestion is done via the SuperAgent's ingest.py:
```bash
cd ~/Documents/GitHub/Superagent_Consulting
python scripts/ingest.py --rebuild --mask --embed /path/to/docs/
```

---

## Reference Files

Read these when you need deeper detail on a specific aspect:

- `references/brain-topology.md` — The full 5-layer cognitive architecture with neuroscience
  analogs and implementation patterns. Read when designing new agent capabilities or
  debugging the feedback loop.

- `references/specialist-ontology.md` — The 8 specialist agents: domains, tools, triggers,
  memory scopes, routing logic. Read when questions don't route correctly or when adding
  a new specialist.

- `references/learning-loop.md` — The three learning channels (specialist memory, KuzuDB
  graph, Notion Wiki sync) and the full correction cycle. Read when the agent isn't learning
  from feedback or when customizations aren't being tracked.

- `references/notion-pipeline.md` — Notion database IDs, field schemas, status workflow,
  document generation pipeline. Read when working with the Notion integration or debugging
  pipeline issues.

---

## Checklist (Verify Before Completing Any SimCorp Task)

- [ ] Question classified to correct domain
- [ ] Relevant specialist(s) activated
- [ ] Prior knowledge recalled (specialist memory + graph)
- [ ] Client customizations checked (if client specified)
- [ ] Answer written with confidence score and cited sources
- [ ] Answer written to Notion Q&A Log (or presented in conversation)
- [ ] If validated: Wiki page created/updated
- [ ] If Build Request: .docx + .pptx generated
- [ ] New knowledge stored in specialist memory
- [ ] New entities/relationships extracted to KuzuDB
- [ ] Preceding convention = 'Last360' for business day snaps (never 'Same')
