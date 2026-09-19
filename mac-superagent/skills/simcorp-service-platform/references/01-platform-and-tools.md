# Service Platform layers, tools and the Service Manager window

Source: Service Administration user manual, March 2026, chapters 1 and 2.

## Layers

| Layer | What it is |
|---|---|
| Service | SimCorp Dimension applications exposing functionality over the network or the database. Split into system services (core, enable the platform, for example the logging service), infrastructure services (must run all the time, for example the data clean-up service) and application services (business logic, for example pricing and key ratios). |
| Service Platform | At least one service agent plus a number of system services. |
| Service agent | Component deployed to a Windows server so that server can host services. Installation specific, not version specific. |
| Server | A Windows instance, physical or virtual. |
| Server farm | The hardware providing those Windows instances. |

Section 1.1, pages 6 and 7.

## Service agents

Agents registered in the System Environment Configuration window are the main
service agents. The main agent starts the system services and thereby starts the
platform. At least one main agent must be started. SimCorp recommends registering
two or three main agents in production. Agents deploy either locally as a Windows
service, which is the production recommendation, or in console mode, which is for
implementation and testing only. Section 1.2.1, page 8.

## System services started by the main agent

| Service | Role |
|---|---|
| API gateway service | Single entry point for all APIs, handles authentication, load balancing and rate limiting. |
| Authentication service | Authenticates the command line utility, and in Kerberos installations synchronises Active Directory users with SimCorp Dimension. |
| Automation service | Manages automated services, and owns suspend platform and restart platform. |
| Cloud authentication service | Authenticates against SimCorp Connect and issues tokens for on premise to SimCorp Evolution communication. |
| Controller service | Starts on each agent, manages the services on that agent. |
| Directory service | Holds information about running, closed and failed services, and hosts the look aside load balancer. |
| Installation service | Gives Installation Manager access to SimCorp Dimension. |
| Logging service | Collects and creates log information. |
| Service operations controller service | Finds the best fitted agent to start a service, and owns the pending actions queue that starts and stops services. |
| System operations alert service | Creates and cancels system operation alerts. |
| System support service | Runs on all agents, supports ScdSvcAgentDump.exe and the Create Dump function in Service Manager. |

The platform is up and running when all system services are running. Section
1.2.2, pages 8 and 9.

## NUMA and large processor counts

The Service Platform assigns processor affinity so Windows never reassigns a
process to a different processor group. On a NUMA server each started service is
given affinity to a single NUMA node, otherwise to a processor group. A processor
group maxes out at 64 logical processors, so servers above that must be split
into equal sized groups. Windows Task Manager cannot be used to add logical
processors to a service. Section 1.3, page 10.

## Service Manager applet

Open System Manager, click Show Applets in the Home ribbon, choose Service
Manager. Section 2.1, page 11.

### Ribbon groups

| Group | Contents and purpose |
|---|---|
| VIEW | Switch between the services pivot, the services grid, the Agents view and the automation state graph. |
| SERVICE | Start and stop services manually, configure blocked service types, open the Alerts Inbox, view logs. |
| HISTORY | Remove previous data for services listed in the pivot or grid. Stale data, closed or faulted services, or both. |
| OPERATION MODE | Production and Maintenance. Production disables the automation management options on the ribbon. Maintenance enables them. |
| AUTOMATION MODEL | Model field, Apply, Edit, Enable, Disable. Edit opens the Service Dependency Editor. Also carries scaling. |
| REBALANCING | Enable or disable monitoring and automatic redistribution of services on overcommitted agents. Runs every 60 seconds when on. |
| PLATFORM | Suspend and Restart the whole platform including automated services. Update Capabilities re-evaluates every capability check on every agent. |
| SUPPORT TOOLS | Profiling, Tracing, Performance Counters. |

Restrict Production and Maintenance to specific users so that control over
automation changes is retained. Section 6.1.3, page 55.

### Services pivot and services grid

The Service state field shows the current state of a service. The Action field
shows one of:

- Undisclosed, the service is not reporting its activity
- Idle, the service is not doing business work right now
- Executing, the service is doing business work right now

Views can be saved. Click the plus symbol in the View field to create a new one.
A workable default layout is Management mode as the first grouping on the y axis,
Service type as second level, Host name as first level grouping on the x axis.
Sections 2.1 and 5.3.1, pages 11 and 44.

### Pending Actions pane

Shows the actions the Service Platform is executing, in real time. Blocked and
blacklisted actions are listed here, together with blacklisted services from
automation models and their start retries. A failed automated start appears in
the queue with the reason "Service faulted during start - new attempt will be
made as defined by Recovery and Blacklisting for the service type". A manual
start is visible here until it has started. When stopping multiple services the
Description carries an asterisk until a specific instance has been selected to
stop. Sections 2.1 and 5.1.2, pages 11 and 40.

### Bottom view pane

Context dependent. Selecting in Pending Actions gives the header Pending action
details. Selecting in the pivot or grid gives Service details. Selecting several
instances gives an overview, and the Instance link opens the details of one
instance while the symbol to the left of it opens the service log. Section 2.1,
page 12.

### Filter pane

Custom filters live in the left pane, for example only faulted services or only
calculation services. A custom filter must belong to a root folder, and the owner
of that root folder can authorise other users to access it. Right click the All
node, New Root Folder, then right click the folder and select New Filter.
Sections 2.1 and 5.3.2, pages 12 and 45.

### Automation state view

Graph of the automation state for the selected strategy.

- Dependency strategy shows the automation model that is currently applied.
- Infrastructure strategy is dynamic. It builds a model from all infrastructure
  services plus load balancer services where load balanced services exist.

The view expands fully, combines services by state, combines all services, dims
online services to highlight what is not online, shows aggregated state symbols
on model groups, and zooms. Section 2.1, page 12.

## Service Dependency Editor

Defines a service dependency model: which services run at any given point in
time and how they relate to each other. Section 2.2, page 13.

## Service Control Utility

Command line access to the platform, for scripting. `ScdSvcCtl.exe` in
`netroot\bin` for full deployment mode. `scLaunchConsole.exe` with
`-command=ServiceControl` for simple deployment mode. Section 2.4, page 14.
Full command set in `05-service-control-utility.md`.

## Service Tag Mapping

Binds service types and their configurations to specific service agents. A tagged
service type can only start on an agent with the same tag, and a tagged agent
will not run a service without a corresponding tag. SimCorp recommends the
Service Capability Checks window instead, for flexibility, with one stated
exception: for the new Order Manager architecture, service tag mapping is
recommended. Sections 2.5 and 7.2, pages 14, 15 and 81.
