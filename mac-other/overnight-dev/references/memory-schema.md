# Memory Schema — Knowledge Graph Entity and Relationship Format

## Directory Structure

```
memory/
  graph/
    entities/
      modules/          — MODULE entities (one JSON per module)
      decisions/        — DECISION entities
      corrections/      — CORRECTION entities
      patterns/         — PATTERN entities
      failures/         — FAILURE entities
      personas/         — PERSONA templates (reusable)
      backlog-items/    — BACKLOG_ITEM entities (linked to Notion)
    relationships/
      index.json        — Master relationship index
    index.json          — Full entity index (type → id → file path)
  session-log/
    {date}.json         — Per-cycle session logs
  sync-state.json       — Last Notion sync timestamp + state
```

## Entity Format

Every entity is a JSON file with this base structure:

```json
{
  "id": "entity-uuid",
  "type": "MODULE | DECISION | CORRECTION | PATTERN | FAILURE | PERSONA | BACKLOG_ITEM",
  "title": "Human-readable title",
  "created": "2026-04-06T00:00:00Z",
  "updated": "2026-04-06T00:00:00Z",
  "source": "dan-correction | agent-discovery | build-review | cycle-learning | bootstrap",
  "tags": ["database", "collector", "retry"],
  "priority": "blocking | high | normal | low",
  "status": "active | archived | superseded",
  "notion_id": "notion-page-id or null",
  "content": {}
}
```

### MODULE Entity

```json
{
  "type": "MODULE",
  "title": "collectors/reddit.py",
  "content": {
    "description": "Reddit signal collector using PRAW library",
    "purpose": "Collects social signals from Reddit subreddits for analysis",
    "interface": "Inherits BaseCollector, implements collect() → list[Signal]",
    "dependencies": ["praw", "BaseCollector", "Signal model"],
    "file_path": "src/collectors/reddit.py",
    "key_classes": ["RedditCollector"],
    "key_functions": ["collect", "parse_submission", "rate_limit_handler"],
    "notes": "Rate limited to 60 requests/minute by Reddit API"
  }
}
```

### DECISION Entity

```json
{
  "type": "DECISION",
  "title": "Use tenacity for retry logic",
  "content": {
    "decision": "All retry logic must use the tenacity library with exponential backoff",
    "rationale": "Consistency across collectors, well-tested library, configurable",
    "context": "Discussed during Twitter collector timeout incident",
    "constraints": [
      "Max 3 retry attempts",
      "Exponential backoff starting at 1 second",
      "Never retry on auth errors (401, 403)",
      "Only retry on transient errors (429, 500, 502, 503)"
    ],
    "alternatives_considered": [
      "Custom retry decorator — rejected: reinventing the wheel",
      "No retries — rejected: too many transient failures in production"
    ],
    "supersedes": null
  }
}
```

### CORRECTION Entity

```json
{
  "type": "CORRECTION",
  "title": "Never use bare except clauses",
  "priority": "blocking",
  "content": {
    "correction": "Never use `except:` or `except Exception:` — always catch specific exceptions",
    "what_was_wrong": "Build agent wrote `except:` in collector error handling",
    "what_to_do_instead": "Catch specific exceptions: `except requests.ConnectionError:`, `except TimeoutError:`, etc.",
    "example_wrong": "try: ... except: logger.error('failed')",
    "example_right": "try: ... except requests.ConnectionError as e: logger.error('Connection failed', exc_info=e)",
    "applies_to": ["all modules"],
    "dan_said": "Don't use bare excepts. Always catch specific exceptions so we know what actually went wrong."
  }
}
```

### PATTERN Entity

```json
{
  "type": "PATTERN",
  "title": "Configuration approach",
  "tags": ["universal", "config", "no-hardcoding"],
  "priority": "blocking",
  "content": {
    "description": "How configuration values are handled in this project",
    "rules": [
      "All environment-specific values come from environment variables",
      "Use pydantic Settings classes for config validation",
      "Provide sensible defaults for all non-secret config",
      "Secrets have no defaults — fail fast if missing",
      "Config is loaded once at startup and injected, not read inline"
    ],
    "example": {
      "wrong": "url = 'https://api.reddit.com/v1'",
      "right": "url = settings.reddit_api_url  # from env var REDDIT_API_URL"
    },
    "files": ["src/config.py", "src/settings.py"]
  }
}
```

### FAILURE Entity

```json
{
  "type": "FAILURE",
  "title": "Twitter collector timeout — hardcoded values",
  "content": {
    "what_happened": "Overnight agent built Twitter collector with hardcoded 5-second timeout. Production Twitter API sometimes takes 10+ seconds. Collector failed silently.",
    "root_cause": "Implementer subagent hardcoded timeout=5 instead of using config",
    "modules_affected": ["collectors/twitter.py"],
    "how_detected": "Quality reviewer missed it. Dan found it in morning review.",
    "resolution": "Moved timeout to config with 30-second default",
    "prevention": [
      "Quality reviewer must scan for ALL hardcoded numbers",
      "Implementer persona must include configuration pattern in memory",
      "Add specific test: assert no numeric literals in collector code"
    ],
    "date_occurred": "2026-04-01"
  }
}
```

### PERSONA Entity (Reusable Templates)

```json
{
  "type": "PERSONA",
  "title": "Database Specialist Implementer",
  "content": {
    "expertise_domains": ["database", "sqlalchemy", "orm", "migrations"],
    "relevant_patterns": ["database-conventions", "configuration-approach"],
    "relevant_corrections": ["no-raw-sql", "no-bare-except"],
    "behavioral_traits": [
      "Always uses ORM, never raw SQL",
      "Tests with fixtures and test databases, not mocks",
      "Paranoid about data integrity — adds constraints",
      "Checks for index usage on queries"
    ],
    "coding_style": "Defensive, well-typed, comprehensive error handling"
  }
}
```

### BACKLOG_ITEM Entity

```json
{
  "type": "BACKLOG_ITEM",
  "title": "Add retry logic to Reddit collector",
  "content": {
    "notion_page_id": "abc123",
    "status": "Done",
    "priority": "P1",
    "build_history": [
      {
        "cycle_date": "2026-04-06",
        "outcome": "success",
        "review_rounds": 2,
        "implementer_persona": "Backend Engineer (Collector Specialist)",
        "key_learnings": ["Reddit rate limit headers need special parsing"],
        "entities_created": ["pattern-reddit-rate-limiting"]
      }
    ],
    "modules_touched": ["collectors/reddit.py", "config.py"]
  }
}
```

## Relationship Index Format

`memory/graph/relationships/index.json`:

```json
{
  "relationships": [
    {
      "from": "module-reddit-collector",
      "to": "pattern-configuration",
      "type": "uses",
      "created": "2026-04-06T00:00:00Z"
    },
    {
      "from": "module-reddit-collector",
      "to": "decision-tenacity-retry",
      "type": "governed-by",
      "created": "2026-04-06T00:00:00Z"
    },
    {
      "from": "correction-no-bare-except",
      "to": "module-reddit-collector",
      "type": "applies-to",
      "created": "2026-03-28T00:00:00Z"
    },
    {
      "from": "failure-twitter-timeout",
      "to": "module-twitter-collector",
      "type": "occurred-in",
      "created": "2026-04-01T00:00:00Z"
    },
    {
      "from": "failure-twitter-timeout",
      "to": "pattern-configuration",
      "type": "prevented-by",
      "created": "2026-04-01T00:00:00Z"
    }
  ]
}
```

## Entity Index Format

`memory/graph/index.json`:

```json
{
  "last_updated": "2026-04-06T00:00:00Z",
  "entity_count": 47,
  "relationship_count": 89,
  "entities": {
    "MODULE": {
      "module-reddit-collector": "entities/modules/reddit-collector.json",
      "module-twitter-collector": "entities/modules/twitter-collector.json"
    },
    "DECISION": {
      "decision-tenacity-retry": "entities/decisions/tenacity-retry.json"
    },
    "CORRECTION": {
      "correction-no-bare-except": "entities/corrections/no-bare-except.json"
    }
  }
}
```

## Session Log Format

`memory/session-log/{date}.json`:

```json
{
  "cycle_date": "2026-04-06",
  "cycle_type": "full",
  "started": "2026-04-06T00:00:00Z",
  "completed": "2026-04-06T04:15:00Z",
  "phases": {
    "remember": {"status": "success", "entities_synced": 5},
    "collect": {"status": "success", "signals": 142, "theses": 3},
    "discover": {"status": "success", "items_proposed": 2},
    "build": {
      "status": "success",
      "items_attempted": 4,
      "items_completed": 3,
      "items_blocked": 1,
      "details": [
        {
          "title": "Add retry logic to Reddit collector",
          "outcome": "success",
          "review_rounds": 2,
          "time_elapsed_minutes": 28
        }
      ]
    },
    "optimize": {"status": "success", "improvement": "Removed dead import in pipeline.py"},
    "brief": {"status": "success", "notion_page_id": "xyz789"}
  },
  "graph_changes": {
    "entities_created": 5,
    "entities_updated": 3,
    "relationships_created": 8
  }
}
```

## Sync State Format

`memory/sync-state.json`:

```json
{
  "last_sync": "2026-04-06T00:00:00Z",
  "notion_db_id": "agent-knowledge-db-id",
  "entities_in_notion": 42,
  "pending_push": [],
  "pending_pull": []
}
```

## Bootstrapping (First Run)

When no graph exists yet:

1. Create directory structure
2. Scan codebase files → generate MODULE entities for each significant file
3. Read existing code → generate PATTERN entities for observed conventions
4. Create CORRECTION: "No hardcoded values" (blocking, applies-to all)
5. Read README, docs, architecture notes → generate DECISION entities
6. Build relationships based on imports, class inheritance, module dependencies
7. Create index files
8. Create Notion Agent Knowledge DB
9. Push all entities to Notion
10. Save sync state
