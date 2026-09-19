---
name: lightrag
description: "Developer co-pilot for LightRAG — graph-based Retrieval-Augmented Generation framework. Customized for SimCorp consulting: Anthropic Claude + Voyage AI (finance embeddings), PostgreSQL all-in-one storage, financial domain entity types. Covers setup, configuration, document ingestion, querying, storage backends, deployment, debugging, and evaluation."
---

# LightRAG Developer Skill

Complete developer co-pilot for the LightRAG framework — graph-based RAG that extracts entities and relationships from documents, builds a knowledge graph, and uses multi-modal retrieval for queries.

> **Customized for Dan's SimCorp consulting practice.** Defaults: Anthropic Claude + Voyage AI (`voyage-finance-2`) for financial domain embeddings, PostgreSQL all-in-one storage, entity types tuned for fund administration and wealth management domains.

## Task Routing

| Task | Section |
|------|---------|
| Install and first run | [Setup](#setup) |
| Configure LLM, embeddings, storage | [Configuration](#configuration) |
| Insert documents and build KG | [Document Ingestion](#document-ingestion) |
| Ingest SimCorp domain knowledge | [SimCorp Use Cases](#simcorp-use-cases) |
| Query the knowledge graph | [Querying](#querying) |
| Choose and configure storage backends | [Storage Backends](#storage-backends) |
| Connect LLM providers | [LLM Providers](#llm-providers) |
| Deploy API server or Docker | [Deployment](#deployment) |
| Debug common issues | [Troubleshooting](#troubleshooting) |
| Evaluate RAG quality | [Evaluation](#evaluation) |
| Architecture deep-dive | [Architecture](#architecture) |

---

## Architecture

LightRAG uses 4 pluggable storage layers:

```
Documents  →  Chunking  →  Entity/Relation Extraction  →  Knowledge Graph
                                                              ↓
Query  →  Keyword Extraction  →  KG Retrieval + Vector Search  →  LLM Response
```

### Storage Types

| Storage Type | Purpose | Recommended Backend |
|-------------|---------|---------------------|
| KV_STORAGE | LLM response cache, text chunks, doc info | **PGKVStorage** |
| VECTOR_STORAGE | Entity/relation/chunk embeddings | **PGVectorStorage** |
| GRAPH_STORAGE | Entity-relation graph structure | **PGGraphStorage** |
| DOC_STATUS_STORAGE | Document processing status tracking | **PGDocStatusStorage** |

> PostgreSQL all-in-one is recommended for your setup — single service to manage, fits within your ~€200/mo cloud budget, and handles the scale of a consulting knowledge base well.

### Query Modes

| Mode | Description | Best For |
|------|-------------|----------|
| `local` | Context-dependent retrieval focused on specific entities | "What is the settlement flow for CUSTODIAN-01?" |
| `global` | Community/summary-based broad knowledge retrieval | "What are the main integration patterns across clients?" |
| `hybrid` | Combines local and global | **General-purpose — use as default** |
| `naive` | Direct vector search without graph | Simple semantic search |
| `mix` | Integrates KG and vector retrieval (recommended with reranker) | Best quality with reranker |
| `bypass` | Pass query directly to LLM without retrieval | When RAG context not needed |

---

## Setup

### Install (Python)

```bash
# Core package
pip install lightrag-hku

# With API server support
pip install lightrag-hku[api]

# Development mode with uv
uv sync
uv sync --extra api          # API support
uv sync --extra test          # Testing
```

### Quick Start (Anthropic + Voyage + PostgreSQL)

This is the recommended setup for your SimCorp consulting practice — Claude for LLM, Voyage Finance for domain-tuned embeddings, PostgreSQL for all storage.

```python
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.anthropic import anthropic_complete_if_cache, anthropic_embed
from lightrag.utils import wrap_embedding_func_with_attrs
import numpy as np

async def main():
    # Use voyage-finance-2 for financial domain embeddings
    @wrap_embedding_func_with_attrs(embedding_dim=1024, max_token_size=32000)
    async def finance_embed(texts: list[str]) -> np.ndarray:
        return await anthropic_embed.func(texts, model="voyage-finance-2")

    rag = LightRAG(
        working_dir="./rag_storage",
        workspace="simcorp_kb",              # Isolate SimCorp data

        # LLM: Anthropic Claude
        llm_model_func=anthropic_complete_if_cache,
        llm_model_name="claude-sonnet-4-20250514",
        llm_model_kwargs={"max_tokens": 4096},

        # Embeddings: Voyage Finance (optimized for financial domain)
        embedding_func=finance_embed,

        # Storage: PostgreSQL all-in-one
        kv_storage="PGKVStorage",
        vector_storage="PGVectorStorage",
        graph_storage="PGGraphStorage",
        doc_status_storage="PGDocStatusStorage",

        # Entity types tuned for SimCorp / fund admin domain
        entity_types=[
            "Organization",       # Clients, custodians, transfer agents, fund admins
            "Person",             # Stakeholders, SMEs, consultants
            "SimCorpModule",      # SimCorp Dimension modules (Front Office, Investment Book of Record, etc.)
            "DatabaseTable",      # Oracle AI* tables (AISETTLEMENTS, AIFUNDORDERS, etc.)
            "DataExchange",       # DEX files, DFS dataflows, file specs
            "Workflow",           # Settlement flows, reconciliation processes, NAV calculations
            "Configuration",      # Module configs, policies, rules, parameters
            "FinancialInstrument",# Securities, funds, asset classes
            "Concept",            # Domain terms, glossary entries
            "Decision",           # Architecture/design decisions with rationale
        ],

        # Chunking
        chunk_token_size=1200,
        chunk_overlap_token_size=100,

        # Concurrency (conservative for solopreneur API budget)
        max_async=4,
        max_parallel_insert=2,
    )

    # CRITICAL: Always initialize storages after instantiation
    await rag.initialize_storages()

    # Insert a document
    await rag.ainsert("Your document text here...")

    # Query
    result = await rag.aquery(
        "What is the settlement workflow for custodian integrations?",
        param=QueryParam(mode="hybrid")
    )
    print(result)

    # Cleanup
    await rag.finalize_storages()

asyncio.run(main())
```

**Environment variables required:**
```bash
# LLM
export ANTHROPIC_API_KEY="your-anthropic-key"

# Embeddings (Voyage AI — Anthropic doesn't have native embeddings)
export VOYAGE_API_KEY="your-voyage-key"

# PostgreSQL
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_USER="your_username"
export POSTGRES_PASSWORD="your_password"
export POSTGRES_DATABASE="lightrag_simcorp"
```

### Minimal Example (File-Based Storage for Dev/Testing)

```python
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.anthropic import anthropic_complete_if_cache, anthropic_embed

async def main():
    rag = LightRAG(
        working_dir="./rag_storage",
        llm_model_func=anthropic_complete_if_cache,
        llm_model_name="claude-sonnet-4-20250514",
        llm_model_kwargs={"max_tokens": 4096},
        embedding_func=anthropic_embed,  # Uses voyage-3 by default
    )

    await rag.initialize_storages()
    await rag.ainsert("Your document text here...")
    result = await rag.aquery("Your question?", param=QueryParam(mode="hybrid"))
    print(result)
    await rag.finalize_storages()

asyncio.run(main())
```

---

## Configuration

### LightRAG Constructor (Key Parameters)

```python
rag = LightRAG(
    # Directory
    working_dir="./rag_storage",        # Where cache and files are stored
    workspace="simcorp_kb",             # Data isolation namespace

    # LLM (Anthropic Claude — your default)
    llm_model_func=anthropic_complete_if_cache,
    llm_model_name="claude-sonnet-4-20250514",
    llm_model_kwargs={"max_tokens": 4096},

    # Embedding (Voyage Finance — financial domain optimized)
    embedding_func=finance_embed,       # See Setup for wrapper definition

    # Storage backends (PostgreSQL all-in-one — recommended)
    kv_storage="PGKVStorage",
    vector_storage="PGVectorStorage",
    graph_storage="PGGraphStorage",
    doc_status_storage="PGDocStatusStorage",

    # Chunking
    chunk_token_size=1200,              # Tokens per chunk (500-1500 recommended)
    chunk_overlap_token_size=100,       # Overlap between chunks

    # Entity extraction (SimCorp domain)
    entity_types=[
        "Organization", "Person", "SimCorpModule", "DatabaseTable",
        "DataExchange", "Workflow", "Configuration",
        "FinancialInstrument", "Concept", "Decision",
    ],

    # Concurrency
    max_async=4,                        # Max concurrent LLM requests
    max_parallel_insert=2,              # Parallel document processing (2-10)

    # Query defaults
    top_k=40,                           # KG entities/relations to retrieve
    chunk_top_k=20,                     # Text chunks to retrieve
    max_total_tokens=30000,             # Total context budget

    # Reranking
    rerank_model=None,                  # Reranker model name
)
```

### QueryParam (Per-Query Configuration)

```python
from lightrag import QueryParam

param = QueryParam(
    mode="hybrid",                  # local|global|hybrid|naive|mix|bypass
    top_k=60,                       # Override KG retrieval count
    chunk_top_k=20,                 # Override chunk count
    max_entity_tokens=6000,         # Max tokens for entities
    max_relation_tokens=8000,       # Max tokens for relations
    max_total_tokens=30000,         # Total context budget
    enable_rerank=True,             # Enable reranking
    stream=False,                   # Streaming output
    only_need_context=False,        # Return only retrieved context
    only_need_prompt=False,         # Return only generated prompt
    response_type="Multiple Paragraphs", # Response format
    user_prompt="Additional instructions", # Extra LLM instructions
    conversation_history=[],        # Chat history for multi-turn
    include_references=False,       # Include citation references
)
```

### Custom Embedding Functions

Use `@wrap_embedding_func_with_attrs` decorator:

```python
from lightrag.utils import wrap_embedding_func_with_attrs
from lightrag.llm.anthropic import anthropic_embed
import numpy as np

# Recommended: voyage-finance-2 for your financial domain work
@wrap_embedding_func_with_attrs(embedding_dim=1024, max_token_size=32000)
async def finance_embed(texts: list[str]) -> np.ndarray:
    # IMPORTANT: Call .func to access the underlying function, not the wrapped one
    return await anthropic_embed.func(texts, model="voyage-finance-2")
```

**CRITICAL**: Cannot wrap already-decorated embedding functions. Use `.func` to access the underlying function.

### Voyage AI Embedding Models

| Model | Dimension | Best For |
|-------|-----------|----------|
| `voyage-finance-2` | 1024 | **Your default** — optimized for financial domain |
| `voyage-3` | 1024 | General-purpose fallback |
| `voyage-3-large` | 1024 | Best general-purpose quality |
| `voyage-3-lite` | 512 | Cost-optimized, lower quality |
| `voyage-code-3` | 1024 | Code-heavy documents |

### Environment Variable Configuration

For the API server, configure via `.env` file (see `references/env-example.md`). Key sections:

| Section | Key Variables |
|---------|--------------|
| Server | `HOST`, `PORT`, `WEBUI_TITLE`, `WORKERS`, `TIMEOUT` |
| Auth | `AUTH_ACCOUNTS`, `LIGHTRAG_API_KEY`, `TOKEN_SECRET` |
| LLM | `LLM_BINDING`, `LLM_BINDING_HOST`, `LLM_BINDING_API_KEY`, `LLM_MODEL` |
| Embedding | `EMBEDDING_BINDING`, `EMBEDDING_MODEL`, `EMBEDDING_DIM` |
| Storage | `LIGHTRAG_KV_STORAGE`, `LIGHTRAG_VECTOR_STORAGE`, `LIGHTRAG_GRAPH_STORAGE` |
| Query | `TOP_K`, `CHUNK_TOP_K`, `MAX_TOTAL_TOKENS` |
| Reranking | `RERANK_BINDING`, `RERANK_MODEL`, `MIN_RERANK_SCORE` |
| Concurrency | `MAX_ASYNC`, `MAX_PARALLEL_INSERT` |

---

## SimCorp Use Cases

### Use Case 1: SimCorp Domain Knowledge Base

Ingest your glossary, schema registry, decisions log, domain pages, and Q&A cache into LightRAG for graph-based retrieval across all SimCorp knowledge.

```python
import asyncio
import json
from lightrag import LightRAG, QueryParam

async def ingest_simcorp_knowledge(rag: LightRAG):
    """Ingest all SimCorp domain knowledge into the graph."""

    # 1. Glossary terms (50+ terms)
    with open("memory/simcorp/glossary.md", "r") as f:
        glossary = f.read()
    await rag.ainsert(glossary, file_paths=["glossary.md"])

    # 2. Schema registry (102 Oracle AI tables)
    with open("memory/simcorp/schema/registry.json", "r") as f:
        schema = json.load(f)
    # Convert schema to text for ingestion
    schema_text = "\n\n".join([
        f"Table: {table['name']}\nColumns: {', '.join(table.get('columns', []))}\n"
        f"Description: {table.get('description', 'N/A')}"
        for table in schema.get("tables", [])
    ])
    await rag.ainsert(schema_text, file_paths=["schema-registry.json"])

    # 3. Decision log (37 decisions with rationale)
    with open("memory/simcorp/decisions/log.md", "r") as f:
        decisions = f.read()
    await rag.ainsert(decisions, file_paths=["decisions-log.md"])

    # 4. DEX patterns
    with open("memory/simcorp/patterns/dex-patterns.md", "r") as f:
        patterns = f.read()
    await rag.ainsert(patterns, file_paths=["dex-patterns.md"])

    # 5. Client profiles
    import glob
    for client_file in glob.glob("memory/simcorp/clients/*.md"):
        with open(client_file, "r") as f:
            await rag.ainsert(f.read(), file_paths=[client_file])

    print("SimCorp knowledge base ingested.")
```

**Recommended query patterns for this use case:**

```python
# Specific factual lookups (use local mode)
result = await rag.aquery(
    "What columns does the AISETTLEMENTS table have?",
    param=QueryParam(mode="local")
)

# Cross-domain questions (use hybrid mode)
result = await rag.aquery(
    "How do DEX settlement files relate to the AIFUNDORDERS table?",
    param=QueryParam(mode="hybrid")
)

# High-level architecture questions (use global mode)
result = await rag.aquery(
    "What are the main data flow patterns across all custodian integrations?",
    param=QueryParam(mode="global")
)
```

### Use Case 2: Client Deliverable Search

Index solution docs, DEX specs, config documents, and test plans across projects for cross-client pattern reuse.

```python
async def ingest_client_deliverables(rag: LightRAG, deliverables_dir: str):
    """Ingest client deliverables for cross-project search.

    IMPORTANT: Apply data masking before ingestion if using shared storage.
    Use your data_masker.py to mask client names before inserting.
    """
    import glob
    from pathlib import Path

    # Use a separate workspace for client docs
    # to isolate from the domain knowledge base
    for docx_path in glob.glob(f"{deliverables_dir}/**/*.txt", recursive=True):
        with open(docx_path, "r") as f:
            content = f.read()
        await rag.ainsert(
            content,
            file_paths=[str(Path(docx_path).name)]
        )

    print(f"Deliverables from {deliverables_dir} ingested.")
```

**Recommended query patterns:**

```python
# Find reusable patterns across clients
result = await rag.aquery(
    "What reconciliation approaches have been used across client implementations?",
    param=QueryParam(mode="global")
)

# Find specific deliverable content
result = await rag.aquery(
    "Show me DEX file specifications for custodian settlement files",
    param=QueryParam(mode="hybrid")
)
```

### Workspace Isolation Strategy

Use separate workspaces to keep domain knowledge and client data isolated:

```python
# Domain knowledge base (glossary, schema, decisions)
domain_rag = LightRAG(workspace="simcorp_domain", ...)

# Client deliverables (masked)
client_rag = LightRAG(workspace="simcorp_clients", ...)

# Per-client workspace (if needed for client-specific queries)
alpha_rag = LightRAG(workspace="client_alpha", ...)
```

### Custom Knowledge Graph: SimCorp Module Relationships

Pre-populate the graph with known SimCorp module relationships:

```python
from lightrag.types import KnowledgeGraph, KnowledgeGraphNode, KnowledgeGraphEdge

kg = KnowledgeGraph()

# SimCorp modules as nodes
modules = [
    ("mod-ibor", "SimCorpModule", {"name": "Investment Book of Record", "abbr": "IBOR"}),
    ("mod-fo", "SimCorpModule", {"name": "Front Office", "abbr": "FO"}),
    ("mod-dex", "SimCorpModule", {"name": "Data Exchange", "abbr": "DEX"}),
    ("mod-dfs", "SimCorpModule", {"name": "Data Foundation Services", "abbr": "DFS"}),
    ("mod-fa", "SimCorpModule", {"name": "Fund Administration", "abbr": "FA"}),
]
for id, label, props in modules:
    kg.nodes.append(KnowledgeGraphNode(id=id, label=label, properties=props))

# Relationships
edges = [
    ("mod-dex", "mod-ibor", "FEEDS_DATA_TO"),
    ("mod-dfs", "mod-dex", "TRANSFORMS_FOR"),
    ("mod-ibor", "mod-fa", "PROVIDES_POSITIONS_TO"),
    ("mod-fo", "mod-ibor", "BOOKS_TRADES_IN"),
]
for i, (src, tgt, label) in enumerate(edges):
    kg.edges.append(KnowledgeGraphEdge(id=str(i), source=src, target=tgt, label=label))

await rag.ainsert_custom_kg(kg)
```

---

## Document Ingestion

```python
# Single document
await rag.ainsert("Text content")

# Batch insertion
await rag.ainsert(["Text 1", "Text 2", "Text 3"])

# With custom IDs
await rag.ainsert("Text", ids=["doc-123"])

# With file paths (for citation tracking)
await rag.ainsert(["Text 1", "Text 2"], file_paths=["doc1.pdf", "doc2.pdf"])

# Synchronous wrapper
rag.insert("Text content")
```

### Insertion Pipeline

1. **Chunking** — Split by token size (default 1200 tokens, 100 overlap)
2. **Entity Extraction** — LLM extracts entities and relationships from each chunk
3. **Merge** — Deduplicate entities/relations across chunks, merge descriptions
4. **Embedding** — Generate embeddings for entities, relations, and chunks
5. **Storage** — Persist to KV, vector, and graph backends

### Custom Knowledge Graph Insertion

```python
from lightrag.types import KnowledgeGraph, KnowledgeGraphNode, KnowledgeGraphEdge

kg = KnowledgeGraph()
kg.nodes.append(KnowledgeGraphNode(
    id="1", label="Organization", properties={"name": "Custodian Corp"}
))
kg.edges.append(KnowledgeGraphEdge(
    id="1", source="1", target="2", label="SETTLES_THROUGH"
))

await rag.ainsert_custom_kg(kg)
```

---

## Querying

```python
# Basic query
result = await rag.aquery("What is X?", param=QueryParam(mode="hybrid"))

# Streaming
async for chunk in await rag.aquery("What is X?", param=QueryParam(stream=True)):
    print(chunk, end="")

# Get only context (no LLM generation)
context = await rag.aquery("What is X?", param=QueryParam(only_need_context=True))

# Multi-turn conversation
param = QueryParam(
    mode="hybrid",
    conversation_history=[
        {"role": "user", "content": "Tell me about DEX settlement files"},
        {"role": "assistant", "content": "DEX settlement files are..."},
    ]
)
result = await rag.aquery("How do they relate to IBOR?", param=param)

# Synchronous wrapper
result = rag.query("What is X?", param=QueryParam(mode="hybrid"))
```

### Context Budget Control

```
MAX_ENTITY_TOKENS + MAX_RELATION_TOKENS < MAX_TOTAL_TOKENS
Chunk_Tokens = MAX_TOTAL_TOKENS - Actual_Entity_Tokens - Actual_Relation_Tokens
```

### Chunk Selection Strategies

| Method | Description |
|--------|-------------|
| `VECTOR` | Pick KG chunks by vector similarity (closer to naive retrieval) |
| `WEIGHT` | Pick KG chunks by entity and chunk weight (more KG-focused) |

Set via `KG_CHUNK_PICK_METHOD` env var. When reranking is enabled, the impact is diminished.

---

## Storage Backends

### Recommended: PostgreSQL All-in-One

For a solopreneur setup with <€200/mo cloud budget, PostgreSQL is the best choice. Single database handles all 4 storage types, easy to back up, and scales well beyond consulting-scale datasets.

```python
rag = LightRAG(
    kv_storage="PGKVStorage",
    vector_storage="PGVectorStorage",
    graph_storage="PGGraphStorage",
    doc_status_storage="PGDocStatusStorage",
)
```

**PostgreSQL .env configuration:**
```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=lightrag
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DATABASE=lightrag_simcorp
POSTGRES_MAX_CONNECTIONS=12

# Vector index (HNSW works well with voyage-finance-2's 1024 dimensions)
POSTGRES_ENABLE_VECTOR=true
POSTGRES_VECTOR_INDEX_TYPE=HNSW
POSTGRES_HNSW_M=16
POSTGRES_HNSW_EF=200

# Storage selection
LIGHTRAG_KV_STORAGE=PGKVStorage
LIGHTRAG_DOC_STATUS_STORAGE=PGDocStatusStorage
LIGHTRAG_GRAPH_STORAGE=PGGraphStorage
LIGHTRAG_VECTOR_STORAGE=PGVectorStorage
```

### Available Backends (for reference)

| Backend | KV | Vector | Graph | DocStatus | Best For |
|---------|:--:|:------:|:-----:|:---------:|----------|
| **PostgreSQL** | **x** | **x** | **x** | **x** | **All-in-one production (recommended)** |
| JSON/NetworkX/Nano | x | x | x | x | Development, testing |
| MongoDB | x | x | x | x | Document-oriented (Atlas for vector) |
| OpenSearch | x | x | x | x | All-in-one with full-text search |
| Neo4j | | | x | | Production graph queries |
| Milvus | | x | | | High-performance vector search |
| Qdrant | | x | | | Cloud-native vector search |
| Faiss | | x | | | GPU-accelerated vector search |
| Redis | x | | | x | Fast KV cache |
| Memgraph | | | x | | In-memory graph analytics |

### Workspace Isolation

Each LightRAG instance can use a `workspace` parameter for data isolation:

| Storage Type | Isolation Method |
|-------------|-----------------|
| File-based (JSON, NetworkX) | Subdirectories |
| Collection-based (Milvus, Qdrant) | Collection name prefixes |
| Relational DB (Postgres, MongoDB) | Workspace column filtering |
| Redis | Key prefixes |

---

## LLM Providers

### Anthropic (Claude) — Your Default

```python
from lightrag.llm.anthropic import anthropic_complete_if_cache, anthropic_embed

rag = LightRAG(
    llm_model_func=anthropic_complete_if_cache,
    llm_model_name="claude-sonnet-4-20250514",
    llm_model_kwargs={"max_tokens": 4096},
    embedding_func=finance_embed,  # voyage-finance-2 wrapper (see Setup)
)
```

Available model functions: `claude_3_opus_complete`, `claude_3_sonnet_complete`, `claude_3_haiku_complete`, `anthropic_complete` (generic).

Embeddings use **Voyage AI** (Anthropic has no native embeddings). Recommended: `voyage-finance-2` for your financial domain. Alternatives: `voyage-3` (general), `voyage-3-large` (best quality), `voyage-3-lite` (cost-optimized).

### Gemini (Alternative)

```python
from lightrag.llm.gemini import gemini_complete_if_cache, gemini_embed

rag = LightRAG(
    llm_model_func=gemini_complete_if_cache,
    llm_model_name="gemini-2.5-flash",
    embedding_func=gemini_embed,
)
```

### OpenAI (Alternative)

```python
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed

rag = LightRAG(
    llm_model_func=gpt_4o_mini_complete,
    embedding_func=openai_embed,
)
```

### Ollama (Local — for cost savings)

```python
from lightrag.llm.ollama import ollama_model_complete, ollama_embed

rag = LightRAG(
    llm_model_func=ollama_model_complete,
    llm_model_name="qwen3.5:9b",
    llm_model_kwargs={"options": {"num_ctx": 32768}},  # CRITICAL: Set 32k+ context
    embedding_func=ollama_embed,
)
```

**IMPORTANT**: Ollama defaults to 8k context. LightRAG requires 32k minimum. Always set `num_ctx: 32768`.

### LLM Requirements

- Minimum 32B parameters recommended
- 32KB context minimum (64KB recommended)
- Avoid reasoning models during indexing
- Stronger models for query stage than indexing stage

### Cost Management Tips (Solopreneur)

- Use `claude-sonnet-4-20250514` for both indexing and querying (best price/performance)
- Set `max_async=4` and `max_parallel_insert=2` to control API spend during ingestion
- Cache LLM responses: `ENABLE_LLM_CACHE_FOR_EXTRACT=true` in `.env`
- For bulk ingestion of large doc sets, consider Ollama locally to avoid API costs

---

## Deployment

### Recommended: Docker with PostgreSQL

For your solopreneur setup, Docker Compose is the simplest path to production:

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: lightrag_simcorp
      POSTGRES_USER: lightrag
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  lightrag:
    build: .
    env_file: .env
    ports:
      - "9621:9621"
    depends_on:
      - postgres
    volumes:
      - ./rag_storage:/app/rag_storage

volumes:
  pgdata:
```

**Estimated monthly cost:** ~€50-100 for a small VPS (2 vCPU, 4GB RAM) running both PostgreSQL and LightRAG server, well within your ~€200/mo infrastructure budget.

### API Server

```bash
# Copy and configure environment
cp env.example .env  # Edit with your LLM/embedding/storage configs

# Build WebUI (optional)
cd lightrag_webui && bun install --frozen-lockfile && bun run build && cd ..

# Run
lightrag-server                                    # Production
uvicorn lightrag.api.lightrag_server:app --reload  # Development
lightrag-gunicorn                                  # Multi-worker
```

### Interactive Setup Wizard

```bash
bash scripts/setup/setup.sh
```

Guides you through selecting LLM, embedding, storage backends, and generates your `.env` file.

### Recommended .env for Your Setup

```bash
# Server
HOST=0.0.0.0
PORT=9621
WEBUI_TITLE='SimCorp Knowledge Graph'
WORKERS=2
TIMEOUT=180

# LLM: Anthropic Claude
# Note: API server uses openai-compatible binding — use OpenRouter or a proxy for Anthropic
# For direct Python usage, use anthropic_complete_if_cache directly
LLM_BINDING=openai
LLM_BINDING_HOST=https://openrouter.ai/api/v1
LLM_BINDING_API_KEY=your_openrouter_key
LLM_MODEL=anthropic/claude-sonnet-4-20250514

# Embeddings: Voyage Finance
# Note: For API server, use Jina or OpenAI-compatible binding
# voyage-finance-2 is best used via Python API directly
EMBEDDING_BINDING=openai
EMBEDDING_BINDING_HOST=https://api.voyageai.com/v1
EMBEDDING_BINDING_API_KEY=your_voyage_key
EMBEDDING_MODEL=voyage-finance-2
EMBEDDING_DIM=1024

# Storage: PostgreSQL all-in-one
LIGHTRAG_KV_STORAGE=PGKVStorage
LIGHTRAG_DOC_STATUS_STORAGE=PGDocStatusStorage
LIGHTRAG_GRAPH_STORAGE=PGGraphStorage
LIGHTRAG_VECTOR_STORAGE=PGVectorStorage

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=lightrag
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DATABASE=lightrag_simcorp
POSTGRES_MAX_CONNECTIONS=12
POSTGRES_ENABLE_VECTOR=true
POSTGRES_VECTOR_INDEX_TYPE=HNSW

# Entity types for SimCorp domain
ENTITY_TYPES='["Organization", "Person", "SimCorpModule", "DatabaseTable", "DataExchange", "Workflow", "Configuration", "FinancialInstrument", "Concept", "Decision"]'

# Concurrency (conservative for API budget)
MAX_ASYNC=4
MAX_PARALLEL_INSERT=2

# Caching
ENABLE_LLM_CACHE_FOR_EXTRACT=true

# Reranking (optional — start without, add later for quality improvement)
RERANK_BINDING=null
```

### REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/query` | POST | Query the knowledge graph |
| `/query/stream` | POST | Streaming query |
| `/documents/text` | POST | Insert text |
| `/documents/file` | POST | Upload file |
| `/documents/batch` | POST | Batch upload |
| `/documents/paginated` | GET | List documents |
| `/graph/label/entities` | GET | Get graph entities |
| `/graph/label/relationships` | GET | Get graph relationships |
| `/health` | GET | Health check |

---

## Reranking

Reranking significantly improves retrieval quality. Use `"mix"` mode when reranker is enabled.

### Configure Reranking

```bash
# In .env
RERANK_BINDING=cohere        # cohere, jina, aliyun, or null
RERANK_MODEL=BAAI/bge-reranker-v2-m3
RERANK_BINDING_HOST=http://localhost:8000/rerank
RERANK_BINDING_API_KEY=your_key
MIN_RERANK_SCORE=0.0         # 0.0 keeps all, 0.6+ for weaker LLMs
```

Recommended models: `BAAI/bge-reranker-v2-m3`, Jina rerankers, Cohere `rerank-v3.5`.

---

## Evaluation

LightRAG integrates RAGAS for RAG quality assessment.

```bash
pip install lightrag-hku[observability]
```

Configure evaluation LLM/embedding in `.env`:
```bash
EVAL_LLM_MODEL=gpt-4o-mini
EVAL_EMBEDDING_MODEL=text-embedding-3-large
EVAL_MAX_CONCURRENT=2
```

### Langfuse Tracing

```bash
LANGFUSE_SECRET_KEY="..."
LANGFUSE_PUBLIC_KEY="..."
LANGFUSE_HOST="https://cloud.langfuse.com"
LANGFUSE_ENABLE_TRACE=true
```

---

## Troubleshooting

### 1. Storage Not Initialized
**Error**: `AttributeError: __aenter__` or `KeyError: 'history_messages'`
**Fix**: Always call `await rag.initialize_storages()` after creating the LightRAG instance.

### 2. Embedding Model Changes
When switching embedding models, you MUST clear the data directory (except optionally `kv_store_llm_response_cache.json`).

### 3. Nested Embedding Functions
**Error**: Wrapping already-decorated embedding functions fails.
**Fix**: Use `.func` to access the underlying function:
```python
# WRONG: EmbeddingFunc(func=anthropic_embed)
# RIGHT: EmbeddingFunc(func=anthropic_embed.func)
```

### 4. Ollama Context Length
Ollama defaults to 8k context. LightRAG requires 32k+.
```python
llm_model_kwargs={"options": {"num_ctx": 32768}}
```

### 5. Anthropic Embeddings
Anthropic doesn't provide native embeddings. The `anthropic_embed` function uses **Voyage AI**. Set `VOYAGE_API_KEY`. For your financial domain work, wrap with `voyage-finance-2` (see Setup section).

### 6. PostgreSQL Connection Issues
If using Docker, use `postgres` (service name) as host, not `localhost`. Ensure `pgvector` extension is installed (use `pgvector/pgvector:pg16` image).

### 7. Data Masking Before Ingestion
When ingesting client deliverables, always run through your `data_masker.py` first to replace real client names with codenames. LightRAG's knowledge graph will connect masked entities — use the same codename registry to keep references consistent.

---

## Testing

```bash
# Default: runs only offline tests
pytest tests

# Integration tests (requires external services)
pytest tests --run-integration
# Or: LIGHTRAG_RUN_INTEGRATION=true pytest tests

# Keep test artifacts for debugging
pytest tests --keep-artifacts

# Configure test workers
pytest tests --test-workers 4
```

### Linting

```bash
ruff check .
```

---

## References

| Topic | File |
|-------|------|
| Algorithm Deep-Dive | `references/algorithm.md` |
| Docker Deployment | `references/docker-deployment.md` |
| Frontend Build Guide | `references/frontend-build.md` |
| Interactive Setup | `references/interactive-setup.md` |
| Concurrency Explained | `references/concurrency.md` |
| Milvus Configuration | `references/milvus-config.md` |
| Offline Deployment | `references/offline-deployment.md` |
| Environment Variables | `references/env-example.md` |
| Anthropic LLM Source | `references/llm-anthropic.py` |
| OpenAI Demo | `references/demo-openai.py` |
| Gemini Demo | `references/demo-gemini.py` |
| Gemini + Postgres Demo | `references/demo-gemini-postgres.py` |
| Ollama Demo | `references/demo-ollama.py` |
| Rerank Example | `references/demo-rerank.py` |
| Custom KG Insertion | `references/demo-insert-custom-kg.py` |
| Graph Visualization | `references/demo-graph-visual.py` |
