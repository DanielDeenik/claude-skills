# Rowboat Architecture Reference

Complete analysis of the Rowboat open-source codebase (github.com/rowboatlabs/rowboat)
for use as architectural reference when building knowledge graph features.

---

## Project Structure

```
rowboat/
├── apps/x/                          # Primary Electron desktop app
│   ├── apps/
│   │   ├── main/                   # Electron main process (Node.js backend)
│   │   ├── renderer/               # React UI (Vite + TailwindCSS)
│   │   └── preload/                # Context bridge (IPC security)
│   ├── packages/
│   │   ├── shared/                 # Types (agents, runs, MCP, workspace)
│   │   └── core/                   # Business logic (107 TypeScript files)
│   │       ├── knowledge/          # Knowledge graph building (27 files)
│   │       ├── agents/             # Agent runtime & execution
│   │       ├── runs/               # Run management (execution logs/state)
│   │       ├── mcp/                # Model Context Protocol integration
│   │       ├── composio/           # Composio tool orchestration
│   │       ├── pre_built/          # Scheduled agents
│   │       ├── models/             # LLM provider abstraction
│   │       ├── voice/              # Voice input/output
│   │       └── application/lib/    # Tool execution, command parsing
```

## Knowledge Graph Implementation

### Entity Model
All entities as markdown with YAML frontmatter. Types: People, Organizations,
Projects, Topics, Meetings.

### Indexing
- PersonEntry: file, name, email?, aliases[], organization?, role?
- OrganizationEntry: file, name, domain?, aliases[]
- ProjectEntry: file, name, status?, aliases[]
- TopicEntry: file, name, keywords[], aliases[]
- Index rebuilt from markdown on each graph build (no database)

### Change Detection
State file: `~/.rowboat/knowledge_graph_state.json`
- processedFiles: map of path → {mtime, SHA256 hash, lastProcessed}
- Hybrid: fast mtime check → hash verification on change

### Processing
- Batch size: 10 files per batch
- Full index rebuild after each batch
- Entity extraction via LLM from new/changed files

## Agent Runtime

### Execution Flow
```
User Message → MessageQueue → AgentRuntime.trigger()
  → Load Agent Definition (YAML frontmatter + markdown instructions)
  → Build LLM Prompt (system + knowledge index + history + tools)
  → LLM Response (Vercel AI SDK, streaming)
  → Tool Calls? → Execute via execTool() → Feed back
  → Final Response + RunEvent[] log
```

### Agent Definition Format
```yaml
---
model: gpt-4-turbo
tools:
  workspace-readFile: { type: builtin }
  web-search: { type: mcp, mcpServerName: exa }
  linear: { type: composio, apiName: linear }
---
# Instructions (markdown)
```

### Built-in Tools (40+)
- workspace-*: File I/O, directory traversal, grep, glob
- skill-load: Fetch skill instructions into context
- mcp-call: Generic MCP tool invocation
- ask-human: Request user input

### Run Management
- FSRunsRepo: Persist runs as JSON files
- Bus: In-memory pub-sub for run events
- AbortRegistry: Graceful (SIGTERM) + force (SIGKILL) abort
- RunsLock: Prevent concurrent run modifications

## Key Design Decisions

1. **Local-first**: All data on user's machine, no cloud unless opted in
2. **Obsidian-compatible**: Standard markdown with [[backlinks]]
3. **Index in prompt**: Entire knowledge index formatted as text in LLM context
4. **Batch processing**: 10-file batches with full index rebuild
5. **Event-driven runs**: Pub-sub bus for real-time UI streaming
6. **Tool attachment abstraction**: Agents reference tools by name, resolved at runtime
7. **Agent notes hierarchy**: Separate directory for agent-written metadata
8. **Permission model**: Explicit tool permissions with always-allow caching
9. **Dependency injection**: Awilix IoC container for testability
10. **Dual tool frameworks**: MCP (open) + Composio (SaaS) simultaneously

## Tech Stack
- Desktop: Electron 39 + React 19 + Vite 7 + TailwindCSS 3
- LLM: Vercel AI SDK (Anthropic, OpenAI, Google, Ollama)
- MCP: @modelcontextprotocol/sdk 1.25.1
- Git: isomorphic-git (pure JS)
- File watching: chokidar 4.x
- Scheduling: cron-parser 5.5.0
- PDF: @react-pdf/renderer 4.3.2
- DI: Awilix 12.x

## Limitations to Avoid
- No vector search (text-based index only) — consider adding for scale
- Index-in-prompt doesn't scale past ~5K entities — need hierarchical indexing
- Batch processing is O(n) with vault size — incremental is critical
- Single-device only — no multi-user collaboration
- Sequential agent runs — parallelize independent agents
