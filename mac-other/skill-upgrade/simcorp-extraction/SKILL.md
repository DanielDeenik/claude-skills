---
name: simcorp-extraction
description: >
  SimCorp Dimension data extraction designer. Designs DEX configs, DFS feeds, .dat
  file specs, and cross-table data pulls using the MiroFish 3-layer architecture:
  GraphRAG Digital Twin (queries the Notion Solution Architecture for tables, FKs,
  ER diagrams), Technical Committee Swarm (Extraction Architect + DB Optimization
  Agent + .DAT Format Auditor in dialogue), Simulation Sandbox (empty result,
  cardinality blow-up, schema drift, code table mismatch checks). Outputs extraction
  definition + .dat spec + dissent log + risk register to Notion. Sister to
  simcorp-super-agent (Q&A) and simcorp-notebooklm-bridge (NotebookLM hand-off).
  Trigger on: data extraction, extraction definition, .dat file, .dat format, DEX,
  DEX config, DFS, DFS feed, Bloomberg feed, file format spec, field mapping,
  extract X to .dat, design extract, cross-table pull, FK traversal extract, DWH
  extract, MiroFish extraction, GraphRAG extraction, extraction architect, format
  auditor, cardinality blow-up, schema drift check.
---

# SimCorp Extraction Designer

Design SimCorp Dimension data extractions using the MiroFish 3-layer architecture.
Use this skill whenever the request is to **produce** a .dat file, DEX config, DFS
feed, or any cross-table/cross-module data pull. For knowledge questions, use
`simcorp-super-agent` instead.

---

## The 3 Layers (run in order, all three required)

### Layer 1 — GraphRAG Digital Twin (Knowledge)

Query the Notion Solution Architecture as the structural source of truth.

1. `notion-search` for the topic in the Solution Architecture parent
   `33d7772fa7ae812c8c44cc10fb0b3144` (master `33d7772fa7ae81daa22fc4641db97fa5`)
2. `notion-fetch` the relevant module sub-page (one of 12) — read hub tables, ER
   diagram, cross-module dependencies
3. Cross-reference `Field_Mapping_Reference.md` to confirm columns are
   IMPORTABLE (not DWH_ONLY / SYSTEM_MANAGED / REFERENCE_CONFIG)
4. Trace cross-module FKs explicitly — list every join with cardinality

**Hub backbone for traversal:** SECURITIES (135 FKs), PORTFOLIOS (130), PARTNERS
(82), TRANSMAIN (73), FUNDS (73), AIASSETS (60).

**Output of Layer 1:** a candidate table list, column list, FK path, cardinality
estimate, and a "what's missing" note.

### Layer 2 — Technical Committee Swarm (Design)

Run three internal personas in dialogue. Loop until two of three concur and any
dissent is logged.

| Persona | Lens | Cares about | Default question | Critique vector |
|---------|------|-------------|------------------|-----------------|
| **Extraction Architect** | Reuse + correctness | "Does this match an existing DEX/DFS pattern?" | "Have we built this before?" | Reinvention, scope creep |
| **DB Optimization Agent** | Performance + cost | "What's the cardinality? Where can we push down filters?" | "What's the row count?" | Cartesian explosions, missing indexes |
| **.DAT Format Auditor** | Strictness + downstream consumption | "Will the .dat parser accept this exact byte layout?" | "What's the field separator and code table?" | Date formats, code table drift, encoding |

**Debate protocol:**
1. Architect proposes extraction definition (reuse if possible, new if needed)
2. DB Agent stress-tests for cardinality, proposes filter pushdown / pre-aggregation
3. Format Auditor stress-tests for .dat strictness (separators, dates, codes,
   encoding, fixed-width vs delimited)
4. Re-iterate until 2 of 3 concur
5. Log dissent (if any) — never silently overrule

**Output of Layer 2:** extraction definition + .dat field spec + dissent log.

### Layer 3 — Simulation Sandbox (Validation)

Run four failure-mode checks before the design ships.

| Check | What it tests | Mitigation if it fails |
|-------|---------------|------------------------|
| Empty result | Will any filter combination produce zero rows? | Header-only file acceptable? Or alarm? |
| Cardinality blow-up | Does the join produce >10x expected rows? | Filter pushdown, pre-aggregation, deduplication |
| Schema drift | Does this rely on `SELECT *` or implicit ordering? | Explicit field list with positional anchors |
| Code table mismatch | Does any code field need translation that may not exist? | Fail-loud guard with code table join |

**Output of Layer 3:** risk register + mitigation list + validation snippet.

---

## Worked Example: ESG Ratings Extraction

**Request:** "extract ESG ratings for active equity portfolios"

**Layer 1:** notion-search "ESG" → fetch Securities & Instruments module sub-page →
hub is SECURITIES, ESG fields live in SECESG (FK to SECURITIES) → trace
PORTFOLIOS → POSITIONS → SECURITIES → SECESG path → confirm IMPORTABLE in Field
Mapping → cardinality estimate 4x.

**Layer 2:**
- Architect: "Reuse the existing portfolio extract DEX, add SECESG join"
- DB Agent: "4x blow-up — push portfolio status filter down to position level
  before joining SECESG"
- Format Auditor: "ESG rating is a code field — need code table join, fail loud
  if a rating maps to NULL"
- Consensus: DEX reuse + filter pushdown + code table join + explicit field list

**Layer 3:**
- Empty result → header-only acceptable, OK
- Cardinality → 4x under control after pushdown, OK
- Schema drift → explicit field list, OK
- Code mismatch → fail-loud guard in place, OK

**Output to Notion:** Q&A Log entry with answer + new Wiki page under Securities
& Instruments module sub-page with extraction def + dissent log + risk register.

---

## Constraints (apply in every layer)

- **Preceding convention `Last360`** for any business day snap, NEVER `Same`
- **Never invent table or column names** — every name traces back to Solution
  Architecture or Field_Mapping_Reference.md
- **Anonymize all client names** in output (Nicola Wealth, NWM)
- **No SELECT *** — explicit field lists only
- **Code table joins must fail loud**, not silently NULL

---

## Escalation to Solution Document

Promote a Wiki extraction page to a full solution document if any of these are true:
- Crosses 3+ modules
- Touches alternatives or fund admin
- Has a non-empty dissent log (becomes "Open Questions" section)
- Client-specific customization required

---

## What This Skill Does NOT Do

- Does NOT execute SQL — only designs the extraction
- Does NOT write SimCorp configs directly — produces specs for human implementation
- Does NOT bypass the Wiki — always reads existing knowledge first
- Does NOT invent field names

---

## Reference

- `references/extraction-architecture.md` — Full 3-layer pattern with debate protocol,
  failure modes, and additional worked examples
