# HTML architecture pack template

One self contained HTML file per flow. No external assets, no scripts required
for reading; everything inline. Sections in order:

1. Header: flow key and name, capture date, environment, evidence files used.
2. Architecture diagram: inline SVG, layered left to right in swimlanes:
   User and client machine, Dimension services, Batch and auxiliary, Database
   and extraction targets. Nodes are rounded rectangles with the source tag
   printed small under the node name (for example "amsim 3.7"). Edges carry
   event or data names from the evidence, never invented labels.
3. Overlay view: the same skeleton repeated with the colour ramp applied and a
   figure block per measured node (fixed cost, marginal cost, runs, records).
   Differences between phases shown by a rule bar under the node, not by
   changing the skeleton.
4. Evidence register: one table row per source file with row counts, window,
   machines seen, and the reconciliation results.
5. NOT MEASURED list: every node with no admissible evidence.
6. Open questions: numbered, each ending in what answer is needed.

## Theme tokens (Nicola document theme, fixed)

NAVY #1E2761 structure and headings. INK #3A3A4A body text. GOLD #A66E08
accents on white. ICE #CBD5EC light fills. Overlay ramp: ICE #CBD5EC to GOLD
#C8860A to amber #8A5A06. NOT MEASURED: #FFFFFF fill, #9AA3B5 dashed outline.
EMPTY PATH: diagonal hatch #CBD5EC on white. Calibri with Arial fallback.

## Layout rules

Compute node positions from the count of nodes per lane; never hard code
coordinates that assume a node count. Wide diagrams scroll inside their own
container. Body background white, text INK. Full sentences everywhere; the
banned glyph set (em dash, en dash, middot, arrows, maths symbols, ellipsis
character) must grep clean before shipping. Roles and teams, never individual
names.

## File naming

NWM_FO_Flow_<FlowKey>_<YYYY-MM-DD>.html into
`i. Client - Nicola Wealth/Performance Testing/` unless told otherwise.
