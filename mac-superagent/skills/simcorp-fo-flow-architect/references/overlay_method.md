# Overlay method

How measured numbers are placed on a grounded flow diagram.

## 1. Segment the evidence into phases

When the test varied configuration over time (auxiliary jobs enabled one at a
time), phase boundaries come from the first fire time of each logged setup, not
from anyone's recollection. In the 19 August 2026 capture the markers were
NW_O_STAMP_ACC_ID first at 10:45:41, WAITLIST_ORDER_UPDATE first at 11:05:32,
FUND_DATE_UPDATE first at 11:23:54. Present the mapping between logged setups
and the jobs the operator says were enabled as an open question until the
client or SimCorp confirms it.

## 2. Separate fixed cost from marginal cost

For each phase, take the single item run and the largest block run. Fixed cost
is the single item elapsed time. Marginal cost is (block elapsed minus fixed
cost) divided by (block size minus one). Report both; never report only a per
item average, because the average hides the fixed cost that dominates small
submissions. 19 August baselines: fixed 6 to 12 seconds per submission across
all phases; marginal 1.4 to 4.2 seconds per order.

## 3. Attribute time to nodes only when the log names the node

An SRM row naming a setup, applet or service attributes its Runtime to that
node. Time inside a composite run that no row explains is drawn as a single
band labelled "inside <run label>, not attributed" on the overlay. Never
distribute unexplained time proportionally.

## 4. Colour scale

Overlay colour encodes measured seconds per order at the node, on a single hue
ramp from ice to gold to a deep amber, with NOT MEASURED nodes in flat grey
outline and EMPTY PATH nodes (ran but did no representative work, such as
Rules=0 compliance) hatched. Structure stays near monochrome navy so the
overlay is the only loud element. Exact tokens in render_html.md.

## 5. Single measurement rule

A figure observed once is a data point, not a rate. Mark it "observed once".
Two independent captures agreeing (the three hour timestamp offset appears in
both 31 July and 14 August evidence and again on 19 August) may be stated as
confirmed twice, still not as explained.

## 6. Known confounds to check on every new capture

- Log note format changes mid capture (unit of work may differ).
- Client machine against server machine rows mixed in one tab.
- Register export missing allocated order numbers.
- Local time against UTC offsets between register and SRM.
- Aux job rows scaling with edit count rather than order count.

## 7. What a bottleneck claim requires

State the node, the measured cost, the share of end to end elapsed it
represents in the capture, the conditions (users, rules in scope, records per
extraction), and what evidence would falsify the claim. If any of the five is
missing the finding ships as an observation, not a bottleneck.
