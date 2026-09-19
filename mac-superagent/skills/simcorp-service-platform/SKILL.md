---
name: simcorp-service-platform
description: >
  SimCorp Dimension Service Platform and Service Manager specialist. Covers the
  Service Manager applet, automation service models and the Service Dependency
  Editor, operation mode, starting and stopping and blocking services,
  blacklisting and recovery, service capabilities and service tag mapping,
  rebalancing and scaling, the Service Control Utility, service agent
  installation, firewall and fixed port setup, and the service catalogue with
  service type IDs. Use when a service will not start, a service is stuck in
  Pending Actions, an automation model has to be built or applied or corrected, a
  service is blacklisted or blocked or stale or faulted, agents are overloaded,
  the platform needs a restart, or someone asks which model is active. Triggers
  on Service Manager, Service Platform, service agent, automation model, Service
  Dependency Editor, ScdSvcCtl, ScdSvcAgent, pending actions, blacklisted,
  blocked service, maintenance mode, load index, rebalancing, Order Manager
  services will not start.
---

# SimCorp Service Platform and Service Manager

Grounded in the March 2026 Service Administration and Service Configuration user
manuals, the September 2025 Front Office Configuration and Copying SimCorp
Dimension user manuals. Every claim in this package cites a section. Where the
manuals are silent, this package says so rather than filling the gap.

## Scope boundary

This skill covers operating the platform that runs services. It does not cover:

- Oracle SQL trace levels and trace file handling. Use `simcorp-database-tracing`.
- SRM, System Performance Check, dotTrace profiling, Communication Monitor,
  Function Trace and the wider diagnostics toolkit. Use `simcorp-performance-toolkit`.
- Oracle optimizer statistics, AWR setup and database side tuning. Use
  `simcorp-oracle-configuration`.
- Communication Server setups, parameter sets and mediator ports. Use
  `simcorp-comm-server`.
- Front Office business flow architecture and measured latency overlays. Use
  `simcorp-fo-flow-architect`.
- Financial performance and TWR. Use `simcorp-performance-specialist`.

Tracing and profiling are reachable from the Service Manager ribbon, so this
package documents where the buttons are and hands the mechanics to the two
skills above.

## Hard rules

1. Read the screenshot, not your memory. Field names, button states and column
   headers come from the image in front of you. If a state is ambiguous in the
   image, say it is ambiguous and ask.
2. Never invent a service type ID, a window name, a command parameter or a model
   name. Every ID in this package traces to the Service Configuration catalogue.
3. Never propose a change to a production Service Platform without naming the
   evidence that supports it and the evidence that is still missing.
4. Separate what the manual says from what the client environment shows. Label
   the second as observation.
5. When an error message has not been supplied, ask for it. Most service start
   failures are named explicitly in a log line, and guessing from symptoms alone
   produces plausible wrong answers.

## The five facts that resolve most Service Manager questions

1. **The active automation model is the one marked with an asterisk.** In the
   Model field of the Automation Model ribbon group, and in the output of
   `ScdSvcCtl.exe model list`, the active model carries a leading asterisk.
   Service Administration section 6.1.3, pages 55 and 56.
2. **You can only switch models in Maintenance mode.** Production mode disables
   the automation management buttons. Maintenance mode is a protection against
   accidental use, not a resting state. The documented sequence ends with a
   click on Production. Section 6.1.3, page 55.
3. **Disable does not stop anything.** Disabling automation stops the model from
   being enforced. Active automated services keep running on the platform.
   Section 6.1.10, page 60.
4. **A failing automated service is retried and then blacklisted.** The default
   is three start attempts, set per service type on the Recovery and Blacklisting
   tab of the Service Type Configuration window. A blacklisted service is ignored
   by the dependency evaluation so that one failure does not hold up the rest of
   the system, and it needs manual intervention. Sections 6.2 and 6.2.1, pages
   62 and 63.
5. **A start action that sits in Pending Actions with no progress and no instance
   in the pivot points at a firewall.** This is the documented symptom in the
   troubleshooting table, not an inference. Section 11, page 101.

## Which reference file to open

| Question | File |
|---|---|
| What is this window, ribbon group, view or pane | `references/01-platform-and-tools.md` |
| Build, apply, edit, disable or monitor an automation model | `references/02-automation-models.md` |
| Service is blocked, blacklisted, faulted or stale, or alerts are piling up | `references/03-blocking-blacklisting-recovery.md` |
| Start or stop a service, read management mode, load index, logs | `references/04-operating-services.md` |
| Any command line action | `references/05-service-control-utility.md` |
| Install or register agents, restart the platform, fixed ports and firewall | `references/06-install-agents-and-platform.md` |
| Capability checks, service tags, service type configuration, rebalancing, scaling | `references/07-capabilities-tags-scaling.md` |
| What is this service, what is its ID, does it need a configuration | `references/08-service-catalogue.md` |
| Anything about the Order Manager service family | `references/09-order-manager-services.md` |
| A service will not start and you need a decision tree | `references/10-triage-playbooks.md` |
| Which manual and page a fact came from | `references/11-source-manual-index.md` |

## Workflow: a service will not start

1. Read the Pending Actions pane. Record the exact Action type, Description
   including the configuration name in brackets, State and Reason.
2. Read the per instance log. Select the instance, then Log in the Service ribbon
   group, or right click and select View Service Log. The log line is the answer.
   Ask for it if you do not have it.
3. Check the Alerts Inbox. Blacklisted, faulted, stale, instance restriction
   violation and licence exceeded each have their own alert type.
4. Run `ScdSvcCtl.exe platform explain` and `ScdSvcCtl.exe blacklist list`. The
   first returns existing platform problems including automation issues caused by
   blacklisted services or configurations.
5. Check the service type in the catalogue. Does it require a configuration, is
   it instance restricted, does it depend on another service being up first.
6. Only then look at the model. Open `references/10-triage-playbooks.md` for the
   ordered decision tree.

## Workflow: change an automation model

1. Confirm which model is active by the asterisk, in the ribbon and again in
   `model list` output.
2. Operation Mode, click Maintenance.
3. Edit Model to open the Service Dependency Editor. Changes to the active model
   take effect immediately on save, and a warning appears first.
4. Model field, select the model, click Apply.
5. Click Enable in the Automation Model ribbon group.
6. Click Production to end maintenance mode.
7. Verify with `ScdSvcCtl.exe automation explain` and the Automation State view.

Note that a model containing disabled services or groups shows a note when
applied and an exclamation mark on the Automation State command in the View
ribbon group. A model containing blocked or blacklisted services will not be
fully operational.

## Pre answer checklist

- Layer identified. Is the question about the platform, the model, one service,
  or the agent hosting it.
- Screenshot read field by field where one was supplied.
- Manual section and page cited for every mechanism claim.
- Client observations labelled separately from manual facts.
- Missing evidence named explicitly, with the exact place it would come from.
- No invented IDs, model names, parameters or window names.
