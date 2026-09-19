---
name: simcorp-notebooklm-bridge
description: >
  Notion-as-data-bus hand-off between NotebookLM (research synthesis brain) and
  Claude in Cowork (action brain) for SimCorp consulting work. NotebookLM holds
  large multi-doc corpora and produces synthesis; Claude in Cowork holds MCP tools
  and ships extractions, Wiki pages, and solution docs. They cannot talk directly,
  so Notion is the neutral middle layer both can read and write. Defines three
  hand-off protocols (NLM→Claude, Claude→NLM, Wiki bidirectional sync) using three
  Notion surfaces (Q&A Log, Wiki, Solution Architecture). Sister to
  simcorp-super-agent (Q&A) and simcorp-extraction (extraction design).
  Trigger on: NotebookLM, NLM hand-off, NotebookLM bridge, NotebookLM brief,
  research synthesis, paste research into Notion, push brief to NotebookLM, Notion
  data bus, research-to-action hand-off, multi-corpus research, SimCorp source
  document research.
---

# SimCorp NotebookLM Bridge

Notion-as-data-bus hand-off between NotebookLM and Claude in Cowork for SimCorp work.
Use this skill whenever the user wants to move research synthesis from NotebookLM
into action work in Claude, or send Claude's findings into a NotebookLM research
brief, or sync Wiki content bidirectionally.

For Q&A inside Cowork, use `simcorp-super-agent`. For extraction design, use
`simcorp-extraction`. This skill is **only** about the hand-off mechanics.

---

## Why a Bridge

- NotebookLM has no public ingest/export API
- NotebookLM cannot call MCP tools, write files, or push to Notion
- Claude in Cowork cannot ingest the same multi-document corpus NotebookLM holds
- Email / Slack / files all fail one of: structured, persistent, MCP-readable,
  human-editable

**Notion is the only channel that satisfies all four constraints.** It is already
the system of record for SimCorp Wiki and Q&A — adding another bus would fragment
the knowledge graph.

---

## The Three Notion Surfaces

| Surface | Direction | Purpose |
|---------|-----------|---------|
| **Q&A Log** | Bidirectional | Inbound research from NotebookLM, outbound briefs from Claude |
| **Wiki** | Bidirectional | Validated long-term knowledge, either brain can author |
| **Solution Architecture** | Read-only | Structural truth (12 module sub-pages + master) both brains agree on |

Solution Architecture parent: `33d7772fa7ae812c8c44cc10fb0b3144`. Master:
`33d7772fa7ae81daa22fc4641db97fa5`. Updated only when SCDAT schema changes.

---

## Protocol A — NotebookLM → Claude (Research → Action)

1. NotebookLM produces a research synthesis on a SimCorp topic
2. Dan copies the synthesis text + cited source list
3. Dan creates a new Q&A Log entry: Question = original prompt, Source = "NotebookLM",
   Body = synthesis + sources, Status = "New"
4. Claude polls Q&A Log via `notion-query-database-view`
5. Claude runs the appropriate action skill (`simcorp-super-agent` for Q&A,
   `simcorp-extraction` for extraction design) against the synthesis
6. Claude writes final answer/extraction back to the same Q&A entry, sets
   Status = "Answered"
7. On human approval, Status → "Validated", Claude promotes to Wiki

## Protocol B — Claude → NotebookLM (Action → Research)

1. Claude hits a gap during work — a question the GraphRAG layer can't resolve
   from Solution Architecture alone
2. Claude creates Q&A entry: Source = "Claude-Cowork", Status = "Needs Research",
   Body = brief (what's known, what's missing, which source docs to investigate)
3. Dan opens NotebookLM, pastes the brief + relevant source PDFs
4. NotebookLM produces a synthesis
5. Dan pastes synthesis back into the same Q&A entry, sets
   Status = "Research Complete"
6. Claude picks it up and completes the work

## Protocol C — Wiki Bidirectional Sync

- Either brain authors a Wiki page in Status = "Draft - NotebookLM" or
  "Draft - Claude-Cowork"
- The other reads it via standard Wiki query path
- Promotion to Status = "Validated" requires human review
- History field tracks which brain authored which version

---

## Status Field as Lock

Only one brain works on a Q&A entry at a time. Status field is the lock:

- `New` → NotebookLM just delivered, Claude can pick up
- `In Progress` → Claude working
- `Needs Research` → Claude bounced to NotebookLM
- `Research Complete` → NotebookLM bounced back
- `Answered` → Claude finished, awaiting human review
- `Validated` → Human approved, eligible for Wiki promotion

---

## Failure Modes and Mitigations

| Failure | Cause | Mitigation |
|---------|-------|------------|
| Claude re-answers a covered question | Wiki not searched first | Always search Wiki at start of every workflow |
| Contradictory answers from both brains | No lock on the entry | Status field acts as lock; one brain at a time |
| Citations lost in copy/paste | Dan forgot source list | Q&A template enforces non-empty Sources field |
| Solution Architecture drifts from reality | SCDAT changes, no update | Quarterly re-ingest of Field_Mapping_Reference + ER diagrams |
| Wiki bloat from duplicate drafts | Both brains author overlapping topics | Search before drafting; edit existing rather than create |

---

## Required Habits (Both Sides)

**Dan (mediating between tools):**
- Always copy the cited source list when moving NotebookLM output into Notion
- Always set the Source field correctly so the other brain knows the origin
- Always change Status when handing off

**Claude (in Cowork):**
- Always search Wiki first (no duplicate research)
- Always check Q&A Log for `Source = NotebookLM` and `Status = Research Complete`
  at session start
- Always include Sources field in any Q&A or Wiki write

---

## What This Skill Does NOT Do

- Does NOT call NotebookLM directly (no API)
- Does NOT design extractions (use `simcorp-extraction`)
- Does NOT answer SimCorp config questions (use `simcorp-super-agent`)
- Does NOT bypass human review

---

## Reference

- `references/notebooklm-bridge.md` — Full bridge documentation with rationale,
  failure modes, and protocol detail
