# Service catalogue, how to read it and the service type IDs

Source: Service Configuration user manual, March 2026, chapters 2, 3 and 4. The
authoritative and complete table is chapter 2 of that manual, and SimCorp notes
that the help version of the table renders and searches better. The manual also
states that the catalogue is a work in progress and that some information is
missing for some service types.

## The columns, and what they decide

| Column | Meaning |
|---|---|
| Service type | The service name. The table is sorted alphabetically. |
| ID | Unique identifier of the service type. Use it in ScdSvcCtl.exe, for example `service start -id:206` or `blacklist closeall -servicetype:214`. |
| Load balancer ID | The identifier of the load balancer service type serving this service type. |
| Description | What the service does. |
| Service category | Business service, exposing business functionality. Infrastructure service, which must run in all installations used by the automation infrastructure strategy, started automatically by automation but able to be blocked. System service, the core services mandatory for the platform. Client service, supporting client applications with centralised caching and server side processing. |
| Configuration | Whether the service must be configured, mandatory or optional, or needs no configuration. |
| Instance restrictions | Whether the service can start multiple instances at the same time. |
| Scalable | Whether the platform can distribute workload across a range of instances. See scaling in `07-capabilities-tags-scaling.md`. |
| Reschedulable | Services without configuration that can be rebalanced when an agent is overcommitted. |
| GC server | Whether server garbage collection is the default for this type. |
| See also | Links to the related manual. |

Two of these columns settle most arguments about an automation model.

- **Configuration Mandatory** means the service will not run without a valid
  configuration. Check what the configuration named in Pending Actions actually
  contains before assuming the model is at fault.
- **Instance restriction Single** means one instance only, platform wide. A model
  asking for a Count above one against a Single restricted type produces a
  Service instance restriction violation alert. Multiple does not mean unlimited:
  individual manuals add their own constraints, for example the Order Manager
  integration services, which allow only one instance per configuration.

## Installation sizing

Chapter 4 of the Service Configuration manual gives, per service ID, the number
of instances that typically run and the CPUs, workspace size and RAM per service,
across three installation sizes named minimum, standard and large. Chapter 3
defines those sizes by live positions, daily peak orders and total compliance
rules. Zero in the table means optional, and N/A in the workspace column means
workspace size is irrelevant for C sharp based services. Use this table when
someone asks how many instances a model should carry, rather than guessing.

The manual adds three cautions worth repeating. Failover is not accounted for, so
consider extra services. Calculation job types as configurations on the
Calculation service are not recommended because they limit dynamic allocation of
calculation capacity. The Real-time Bloomberg service is only relevant with a
central Bloomberg data licence service, and each instance delivers results for
one data source.

## Service type IDs

Extracted from the March 2026 Service Configuration catalogue. Use this to
resolve an ID seen in a command, a log path or an alert. Where a name looks
truncated, confirm against the manual before quoting it to a client.

| ID | Service type |
|---|---|
| 4 | Service stress test load balancer |
| 17 | Statistics gathering service |
| 41 | Compliance pre-trade service |
| 42 | Compliance engine front end service |
| 43 | Service stress test |
| 51 | Compliance broker restrictions service |
| 53 | Logging service |
| 59 | Compliance post-trade service |
| 60 | Forecast cash flow service |
| 61 | Compliance order manager integration service |
| 64 | Order Manager - Order service |
| 65 | Real-time Bloomberg service |
| 67 | Order Manager - Management service |
| 68 | Real-time infrastructure service |
| 69 | Directory service |
| 70 | Order Manager - Elvin service |
| 79 | Commission service |
| 80 | Controller service |
| 81 | System operations alerts service |
| 82 | Client application service |
| 83 | Shell script service |
| 84 | Pricing and key ratios service |
| 89 | Asset manager calculation service |
| 90 | Authentication service |
| 91 | Collateral dashboard service |
| 92 | APL worker service |
| 94 | Data adaptor service |
| 95 | Web api service |
| 96 | Data adaptor service load balancer |
| 97 | APL worker service load balancer |
| 98 | Analytics service |
| 99 | Service operations controller service |
| 100 | Automation service |
| 101 | System support service |
| 102 | Log gateway service |
| 104 | Application service API |
| 105 | Web application service |
| 107 | User traffic manager service |
| 111 | Trade processing dashboard service |
| 112 | Communication mediator service |
| 113 | Communication service |
| 116 | Cloud proxy service |
| 117 | Cloud authentication service |
| 118 | Data import service |
| 119 | Key performance service |
| 120 | Corporate actions service |
| 130 | Collateral auto allocation |
| 133 | Collateral event resolver |
| 134 | Installation service |
| 135 | API gateway service |
| 137 | Collateral automation service |
| 138 | Collateral communication service |
| 143 | Service stress test look-aside |
| 200 | Message queue service |
| 201 | MQ service |
| 203 | Download real-time market data service |
| 205 | Order cache service |
| 206 | Client reporting service |
| 207 | Event calendar service |
| 208 | Front office service |
| 209 | Batch service |
| 210 | Market data validation service |
| 211 | Audit translation service |
| 212 | Corporate actions elections synchronization service |
| 213 | Group code update service |
| 214 | Reporting data jobs service |
| 215 | Calculation service |
| 216 | STP service |
| 217 | Order Manager message service |
| 218 | WM service |
| 219 | Real-time service |
| 221 | Risk pricing and key ratios service |
| 222 | Business rules alert service |
| 223 | Risk analytics service |
| 224 | Performance analytics service |
| 225 | Calculation capacity controller service |
| 229 | Trade repository pool |
| 231 | Automatic recalculation of Portfolio Calculations |
| 232 | Data clean-up service |
| 233 | Automatic recalculation of MO-Position Calculation |
| 250 | Trade processing alerts service |
| 260 | General reconciliation alerts service |
| 270 | Payment reconciliation status alert service |
| 280 | Corporate actions alert service |
| 305 | Securities finance forecast service |
| 306 | Asset Manager message service |
| 307 | Order Manager - Cache service |
| 308 | Compliance online service |
| 309 | Performance date service |
| 316 | Payment reconciliation status service |
| 319 | Composite rating update service |
| 325 | Pricing and key ratios priority request service |
| 328 | Order Manager - Workflow service |
| 329 | Order Manager - Data Store service |
| 331 | Middle office analytics service |
| 332 | Personal data retirement service |
| 333 | Pricing and key ratios worker service |
| 334 | Pricing and key ratios worker service load balancer |
| 335 | Front office decomposition and conversion service |
| 336 | Middle office analytics service |
| 338 | Configuration service |
| 340 | Order Manager - Position Status service |
| 342 | Order Manager - Message Broker service |
| 343 | Order Manager - Transformation service |
| 344 | Reinvestment service |
| 346 | Asset manager calculation service load balancer |
| 348 | Order Manager - Data Extract Service |
| 349 | Order Manager - API Service |
| 353 | Order Manager - Automation Service |
| 354 | Front office worker service |
| 355 | Front office worker service load balancer |
| 357 | OTC Internal API Service |
| 358 | Configuration messaging service |
| 365 | Alternatives cash flow service |
| 367 | Flexible Analytics Service |
| 368 | OTC Web API Service |
| 372 | Advances API service |
| 373 | Asset Manager Cache |
| 374 | Front office data service load balancer |
| 375 | Pricing and key ratios queue handler worker service |
| 376 | Order Manager - External Integration service |
| 379 | Transaction API service |
| 380 | Front Office Order Cache Service |
| 381 | Front office data service |
| 383 | Compliance AI search host service |
| 385 | Order Manager - FIX Router |
| 389 | OTC Web API Service load balancer |
| 393 | Axioma Portfolio Optimizer service |
| 394 | Collateral calculation controller |
| 395 | Data Integration API Service |
| 396 | Data Integration Worker Service |
| 397 | Order Manager - FIX API Service |
| 401 | Compliance migration service |
| 404 | Asset Manager Cache Monitor |
| 407 | IAP Direct Communication Service |
| 408 | Data synchronization service |

The FIX.NET Server appears in the sizing table with ID N/A. It is not a Service
Platform service type.
