# Installing agents, starting and restarting the platform, ports and firewall

Sources: Service Administration user manual, March 2026, chapters 3, 4, 9 and 10.
Service Configuration user manual, March 2026, chapter 8.

## Prerequisites before starting the platform

- The user must have permission to change the System Environment Configuration
  window.
- Set the service authentication mode to Windows, in System Environment
  Configuration, Services tab, Authentication mode. This is what lets
  ScdSvcCtl.exe work.
- Enable logging, for example `unifiedlogging=3` in cnf.ini, where 3 is the
  default and values range from 2 to 4. Specify targets for LogWriter1 and
  LogWriter2, either database or file. If they are unset, log messages are not
  recorded anywhere.
- Access to the Service Manager applet in the System Manager window.
- SimCorp Dimension must be shut down for maintenance when main service agents
  are enabled, because starting the platform changes internal service discovery
  properties and users must restart their sessions.
- On every machine running an agent, the netroot file share must be trusted for
  the users starting the agents and cache manager instances.
- The user starting the cache manager service must be able to create symbolic
  links, local to remote.

Section 3.1, pages 16 and 17.

## Install a main service agent, full deployment mode

```
ScdSvcAgent.exe -install
ScdSvcAgent.exe -uninstall
ScdSvcAgent.exe -help
ScdSvcAgent.exe -install -user=SERVERUSER_NAME/SERVERUSER_PASSWORD
ScdSvcAgent.exe -install -osuser=scdom\Svc_con_test$ -cachemanagerosuser=scdom\Svc_con_test$
netroot\bin\scdsvcagent.exe -checkcompatibility="c:\Program Files\SimCorp\Service Agent\PROD\ScdSvcAgent.exe"
```

Run from the installation bin folder. The installer prompts for the Windows OS
user and password, which is a different user from the built in SERVER user in
SimCorp Dimension. It also prompts for the cache manager OS user, and for
security reasons that should be a different OS user. By default the agent uses
the built in SERVER user to talk to the system, and a different SimCorp Dimension
user can be given with `-user`, whose user type must be Service user. Managed
Service Accounts are supported through `-osuser=DOMAIN\MSA_Agent$` and
`-cachemanagerosuser=DOMAIN\MSA_Cache$`.

**Do not start the agent immediately after installing.** It must be registered in
SimCorp Dimension first, otherwise it does not act as a main agent.

`-checkcompatibility` returns 0 when the installed agent executable is
compatible and 2 when it is not and must be reinstalled. Incompatible agents
cannot start the node controller and the platform cannot be used. Breaking
changes are announced in the Release Notes. Sections 3.2 and 3.2.2, pages 17,
18, 20 and 21.

Simple deployment mode uses
`scLaunchConsole.exe -product=scd -installation=<installation root> -command=ServiceAgent -installService`
and `-uninstallService`. Section 3.3, pages 21 to 23.

## Cache manager

Installed automatically with the first agent on a server, as a Windows service
maintaining a local file cache of everything from netroot that the platform uses.
When an agent starts it checks whether the cache needs updating and instructs the
cache manager, then starts as normal. Not supported in simple deployment mode.
The cache manager is removed automatically when the last agent on the server is
uninstalled, and it should never be installed on a local client.

Recommended access rights to the file cache directory: service agent Read and
Execute, cache manager Read and Write. Neither should have both write and execute.

Skip it with `-cachemanagermode=none`, though SimCorp recommends against that.
After updating the central installation, restart the service platform to refresh
the local file cache. Section 3.2.1, pages 19 and 20.

## Register the main agent

1. System Environment Configuration window, Services tab.
2. In the Directory services section, register the host name including domain of
   the server holding the agent.
3. Set a free TCP port for the directory service. Use the dynamic range, normally
   49152 to 65535 on Windows, and exclude the chosen port from the dynamic range
   with netsh so nothing else grabs it and blocks the agent from starting.
4. Click OK.

Two or three main agents on different servers are recommended in production for
fault tolerance. Section 3.4, pages 23 and 24.

## Several agents on one server

One agent per server is the recommendation. Where several run on one server,
enable shared load data so the load index accounts for the other agents on the
same machine, including agents belonging to other SimCorp Dimension
installations. System Environment Configuration, Services tab, Shared load data
check box. This writes `SvcSharedLoadData=1` to cnf.ini. Section 3.5, page 24.

## Start the platform

Start the main agent in the Windows Services window, remembering to start both
the cache manager and the agent. Bootstrapping takes about a minute, longer the
first time after an installation or a central update while the file cache
refreshes.

Agent output goes to the Windows Event Log with source
`SimCorpDimensionServiceAgent<state>` and, in full deployment mode,
`SimCorpDimensionCacheManager<state>`, where `<state>` is defined in cnf.ini.
Build a custom view in Event Viewer filtered on those sources.

Three ways to verify the platform is running: the Windows Event Log, the Service
Control Utility, and the Service Manager applet. Section 3.6, pages 24 and 25.

## Platform options

Service Options window, Service Platform tab, number of hours to keep historic
service states. General tab, number of days to keep service history and how long
to keep statistics. Right click any field and select Help for the rest.
Section 3.7, page 25.

## Maintain or update the installation

1. Block logons through MUCS, with the MUCS window Disable logon, the Block Users
   window, or `SCD.exe -blocklogon`.
2. Shut down users, interactive first then batch, with the Shut Down Users window
   or `SCD.exe -shutdown`. This does not affect processes running on the platform.
3. Restart the platform. Because logon is blocked the agents will not start up.
   They wait, running from local disk, holding no resources in netroot, MUCS or
   the database, and start the platform again once they can log on.
4. Update the installation, for example install a new INS file.
5. Re-enable logon in MUCS.

Section 4.2, pages 33 and 34.

## Restart the platform

```
ScdSvcCtl.exe platform restart -reason:"Restarting platform"
```

or Restart in the Platform ribbon group of the Service Manager. The orchestrated
restart shuts every service down, in dependency order where a model is
operational, waiting for pending actions to finish. Agents unload and disconnect,
and when the last one has gone they all start again in a coordinated fashion, and
the services in the model start automatically. **The manual is internally
inconsistent on manual services here.** Section 4.3 page 34 reads "The Service
Platform does start manual services after a platform restart", immediately
followed by "Use automation to ensure that your system is automatically restored
after a restart". The Restart row of the automation mode table at section 6.1.10
page 61 says "You will need to restart manual services after you suspend the
Service Platform". Treat manual services as needing a manual restart, plan for
it, and verify in a non production environment rather than quoting either
sentence to a client as settled.

Restarting individual agents instead produces waste error messages in the logs.
To restart one agent, right click its controller service in the Service Manager
and select Restart Agents, or use `ScdSvcCtl.exe agent restart -id:<agent>
-reason:<reason>`. Restarting several requires a reason.

The orchestrated restart requires modify permissions on
`<netroot>/maintenance/lock` for the main agents running the automation service.
Missing permissions cause uncoordinated restarts, visible in the automation
service log. The restart affects only SimCorp Dimension services, the Windows
services representing the agents stay up, and the restart appears in the Windows
Event Log. Sections 4.3 and 4.4, pages 34, 35 and 36.

The Lock folder at `..\Maintenance\Lock` holds a `.nostart` file, created first to
stop new agents starting, then a `.stop` file once all services are stopped, which
stops running agents. All agents need read access, main agents need read and
write. Section 4.4, page 36.

## Firewall and fixed ports

By default application services use dynamic ports, a different one each start.
Behind a firewall they must be fixed. Service Administration section 3.9,
pages 25 and 26, and Service Configuration chapter 8, pages 67 to 71.

Typical fixed ports:

| Configuration | Port | Set where |
|---|---|---|
| Connectivity to the directory service | 49152 | System Environment Configuration |
| Connectivity to the system services | 49152 | Service agent |
| Connectivity to the application services | 49153 | Service Type Configuration |

Procedure, per machine hosting agents: look up the dynamic port range and
subtract two, activate the Net.Tcp Port Sharing Service by setting it to
Automatic startup, configure it in `SMSvcHost.exe.config`, then start or restart
it. Then per agent, fix the system service port. Then once in SimCorp Dimension,
fix the directory service port in System Environment Configuration and the
application service port in Service Type Configuration.

```
netsh int ipv4 show dynamicport tcp
netsh int ipv4 set dynamicport tcp start=49154 num=16382
```

Net.Tcp Port Sharing lets several services share one TCP port instead of each
opening its own, and the users starting the services must be specified in its
config so unidentified users cannot talk to them.
