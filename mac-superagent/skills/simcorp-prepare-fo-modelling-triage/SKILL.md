---
name: simcorp-prepare-fo-modelling-triage
description: >
  SimCorp Dimension Prepare Front Office Modelling and Prepare Front Office
  Holdings triage. Use when the Prepare Front Office Modelling batch or the
  FO_PREP_HOLDING batch job group runs for hours, hangs, or finishes with red
  or yellow rows in the Status Log, when model portfolio component weights or
  client specific TAA and SAAM weights are missing or stale in Asset Manager,
  when synthetic model holdings do not appear, when the problem returns on a
  refreshed or copied environment, or when someone changes the pricing or FX
  rate profile on the Modelling tab of the Front Office Options window and asks
  whether that fixes it. Grounded in Front Office Configuration 3.12, Front
  Office Operations 3.5, 3.6, 5.4, 6.1, 6.4, Service Configuration service 215
  and Copying SimCorp Dimension chapter 4. Triggers on Prepare FO Holdings,
  Prepare FO Modelling, Update MP components, Update Client specific data,
  batch tasks 518 519 520, modelling calculation service, environment refresh,
  RESET_AFTER_COPY.
---

# SimCorp Prepare Front Office Modelling triage

Every claim below cites a manual section. Where the manuals are silent the
package says so. Never name a cause before the evidence list in the workflow
has been collected. Never guess parameter labels from a configuration export.

## What the batch actually does (why it can run for hours)

1. The Front Office Model batch tasks do not do all the work themselves. The
   Update 'MP Components' Data task calculates the model portfolio component
   weights in the Front Office Holdings table and then QUEUES portfolios for
   recalculation (Front Office Operations 3.6). The queued work is performed by
   the Front office data service, which queues and then recalculates
   portfolios, and by the Front office modelling calculation service, which
   updates the status of model and client specific portfolios and recalculates
   the weights (Front Office Configuration 3.12).
2. The Update 'Client specific' Data task calculates the individual model
   portfolio weights according to TAA and SAAM for the included portfolios
   (Front Office Operations 3.6). With no portfolio and no segment on the job,
   every portfolio is included.
3. Multiple Front office modelling calculation services may run at the same
   time and this is the documented way to optimise performance for large
   amounts of model portfolio and client specific data (Front Office
   Configuration 3.12.2). Sizing: service 215 with job type Front office
   modelling calculation is Minimum 1 service, Standard 2, Large 3 (Service
   Configuration, installation guidelines table).
4. A wrong retry setting can keep a service permanently busy. If
   Automatically recalculate erroneous is on with a Time interval in minutes
   between attempts below 60, SimCorp warns the service can be kept
   permanently busy retrying erroneous models (Front Office Configuration
   3.12.1 step 8 note). Errors are typically missing prices or FX rates for
   changed or new components (3.12.3.2).

## Why a refreshed environment behaves differently

1. The RESET_AFTER_COPY job automatically unloads the automation model
   (Copying SimCorp Dimension 4.1.9 and 4.2.15). Until a model matching the
   test environment is loaded again, the Front office data service, the Front
   office modelling calculation service and the PKR services do not start by
   themselves. Queued modelling work then waits. Loading and verifying the
   model is the simcorp-service-platform skill's job.
2. After a restore every system option stored in the database must be
   reviewed for the target (Copying SimCorp Dimension 4.2.18). Front Office
   Options is such a window, so a change made in one environment exists in a
   refreshed environment only if the source of the copy already held it.
3. Blacklists carried over from the source may be closed after a refresh
   (Copying SimCorp Dimension 4.2.20). A blacklisted service needs manual
   intervention (Service Administration 6.2).
4. Slow Front Office actions after an upgrade or a new Front Office
   implementation call for a database statistics update (Front Office
   Operations 6.4.3). A restored database is the same situation.
5. Prices from the PKR service exist only for securities inside the monitored
   segment; modify the segment and restart the service when a security shows
   Execution type No execution (Front Office Operations 6.4.2).

## Workflow: collect before you conclude

1. Batch log of the run: which job in the group is open, its start time, and
   whether the log shows the job finished quickly while Asset Manager stayed
   stale (work queued to a service) or the job itself is still running.
2. Service Manager: is the Front office data service running, how many Front
   office modelling calculation services are running, are PKR services
   running, which automation model is active, and are any services
   blacklisted or in Pending Actions. Route to simcorp-service-platform.
3. Front Office Options, Modelling tab, in the affected environment: Pricing
   profiles, FX rate profiles, Use profiles from model portfolios,
   Automatically recalculate erroneous and its interval. With Use profiles
   from model portfolios on, every model in one TAA must share one pricing and
   FX profile or the weights calculation can fail (3.12.1 step 5).
4. Prepare Front Office Modelling window: Status Log applet (red errors,
   yellow requires recalculation, green calculated) and Error Log applet text
   (3.12.3.1 and 3.12.3.2). Count the red rows and read the first error.
5. Prices and FX rates for the analysis date in that environment: run the
   Search Missing Prices check on the profile named on the Modelling tab.
6. Performance counters for the Front office data service from Service
   Manager show how much work is queued and how often holdings update (Front
   Office Operations 5.4.1). The Front Office holdings trace from Support Tool
   Options, Front Office tab, logs queued and processed positions (6.1).
7. Only then write the finding: one cause, the section that supports it, and
   the single change to make. If two causes remain, say both and name the
   evidence that separates them.

## Decision table

| Evidence | Reading | Action and source |
|---|---|---|
| Job finished fast, weights stale, services not running | Work queued, nobody consuming | Load the automation model or start the services (Copying 4.2.15, FO Config 3.12) |
| Status Log red, Error Log says no price or FX | Pricing input missing | Load prices or FX for the profile on the Modelling tab (FO Config 3.12.3.2) |
| Red rows retried every few minutes | Erroneous retry interval too short | Set interval to at least 60 minutes (FO Config 3.12.1) |
| Client specific job runs for hours on all portfolios | Scope too wide for one service | Add modelling calculation services or set a segment (FO Config 3.12.2, Operations 3.6) |
| Slow only on the restored copy | Statistics stale | Update database statistics (FO Operations 6.4.3) |
| Profile changed in one environment only | Option not copied | Re apply on the refreshed copy (Copying 4.2.18) |

## Nicola facts on record

FO_PREP_HOLDING (export 22-May-2026, TEST 25.10 SP0): sort 1 FO_FND_DELETE_ALL
task 520 inactive, sort 2 FO_FND_UPD_ALL_MP_COMP task 519 with PARM1 Yes and
PARM2 No, sort 3 FO_FND_UPD_CL_SPE_DATA task 518 with no portfolio and no
segment. The export does not carry parameter labels; read them from the Batch
Jobs window before interpreting PARM1 and PARM2. See references/03-nicola-group.md.

## Scope boundary

Service start, automation models and blacklisting belong to
simcorp-service-platform. PKR definitions and segments belong to
simcorp-pricing-precedence. Batch job group construction belongs to the batch
job builder template. Decomposition batch jobs belong to the decomposition
notes. This package covers only the modelling data preparation chain.

## References

- references/01-manual-grounding.md, verbatim manual passages by section.
- references/02-refresh-checklist.md, what a copy changes and the verify list.
- references/03-nicola-group.md, the FO_PREP_HOLDING group and open questions.
