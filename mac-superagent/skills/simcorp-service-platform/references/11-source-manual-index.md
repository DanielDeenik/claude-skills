# Source manual index

Every fact in this package traces to one of the manuals below. All of them sit in
the connected folder `ii. Manuals & Documentation/PDFs/`. Convert with
`pdftotext -layout` before searching.

## Primary sources

| File | Manual and edition | What it supplies here |
|---|---|---|
| `srvicad.pdf` | Service Administration user manual, March 2026 | The backbone. Platform layers and system services chapter 1. Tools and the Service Manager window chapter 2. Installing agents chapter 3. Operating the platform chapter 4. Operating services chapter 5. Automation models, blacklisting, rebalancing and scaling chapter 6. Service type configuration, tags, capabilities, flooding protection, garbage collection chapter 7. Support tools chapter 8. Agent command line references chapters 9 and 10. Troubleshooting chapter 11. |
| `srvicconf.pdf` | Service Configuration user manual, March 2026 | The service catalogue and its column semantics chapter 2. Installation size categories chapter 3. Per service sizing guidance chapter 4. Calculation service jobs chapter 5. Calculation capacity controller chapter 6. Net.Tcp Port Sharing chapter 7. Fixed port numbers and firewall setup chapter 8. Middle office analytics chapter 9. Axioma Portfolio Optimizer chapter 10. Installation service chapter 11. |
| `foconfig.pdf` | Front Office Configuration user manual, September 2025 | Order Manager service overviews section 16. Certificates in Order Manager section 17.19. Streaming API configuration and the External Integration start rules section 17.20. Preparing Order Manager for operation chapter 18. New Order Manager architecture reference chapter 21. |
| `copyscd.pdf` | Copying SimCorp Dimension user manual, September 2025 | Copying the new Order Manager architecture section 3.2, covering the API configuration parameter, security certificates, the Data Store password and encryption key, configuration data and source and target confusion. Restoring Data Store data files section 4.1.5. |
| `foops.pdf` | Front Office Operations user manual | Order Manager troubleshooting section 6.5, including named Management service, FIX session, FIX.NET Server and Operations Console failures. |

## Secondary and adjacent

| File | Why you might reach for it |
|---|---|
| `sysmn.pdf` | System Maintenance user manual, March 2026. The wider System Manager window, SRM, System Performance Check, Trace File window, Operations Console FIX session colours. Diagnostics belong to `simcorp-performance-toolkit` and `simcorp-database-tracing`. |
| `ssam.pdf` | System Administrator's Manual. Named repeatedly by the Service Administration manual as the source for cnf.ini parameters, logging parameters, event driven messaging, Azure Service Bus authentication methods, Workflow Server Parameters fields and lock folder permissions. |
| `deployment.pdf`, `simpledeployment.pdf` | Deployment guidance for the two deployment modes. |
| `auxjob.pdf`, `brm.pdf` | Auxiliary jobs and the Business Rules Manager, the latter being where an alert can be turned into an email. |
| `commserv.pdf`, `commseri.pdf` | Communication Server. Route those questions to `simcorp-comm-server`. |
| `preorac.pdf` | Oracle preparation. Route to `simcorp-oracle-configuration`. |

## Known gaps, do not fill them by inference

1. **The System Administrator's Manual is referenced constantly and is not held
   locally under an obvious name.** Anything the Service Administration manual
   defers to it for, specifically cnf.ini parameter definitions, Front Office
   installation guidelines per service type, event driven messaging, Azure
   Service Bus authentication methods and modes, and Workflow Server Parameters
   field definitions, is not verifiable from this package. Say so rather than
   reasoning from plausibility.
2. **Azure Service Bus setup for the streaming API** has three of its four steps
   documented only in that manual.
3. **The Order Manager help** is cited for data extraction in the new
   architecture and is not a PDF in the folder.
4. **Trace level numbering across surfaces.** The Service Manager tracing switch
   and the batch job trace facility are documented separately, and the level
   numbering has not been confirmed to be identical across them. This is recorded
   as an open point in `simcorp-database-tracing`.
5. **The service catalogue is explicitly a work in progress** in SimCorp's own
   words, and some information is missing for some service types. An empty cell
   in the catalogue is not evidence of a None value.

## How to check something quickly

```
cd "<manuals folder>/PDFs"
pdftotext -layout srvicad.pdf /tmp/srvicad.txt
grep -n -i "<phrase>" /tmp/srvicad.txt
sed -n '<start>,<end>p' /tmp/srvicad.txt
```

Search the Service Administration manual first for anything about running the
platform, the Service Configuration manual first for anything about a specific
service type, and the Front Office Configuration manual first for anything with
Order Manager in the name.
