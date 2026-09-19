# Notion Database Schemas

## Existing Databases

### Product Backlog DB
**ID:** `1fed676f-1cff-473c-b9c9-2c4c646fe529`
**Data source:** `collection://386c820d-dd57-4e50-9966-3930d1a81d15`

| Column | Type | Values |
|--------|------|--------|
| Feature | Title | (task name) |
| Category | Select | Infrastructure, Collector, Analysis, Frontend, API, Testing |
| Effort | Select | S, M, L, XL |
| Layer | Select | L1 Peripheral, L2 Mosaic, L3 Asymmetry, L4 Timing, L5 Conviction |
| Priority | Select | P0 Critical, P1 High, P2 Medium, P3 Low |
| Sprint | Select | (sprint identifier) |
| Status | Select | Done, In Progress, Backlog, Blocked, Needs Review, Needs Clarification |

**Agent behavior:**
- READ: Query for items where Status = `Approved` or `Backlog`, ordered by Priority
- WRITE (status): Update status as agent works (In Progress → Done/Blocked)
- WRITE (propose): Create new items with Status = `Needs Review`
- NEVER: Delete items, change Priority, change items with Status = `Done`

### Research Hub
**ID:** `3127772f-a7ae-8164-a661-fb85c6dad3c9`

Used as parent page for daily briefings. Agent creates child pages here.

### Product Roadmap
**ID:** `32d7772f-a7ae-81ec-892c-d27165425313`

READ ONLY. Agent reads for strategic context but never modifies.

## New Database: Agent Knowledge

**Create on first run if not exists.**
**Parent:** Under Founder OS root (`2b37772f-a7ae-80ea-afc8-d7bdc7851472`)

| Column | Type | Values / Description |
|--------|------|---------------------|
| Title | Title | Entity title |
| Type | Select | MODULE, DECISION, CORRECTION, PATTERN, FAILURE, PERSONA |
| Tags | Multi-select | Flexible — e.g., database, collector, config, universal, api |
| Date | Date | When the entity was created/last significant update |
| Content | Rich text | Full entity content (JSON rendered as readable text) |
| Source | Select | dan-correction, agent-discovery, build-review, cycle-learning, bootstrap |
| Related Entities | Rich text | Comma-separated entity IDs (workaround if relations aren't possible) |
| Modules | Multi-select | Which modules this relates to |
| Priority | Select | blocking, high, normal, low |
| Status | Select | active, archived, superseded |
| Local ID | Rich text | Matches the entity ID in local graph (for sync) |

### Sync Protocol

**At cycle start (Phase 0: REMEMBER):**

1. Read `sync-state.json` for last sync timestamp
2. Query Notion Agent Knowledge DB for entries where Last Edited > last sync
3. For each newer Notion entry:
   - If Local ID exists locally → update local entity with Notion content
   - If Local ID doesn't exist locally → create new local entity from Notion
4. Check for entries that exist locally but were deleted from Notion → mark as `archived`
5. For each local entity without a `notion_id` → create in Notion, save `notion_id` back
6. For each local entity updated since last sync → update Notion entry
7. Update `sync-state.json`

**Conflict resolution:**
- Notion wins if Dan edited it (Dan's changes are corrections by definition)
- Local wins if it's a new entity from the current cycle (not yet in Notion)
- If both edited: Notion wins (Dan's intent takes priority)

**Error handling:**
- If Notion is unreachable: skip sync, set flag `sync_pending = true`
- Next cycle will attempt a full sync
- Local graph is always the working copy — Notion is the mirror
