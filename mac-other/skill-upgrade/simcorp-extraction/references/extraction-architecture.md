# Data Extraction & .dat Format Architecture

This reference covers the **MiroFish-style multi-agent architecture** for SimCorp data
extraction work — designing DEX/DFS configurations, generating .dat file formats, building
SQL extraction queries, and validating proposed schemas before they ship.

It anchors on three patterns running **simultaneously** rather than as alternatives:

1. **GraphRAG Digital Twin** — knowledge layer
2. **Technical Committee Swarm** — design layer
3. **Simulation Sandbox** — validation layer

The Solution Architecture pages already published in Notion (12 module sub-pages under
"🌐 Solution Architecture — Enterprise Module Network", parent page
`33d7772fa7ae812c8c44cc10fb0b3144`) **are** the GraphRAG layer. Don't rebuild them — query
them.

---

## Layer 1 — GraphRAG Digital Twin (Knowledge)

**Purpose:** Before any extraction work begins, the agent must know which SCDAT tables and
columns hold the data being requested. Hallucinated table names are the #1 failure mode
for SimCorp consulting AI.

**Source of truth (already built):**

| Asset | Location | Use |
|-------|----------|-----|
| Solution Architecture master | Notion page `33d7772fa7ae81daa22fc4641db97fa5` | Cross-module dependency map, hub table backbone, top-20 FK matrix |
| 12 Module sub-pages | Sub-pages of the master | Per-module ER diagram (Mermaid), hub tables, sub-modules, cross-module FK lists |
| Field mapping reference | `vi. Config & Architecture/Schema Reference/Field_Mapping_Reference.md` | All 197,684 fields classified as IMPORTABLE / DWH_ONLY / SYSTEM_MANAGED / REFERENCE_CONFIG / MODULE_SPECIFIC |
| ER diagram source | `vi. Config & Architecture/Schema Reference/ER_Diagrams/*.mermaid` | Raw Mermaid source for each module |
| Interactive overview | `vi. Config & Architecture/Schema Reference/SimCorp_Solution_Architecture.html` | Single-page HTML with all 12 diagrams + dependency matrix |

**Query pattern:** when a user asks to extract a data point, the agent **must** first:

1. Use `notion-search` scoped to the Solution Architecture master page to find the module
   that owns the entity (e.g. "ESG ratings" → Securities & Instruments)
2. Use `notion-fetch` on that module sub-page to read its hub tables and ER diagram
3. Cross-reference the Field Mapping doc to confirm the column is IMPORTABLE (not DWH_ONLY)
4. Trace cross-module FKs from the master page to find any join paths needed (e.g.
   PORTFOLIOS → SECURITIES via 44 FKs)

Only after this graph traversal completes does the agent move to Layer 2.

**Hub table backbone (memorize these — they appear in almost every extraction):**

| Table | FK Refs | Role |
|-------|---------|------|
| `SECURITIES` | 135 | Instrument master (every asset references) |
| `PORTFOLIOS` | 130 | Portfolio master |
| `PARTNERS` | 82 | Counterparties / brokers / custodians |
| `TRANSMAIN` | 73 | Transaction header |
| `FUNDS` | 73 | Fund master (NAV, distributions, share classes) |
| `AIASSETS` | 60 | Alternative investment master |

---

## Layer 2 — Technical Committee Swarm (Design)

**Purpose:** No single perspective produces a robust .dat extraction. The agent runs three
internal personas in dialogue, each with a distinct critique vector. The output is the
artifact they reach consensus on, **plus the dissent log** (important — dissent is where
edge cases hide).

### The three personas

#### Extraction Architect
- **Lens:** SimCorp Data Extractor (DEX/DFS) configuration semantics
- **Cares about:** Filter logic, field selection, output channel (file vs DB), scheduling,
  delta vs full extracts
- **Default question:** *"Does this match an existing extraction definition we can clone,
  or do we need a new one?"*
- **Critique vector:** Reuse over invention. Pushes back on bespoke extracts when a standard
  one exists.

#### DB Optimization Agent
- **Lens:** Underlying Oracle SQL — joins, indexes, row counts, partition pruning
- **Cares about:** FK join cardinality, full-table scans, snapshot date semantics, run-time
  estimates
- **Default question:** *"What's the row count of the driving table, and which index does
  this query hit?"*
- **Critique vector:** Performance over convenience. Pushes back on cartesian risk and
  unindexed lookups.

#### .DAT Format Auditor
- **Lens:** SimCorp's strict file format requirements — delimiters, header rows, encoding,
  null handling, code table mappings
- **Cares about:** Field order, padding, date formats, decimal separators, code table
  translation (alpha-3 → alpha-2 country codes is a recurring trap)
- **Default question:** *"Will SimCorp's import parser accept this exact byte sequence
  on the first try?"*
- **Critique vector:** Format strictness. Pushes back on anything that "should work" but
  hasn't been validated against a known-good import.

### The debate protocol

1. Architect proposes the extraction definition
2. DB Agent runs the SQL mentally and reports any cardinality / performance concern
3. Format Auditor runs the proposed output through known import rules and reports any
   format risk
4. If any persona dissents, the proposal goes back to the Architect with the objection
5. Loop until two of three concur and dissent (if any) is logged

**Output of Layer 2:**
- Final extraction definition (DEX config or SQL)
- .dat file format spec (delimiter, fields, sample row)
- Dissent log (any unresolved concern flagged for human review)

**Important — preceding convention rule:** the Format Auditor must always check that
business-day snaps use `Last360`, never `Same`. `Same` is calendar-days only. This rule
has caused production incidents and is the kind of thing the Auditor exists to catch.

---

## Layer 3 — Simulation Sandbox (Validation)

**Purpose:** Before the design ships, the agent simulates failure modes. This is *not*
running the SQL — it's reasoning through what could go wrong with mock inputs.

### Sandbox checks (run all four)

**1. Empty result simulation**
- *"What if the snapshot date has zero rows for this filter?"*
- Does the .dat output produce a header-only file or fail entirely?
- Does downstream consumption tolerate empty files?

**2. Cardinality blow-up simulation**
- *"What if the driving table doubles in row count next quarter?"*
- Does the join still complete in the scheduled window?
- Is the file size still within SimCorp's import buffer?

**3. Schema-drift simulation**
- *"What if SimCorp adds a column to a referenced table next release?"*
- Does the extraction break, silently change shape, or stay stable?
- Are we using `SELECT *` anywhere that would cause silent drift? (Always answer no.)

**4. Code table mismatch simulation**
- *"What if the source data contains a code that's not in our mapping table?"*
- Does the extraction fail loudly, or silently emit nulls?
- For country / currency / classification codes, the answer must be: **fail loudly**.

### Output of Layer 3
- Risk register: each simulation that surfaced a concern, with severity (block / fast-follow / track)
- Mitigation list: what to add to the design before sign-off
- Validation snippet: SQL or check the human can run on a real environment to confirm

---

## Putting it together — the full extraction workflow

When a user asks "extract ESG ratings for active equity portfolios":

1. **GraphRAG (Layer 1):**
   - Search Notion Solution Architecture for "ESG"
   - Identify owning module (Securities & Instruments)
   - Fetch the module sub-page, find the relevant hub tables
   - Cross-reference Field Mapping to confirm columns are IMPORTABLE
   - Trace FKs from PORTFOLIOS to the ESG fields

2. **Swarm (Layer 2):**
   - Architect proposes a DEX definition reusing an existing portfolio extract
   - DB Agent flags that ESG joins multiply row count 4x — proposes filter pushdown
   - Format Auditor flags that one ESG field is a code and needs code table mapping
   - Consensus: DEX with filter pushdown + code table join, format spec attached

3. **Sandbox (Layer 3):**
   - Empty result: header-only file is acceptable downstream → OK
   - Cardinality: 4x multiplier under control after pushdown → OK
   - Schema drift: explicit field list, no SELECT * → OK
   - Code mismatch: code table join with NOT NULL guard → fail-loud → OK

4. **Output to Notion:**
   - Q&A Log entry with the answer
   - New Wiki page under the relevant module with the extraction definition + risk register
   - Link to source ER diagram on the module sub-page
   - Status → Validated only after human review

---

## When to escalate to a Solution Document

If the extraction crosses 3+ modules, touches alternatives or fund admin, or the dissent
log is non-empty, escalate from Wiki page to full solution document via the standard
.docx + .pptx pipeline. The dissent log becomes the "Open Questions" section of the doc.

---

## What this layer does NOT do

- Does not execute SQL against real environments (humans do that)
- Does not write to SimCorp configs directly (humans do that)
- Does not bypass the Notion Wiki review step (every validated answer must be promoted
  by a human)
- Does not invent table or column names — if GraphRAG (Layer 1) doesn't surface a name,
  the agent says "not found in Solution Architecture, need source-data confirmation"
  rather than guessing
