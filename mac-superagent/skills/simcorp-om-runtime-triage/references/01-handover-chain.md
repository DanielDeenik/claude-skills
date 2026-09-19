# The handover chain from a released order to the Data Store

Sources: Front Office Operations September 2025 sections 6.2.3, 6.5.1 and
6.5.12. Front Office Configuration September 2025 sections 16.4, 16.5, 17.4.1.4,
17.4.1.5, 18.7 to 18.12 and 21.1.6. Service Configuration March 2026 chapter 2.
Event names and warning texts marked observation come from Nicola screenshots of
7 September 2026 and are not in the manuals held locally.

## The chain, one hop per row

| Hop | What happens | Service that carries it | Documented proof it worked | Documented failure |
|---|---|---|---|---|
| 1 | Order saved with Requested status Released. Pre trade compliance runs, the order is released | SimCorp Dimension client or Asset Manager scale out | Order Events "Order created", "Order validated", "Released to Order Manager" (observation: these are Status and Internal event types written by SimCorp Dimension, not acknowledgements from Order Manager) | Restrict order types or force times to Order Manager in Order Options block the release (foconfig 17.4.1.5). A dealing desk without a portfolio master cannot release (18.1) |
| 2 | The order is handed to Order Manager | Order Manager Message Service, ID 217, "SCD to OM Integration Service" (foops 6.5.1). Configuration Optional | Its service log in the Log Viewer applet (foconfig 18.10.2) | Service not started or not configured; foops 6.5.16 lists "The Message service is not started" and "unable to retrieve messages due to sequence number issues" |
| 3 | Order Manager takes the order | Classic: Order Manager - Order service, ID 64. New architecture: Order service and Order Manager - Workflow service, ID 328, both required (foconfig 16.4 note) | Order Manager client logs in without error (18.12); order visible in Order Manager | Workflow still starting when the message arrives: message lost (16.4 note). Order service down: login error or credential prompt (foops 6.5.15) |
| 4 | The trading event is written | Order Manager - Data Store service, ID 329, event sourced cluster | Node log shows the write; state healthy on a quorum of nodes | Fewer than half the nodes up: reads continue, writes stop, "arrival of new orders" is not written (16.4). See `02-data-store-cluster.md` |
| 5 | Status flows back to SimCorp Dimension | Order Manager Message Service processes the Order Manager response queue (catalogue 217); queue table of FOOMRESPONSE_Q in the Order Manager schema, order by SEQUENCENUMBER desc (foops 6.2.3) | Order status updated in Asset Manager; Order Manager Messages window | foops 6.2.3: status not updated in Asset Manager; foops 6.5.16: no transactions after allocation |
| 6 | Placement to the venue | Message Broker 342, Transformation 343, FIX Router 385, FIX.NET Server | FIX session running in the Operations Console | foops 6.5.7 to 6.5.12. Transformation or Message Broker unavailable gives Order Send Failed; Resend or Force Cancel (6.5.12) |

## What the Order Outbox tells you (observation, 7 September 2026)

- Tree counters such as "Working orders [0/3/0]" with Amount placed 0.00 on
  every row: the orders sit at Released on the SimCorp Dimension side with no
  placement.
- Errors and Warnings row, Field "Order Manager": "Order/Program trade is not
  received in the Order Manager. Please contact your system administrator. The
  Order Manager services might not be started." This text was not found in the
  Front Office Operations or Configuration manuals. Treat it as the symptom of
  hops 2 to 4, never as proof of which hop.
- Order Events with Event type. Seen types: Status (Order created, Released to
  Order Manager), Internal (Order validated, Override, Released as part of
  Override, Force finish), Change request (Order deleted after release).
- "Released as part of Override" follows an "Override" event by one second:
  compliance results were overridden and the release proceeded.
- "Force finish" is a manual close out of an order that will not progress. It is
  an intervention, not a system event.

## Change requests on released orders

Front Office Configuration 17.4.1.4, page 192, Order Options window, Fields
section: internal change request fields trigger a change request between
portfolio manager and dealer when changed on an order; external change request
fields do the same between dealer and market; changing a compliance invalidation
field on a released order triggers a change request. The Order amend section of
17.4.1.5 (Allow amend of orders, Available change request accept method) decides
where and how the request is handled. Observation: deleting an order that has
already been released is logged with Event type Change request. The deletion
case is not spelled out in the manual text held locally.

## Prerequisite and dependent services (foconfig 18.7 to 18.9)

Prerequisites before any Order Manager service: Elvin (in the dependency model)
and FIX.NET. Order Manager services in the model: Management service and Order
service. Dependent and related services, added as dependents only: Message
Service, STP Service, Analytics, Trade Order Status, Compliance, Commission,
Compliance Broker Restrictions (the last five optional). Foops 6.5.1 adds the
new architecture set: Workflow, Data Store, Message Broker, Transformation, Data
Extract, API, Position Status, FIX Router, FIX API.

## Ports (foconfig chapter 19)

Management to Elvin, Management to Order, Order to Elvin, Oracle to Management,
client to Elvin, Management and Order, Ops Console to all three, Position Status
to the new architecture and Workflow to Position Status are dynamically
allocated and announced by MUCS. Data Store TCP and HTTP ports sit on the
Workflow Server Parameters tab and apply to every node listed under Hostname;
the firewall must also open the TCP port minus one (16.4.2, page 162).
