# Blocking, blacklisting, recovery and alerts

Source: Service Administration user manual, March 2026, sections 5.1.3, 5.3.6,
6.2 and 6.2.1.

## Blocking a service type

Blocking prevents a service type from starting at all. It works from the System
Manager and from the Service Control Utility. All non system service types can be
blocked, for example during maintenance. Three levels are possible:

- Block a service type that has no configuration.
- Block a service type for one specific configuration. Other configurations of
  the same service type, and service types without configurations, are not
  affected.
- Block a service type and all of its configurations.

To block from the Service Manager:

1. Service Manager ribbon of the System Manager window.
2. SERVICE group, click Blocks to open the Blocks sub window.
3. Click New.
4. In Edit Block, select the service type in the Service type field.
5. Optionally select a specific Configuration.
6. Optionally enter a Reason explaining why the type is blocked.
7. Click OK, repeat for further types, then save and close the Blocks sub window.

A blocked service type will not start until it is deleted from the Blocks sub
window. When blocks exist, an icon for this appears in the automation state
model. Section 5.1.3, pages 40 and 41.

## Blacklisting

Blacklisting is how automation communicates that a service cannot be started even
after several attempts. A blacklisted service requires manual intervention.

While a service is blacklisted, automation ignores its state when evaluating
service dependencies, so that a single failing service does not hold up start up
of the rest of the system. This is important when reading an automation state
graph: the rest of the model can look healthy while one service is quietly
excluded.

Blacklisted model groups and services are marked with the attention icon in the
Automation State view. Monitor the Alerts Inbox for blacklisted services.
Section 6.2, pages 62 and 63.

## Recovery and blacklisting parameters

Set globally and per service type in the Service Type Configuration window, on
the Recovery and Blacklisting tab.

Options:

- Inherit, to take the default setting. For the (All) service type this option is
  called Default.
- Infinite start-up attempts of automated service.
- Limited start-up attempts of automated service.

Fields:

- Minimum interval between start-up attempts (seconds).
- Number of start-up attempts before blacklisting. Range 1 to 1000, **default 3**.
  The field is only enabled when Limited start-up attempts is selected.

Section 6.2.1, page 63.

## Service Control Utility commands for blacklisted services

Full deployment mode:

```
ScdSvcCtl.exe platform explain
ScdSvcCtl.exe blacklist list
ScdSvcCtl.exe blacklist closeall -servicetype:214
ScdSvcCtl.exe blacklist close -servicetype:214
```

`platform explain` returns existing problems in the Service Platform including
automation issues caused by blacklisted services or configurations. `blacklist
list` lists currently blacklisted services and indicates the service types or
configurations that are relevant for the active automation model. The two close
commands close blacklist alerts, either all of them or those for one service
type.

Simple deployment mode uses the same verbs behind
`scLaunchConsole.exe -product=scd -installation=<installation root> -command=ServiceControl --`.

Section 6.2.2, pages 63 and 64.

## Alert types for services

Open the Alerts Inbox applet in the System Manager window, or click Show Alerts
Inbox in the Service ribbon group of the Service Manager. Alerts group into these
service types.

| Alert | Meaning and first action |
|---|---|
| Service instance restriction violation | Some service types restrict how many instances may be started. Check the Instance restriction column in the service catalogue for that type. |
| Service is blacklisted | The service could not be started after the configured number of attempts. Check the log file, close the alert, then try to restart the service. Use the Log Viewer in System Manager, or right click in Service Manager and select View Service Log. |
| Service is faulted | The service has failed and is not running. Check the log by clicking Log from the Service Platform ribbon. |
| Service is stale | The service does not respond. The agent has stopped sending periodic updates about its services to the platform, for example after a network failure or a server being turned off. |
| Service licence exceeded | Licences must be purchased for some services, specifically the calculation service, the message queue service and the batch service. The alert fires when the licence is exceeded. |

Section 5.3.6, pages 50 and 51.

## Stale data in the pivot

Stale information is marked in the Service Manager pivot with a small grey
triangle in the upper right corner of the cell holding the stale data. It appears
when a service agent stops sending periodic updates about its services. Causes
include network failure, servers turned off, a crashed service agent or a
firewall being enabled. The triangle disappears when the agent resumes sending
updates. Section 11, page 101.

## Automating alert clean up

Closed alerts are deleted automatically by the data clean-up service every 24
hours. This covers system operation alerts related to system runtime
measurements, services and telemetry. The number of days to keep closed alerts
before deletion must be set, otherwise they are not deleted at all.

1. Open the Miscellaneous Options window.
2. Miscellaneous-3 tab, Alerts section, enter the number of days.
3. Click OK.

A rule in the Business Rules Manager window can send an email when an alert
appears in the Alerts Inbox. Section 5.3.6, page 51.

## Reading a blocked or blacklisted situation correctly

Three states look similar in a screenshot and are not the same thing.

1. **Blocked.** Someone deliberately added the type, or the type plus one
   configuration, to the Blocks sub window. It will never start until removed.
2. **Blacklisted.** Automation tried and gave up. There is a root cause in the
   service log, and an alert in the inbox.
3. **Disabled in the model.** The service or its group has the Enabled check box
   cleared in the Service Dependency Editor. Automation does not try at all, and
   the Automation State command carries an exclamation mark.

When a service is both blocked and blacklisted, the display shows blocked.
Section 6.1.3, page 56.
