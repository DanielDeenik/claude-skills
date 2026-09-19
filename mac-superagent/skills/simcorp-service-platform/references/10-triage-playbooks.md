# Triage playbooks

Manual grounded decision trees first, then one worked client case clearly marked
as observation rather than documentation.

## The documented troubleshooting table

Service Administration user manual, March 2026, chapter 11, pages 101 and 102.

| Symptom | Documented cause and action |
|---|---|
| Service agent is started but appears as not running, for example cannot be reached from Service Manager | Check the Windows event log on the machines running the agents. |
| Service Manager freezes for up to a minute and stops refreshing service details after clicking a controller service | Firewall issue. |
| A service shows in Pending Actions as being started, and is still not visible in the pivot after a minute, with no progress | Firewall issue. Services being started are normally visible in the pivot. |
| Information about a service is marked stale, shown as a small grey triangle in the upper right of the cell | The agent has stopped sending periodic updates. Network failure, servers turned off, crashed agent, firewall enabled. The triangle clears when updates resume. |
| Maximum number of running service instances on an agent reached | Default limit is three times the number of CPU cores. See flooding protection. |
| Cache manager does not populate or update the local file cache | Usually a Windows security violation. Stop the agent and cache manager Windows services, start `ScdSvcCacheManager.exe` interactively from the cache manager installation, then start the agent service, and Windows will display the security message. Typically the cache manager user lacks trust to the netroot file share or cannot create symbolic links. |

Note that two separate rows point at a firewall. A stalled Pending Action is a
network symptom in the manual's own reading, not automatically a model fault.

## Playbook A: a service will not start

Work in this order and record the answer at each step.

1. **Read the Pending Actions row exactly.** Action type, Description including
   the configuration name in brackets, State, Reason. Count the rows. Two rows
   for the same service and the same configuration is itself a finding.
2. **Read the service log for that instance.** Service Manager, select the
   instance, Log in the Service ribbon group, or right click and View Service
   Log. Certificate failures, subscription failures and configuration mismatches
   all announce themselves here by name.
3. **Read the Alerts Inbox.** Blacklisted, faulted, stale, instance restriction
   violation and licence exceeded are distinct alert types with distinct causes.
4. **Run the platform commands.** `platform explain`, then `blacklist list`,
   then `automation explain` and `model list`.
5. **Check the catalogue entry for the service type.** Configuration mandatory,
   instance restriction, load balancer, scalable, reschedulable.
6. **Check whether the service type is blocked.** SERVICE ribbon group, Blocks.
7. **Check whether the service or its group is disabled in the model.** An
   exclamation mark on the Automation State command in the VIEW ribbon group is
   the tell.
8. **Check capabilities and tags.** `service explain` prints the capabilities the
   agent satisfies. A tagged agent runs nothing that does not require its tag.
9. **Check recovery settings.** Service Type Configuration, Recovery and
   Blacklisting. Three attempts by default, then blacklisting.
10. **Check the environment.** Firewall and fixed ports, certificates in the
    Windows store, cnf.ini hostnames and paths if this installation was copied.

## Playbook B: automation is doing nothing

1. Is automation Enabled or Disabled in the Automation Model ribbon group.
   Disable leaves already running services running, so a healthy looking grid
   proves nothing.
2. Is the platform in Production or Maintenance. Model changes require
   Maintenance, and the documented sequence ends by returning to Production.
3. Which model is active. Asterisk in the Model field, confirmed by `model list`.
4. Does the model actually contain the services you expect. Automation only
   refers to the System group and its relations, and ignores model groups not
   related to it.
5. Are groups time constrained. Grey nodes in the graph mean the current time
   sits outside the group's window.
6. Are services disabled inside the model.
7. Are services blocked or blacklisted. Either state stops the model being fully
   operational.

## Playbook C: a model is being replaced

1. Take the before picture. `model list`, `automation explain`, a screenshot of
   the Automation State graph and the Pending Actions pane.
2. Establish that the target model is the intended one by opening it in the
   Service Dependency Editor and reading its Content tab, not by trusting the
   name.
3. Compare instance counts against the installation sizing guidance in Service
   Configuration chapter 4, per service ID.
4. Follow the documented sequence: Maintenance, select, Apply, Enable,
   Production.
5. Verify after. `automation explain` should report automation Enabled and the
   dependency strategy state, and the Automation State graph should show the
   model settling.

Remember that editing the model that is currently active takes effect the moment
it is saved.

## Worked case, client observation, Nicola Wealth PROD, 24 August 2026

**This section records what a screenshot and an email showed. It is not
documentation, and the conclusions below were not confirmed at the time of
writing.**

Reported: Order Manager services were run in PROD with automation, they kept
failing, so automation was disabled for the OM services. An error was quoted in
the email but its text was not included.

Visible in the Service Manager screenshot:

- The Model field read `*NICOLAPFW_PREPROD`. Per Service Administration section
  6.1.3 the asterisk marks the active model, so a model named for pre production
  was the active model on hosts named NICOLAPROD01 and a second NICOLAPROD server.
- Operation Mode showed Maintenance selected, and Disable was lit in the
  Automation Model group, consistent with automation having been switched off.
- Pending Actions held two rows, both
  `Start / Order Manager - External Integration service (DEFAULT) / Processing /
  Service is starting`.
- The status bar showed 232 alerts.

Findings that follow from documentation, each with its check:

1. Two start actions for one service under one configuration name conflicts with
   Front Office Configuration section 17.20.1, which states that only one
   instance of an integration service with the same configuration can run at a
   time. Check the Count on that service in the model's Content tab.
2. Service 376 carries Configuration Mandatory in the catalogue. Check what the
   configuration named DEFAULT contains in the Order Manager API Service
   Configuration window, and specifically whether the non trading data
   subscription is included, since its absence is a documented start failure.
3. The Management service must be running before the External Integration
   service starts. Check whether the model enforces that order with a group
   dependency.
4. A stalled Pending Action with no instance in the pivot is the manual's own
   firewall symptom. Check ports 5671, 5672, 443 and 4222 on both agents.
5. Certificates for this service are configured in the OM API Service
   Configuration window and a missing one fails the start with a named log line.
6. A PREPROD model active on PROD hosts raises the question of an environment
   copy, which brings the four Copying SimCorp Dimension pitfalls into scope.

Open questions that were outstanding and should be answered before any PROD
change:

1. The actual service log text for the External Integration service and for the
   Management service.
2. Whether `NICOLAPFW_PREPROD` is the intended PROD model, and what `model list`
   returns.
3. Whether this PROD installation was copied or refreshed recently.
4. What the OM API Service Configuration named DEFAULT contains.
5. How many instances of service 376 the model requests, and against which
   configurations.
6. Whether certificates are installed on both PROD servers and the four ports are
   open on both agents.
7. Exactly which services and groups were disabled when automation was turned off.

When this case is revisited, replace the unanswered items with the answers rather
than carrying the hypotheses forward as if they were established.
