---
name: simcorp-om-runtime-triage
description: >
  SimCorp Dimension Order Manager runtime triage. Use when orders are released
  in SimCorp Dimension but Order Manager reports them as not received, when the
  Order Outbox warns that Order Manager services might not be started, when the
  Order Manager Data Store cluster is degraded or shows nodes as DEAD, when
  Order Manager services show green in Service Manager yet nothing flows, when
  FIX sessions or the FIX Router misbehave, when no transactions are created
  after allocation, or when a Service Manager log export (xlsx or csv with Date,
  Message, Message type) has to be turned into a timeline and a finding. Grounded
  in Front Office Operations September 2025 chapter 6.5 and Front Office
  Configuration September 2025 sections 16.4, 16.5 and 18. Triggers on Order
  Manager not receiving orders, Data Store service, EventStore, Gossip send
  failed, Workflow service, Order Manager Message Service, FIX session does not
  start, End of Day sequence numbers, Operations Console, Force finish.
---

# SimCorp Order Manager runtime triage

Order Manager is a chain of services, and a green cell in the Service Manager
pivot only proves a process exists. This skill walks the chain from the released
order to the Data Store write, names the documented failure for each link, and
reads service log exports into evidence. Nothing here is inferred from symptoms
alone; every mechanism cites a manual section and every client fact is labelled
observation.

## Scope boundary

This skill covers what happens after an order is released and before it is
placed. It does not cover:

- Automation models, Pending Actions, blacklisting, agents, ports and the
  service catalogue. Use `simcorp-service-platform`.
- Auxiliary jobs, extraction setups and message queue content on the SimCorp
  Dimension side. Use `simcorp-extraction` and `simcorp-fo-flow-architect`.
- Communication Server, mediators and gateways. Use `simcorp-comm-server`.
- Oracle tracing and profiling. Use `simcorp-database-tracing` and
  `simcorp-performance-toolkit`.

## Hard rules

1. Read the screenshot or log export, not your memory. Quote the exact warning
   text, event names, timestamps, host names and IP addresses.
2. Never name a cause for which the log line has not been seen. Write the line
   that would prove it and ask for it.
3. Separate manual facts from client observations. Label the second.
4. Never propose a production change without the model content, the service
   logs of every node involved and the manual section that supports the change.
5. The Data Store is not Oracle. Order state cannot be queried with SQL
   (foops 6.5.18). Do not offer SQL for it.
6. No dashes, middots, arrows or maths glyphs in any output.

## The six facts that resolve most Order Manager runtime questions

1. **The carrier from SimCorp Dimension to Order Manager is the Order Manager
   Message Service.** The operations manual calls it the "SCD to OM Integration
   Service (Order Manager Message Service)". Front Office Operations 6.5.1,
   page 53. Service type 217, configuration Optional.
2. **On the new architecture both the Order service and the Workflow service
   must be running to move orders, and messages sent while the Workflow service
   is still starting are lost.** Model start order: Data Store, Workflow, Order
   service. Front Office Configuration 16.4 and 16.5, pages 161 and 165.
3. **A Data Store cluster writes only while at least half its nodes are up.**
   Production needs a minimum of three nodes, an odd number. With two of three
   stopped, Workflow can still read but "no new data such as the arrival of new
   orders is written in the Data Store cluster". Front Office Configuration
   16.4, page 161. This is the documented cause of orders released but not
   received while every service shows green.
4. **If any one of Elvin, Management, FIX.NET, Order Service or Order Manager
   Message Service is not running properly, restart all of them,** and use Stop
   then Start, never Restart. Front Office Operations 6.5.1 and 6.5.4, pages 53
   and 55.
5. **The Management service usually starts even when something is wrong.**
   The proof it started properly is that the Order Manager Operations Console
   opens. Front Office Operations 6.5.6 and 6.5.14, pages 55 and 59. The proof
   the Order service is up is that the Order Manager client logs in without an
   error and without a user name prompt. Front Office Configuration 18.12,
   page 253, and Front Office Operations 6.5.15.
6. **FIX sequence numbers are reset on both ends.** If a session fails with
   sequence number too low, run End of Day in both the Operations Console and
   the EMS, or raise the TX sequence number to the value the FIX log demands.
   Front Office Operations 6.5.7 and 6.5.8, pages 56 and 57.

## Which reference file to open

| Question | File |
|---|---|
| Where does a released order go and which service carries each hop | `references/01-handover-chain.md` |
| Data Store cluster rules, node counts, log signatures, restart order | `references/02-data-store-cluster.md` |
| A named Order Manager failure, FIX session, Operations Console, allocation | `references/03-named-failures.md` |
| A Service Manager log export has to become a timeline | `references/04-log-export-reader.md` and `scripts/read_service_log.py` |
| The Nicola case of 7 September 2026, as the worked example | `references/05-worked-case-2026-09-07.md` |
| Which manual and page a fact came from | `references/06-source-index.md` |

## Workflow: orders released but not received in Order Manager

1. Read the Order Outbox. Record Actual status, Amount placed, the Errors and
   Warnings text verbatim, and the Order Events list with Event type.
2. Place the order on the handover chain in `references/01-handover-chain.md`.
   "Released to Order Manager" is a SimCorp Dimension status event; it does not
   prove receipt.
3. Ask for the service logs, in this order: Order Manager Message Service,
   Order service, Workflow service, every Data Store node. Log Viewer applet in
   System Manager, Front Office Configuration 18.10.2.
4. Run `scripts/read_service_log.py` on each export. Read the collapsed
   timeline, the flagged lines and the repeated pattern counts.
5. Match the log against `references/02-data-store-cluster.md` and
   `references/03-named-failures.md`. Quote the manual sentence that matches.
6. State the finding, the evidence lines, the manual citation, and what is
   still unverified. Then, and only then, name the change and the model
   content it needs.

## Workflow: FIX session or FIX Router problem

Operations Console first, service second, service log third, service tag last.
Front Office Operations 6.5.7 gives that order and the exact ProxyException
text that means a service user is missing. `references/03-named-failures.md`
carries the full decision list for 6.5.7 to 6.5.12 and 6.5.17.

## Pre answer checklist

- Layer identified: SimCorp Dimension side, carrier, Order Manager service,
  Data Store node, FIX.NET, or trading venue.
- Every warning and log line quoted verbatim with its timestamp.
- Manual section and page cited for every mechanism claim.
- Client observations labelled as such, with date and environment.
- Missing evidence named, with the exact window or log that holds it.
- No SQL offered for Data Store content, no cause named without its log line.
