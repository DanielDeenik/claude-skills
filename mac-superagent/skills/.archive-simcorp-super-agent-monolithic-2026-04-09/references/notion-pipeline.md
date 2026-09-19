# Notion Pipeline — Integration Reference

How the SimCorp Super Agent connects to Notion for input, output, and knowledge management.

---

## Pipeline Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Q&A Log    │────→│  SuperAgent      │────→│  Q&A Log    │
│  (New)      │     │  ReACT Engine    │     │  (Answered) │
└─────────────┘     └──────────────────┘     └──────┬──────┘
                                                     │
                                              Dan Reviews
                                                     │
                              ┌───────────────┬──────┴──────┐
                              ↓               ↓             ↓
                        ┌──────────┐   ┌──────────┐  ┌────────────┐
                        │  Wiki    │   │ Decisions │  │ Deliverable│
                        │ (Valid.) │   │  (Log)    │  │ (.docx/    │
                        └──────────┘   └──────────┘  │  .pptx)    │
                                                     └────────────┘
```

## Two Operating Modes

### Mode 1: Cowork (MCP Notion Tools)
When running inside Cowork/Claude, use MCP tools directly:
- `notion-search` — find existing pages
- `notion-create-pages` — create Q&A entries, Wiki pages
- `notion-update-page` — update status, write answers
- `notion-query-database-view` — query Q&A Log for new questions
- `notion-fetch` — read page content

### Mode 2: CLI (Direct API via notion_pipeline.py)
When running from terminal on Dan's Mac:
```bash
cd ~/Documents/GitHub/Superagent_Consulting
python scripts/notion_pipeline.py --process-inbox    # Answer new questions
python scripts/notion_pipeline.py --promote-wiki     # Push validated → Wiki
python scripts/notion_pipeline.py --generate-docs --domain "Fund Admin" --topic "NAV Setup"
python scripts/notion_pipeline.py --full-cycle        # All of the above
```

## Q&A Log Status Workflow

```
New → Processing → Answered → Validated → Build Request
                      ↑                       ↓
                   (agent)              (doc generation)
```

| Status | Who Sets It | What Happens |
|--------|------------|-------------|
| New | Human (or auto) | Question waiting for agent |
| Processing | Agent | Agent is working on it |
| Answered | Agent | Answer written, awaiting review |
| Validated | Human | Answer confirmed correct |
| Build Request | Human | Triggers .docx/.pptx generation |

## Q&A Log Fields

| Field | Type | Purpose |
|-------|------|---------|
| Question | Title | The question text |
| Domain | Select | Front Office / Middle Office / Back Office / DEX/DFS / Alternatives / Fund Admin / Cross-Domain |
| Status | Select | New / Processing / Answered / Validated / Build Request |
| Answer | Rich text | Agent's response |
| Confidence | Select | High - Cited / Medium - Inferred / Low - Flagged |
| Sources | Rich text | Comma-separated source document names |
| Answered By | Select | Which specialist(s) answered |
| Client | Select | Client context (if applicable) |

## Wiki Page Structure

Validated answers promote to Wiki with this structure:
- **Title**: `[Domain] — [Topic]`
- **Tags**: Module, sub-topic, client (if applicable)
- **Body**: Summary → Detail → Sources → Customizations → Learned date

## Document Generation

When status = "Build Request", the pipeline triggers:
1. `notion_pipeline.py` exports context JSON (question + answer + Wiki context)
2. `generate_solution_doc.js` creates .docx (formal solution design)
3. `generate_solution_deck.js` creates .pptx (presentation summary)
4. Both saved to workspace and tracked in Deliverables database

## Domain → Ontology Mapping

| Notion Domain | Ontology Domain | Primary Specialist |
|--------------|----------------|-------------------|
| Front Office | Trading | Solution Architect |
| Middle Office | Risk/Compliance | Solution Architect |
| Back Office | Settlement | Config Engineer |
| DEX/DFS | DEX/DFS | DEX Builder |
| Alternatives | Alternative Investments | Config Engineer |
| Fund Admin | Fund Administration | Config Engineer |
| Cross-Domain | (all) | Solution Architect |
