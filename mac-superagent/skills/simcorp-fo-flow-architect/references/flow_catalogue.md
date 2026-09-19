# FO flow catalogue

Eight flows. Each carries its grounding manuals (all in
`ii. Manuals & Documentation/PDFs/`) and its measured status as of
24 August 2026. A flow may be drawn structure-only, but its overlay stays
NOT MEASURED until admissible evidence exists.

## F1 Data preparation and load
Sources: foops 2 (daily tasks), foops 3 (AM cache create, historical, stop,
delete; FO Data Update; Prepare model portfolio data; benchmark cache),
foops 4.2 to 4.4 (holdings update, decomposition, key compression),
foconfig 3 (FO data layer: Service Platform, FO batch jobs, FO data services,
Order Cache Service, pricing and key ratios services, decomposition data,
Forecast Cash Flow Service, AM Calculation Service, modelling data).
Measured: PARTIAL. 19 August 2026 SRM: Asset Manager FO_LOAD_GROUP1 load 16
seconds returning 11,311 portfolio sheet rows; FO_LOAD_GROUP11 1 second
returning 0 rows.

## F2 Simulation to order
Sources: amsim 1.2 (simulations in the daily workflow), amsim 1.3 (nominal
and value basis), amsim 2 (creating simulations), amsim 3.7 (create and
release an order from a simulation), amsim 3.3 (assign defaults).
Measured: YES. 19 August 2026 SRM simulation runs: 82 simulations in 6
seconds, 49 in 3, 21 in 1; single simulations 0 to 2 seconds.

## F3 Order lifecycle and auxiliary jobs
Sources: auxjob 1 (statuses), auxjob 2 (order aux job definitions, segments,
triggers, service execution), foops 2.3 (Order Manager daily maintenance),
foconfig 3.7 (order status names).
Measured: YES. 19 August 2026 SRM: 13 order runs, 123 orders, 351 seconds;
fixed cost 6 to 12 seconds per submission, marginal 1.4 to 4.2 seconds per
order. 31 July 2026 captures: per order event timelines and aux job firing.

## F4 Compliance validation
Sources: foconfig 4 (compliance options and services), foconfig 5 (FO
Options compliance tabs), foops 3.9 (Compliance Validate Validation Group
batch task).
Measured: EMPTY PATH ONLY. All six 19 August validations ran with Rules=0.
Production rule set timings do not exist yet.

## F5 Rebalancing
Sources: forebal 2 (process, client restrictions, post rebalancing
workflows), forebal 3 (TAA rebalancing steps 1 to 4), forebal 4 (security
rebalancing), forebal 5 (FX and cash rebalancing); modlling 3.6 (workflow
modelling, rebalancing, performance), modlling 4 (model portfolios).
Measured: NO.

## F6 Extraction and downstream feeds
Sources: dataextr 1 (workflow, database structure), dataextr 2 (extraction
definitions), dataextr 3 (extraction setups, schemas, flat file, XML, message
queue, communication server, external application).
Measured: YES for the three order path setups. 19 August 2026:
NW_O_STAMP_ACC_ID 55 runs 3 seconds total, WAITLIST_ORDER_UPDATE 30 runs 5
seconds, FUND_DATE_UPDATE 11 runs 5 seconds, every run 1 record.

## F7 Transaction processing and matching
Sources: traproc 2 (business and elementary transactions), traproc 3
(status levels and flow), match 1 (matching workflow), match 2 (auxiliary
components and STP), match 4 (executing matching), match 7 (STP services).
Measured: NO. The 19 August orders show no fills and no executions.

## F8 Cash management
Sources: cabu 2 to 4 (cash buckets, setup, transactions), cabu 6 (cash
bucket in modelling).
Measured: NO.

## Cross flow spine

The Wealth order path crosses F1, F2, F3, F4 and F6 in that order. This spine
is the only end to end path with measured segments today, and it is the
default subject when Dan says "the order flow".
