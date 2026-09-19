# Refreshed environment checklist for the modelling chain

Use this list on any environment that was restored from a copy of another
installation (Copying SimCorp Dimension September 2025, chapter 4). Each line
names the manual section that makes the check necessary. Record the answer,
never assume it.

## What a copy changes

1. The automation model is unloaded by RESET_AFTER_COPY (4.1.9, 4.2.15).
   Consequence: no Front office data service, no Front office modelling
   calculation service and no PKR service starts on its own. The modelling
   batch queues work that nobody consumes (Front Office Operations 3.6, Front
   Office Configuration 3.12).
2. Every system option lives in the copied database (4.2.18). Consequence:
   the Front Office Options window of the refreshed environment shows the
   values of the SOURCE at copy time. A pricing profile changed in another
   environment after that moment is not present.
3. Blacklists may carry over (4.2.20). Consequence: a service that was
   blacklisted in the source stays blacklisted in the copy until closed.
4. Absolute path references and server names can point at the source (4.2.18
   note). Consequence: the Support Tool Options trace directory and any file
   based inputs may be wrong.
5. Optimizer statistics belong to the restored database, not to the running
   workload (Front Office Operations 6.4.3 lists new Front Office
   implementations as a reason to update statistics).

## Verify list, in order

1. Which installation was the source, and at what date and time was the copy
   taken. Write it down; it decides whether any later change exists here.
2. Service Manager: active automation model, and the running state of Front
   office data service, Front office data service load balancer, Front office
   modelling calculation service (count of instances), PKR services. Any
   service in Pending Actions or blacklisted. Hand over to
   simcorp-service-platform for the fix.
3. Front Office Options, Modelling tab: Include model portfolios or Include
   all, Pricing profiles, FX rate profiles, Use profiles from model
   portfolios, Automatically recalculate model portfolio components,
   Automatically recalculate client specific weights, Automatically
   recalculate erroneous and the interval in minutes. Screenshot it.
4. Front Office Options, Options tab: Front office holdings portfolio segment,
   and whether the batch and service users are authorised to every portfolio
   in it (Front Office Operations 3.5, Authorisations).
5. Prices and FX rates for the analysis date under the profile named in step
   3. Search Missing Prices on that profile.
6. PKR monitored segment includes every security referenced by model portfolio
   components and replacement rules (Front Office Operations 6.4.2).
7. Batch Jobs window: open the three jobs of the modelling group and read the
   parameter labels and values. Note the portfolio or segment on the client
   specific job; empty means every portfolio.
8. Batch log of the last run: per job start and end lines with times.
9. Prepare Front Office Modelling window: Status Log colour counts and the
   first three Error Log messages.
10. Ask the hosted DBA whether statistics were gathered after the restore.

## Reading the result

If step 2 shows the services down or the model unloaded, that is the cause
regardless of what the batch log says; the batch cannot finish work it only
queued. If the services are up and step 9 shows red rows with price or FX
errors, the cause is pricing input for the profile on the Modelling tab, and
changing the profile helps only if the new profile actually has prices for the
analysis date in this environment. If the services are up, the Status Log is
green and the client specific job still runs for hours, the cause is scope
and capacity: every portfolio on one calculation service; the documented
remedy is more Front office modelling calculation services or a narrower
segment (Front Office Configuration 3.12.2).

## Make the fix stick across refreshes

A fix applied in the SOURCE before the next copy is carried over by the copy.
A fix applied only in a target is lost on the next refresh. Options, the
automation model name and the batch job definitions can be moved with
Configuration Transport (Copying SimCorp Dimension 4.2.18 refers to the
Service Administration user manual); the Prepare Front Office Modelling
definition is a transportable ConfigurationType (Front Office Configuration
chapter 14 list).
