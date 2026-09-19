# RAG Gate Protocol (Hard Fail)

This protocol is mandatory for every invocation of `simcorp-super-agent`. It
exists because the AKG persistent RAG has already ingested 13,853 source
citations across 124 decomposition-related sources plus the full Nicola
corpus. Re-reading those sources instead of querying the RAG costs time,
burns context, and causes the agent to drift from prior synthesised answers.

## The Rule

Before any file read, any answer draft, any deliverable production, or any
Notion write: invoke the gate.

```bash
python3 scripts/rag_gate.py --query "<keywords>"
```

Paste the returned `<rag-gate ...>` token block at the top of your response —
before any other content. This is the audit trail that proves the gate ran.

## When to Gate

Gate when any of the following is true:

- The user asks a SimCorp factual question (config, formula, module, field, SGC,
  batch job, profile, code table).
- The user asks about a Nicola client configuration, deliverable, or workflow.
- The user asks to produce a solution document, Wiki page, or other deliverable.
- The user asks to process the Notion Q&A inbox or promote to Wiki.
- The user asks a question whose answer could already be in prior synthesised work
  (solution docs, configuration documents, prior meeting transcripts).

## When to Skip

Skip the gate only when:

- The request is pure UI / chat (for example, greetings, meta-questions about
  the skill itself, questions about the conversation history).
- The request explicitly asks for content unrelated to SimCorp (for example, an
  off-topic aside).
- The user has already pasted the full source content inline and the task is
  purely to transform it (for example, "reformat this text as a table").

When in doubt, gate. A gate call is cheap; a duplicated solution document is
expensive.

## Token Format

The gate emits a token block of the form:

```
<rag-gate id="gate_YYYYMMDD_HHMMSS_XXXX" hits="N">
  query: "<the keywords searched>"
  db: akg.duckdb.cowork
  top_sources:
    - [tier N] <source name> (K hits)
    - ...
</rag-gate>
```

Paste this verbatim at the top of your response. Do not paraphrase it. Do not
fabricate a token without invoking the script — the gate logs every real
invocation to `~/.auto-memory/rag_gate.log.jsonl` for audit.

## Failure Modes

### hits = 0 (RAG-EMPTY)

The keywords did not match anything in the corpus. Possible reasons:

- The keywords are too specific (try shorter or reworded query).
- The topic is genuinely new and not yet ingested (for example, today's meeting
  transcript has not been added to the AKG).
- The corpus is misconfigured or the wrong DB file was opened.

Before proceeding, you MUST:

1. Retry with broader or alternative keywords (at least one retry).
2. If still zero, declare `RAG-EMPTY` in the response and state explicitly why
   you are proceeding to read source files or produce an answer without RAG
   grounding.
3. If the topic is legitimately new, flag for ingestion into AKG by noting:
   "This content is not yet in AKG — recommend ingestion after this session."

### gate script errors

If the gate script fails (DuckDB not installed, DB path not found, etc.):

1. Install dependencies if missing: `pip install duckdb --break-system-packages`.
2. Set `AKG_DB_PATH` environment variable to point at the populated DB.
3. On the Cowork VM, the canonical path is
   `/sessions/<session-id>/mnt/a. Consulting - SimCorp/akg/data/akg.duckdb.cowork`.
4. On the Mac, the canonical path is `~/Documents/GitHub/akg/data/akg.duckdb`
   (per the `feedback_run_from_github` memory rule: run from the GitHub clone,
   not the iCloud workspace).

Do not proceed if the gate cannot be invoked. Escalate to Dan for resolution.

### Fabricating a token

Do not invent a gate token. The log file is auditable. Fabricated tokens break
trust and corrupt the audit trail. If the gate cannot run, follow the escalation
path above.

## Post-Gate Behaviour

Once the gate returns:

1. **If hit_count > 0 AND a top source is a prior solution document**
   (for example, `Nicola_SAAM_TAA_Decomposition_Solution_Document.docx`,
   `NWM - Solution document - Lookthrough and Decomposition v2.docx`,
   `NWM - Configuration Document - Core Decomposition_V1.pdf`): link to that
   document in your response and build on it. Do not re-derive what is already
   written.

2. **If hit_count > 0 AND sources are vendor manuals only** (tier 1): the
   canonical definition is in a vendor doc. Cite the specific vendor source
   alongside any Nicola-specific divergence.

3. **If hit_count > 0 AND sources include prior meeting transcripts** (tier 4
   filenames ending with `-Meeting Recording-en-US.docx`): the answer likely
   includes verbatim client guidance. Pull the transcript passage before
   synthesising.

4. **If hit_count = 0**: follow the RAG-EMPTY protocol above.

## Interaction with Sister Skills

- `simcorp-extraction` also follows this gate. An extraction design that repeats
  prior DEX work is the most expensive kind of duplicated work. Gate first.
- `simcorp-notebooklm-bridge` uses the gate output as the seed for NotebookLM
  briefs. Pass top_sources to NotebookLM as the starting reading list.
