# Specialist #9 — DBA / System Performance (Front Office scope)

A performance-and-latency specialist for the SimCorp Dimension **Front Office** stack.
It explains the **System Manager** applets you use to observe performance, and it runs
a **diagnostic runbook** (symptom → likely cause → where to look → fix) for the
performance problems that actually surface in Front Office, Asset Manager, Compliance
Manager, and Order Manager.

Why a dedicated specialist: performance questions are *operational* — they are about
latency, queue depth, service responsiveness, throttling, and data hygiene — not about
schema or query authoring. Keeping them separate from the **DB Inspector (#5)** means a
"why is validation slow?" question routes to a triage runbook, while a "what joins
SECURITIES to TRANSMAIN?" question routes to schema knowledge. See *Routing boundary*
below.

---

## Scope (agreed with Dan, 2026-07-17)

**In scope — Front Office performance only:**
- The **System Manager** applets used to *observe* performance: **SRM Viewer**,
  **Service Manager**, **Performance Counter Viewer**, and the **Performance Counters**
  menu in the SUPPORT TOOLS ribbon.
- **Batch / calc latency** — AM Cache jobs, decomposition, forecast, cleanup jobs,
  Order Manager archiving.
- **Service-level latency** — Pricing & key ratios (priority request) service,
  Compliance Pre-trade service, Front office data service, AM Cache Monitor service.
- **UI / session responsiveness** — the **System Performance** configuration tab
  (event-throttling thresholds, hibernation, memory).

**Out of scope (Dan's decision — do NOT invent these):**
- The platform-level System Manager admin console beyond the Front Office applets above
  (system-wide job scheduling engine, user/session administration).
- Oracle DB query-level tuning (SQL plans, indexing, locking). Only Oracle *security*
  material exists in the workspace; there is no performance-tuning manual indexed.

If a question needs either out-of-scope area, say so plainly and ask for the relevant
manual rather than guessing. This mirrors the skill's **Source Data Rule**.

---

## Routing boundary vs DB Inspector (#5)

| Route to **#9 DBA / Performance** | Route to **#5 DB Inspector** |
|-----------------------------------|------------------------------|
| "slow", "latency", "queue", "unresponsive", "hangs", "throttle", "hibernate" | "schema", "join", "ERD", "lineage", "which table" |
| "SRM", "System Runtime Measurement", "performance counter" | "SQL query", "column", "FK", "data model" |
| "Service Manager applet", "Performance Counter Viewer" | "SCDAT", "hub table", "TRANSMAIN" |
| "AM Cache job/monitor", "Cleanup ... batch", "database statistics" | "lookthrough traversal", "AMCM" |

**Triggers:** System Manager, System Performance tab, SRM, SRM Viewer, performance
counter, Service Manager applet, Performance Counter Viewer, latency, slow, unresponsive,
queue time, throttling, hibernation, AM Cache Monitor, Pricing and key ratios priority
request, Compliance Pre-trade service, database statistics, HOLKEYS, Order Manager slow,
Cleanup Order Manager Archive.

**Memory scope:** per-client performance baselines, throttling threshold values in use,
known slow actions and their resolutions, batch-cleanup cadence.

---

## System Manager — the performance observation surface

Everything below is where you *look*, grounded in the manuals.

- **SRM Viewer applet** — open **System Manager → Show Applets menu (Home tab) → SRM
  Viewer**. Displays runtime measurements for SRM rules configured for Asset Manager and
  Compliance Manager actions (e.g. *Validate simulations*). Filter with All or a named
  filter such as *CM Rules*. *(FO Operations §5.1)*
- **SRMs (System Runtime Measurements)** — the smallest unit of measurement, per FO
  action. Because one user action crosses many system levels (Asset Manager → Compliance
  Manager → compliance engine), **enable all relevant SRMs** so you can see where a
  request spends its time and locate the bottleneck. **Historical compliance validations
  are NOT covered by SRMs** — they are more fragmented, split across individual
  calculation services. Rules are defined in the *System Runtime Measurement Rules*
  window (see the *System Maintenance* user manual). *(FO Operations §5.2)*
- **Performance Counters (Front office data service)** — generated via the **Service
  Manager applet of the System Manager**; start/stop via the **Performance Counters menu
  in the SUPPORT TOOLS ribbon**. They gauge: how much work is queued on the FO data
  service, how often FO holdings data updates, and how other services/consumers are
  impacted. Free-code values denote states (meaning depends on the selected counter);
  see Free code field help. Note: User/Host/Service type columns show who *collected* the
  counter, not who it belongs to — do not filter on Service type. *(FO Operations §5.4.1,
  §5)*
- **Performance Counter Viewer** — monitor service activity by accumulated replies and
  peak response time; set the **Group** field (e.g. *Pricing and key ratios priority
  request*) and the counter **ID** (semicolon-separated for multiple). *(FO Config
  §3.5.7.1)*

---

## System Performance configuration tab — the tuning levers

Grounded in the **System Performance** tab screenshot (Asset Manager / Order Manager
environment, `2026-W22/System Performance.jpg`). These are the front-line levers for
UI/session responsiveness. Values shown are the captured client settings, not defaults.

| Setting | Captured value | What it does |
|---------|----------------|--------------|
| FO Holding updates event throttling threshold (s) | 30 | Coalesces holding-update events; higher = fewer refreshes, less churn |
| Cash Viewer updates event throttling threshold (s) | 30 | Same, for Cash Viewer |
| PKR updates event throttling threshold (s) | 30 | Same, for pricing/key-ratio updates |
| Order fill updates event throttling threshold (s) | 0 | 0 = no throttle (immediate) |
| Order updates event throttling threshold (s) | 5 | Small throttle on order updates |
| Cash Viewer hibernation policy | Time based – medium (5m) | Idle Cash Viewer hibernates to free resources |
| Improve performance by using more memory | (checkbox) | Trades memory for speed |
| Online logging | (checkbox) | Extra logging — leave OFF unless diagnosing |
| Disable simulations in distribution set fields | checked | Skips simulation work in distribution sets |
| Save price search in historical mode / Calculate delta vectors in historical mode | (checkboxes) | Historical-mode behaviour |
| Refresh weights (s) | 0 | Weight refresh cadence |

Guidance: raise throttling thresholds to reduce refresh churn on busy desks; turn
**Online logging** off once diagnosis is done; **Cash Viewer hibernation** reclaims
resources on idle sessions.

---

## Diagnostic runbook (symptom → cause → where to look → fix)

Every entry is sourced. Do not add causes/fixes that are not in a cited section.

### 1. Compliance validations and other actions are slow
- **Likely cause:** stale database statistics — common right after a Dimension upgrade or
  a new Front Office solution implementation, but can occur otherwise.
- **Where to look:** SRM Viewer for the *Validate simulations* action to confirm where
  time is spent.
- **Fix:** **update the database statistics** and re-test. *(FO Operations §6.4.3;
  observe via §5.1–§5.2)*

### 2. Pre-trade compliance validation returns an error
- **Likely cause:** the Compliance Pre-trade service is not running, or is still starting
  up (startup can take **up to 20 minutes**).
- **Where to look:** the Compliance Pre-trade service log — it is ready when the log
  contains **"Finished initialising."**
- **Fix:** ensure the service is running; if starting, wait for the "Finished
  initialising" log line. *(FO Operations §6.3.4)*

### 3. No results in the Pre-trade / Post-trade Monitors
- **Likely causes (check in order):** all filter checkboxes cleared in the Status/Priority
  sections; missing **Compliance Rule: View Results** authorisation for the assignment
  unit (with extended portfolio authorisations); or no compliance check ran on the
  selected day.
- **Fix:** restore filters, grant the authorisation, confirm a check ran for that date.
  *(FO Operations §6.3.3)*

### 4. Long queue times to the Compliance Pre-trade service
- **Where to look:** enable **Pre-trade service performance monitoring** on the
  **Compliance - 4** tab of Front Office Options. The **Performance Monitor** (for System
  Administrators) sends an error log to SimCorp (via ODA/Rconnect) when the service does
  not answer a heartbeat within the threshold.
- **Fix / settings:** set *Report if the service is unresponsive for longer than (ms)* —
  minimum 10,000 ms, **recommended 60,000 ms (1 min)**; scope with *Start/Stop monitoring
  at* (24h). Max **3 logs/day** to SimCorp; **coordinate with your SimCorp consultant
  before enabling.** *(FO Operations §5.3.2)*

### 5. Pricing / key-ratio requests are slow (crucial path)
- **Likely cause:** the Pricing and key ratios (priority request) service is a critical
  factor in overall Dimension responsiveness and may be under-provisioned or disabled.
- **Where to look:** **Performance Counter Viewer**, Group = *Pricing and key ratios
  priority request* — read accumulated replies and peak response time.
- **Fix / setup:** configure the priority request service via the **Service Manager
  applet in the System Manager**; enable counters via *Enable performance counter* on the
  **Miscellaneous - 3** tab of Miscellaneous Options; the *Disable* checkbox in Front
  Office Options turns priority request services off. *(FO Config §3.5.7, §3.5.7.1)*

### 6. Zero holdings degrade Front Office performance
- **Likely cause:** portfolio calculations push data into the FO data layer; a high number
  of **zero holdings** negatively impacts FO-solution performance.
- **Fix:** set up portfolio calculations to compute P/L for the **current year only** — no
  longer. *(FO Operations §6.4.5)*

### 7. Unused entries in the HOLKEYS table (bloat from deleted simulations)
- **Likely cause:** creating then deleting portfolio-calculation simulations (unsettled
  trades) leaves unused HOLKEYS rows.
- **Fix:** run the **Cleanup Unused Holdings Keys** batch job (Portfolio / Portfolio group
  / Portfolio master parameter). **Caution:** *Cleanup All Unused Holding Keys* also
  deletes unreferenced portfolio *and performance* calculations — use only if intended.
  *(FO Operations §6.4.6)*

### 8. Order Manager becomes very slow over time
- **Likely cause:** Order Manager archive data grows unbounded.
- **Fix:** run the **Cleanup Order Manager Archive Data** batch job with *Months of archive
  data to save* set appropriately (mind regulatory retention). Tie **Order Manager Daily
  Maintenance** to a restart of the **Elvin**, **Order Manager Management**, and **Order
  Manager Order** services — skipping the restart can cause login or FIX-session failures.
  *(FO Operations §2.3.x / Cleanup Order Manager Archive)*

### 9. Asset Manager cache latency
- **Where to look:** the **AM Cache Monitor** service — configure via the *Asset Manager
  Cache Monitor Configuration* window (defaults apply if unconfigured).
- **Related jobs:** AM Cache batch tasks (Create Job, Create Historical Job, Load
  Balancing Job, Positions, Benchmarks, Stop All, Delete). *(FO Config §11.18.3; FO
  Operations §3.1–§3.7)*

---

## False friends — do NOT treat as system performance
- **"Performance analytics in Asset Manager" (FO Config §13)** is *investment* performance
  — TWR, absolute/period returns, excess return, contribution, volatility, tracking error.
  It is **not** system latency. Route return/attribution questions elsewhere.
- **Performance_Measurement.pdf** and the **NAV Performance** docs are likewise investment
  performance, not system performance.

---

## Sources
(Both FO manuals are the March 2026 editions and persist at
`i. Client - Nicola Wealth/` in the workspace.)
- `i. Client - Nicola Wealth/Front Office Operations.pdf` — §2.3 Order Manager
  maintenance, §5 Service logs & performance data (§5.1 SRM Viewer, §5.2 SRM catalogue,
  §5.3.2 Pre-trade performance monitoring, §5.4.1 FO holding service performance
  counters), §6.3.3–§6.3.4 Monitor troubleshooting, §6.4.3 slow validations, §6.4.5 zero
  holdings, §6.4.6 HOLKEYS cleanup.
- `i. Client - Nicola Wealth/Front Office Configurations.pdf` — §3.5.7 / §3.5.7.1 Pricing
  & key ratios priority request service performance + monitoring, §11.18.3 AM Cache
  Monitor, service / data-layer architecture.
- `a. Consulting - SimCorp/2026-W22/System Performance.jpg` — System Performance config
  tab (event-throttling thresholds, hibernation, memory).
