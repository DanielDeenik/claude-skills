# Automation service models and the Service Dependency Editor

Source: Service Administration user manual, March 2026, chapter 6.

## What automation does

The Automation service detects changes in the system and starts or stops services
in response, according to a single service dependency model at a time. If the
agent hosting a service shuts down, automation detects the missing service and
starts a new instance on another agent. Services started manually are not touched
by automation. The Management mode field distinguishes manual services from
automated ones. Multiple models can exist and be switched between, for example a
working day model, a reduced weekend model and a period closure model. SimCorp
recommends using automation in production, at least for the most fundamental
services. Section 6.1, pages 52 and 53.

## Model elements

- **Model groups.** Named containers for services that work together. Every model
  contains a System group, and automation only refers to the System group and its
  relations. Model groups not related to the System group are ignored.
- **Service dependencies.** A group can contain other groups, and a group can
  belong to several groups. Starting the parent starts the children. Automation
  takes these into account when starting or stopping whole chains.
- **Time dependencies.** A group can be limited to a time period of the day.
  Outside that period the group appears inactive to automation and its services
  are shut down.
- **Scaling.** A minimum and maximum instance range per service. Requires the
  Elastic Services sales module.

Sections 6.1.1 and 6.1.6, pages 53 and 58.

## Create a model

1. Open the Service Dependency Editor window, or click Edit in the Automation
   ribbon group, which opens the active model by default.
2. Press ctrl and n to create a new model.
3. Enter a name in the Model field.
4. Click the System group in the Model groups pane.
5. Click Add service on the Content tab.
6. In the Add service dialog specify Service type, Configuration if applicable,
   and Count, which is the number of instances of this service.
7. Click OK, add more services as needed, and save.

To add a group: right click in the Model groups pane, Append row, name it, add
services to it with Add service, then select the System group or another group
and use Add group on the Content tab to attach it. Sections 6.1.2 and 6.1.6,
pages 54 and 58.

## Activate a model

Changing the model can have a significant impact on the installation, so models
can only be switched in Maintenance mode. Maintenance mode does not affect the
installation, it gives access to platform wide functionality and exists as a
protection against accidental use. Section 6.1.3, page 55.

In the Service Manager applet:

1. Operation Mode ribbon group, click Maintenance.
2. Model field in the Automation Model ribbon group, select the model, click Apply.
3. Click Enable in the Automation Model ribbon group to ensure automation is on.
4. Click Production to end maintenance mode. The model is now active.

In the Service Control Utility, full deployment mode:

```
ScdSvcCtl.exe maintenance begin
ScdSvcCtl.exe model list
ScdSvcCtl.exe automation enable
ScdSvcCtl.exe automation load -model <modelname>
ScdSvcCtl.exe maintenance end
```

Simple deployment mode uses the same verbs behind
`scLaunchConsole.exe -product=SCD -installation=<installation> -command=ServiceControl --`,
with `automation load -model=<modelname>`.

**The active model is marked with an asterisk in the model list output.** Section
6.1.3, pages 55 and 56.

If the model contains blacklisted or blocked services it will not be fully
operational. Blocks are visible in the Automation State view in the same way as
blacklisting, and a service that is both blocked and blacklisted displays as
blocked. Section 6.1.3, page 56.

## Modify a model

Non active model: open the Service Dependency Editor, press F5 and select the
model, select a service on the Content tab, Edit, then save. Section 6.1.4,
page 57.

Active model: open the Service Manager applet, click Edit Model in the Automation
Model ribbon group, which requires access to the Service Dependency Editor
window, make the change and save. **All changes to the active model take
immediate effect on save, and a pop up warns before saving.** Section 6.1.5,
page 57.

## Disable services and groups inside a model

Disabling removes a service or group from the model without deleting it.
Disabling a group disables all its subgroups and services.

- Group: select it in Model Groups, then clear the Enabled check box on the
  Content tab.
- Service or submodel group: select it on the Content tab, click Edit to open
  Edit service or Edit group relation, and clear the Enabled check box.

Disabled items are greyed out in the graph. In the Service Manager applet
disabled services and groups are not shown in the automation model graph, but
applying a model that contains them raises a note in the window, and this is also
visualised by an exclamation mark on the Automation State command in the View
ribbon group. Section 6.1.7, pages 58 and 59.

## Time constraints

Select a group in the Model groups pane, open the Time constraints tab, select
the Enable daily between radio button and set the interval. Drag the slider in
the Service Dependency Editor to simulate which groups are active through the
day. Active groups appear green, inactive groups grey. Section 6.1.8, page 59.

## Review and monitor

A graphic overview of a whole model is available from Graph in the System view
ribbon group of the Service Dependency Editor, with the same 24 hour slider.
Section 6.1.9, page 60.

Automation State in the VIEW ribbon group of the Service Manager applet shows the
progress of automation while a model is being applied, per service and per model
group, and Pending Actions shows every action the automation service is taking.
Section 6.1.10, page 60.

## Operation mode and automation mode buttons

Operation mode switches between production and maintenance. Maintenance is the
required mode for actions on the current dependency model, for example replacing,
starting or pausing it.

In maintenance mode, authorised users can replace the current model by selecting
from the drop down and clicking Apply. The automation buttons then behave as
follows.

| Button | Effect |
|---|---|
| Enable | Enables automation with the dependency model of your choice. |
| Disable | Disables automation of the current dependency model. Active automated services keep running on the Service Platform. |
| Suspend | Suspends all services except those with management mode System or External. Click Enable Automation to start suspended automated services. Manual services must be restarted by hand afterwards. |
| Restart | Restarts the entire Service Platform including system services and agents. Everything shuts down, system services last, then system services start first and the rest of the model follows. Manual services must be restarted by hand afterwards. |
| Update Capabilities | Re-evaluates all capability checks. |

Section 6.1.10, pages 60 and 61.

## Reading the automation state graph

- Green rounded nodes are model groups.
- Blue rectangular nodes are services.
- Grey rounded nodes are model groups currently disabled by time constraints.
- Grey rectangular nodes are services disabled by the time constraints of the
  group they belong to.

State icons distinguish: service running, service cannot start, service stopped
or not yet running, and service not supposed to run because the parent group is
time constrained, with a further variant for a service that is time constrained
and also blocked or blacklisted. Group icons carry the aggregated equivalent,
plus a red triangle variant meaning all underlying services are running but one
or more is time constrained and cannot start at a future point in time. Select
Dim running to highlight the services that are not online. Section 6.1.10,
pages 61 and 62.
