# Named Order Manager failures, indexed

Source: Front Office Operations user manual September 2025, chapter 6, pages 48
to 63, plus Front Office Configuration September 2025 where noted. Each row
gives the documented causes only. When the manual gives an ordered procedure,
the order is kept.

## Services and start problems

| Symptom | Section | Documented causes and actions |
|---|---|---|
| Any Order Manager service not running properly | 6.5.1, p.53 | Restart all of Elvin, Management, FIX.NET Server, Order Service, Order Manager Message Service. Not all services sit on the same server; System Manager shows where |
| Restart from the Services panel does nothing | 6.5.4, p.55 | Known issue. Use Stop, then Start |
| Management service does not start, log `ERROR:SVC67: Unable to initialize management service ... Value cannot be null. Parameter name: directory` | 6.5.5, p.55 | NETROOT path commented out in cnf.ini. Remove the comment |
| Management service does not start with a Counterparty Manager error | 6.5.6, p.55 | Wrong SQL Server details in the Order Manager Configuration window (shows as an Oracle error); FIX sessions in the FIX.NET database not matching OM3_FIXSESSIONS, fix with FIX Server Explorer before restart. The service usually starts anyway; the proof is that the Operations Console opens |
| Operations Console shows a splash screen then nothing | 6.5.14, p.59 | Management service not started properly. Check the Elvin details in the Order Manager Configuration window |
| User name and password prompt on Order Manager client start | 6.5.15, p.59 | Order service not fully started, possibly because Management did not start properly; or the SimCorp Dimension user was not created in the Operations Console |
| Cannot connect to the Workflow service, log says `Keyset does not exist` | 6.5.3, p.55 | No access to the certificate, no private key, or the logged in user cannot read the private key. Give the agent account full control on the private key |
| Data Store service will not start | foconfig 16.4.1, p.162 | Configured directory without valid EventStore files. First setup needs a directory with a `.start` marker file |
| Data Store error `Access to the registry key 'Global' is denied` | foconfig 16.4.10, p.168 | Agent account permissions |
| Data Store log `The data store configuration appears to be out of date for this installation` | copyscd 3.2, p.12 | Source folder structure copied by accident. Fix OM_DATASTOREHOSTNAMES and OM_DATASTOREPATHS in cnf.ini and the hostname and path parameters in the Order Manager Configuration window |
| External Integration or API service will not start | foconfig 17.20.1, p.243 | Management service must run first; only one instance per configuration; the required subscription must be in the configuration; ports 5671, 5672, 443 and 4222 open on the agent |

## Orders and status

| Symptom | Section | Documented causes and actions |
|---|---|---|
| Orders released, Order Manager reports them as not received (observation text: "Order/Program trade is not received in the Order Manager") | foconfig 16.4, p.161; foops 6.5.1 | Walk the chain in `01-handover-chain.md`: Message Service log, Order service and Workflow both running, Data Store quorum. Not a named section in the manual |
| Order status not updated in Asset Manager | 6.2.3, p.48 | Check the FOOMRESPONSE_Q queue table in the Order Manager schema, order by SEQUENCENUMBER desc, for allocation messages; check the Order Manager Messages window; the SimCorp Dimension party must be both counterparty and broker |
| No transactions created after allocation | 6.5.16, p.60 | STP service or Message queue service not started; a required order filter missing; Message service not started; Message service blocked by sequence number issues; message stuck in the queue through error or slow processing |
| Order Send Failed on the new architecture | 6.5.12, p.58 | Transformation or Message Broker unavailable. Resend, or Force Cancel. Inbound FIX messages are queued by the Message Broker while Transformation or Workflow are down and resume on recovery; each inbound FIX message has a unique message ID |
| Problematic order data on the new architecture | 6.5.18, p.60 | No SQL. Export Order Data from Order Manager System Maintenance for SimCorp support; Order Events Explorer is a SimCorp internal tool matched to the release version; Force Archive Orders only when instructed by support. Requires access to Trading, Orders, Order Manager, System Maintenance in Authorisation Tasks and Commands |
| Netting warnings | 6.5.19, p.63 | No netting opportunities; active placements must be cancelled; outstanding change requests must be accepted or rejected first; internal broker must be selected on the Order Manager 2 tab of Order Options |
| Broker restrictions not applied | 6.5.13, p.59 | Compliance broker restrictions service not running (rename a broker in Parties and wait a minute); rule priority all Continue; order not in Front Office holdings; restrictions created after release need a service restart to apply |

## FIX

| Symptom | Section | Documented causes and actions |
|---|---|---|
| Disconnected FIX sessions or missing FIX messages | 6.5.7, p.56 | 1 Operations Console: is the session running, start it. 2 If start fails, read the status messages under the FIX Sessions tab; sequence number too low means run End of Day in both the Operations Console and the EMS. 3 System Manager: is the FIX Router service running, start it. 4 Service log for errors. 5 Log error `Failed to start service instance ... ProxyException ... AuthenticationError` means create a service user under Maintenance, System Access, User Administration and add it to the environment's user groups. 6 Last resort: run the FIX Router on the same machine as the other Order Manager services through Service Tag Mapping |
| FIX session does not start on request | 6.5.8, p.57 | FIX.NET Server details wrong in the Order Manager Configuration window; FIX.NET Server not running; Order Service not started; wrong URLs in FIX DataRemoting.config; session already started; initiator and acceptor sequence numbers out of sync, run End of Day if safe or manually increase the TX sequence number to the value stated in the FIX log; Sender and Target CompID reversed or misspelt; FIX version mismatch; heartbeat mismatch |
| FIX session does not stop on request | 6.5.9, p.57 | FIX.NET Server details wrong; Order Service not running; wrong URLs in FIX DataRemoting.config; session already stopped |
| FIX.NET Server does not start | 6.5.10, p.57 | Windows Application event log; database connection, test with a .udl file; registry DatabaseConnectionString under HKLM\SOFTWARE\SimCorp\FIX.NET must match the UDL; stored procedure permissions |
| FIX.NET Server rejects inbound messages with `Access to the registry key Global is denied` | 6.5.11, p.57 | Performance counter permission. Add the FIX.NET service account to the permissions of HKLM\SYSTEM\CurrentControlSet\Control\SecurePipeServers\winreg |
| End of Day warns that sequence numbers were not reset | 6.5.17, p.60 | FIX.NET Server unreachable through wrong details, or no clean logout at the end of the last session (FIX_SESSION_STATE table). The warning can be ignored and the process continued |

## FIX sequence recovery, what is and is not documented

Documented: sequence resets and End of Day are performed on both the Order
Manager side and the EMS side (6.5.7), and the alternative is to raise the TX
sequence number to the value the FIX log states (6.5.8). Not documented locally:
field names on the Edit FIX Session window and any rule that the Received
sequence must be left unchanged. A recovery procedure supplied by anyone other
than the manual or SimCorp support is an open incident note until the FIX log
line and the outcome are on file. Record the session ID, both expected values,
the log line, who reset what, and whether the session came up.
