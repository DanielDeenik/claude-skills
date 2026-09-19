# Reading a Service Manager log export

Source for the mechanics: Service Administration March 2026 (Log in the Service
ribbon group, View Service Log on the instance) and Front Office Configuration
September 2025 section 18.10.2 (Log Viewer applet for the Order Manager message
service, STP service and related services). The export format below is what the
client exports look like (observation, 7 September 2026).

## The export format

- Excel or csv with three columns: Date, Message, Message type.
- Row one may hold a single cell with the support case URL. Keep it; it ties
  the log to the ticket.
- Message type values seen: Information, Start. Errors and warnings carry their
  own types when present. A line can carry an exception text at Information
  level; the type is not the severity.
- The Date column is the Service Platform timestamp. Timestamps embedded inside
  a message (for example an EventStore connection close line) can sit in a
  different time zone. Observed offset on 7 September 2026: four hours between
  the Date column and the embedded time. Never mix the two in one timeline
  without stating which one you use.

## Run the script

```
python3 scripts/read_service_log.py <export.xlsx or .csv> [--keep 2] [--out timeline.md]
```

Requires openpyxl for xlsx input. The output has four blocks.

1. Header: row count, time span, counts per message type, case URL.
2. Data Store membership (only when the log is a Data Store node log): this
   node, the other configured hosts, the configured node count, the nodes
   reported DEAD, the ports, and the arithmetic against the "at least half"
   rule of Front Office Configuration 16.4.
3. Collapsed timeline: every line in time order, except that a pattern seen
   more than `--keep` times is printed `--keep` times with a repeat count on its
   first occurrence. Patterns are built by replacing GUIDs and numbers, so
   reconnect loops collapse to one line each.
4. Repeated patterns with count, first and last time, then flagged lines: every
   non Information row plus every row matching DEAD, Unknown, ConnectionReset,
   exception, error, fail, denied, not found, could not load, out of date,
   refused, timeout.

The script reports counts, order and matches. It never names a cause. The cause
comes from matching the flagged lines against `02-data-store-cluster.md` and
`03-named-failures.md` and quoting the manual sentence.

## Reading rules

- Start with the Start row: who requested the start (Dependency Strategy means
  the automation model, a user name means a manual start) and from which agent
  host. That decides whether the model or a person owns the state.
- Read the first sixty seconds in full. Configuration, membership, ports,
  checkpoints and load exceptions all appear there.
- A repeated pattern at a fixed interval is a loop. Name the interval and the
  client address; the client address identifies the calling service host.
- "Service is successfully started" is the line behind the green cell in the
  Service Manager pivot. Everything after it is what the pivot cannot show.
- An exception logged at Information level is not evidence of a fault and not
  evidence of harmlessness. Record it as NOT VERIFIED with the assembly name and
  version, and ask SimCorp support whether it is expected for the release shown
  in the LocalRepo path.
- One log is one node. A cluster finding needs the log of every node, or the
  explicit statement that the other logs were not supplied.

## What to hand over

A finding block with five parts: the evidence lines quoted with the Date
column value, the manual sentence that explains them with section and page,
the configuration or model item that has to change, what is still unverified
and where its proof lives, and the check that proves the fix (see the last
section of `02-data-store-cluster.md`). Attach the timeline file to the case.

## Other exports this method covers

The same script reads exports of any Service Platform service log with the
three column layout: Order Manager Message Service, Order service, Workflow
service, FIX Router, STP service. The membership block only appears for Data
Store logs. For the Order Events grid of a portfolio order, export it with the
Created at, Event and Event type columns and read it by hand; the event names
and their meaning are in `01-handover-chain.md`.
