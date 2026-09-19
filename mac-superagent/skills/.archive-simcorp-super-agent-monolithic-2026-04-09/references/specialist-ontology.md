# Specialist Ontology — 8 SimCorp Agents

Each specialist has a defined domain, tools it can use, and memory scope. The ReACT
orchestrator routes questions to the right specialist(s) based on keyword matching and
domain classification.

---

## Specialist Roster

### 1. Solution Architect
- **Domain**: Cross-domain system design, module integration, implementation planning
- **Tools**: All docs, KuzuDB graph, Wiki, Deliverables generation
- **Memory scope**: Architecture decisions, client requirements, integration patterns
- **Triggers**: "how should we set up", "design", "architecture", "implementation plan",
  "solution", "best practice"

### 2. DEX Builder
- **Domain**: Data Exchange (DEX/DFS) imports, file formats, field mappings, Bloomberg feeds
- **Tools**: DEX manuals, SQL scripts, config files, format specifications
- **Memory scope**: DEX configurations per client, field mapping tables, format codes
- **Triggers**: "DEX", "DFS", "import", "file format", "field mapping", "Bloomberg",
  "data feed", "S1-S9 imports"

### 3. Config Engineer
- **Domain**: SimCorp Dimension configuration — dropdowns, lookups, code tables, formulas
- **Tools**: Config files, training modules, dropdown audit spreadsheets
- **Memory scope**: Client-specific configs, formula definitions, preceding conventions
- **Triggers**: "config", "dropdown", "lookup", "formula", "SGC", "COND_DEFAULT",
  "code table", "setup", "configure"

### 4. Test Engineer
- **Domain**: Test scenarios, validation, UAT scripts, reconciliation checks
- **Tools**: Test templates, SQL validation scripts, reconciliation tools
- **Memory scope**: Test results per client, known issues, regression patterns
- **Triggers**: "test", "validate", "UAT", "reconciliation", "verify", "check",
  "expected vs actual"

### 5. DB Inspector
- **Domain**: SimCorp Dimension database schema, SQL queries, data lineage, lookthrough
- **Tools**: SQL scripts, schema documentation, database ERDs
- **Memory scope**: Table relationships, common joins, performance notes
- **Triggers**: "SQL", "database", "table", "query", "schema", "lookthrough",
  "data model", "join"

### 6. Training Creator
- **Domain**: Training materials, user guides, step-by-step procedures
- **Tools**: Training modules, screenshots, workflow diagrams
- **Memory scope**: Training feedback, common user mistakes, knowledge gaps
- **Triggers**: "training", "guide", "how to", "step by step", "procedure",
  "user manual", "walkthrough"

### 7. Project Runner
- **Domain**: Project management, timelines, dependencies, status tracking
- **Tools**: Notion databases, calendar, task lists
- **Memory scope**: Project milestones, blockers, resource allocation
- **Triggers**: "project", "timeline", "milestone", "status", "blocker",
  "deadline", "dependency"

### 8. Notion Pipeline
- **Domain**: Notion database operations, Q&A processing, Wiki management, doc generation
- **Tools**: Notion MCP tools, notion_pipeline.py, generate_solution_doc.js, generate_solution_deck.js
- **Memory scope**: Pipeline state, document catalog, processing history
- **Triggers**: "notion", "pipeline", "wiki", "Q&A", "document", "deliverable",
  "solution doc", "deck"

---

## Routing Logic

The orchestrator routes using a two-pass system:

**Pass 1 — Keyword match**: Check question against each specialist's trigger keywords.
Multiple matches are normal — a question about "DEX config for Bloomberg feed" hits both
DEX Builder and Config Engineer.

**Pass 2 — Domain classification**: Use the Notion domain mapping to narrow:
- Front Office → Trading specialists
- Middle Office → Risk/Compliance
- Back Office → Settlement
- DEX/DFS → DEX Builder (primary) + Config Engineer (secondary)
- Alternatives → Config Engineer + DEX Builder (for PELP mappings)
- Fund Admin → Config Engineer + Solution Architect
- Cross-Domain → Solution Architect (orchestrates)

**Multi-specialist queries**: When 2+ specialists are needed, the orchestrator:
1. Runs each specialist independently
2. Merges their outputs
3. Solution Architect resolves any conflicts
4. Combined answer gets the lowest confidence of any contributing specialist

---

## Memory Hierarchy

Each specialist has three memory tiers:

1. **Session memory** (in-conversation): Current question context, clarifications
2. **Persistent memory** (JSON files): Accumulated knowledge per specialist, survives
   sessions. Stored in `memory/specialists/{name}.json`
3. **Graph memory** (KuzuDB): Structural relationships between entities. Shared across
   all specialists. Queryable by relationship type.

When a specialist learns something new (human corrects an answer, new config pattern
discovered), it stores at all three levels:
- Session: immediate recall for follow-up questions
- Persistent: keyword-indexed for future sessions
- Graph: entity-relationship for structural queries ("what modules depend on this config?")
