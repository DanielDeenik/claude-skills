# Service Control Utility command reference

Source: Service Administration user manual, March 2026, sections 3.10, 4.1.2,
5.2, 6.1.3, 6.2.2, 6.3.1 and 8.

Two deployment modes, same verbs.

- **Full deployment mode.** `netroot\bin\ScdSvcCtl.exe`
- **Simple deployment mode.** `scLaunchConsole.exe -product=scd -installation=<installation root> -command=ServiceControl --`

Everything below shows the full deployment form. Prefix the simple deployment
wrapper to get the other form. Note the manual writes the wrapper with a double
dash before the verb.

## Authorisation, do this first

The utility is authorised in Windows through the User Principal Name. Map the UPN
of each user who needs access to the corresponding SimCorp Dimension user.

1. System Environment Configuration window, Services tab, set Authentication mode
   to Windows. If the mode is None, most commands fail with an authorisation
   error.
2. Users window in SimCorp Dimension, add the UPN in the Principal name field,
   save.

Section 3.10, page 26.

## Help

```
ScdSvcCtl.exe help
ScdSvcCtl.exe service start help
ScdSvcCtl.exe exporthelp -destination:<folder>
```

`exporthelp` writes the whole command help as an HTML page. Adding `help` after
any command shows that command's parameters. Section 5.2.3, page 43.

## Platform

```
ScdSvcCtl.exe platform ping
ScdSvcCtl.exe platform verify
ScdSvcCtl.exe platform explain
ScdSvcCtl.exe platform restart -reason:"Restarting platform"
```

`platform ping` returns "Service platform is running" and exit code 0 when it is.
`platform verify` returns for example "2 set(s) of system services are running"
and exit code 0 when all system services are running. `platform explain` returns
existing problems in the platform, including automation issues caused by
blacklisted services or configurations. **The platform must be in maintenance
mode when you restart it.** Sections 4.1.2.1, 4.3 and 6.2.2, pages 29, 34 and 63.

## Maintenance mode

```
ScdSvcCtl.exe maintenance begin
ScdSvcCtl.exe maintenance end
```

Section 6.1.3, page 55.

## Automation and models

```
ScdSvcCtl.exe automation explain
ScdSvcCtl.exe automation enable
ScdSvcCtl.exe automation load -model <modelname>
ScdSvcCtl.exe model list
```

`automation explain` returns whether automation is Enabled, then the
Infrastructure strategy with its automation state, then the Dependency strategy
with its Configuration and automation state. **In `model list` output the active
model is marked with an asterisk.** Simple deployment mode writes the load
command as `automation load -model=<modelname>`. Sections 4.1.2.1 and 6.1.3,
pages 29, 55 and 56.

## Services

```
ScdSvcCtl.exe service ping -service:"Hostname"
ScdSvcCtl.exe service explain -service:"Hostname"
ScdSvcCtl.exe service start -id:206 -agent:<hostname>
ScdSvcCtl.exe service stop -id:<hostname>
ScdSvcCtl.exe servicetype list
```

`service ping` returns for example `Service instance "Hostname" responded (State:
Online; Stale: No)`.

`service explain` returns a block that is the fastest way to establish what one
instance actually is:

```
Compliance post-trade load balancing service (Hostname)
Service state : Online
Management mode : Infrastructure
Action : Undisclosed
Service instance : 323-1
Configuration : BFK BRANCH
Service agent
Agent : Hostname
Description : Hostname
Capabilities : IISCERT, SCDCERT, SIMCORPROOTCAINSTALLED, WEBCLIENTCERTIFICATE
Service endpoints
net.tcp://Host/SimCorp/SCD/Dev/Installation/1-1-1/std/323/Internal/323-1
Processes
(pid: 30588) SimCorp.IMS.Framework.Service.Process
```

Note that `service explain` reports the Capabilities the agent satisfies. When a
service will not start on an agent, compare this list against the capability
checks assigned to the service type. Sections 4.1.2.1, 5.2.1 and 5.2.2, pages 28,
29, 42 and 43.

APL start up parameters: the service start command uses the default parameters
from the Service Type Configuration window unless `-aplstartupparameters` is
given, in which case only those parameters are used. Section 7.1, page 80.

## Agents

```
ScdSvcCtl.exe agent list
ScdSvcCtl.exe agent restart -id:<agentid> -reason:"Testing"
ScdSvcCtl.exe agent dumpprocess
ScdSvcCtl.exe agent dumpprocess help
```

`agent list` returns one line per agent with Agent, Description and Tag where a
tag exists, for example `Agent: DK01SVT471 Description: TEST SA master server
Tag: MASTERSERVER.` A tag in this output is the fastest confirmation that service
tag mapping is in play on that agent. Sections 4.1.2.1, 4.3 and 8.4, pages 29,
36 and 93.

## Blacklist

```
ScdSvcCtl.exe blacklist list
ScdSvcCtl.exe blacklist closeall -servicetype:214
ScdSvcCtl.exe blacklist close -servicetype:214
```

`blacklist list` indicates the service types or configurations that are relevant
for the active automation model. Section 6.2.2, pages 63 and 64.

## Rebalancing

```
ScdSvcCtl rebalancing enable
ScdSvcCtl rebalancing disable
ScdSvcCtl rebalancing getmode
```

`enable` has the alias `on` and `disable` has the alias `off`. Section 6.3.1,
pages 66 and 67.

## Tracing and profiling from the command line

On `service start`:

- `-apptraceconfig` full path to an application trace configuration file. Create
  one from the Toggle Tracing window, or from Service Manager applet, Support
  Tools ribbon group, Tracing, Application Tracing.
- `-dbtraceconfig` trace file ID and trace level for database tracing, format
  `<TraceFileId,TraceLevel>`.
- `-functraceconfig` function tracing, format
  `<FunctionsOrPrefix,ThresholdInPercent,ThresholdInMilliSeconds>`.
- `-performancecounters` enables service model performance counters.
- `-profilingconfig=<path>` or `-profile=<path>` for profiling.

On a running service:

```
ScdSvcCtl.exe service starttrace help
ScdSvcCtl.exe service stoptrace help
```

Trace level semantics belong to `simcorp-database-tracing`. This package only
records where the switches are. Sections 8.1 and 8.2, pages 90, 91 and 92.

## Ordered diagnostic sequence

When a service will not start and you have shell access, run these in order and
keep the output:

```
ScdSvcCtl.exe platform ping
ScdSvcCtl.exe platform verify
ScdSvcCtl.exe platform explain
ScdSvcCtl.exe automation explain
ScdSvcCtl.exe model list
ScdSvcCtl.exe blacklist list
ScdSvcCtl.exe agent list
ScdSvcCtl.exe service explain -service:"<instance>"
```

The first two establish that the platform itself is healthy, the next three
establish what automation is being asked to do and under which model, and the
last three establish why one particular service is not where it should be.
