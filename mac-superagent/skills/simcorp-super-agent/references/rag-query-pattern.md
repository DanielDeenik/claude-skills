# RAG Query Patterns for the AKG Facts Store

The AKG persistent RAG stores every ingested document in a DuckDB facts store
(`akg.duckdb.cowork` on the VM, `akg.duckdb` on the Mac). The primary table is
`facts.source_citations`; embeddings live in `facts.chunk_embeddings` and
`facts.entity_embeddings`. The canonical HNSW index and semantic search are
exposed through the `simcorp-twin-mcp` FastMCP server (6 tools: sql_query,
semantic_search, graph_neighbors, inspect_table, write_wiki,
write_solution_doc). This document lists the queries that matter.

## Table Schema

```
facts.source_citations
  id                VARCHAR PRIMARY KEY
  source_uri        VARCHAR    -- file:// URI of the ingested source
  tier              INTEGER    -- 1 vendor, 3 curated xlsx, 4 sessions
  page              VARCHAR    -- page marker (p1, p2, <body>, <document>)
  section           VARCHAR    -- section heading or table_N
  span              VARCHAR    -- span within the section
  extracted_text    VARCHAR    -- the actual text
  parent_citation_id VARCHAR   -- parent chunk
  content_hash      VARCHAR
  created_at        TIMESTAMP
```

## Pattern 1 — Keyword Count by Source

Used by `scripts/rag_gate.py`. Returns the top sources mentioning the keyword,
with hit counts.

```sql
SELECT source_uri, tier, COUNT(*) AS hits
FROM facts.source_citations
WHERE lower(extracted_text) LIKE '%<keyword>%'
GROUP BY source_uri, tier
ORDER BY hits DESC
LIMIT 10;
```

## Pattern 2 — Keyword Passage Dump for a Specific Source

When the gate surfaces a relevant source, pull its passages for the topic.

```sql
SELECT page, section, extracted_text
FROM facts.source_citations
WHERE source_uri LIKE '%<source_filename>%'
  AND lower(extracted_text) LIKE '%<keyword>%'
ORDER BY page, span;
```

## Pattern 3 — Enumerate Sections in a Document

Gives the structural map of a document (for solution documents with heading
structure, this exposes the table of contents).

```sql
SELECT DISTINCT section
FROM facts.source_citations
WHERE source_uri LIKE '%<source_filename>%'
ORDER BY section;
```

## Pattern 4 — Pull a Specific Table from a Document

Ingested documents have their tables captured as `section = 'table_N'`.

```sql
SELECT extracted_text
FROM facts.source_citations
WHERE source_uri LIKE '%<source_filename>%'
  AND section = 'table_<N>';
```

## Pattern 5 — Batch-Job-ID Mentions Across the Corpus

Find every source that references a specific SimCorp batch job.

```sql
SELECT source_uri, tier, section, substring(extracted_text, 1, 200) AS preview
FROM facts.source_citations
WHERE extracted_text LIKE '%FO_FND_MP_COMP_UPD%'
   OR extracted_text LIKE '%FO_TAA_UPD%'
   OR extracted_text LIKE '%FO_FND_FOH_UPD%'
ORDER BY tier, source_uri;
```

## Pattern 6 — Tier Filtering

Restrict to authoritative vendor sources (tier 1), curated client sources
(tier 3), or session artefacts (tier 4).

```sql
-- Vendor-only (tier 1)
SELECT source_uri, COUNT(*) hits
FROM facts.source_citations
WHERE tier = 1
  AND lower(extracted_text) LIKE '%<keyword>%'
GROUP BY source_uri
ORDER BY hits DESC;

-- Meeting transcripts only (tier 4, filename pattern)
SELECT source_uri, COUNT(*) hits
FROM facts.source_citations
WHERE tier = 4
  AND source_uri LIKE '%Meeting Recording%'
  AND lower(extracted_text) LIKE '%<keyword>%'
GROUP BY source_uri
ORDER BY hits DESC;
```

## Pattern 7 — Semantic Search via simcorp-twin-mcp

When keyword search misses (the user is asking about a concept expressed in
different words than the source uses), switch to semantic search. The canonical
path is through the MCP server:

```
Tool: simcorp-twin-mcp:semantic_search
  query: "what drives the daily decomposition chain in Nicola"
  top_k: 10
  level: chunk  # or domain, chain, table_curated, table_db, fk_db, column_db
```

The MCP server runs the voyage-finance-2 embedder (1024-dim), searches the HNSW
cosine index on `sc.embedding`, and returns ranked chunks with source URIs.

## Pattern 8 — Graph Traversal via simcorp-twin-mcp

For questions about schema relationships:

```
Tool: simcorp-twin-mcp:graph_neighbors
  table: "AIASSETS"
  layer: "foalts"     # foalts / db / curated
  hops: 2
```

Returns neighbouring tables via FK edges up to the specified hop depth.

## Opening the DB from Python (outside the gate)

```python
import duckdb
con = duckdb.connect(
    "/path/to/akg.duckdb",   # or akg.duckdb.cowork on the VM
    read_only=True
)

# List tables
con.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "ORDER BY table_schema, table_name"
).fetchall()
```

## What NOT to Do

- Do not write to the facts store directly. Ingestion is owned by the
  `akg ingest` CLI and the AKG ingestion pipeline.
- Do not invent table names. The schema is listed above; if another table is
  needed, check with `information_schema.tables` first.
- Do not cache DB handles across sessions. Open read-only per call.
- Do not run semantic search directly against the VM DuckDB without the MCP
  server — the HNSW index and the embedding function live inside
  `simcorp-twin-mcp`. Keyword search is fine via DuckDB alone.
