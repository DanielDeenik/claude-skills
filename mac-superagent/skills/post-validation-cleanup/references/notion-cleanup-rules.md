# Notion structure cleanup ruleset

Source of truth for the cluster IA: `feedback_kb_routing_rules.md` in memory.

## The 6-cluster IA (at SimCorp KB root)

| Cluster | Purpose | Typical pages |
|---------|---------|---------------|
| REF | Static reference — code tables, AIM data dictionary, lexicons | Field catalogues, taxonomy reference, code table inventories |
| ARCH | Architecture & design — Solution Architecture §18, schemas, ER diagrams | NWM PKR/KRM v3, sc_model, AKG architecture |
| FLOW | Capital + data flow — day-in-the-life, intake → setup → ops → exit | Private Capital Data Process Flow, NWM Daily Chain, decomposition runbook |
| TRAIN | Training materials — guides, decks, lifecycle phases | §18.22 Alts Training Hub, §18.25 Verticals × Phases |
| IMPL | Implementation tracking — boards, test cases, run-books | PD Test Cases, BRM Rules Catalogue, Implementation PM Board |
| GOV | Governance — sign-offs, decisions, escalations, Q&A Log | Q&A Log, SME Gates tracker |
| ARCHIVE | Retired / superseded | Old drafts, retired skills, Q&A Log entries already promoted to Wiki |

Every page **must** attach to one of the 7 clusters. Root-level pages
outside this taxonomy are anomalies.

## Categories — what counts as redundant in Notion

### Category N1 — Orphan root pages
**Rule:** a page directly under the SimCorp KB root whose `parent` is not
one of the 7 cluster pages is an orphan. Flag with a proposed re-home.

**Audit:** `notion-search` with empty query against the KB workspace, then
for each top-result, fetch and check its parent.

### Category N2 — Duplicate titles
**Rule:** any two pages with identical normalized titles
(case-insensitive, trimmed, hyphen/space-equivalent) are candidates for
merge. Keep the one with later `last_edited_time` AND more content; archive
the other after copy-over verification.

**Examples:** two pages both titled "NWM PE Mapping" created in different
sessions; "Day in the Life" appearing twice.

### Category N3 — Q&A Log entries already promoted
**Rule:** Q&A Log entries (DB `33d7772fa7ae81daa22fc4641db97fa5` per
`project_notion_pipeline.md`) with `Status = Wiki Promoted` and
`Last edited > 30 days ago` → archive. Their content already lives in the
Wiki; the log entry is historical only.

### Category N4 — Drafts whose final is published
**Rule:** pages with `(draft)`, `WIP`, `v1`, `v2` in the title where a
later version exists. Same `mtime` + content threshold as Category N2.

### Category N5 — Empty stubs
**Rule:** pages with `< 50 characters` of content (excluding title) that
haven't been edited in `> 14 days`. Likely abandoned outlines. Flag.

## NEVER auto-flag

- Pages under the active Solution Architecture master page
  `33d7772fa7ae81daa22fc4641db97fa5` and its 12 module sub-pages
- The Wiki, Q&A Log, and Deliverables databases themselves (only their entries
  per the rules above)
- Any page Dan tagged "pin" or "keep" via a tag property
- Pages with active comments from anyone other than Dan or Claude
- Pages linked to from a Notion view or dashboard that's still active

## Stage 1 action — Archive, not delete

For every flagged page Dan approves:
1. `notion-update-page` with `archived: true`
2. Add a property `archive_reason` if the page schema supports it; otherwise
   prepend the reason to the page body
3. Record the page ID, URL, archive timestamp, and reason in the cleanup
   manifest

Notion's archive is reversible from the Notion UI. Hard delete only happens
at Stage 2 after 7 days untouched.

## Stage 2 action — Hard delete

If the Notion API/MCP cannot permanently delete archived pages, the Stage 2
sweep escalates to Dan with the list of pages that hit the 7-day mark, with
a one-click "delete from trash" link to each. Do not attempt aggressive
workarounds.

## Reporting format

Per candidate:
```
{
  "page_id": "...",
  "title": "...",
  "url": "https://notion.so/...",
  "last_edited": "2026-04-15",
  "category": "N1 | N2 | N3 | N4 | N5",
  "reason": "human-readable why",
  "merge_target": "..."  // for N2 only
}
```
