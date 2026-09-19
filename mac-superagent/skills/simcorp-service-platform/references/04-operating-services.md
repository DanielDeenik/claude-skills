# Operating services in the Service Manager

Source: Service Administration user manual, March 2026, chapter 5, plus sections
7.4 and 7.6.

## Start a service manually

1. Open System Manager, then the Service Manager applet.
2. Right click in the pivot grid and select Start Service, or click Start in the
   Service Manager ribbon.
3. In the Start service configuration window:
   - **Service type.** The available services are listed in the field.
   - **Configuration.** Required if the service needs one. The information icon
     in the field opens the related service configuration window, for example to
     create a new configuration.
   - **Agent.** Choose a specific agent, or let the system decide, which starts
     the service on the agent with the highest resource index.
   - **Count.** How many instances to start.
   - **Nickname.** Optional. Lets you control all services under the same
     nickname at once, from the Service Control Utility or through filters.
   - **Advanced.** Opens Management mode, Application parameters, Tracing,
     Profiling and Memory dump.
4. Click Start.
5. View the active instances in the applet. Right click an instance to stop it,
   view logs or view details.

Section 5.1.1, pages 38 and 39.

## Let automation take over a running manual service

The Allow to be Automated command hands ownership of an already running service
to automation, so it no longer has to be started and stopped by hand.

1. The operation mode must be Maintenance and the Automation model must be turned
   off for the command to be enabled.
2. In the Services Grid, right click the services concerned.
3. Select Allow to be Automated, then Yes.

This sets the management mode of those services to Automated so automation
recognises them as services it started. Only services that are not system
services and not infrastructure services started by automation can be selected,
and the option only appears on a service type that is not already automated.

The same result comes from setting Management Mode to Automated on the Advanced
tab of the Start service dialog, from the `-automated` argument on the Service
Control Utility service start command, or from adding the services to the
dependency model. Section 5.1.1.1, page 39.

## Stop services

Selected services: select in the main grid, then Stop Selected in the Service
ribbon group.

Multiple services: click Stop Filtered, then in the Stop service window enter or
select at least one of Service type, Management mode or Nickname. The number of
matching services appears under the Count label. Click Stop.

When stopping multiple services the selection is based on the resource index of
the agents. The agent with the lowest index that holds matching services is
chosen first. In Pending Actions the Description carries an asterisk until a
specific instance has been selected to stop.

Services started by the system, and external services in a service harness,
cannot be stopped from the Service Manager. Use the management mode grouping in
the pivot grid to tell them apart. Section 5.1.2, page 40.

## Balancing services evenly

When services are started without naming an application server, whether from
Start in the Service Manager, from an automation model or from the Service
Control Utility, SimCorp Dimension distributes them evenly across all available
application servers whose configurations allow starting services. It picks the
server with the smallest number of currently running or starting services of that
type, and breaks ties by the lowest Load Index. When stopping, it picks the
server with the largest number of that service type and breaks ties by the
highest Load Index. This behaviour is on by default and is disabled with the
cnf.ini parameter `DisableBalanceServicesEvenly=1`. Section 7.6, pages 88 and 89.

## Flooding protection

The maximum number of services one agent can start defaults to three times the
number of CPU cores. A four core machine therefore allows twelve instances. The
limit can be overridden at install time with `-maxrunningservices`, and accepts
between zero and ten times the number of cores. Higher values are rejected with a
warning and the platform sets the maximum to ten times the core count. Installing
several agents on one machine multiplies the limit but is not recommended,
because hardware resources are then too scarce for smooth operation. The same
risk applies to virtual machines. Section 7.4, page 87.

## Service history and grey instances

Grey instances in the pivot grid are stopped services. Their logs are still
readable. They leave the grid according to Service Options window, Service
Platform tab, "Hours to keep the historic service states for viewing". They can
also be removed by hand with Clear All or Clear Selected in the History ribbon
group. The Service History applet of System Manager shows current state, start
and end time, and the log messages per instance. Section 5.3.1, page 44.

## Agents view and load index

The Agents view in the VIEW group shows the servers hosting agents and their load
index. Load index is calculated from memory capacity, CPU usage and number of
services. Main service agents are highlighted.

The Load index field is colour coded:

| Colour | Utilisation |
|---|---|
| Blue | Very low |
| Green | Medium |
| Yellow | High |
| Red | Very high |

Thresholds are set in Service Options window, Service Platform tab, Service agent
thresholds section, as percentages across the four categories. Available memory
threshold defaults to 20 GB and influences the load index calculation. On a
machine with plenty of free memory it has little effect. Setting it too low risks
a service failing to start for lack of memory even while the indexes still show
green. SimCorp recommends setting it by trial and observation.

Right click a row for View Details, View log, or Restart Agents. The Services on
server field only appears when shared load data across multiple agents has been
enabled, and shows the total number of SimCorp Dimension services running on that
server across all installations. Section 5.3.3, pages 45, 46 and 47.

## Logs

The Single Log Viewer displays log information from System Manager applets, being
Log Viewer, Service Manager, Service History, Batch History, Batch Monitor and
Alerts Inbox, and from the Batch Jobs, Batch Jobs Groups and Communication Server
Parameter Sets windows. The button or menu item names vary, for example View Log,
View Full log, View Latest Log, View Service Log and View Batch Log, and they all
open the same window.

To read a service log: Service Manager ribbon, Services Pivot in the VIEW group,
find the instance, right click and select View Service Log, or select the
instance and click Log in the Service ribbon group. Section 5.3.5.1, pages 48
and 49.

Log message files land under a sub folder of the Log folder, for example
`<netroot>/Log`, and require LogWriter1 or LogWriter2 to be set to file in
cnf.ini. Service logs sit under
`Services\<serviceTypeInt>_<serviceType>\<short AgentId>_<InstanceId>_<hostname><UTC timestamp>_<processId>`,
for example `Services\98_AnalyticsService\98-1_Host1001_20170823_100200300`.
Order Manager logs sit under `SCD\OM_<hostname><UTC timestamp>_<processId>`.
Files split every 10 MB with a numeric counter appended. Each log line carries
timestamp in PC UTC, timestamp in database UTC where available, severity, event
number, message, event property bag, contexts and exception details.
Section 5.3.5.2, pages 49 and 50.

## Detecting slow service calls

System Environment Configuration window, Services tab, select Enable measurement
to switch on service metrics. Expected response times are near real time 500 ms,
online request 5000 ms and long running 1200000 ms by default. SimCorp Dimension
then checks the response time of individual service calls and writes a warning in
the log when the expectation is exceeded. Section 11, page 102.
