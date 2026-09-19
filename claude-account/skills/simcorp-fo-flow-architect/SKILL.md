---
name: simcorp-fo-flow-architect
description: Build front office flow architecture packs for SimCorp Dimension with measured data overlays that show where time is actually spent. Covers the full FO flow set (data preparation, simulation to order, order lifecycle and auxiliary jobs, compliance validation, rebalancing, extraction and feeds, transaction processing and matching, cash management). Every diagram node must trace to a named manual section and every overlay number to an admissible evidence file; anything else is refused or marked NOT MEASURED. Produces a self contained HTML architecture pack and a PPTX deck in the Nicola theme. Use when asked to map an FO flow, overlay performance results on an architecture, locate a bottleneck, or extend the measured flow set.
---

# SimCorp FO Flow Architect

Turns manuals plus measured results into architecture flow diagrams with data
overlays that show bottlenecks. Two hard rules govern everything: structure
comes only from SimCorp manuals or verified client config, and overlay numbers
come only from admissible evidence files. Nothing is invented to fill a gap;
gaps are printed as NOT MEASURED.

## Before anything else

1. Read project memory. Recall the flow, prior captures and settled findings
   before rebuilding anything. The 19 August 2026 order test baselines live in
   project_order_perf_test_2026_08_19 and the 31 July order workflow model in
   project_wealth_order_workflow_steps_2026_08_10.
2. Read `references/evidence_contract.md` and refuse any evidence source not
   listed there.
3. Read `references/flow_catalogue.md` and work only on flows it defines. A new
   flow enters the catalogue only with a manual citation.

## Method, five phases in order

**Phase 1, recall.** Grep MEMORY.md for the flow name and any uploaded file
signature. Never re-derive a settled finding.

**Phase 2, ground the structure.** Every node and edge in the diagram carries a
source tag: manual section (for example amsim 3.7, auxjob 2.3, dataextr 3),
verified client config object (CEI, extraction definition, batch job group), or
a screenshot Dan supplied. If a step cannot be tied to one of these, it does not
appear as a node; it may appear in an Open Questions list.

**Phase 3, ingest evidence.** Parse the admissible files per the contract.
Reconcile counts before using them (register rows vs log order counts vs
allocated number ranges). Log every reconciliation gap; never average it away.

**Phase 4, overlay.** Apply `references/overlay_method.md`. Separate the fixed
cost of an operation from the marginal cost per additional item. Attribute time
to a node only when the log names that node. Unattributed time is shown as its
own labelled band, never spread across nodes.

**Phase 5, render.** Build the HTML pack per `references/render_html.md`, then
the deck per `references/render_pptx.md`. Both are generated from the same
grounded model file so they can never disagree.

## Outputs

One HTML architecture pack per flow (inline SVG diagram, overlay view, evidence
register, NOT MEASURED list, open questions) and one PPTX deck in the Nicola
theme. File names follow `NWM_FO_Flow_<FlowKey>_<YYYY-MM-DD>` and land in
`i. Client - Nicola Wealth/Performance Testing/` unless Dan names a location.

## Hard prohibitions

No fabricated timings, node names, service names or field names. No dashes,
middots, arrows or maths glyphs in any generated text; grep for the banned set
before shipping. No averaging across runs with different log note formats. No
treating a Rules=0 compliance validation as evidence about the compliance
engine under load. Do not claim a cause for a timing difference measured only
once; raise it as an open question instead.

## Scope boundary

This skill maps flows and overlays measured results. Oracle level diagnosis
belongs to simcorp-database-tracing and simcorp-performance-toolkit. Business
impact labelling of tickets belongs to simcorp-performance-specialist. DEX
design validation belongs to simcorp-dex-validator. Comm Server internals
belong to simcorp-comm-server.
