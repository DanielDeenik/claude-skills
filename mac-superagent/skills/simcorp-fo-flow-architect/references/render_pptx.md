# PPTX deck template

Generated from the same grounded model as the HTML pack, never authored
separately. Deck shape, in order: title slide; one flow structure slide per
flow in scope; one overlay slide per measured flow; one evidence slide; one
open questions slide; one position slide.

## Geometry, mandatory

Derive every card and column width from the available slide width divided by
the item count with margins; never hard code a width that assumes a count.
Before saving, assert programmatically that no shape extends beyond slide
bounds; a failed assertion is a build failure, not a warning. A 16:9 slide is
12.19M by 6.86M EMU.

## Style

Nicola theme tokens as in render_html.md. White slides use INK copy and NAVY
headings with GOLD #A66E08 accents; navy slides use white copy with GOLD
#C8860A accents. Calibri throughout. Full sentences on every slide, no banned
glyphs, roles and teams never individual names. Every process step carries a
meaningful icon drawn in the ink colour of its slide.

## Overlay slides

Same skeleton as the structure slide with the colour ramp applied. Phase
differences marked with a rule bar under the affected node. Each measured node
shows fixed cost and marginal cost as two labelled figures. A footnote names
the evidence file and capture window. NOT MEASURED nodes keep the dashed grey
outline so the audience sees the boundary of the evidence.

## Verbal discipline

Findings that meet the seven point bottleneck test in overlay_method.md may be
called bottlenecks. Everything else is written as an observation with its open
question number. The deck closes with the position slide stating the
conditions of measurement (users, rules in scope, records per extraction) so
the numbers cannot be quoted out of context.
