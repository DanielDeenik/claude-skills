# Source index

Manuals held in `ii. Manuals & Documentation/PDFs`. Page numbers are the
printed page numbers of the PDF editions named. Where a fact came from a client
artefact rather than a manual, the artefact and date are named instead.

## Front Office Operations user manual, September 2025 (foops.pdf)

| Section | Page | Used for |
|---|---|---|
| 2.3.2 Order Manager daily maintenance, service restart | 10 and 11 | Elvin, Management and Order service restart tied to daily maintenance; dependent services do not need a daily restart |
| 6.2.3 Order status not updated in Asset Manager | 48 | FOOMRESPONSE_Q queue table, Order Manager Messages window, party as counterparty and broker |
| 6.5.1 Order Manager services | 53 | Full service list, "SCD to OM Integration Service (Order Manager Message Service)", restart all five rule |
| 6.5.2 Position Status service log data | 54 | Trace fields available in that log |
| 6.5.3 Keyset does not exist | 55 | Workflow certificate private key permissions |
| 6.5.4 Services do not restart from Services panel | 55 | Stop then Start |
| 6.5.5 and 6.5.6 Management service does not start | 55 | NETROOT in cnf.ini; Counterparty Manager, OM3_FIXSESSIONS, Operations Console as the proof |
| 6.5.7 Troubleshoot FIX Router | 56 | Six step procedure, ProxyException text, service tag last resort |
| 6.5.8 and 6.5.9 FIX session does not start or stop | 57 | Cause lists, sequence number synchronisation, CompID, FIX version, heartbeat |
| 6.5.10 and 6.5.11 FIX.NET Server | 57 | UDL test, registry connection string, winreg permissions |
| 6.5.12 FIX messages when services are unavailable | 58 | Order Send Failed, Resend, Force Cancel, Message Broker queues inbound messages, unique message ID |
| 6.5.13 Broker restrictions | 59 | Service check by renaming a broker, restrictions apply at release |
| 6.5.14 and 6.5.15 Operations Console and credential prompt | 59 | Management not started properly, Order service not fully started, user not created in the Operations Console |
| 6.5.16 No transactions after allocation | 60 | STP, Message queue service, Message service, sequence numbers, stuck message |
| 6.5.17 End of Day sequence number warning | 60 | FIX.NET details, unclean logout, FIX_SESSION_STATE, warning can be ignored |
| 6.5.18 Problematic data in the Data Store | 60 to 63 | No SQL, Export Order Data, Order Events Explorer, Force Archive Orders, authorisation node |
| 6.5.19 Internal netting | 63 | Change requests block netting, internal broker on Order Manager 2 tab |
| 6.5.20 Information sources | 63 | UDL database connection test |

## Front Office Configuration user manual, September 2025 (foconfig.pdf)

| Section | Page | Used for |
|---|---|---|
| 16.4 Overview of the Data Store service | 161 | Quorum sentence, three node minimum, odd node count, start order note |
| 16.4.1 Data Store file storage | 162 | Valid EventStore files, `.start` marker |
| 16.4.2 Data Store ports | 162 | Ports apply per hostname, TCP port minus one on the firewall |
| 16.4.4 Data Store password | 163 and 164 | changeit default, change order, encryption key fixed |
| 16.4.5 Network encryption | 164 | Not supported in cluster mode of three or more nodes |
| 16.4.6 Operate the cluster from the Service Platform | 165 | Hostname and Directory path rows, cnf.ini parameters, dedicated machines, service tag, maxrunningservices |
| 16.4.7 File backup | 165 | Data stream backup |
| 16.4.10 User permissions | 168 | Registry key Global |
| 16.5 Workflow service overview | 165 | Order service and Workflow both required, message loss while starting |
| 17.4.1.4 Order Options Fields section | 192 | Change request field lists, compliance invalidation fields on released orders |
| 17.4.1.5 Order Options Options tab | 200 to 203 | Release order on save and STP Hold, Order restrictions to Order Manager, Order amend section |
| 17.19 Certificates | 240 to 242 | Certificate locations per service |
| 17.20.1 Integration service start rules | 243 and 244 | Management first, one instance per configuration, subscriptions, four ports |
| 18.1 Dealing desk portfolio master | 245 | Cannot release without it |
| 18.7 to 18.9 Start services | 250 | Prerequisites, Order Manager services, dependent services |
| 18.10.2 View logs | 251 | Log Viewer applet, services to monitor |
| 18.11 and 18.12 Check Management and Order service | 252 and 253 | Operations Console, Order Manager login |
| 19 Order Manager ports | 253 | Dynamic ports announced by MUCS |
| 21.1.6 New Order Manager architecture | 259 to 261 | Service roles in the new architecture |

## Service Configuration user manual, March 2026 (srvicconf.pdf)

Chapter 2 catalogue rows for 64, 67, 70, 217, 328, 329, 340, 342, 343, 348,
349, 353, 376, 385, 397; chapter 4 sizing table pages 50 to 57 with the Data
Store footnote on page 57.

## Copying SimCorp Dimension, September 2025 (copyscd.pdf)

Section 3.2, pages 11 and 12: certificates, Data Store password and key,
cnf.ini hostnames and paths, "configuration appears to be out of date".

## Client artefacts (observation only)

- Service Manager pivot screenshot, 7 September 2026.
- Portfolio Orders and Extra Information screenshot, order 20260907000788.
- Order Outbox and Order Events screenshots, NWM300_A TECN SW, 7 September.
- Service log export "Order Manager Data Store Service.xlsx", 329-1, 7 September
  16:02 to 17:03, case 500Tb00001NaIALIA3.
- Louis test rounds 20 and 21 August 2026 (FO_OM_MQ Order Defaults rows).

## Not held locally

System Administrator's Manual (Azure Service Bus setup, cnf.ini parameter
reference), the Portfolio Orders window field help (STP order status queue
fields), and the Order Manager Operations Console help (Edit FIX Session field
names). Say so when a question lands there.
