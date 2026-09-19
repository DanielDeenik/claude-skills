# Service type configuration, capabilities, tags, rebalancing and scaling

Source: Service Administration user manual, March 2026, sections 6.3, 6.4, 7.1,
7.2, 7.3 and 7.5.

## Service Type Configuration window

Global configurations per service type. New in the Actions ribbon group on the
Home ribbon, then select Service type and Configuration where applicable. Select
(All) for settings that apply to every service. Open Configuration in the Actions
ribbon group opens the service specific window, for example Front Office Holding
Service Configuration.

Some service types require a configuration. **Even where the configuration is
mandatory you can still create an entry without one, which then acts as a common
entry for that service type, similar to (All) but scoped to the type.** This is
worth knowing when a service is running under a configuration name nobody
recognises.

Tabs:

| Tab | What it sets |
|---|---|
| Capabilities | Capability checks required for this service type. |
| Communication | Port and throttling for the service type. |
| Application Parameters | APL command line parameters for services with an APL instance. These pre-populate the Start service window and can be changed before starting. Automation always uses the parameters from this window when they exist. |
| Recovery and Blacklisting | Start attempt behaviour on failure. See `03-blocking-blacklisting-recovery.md`. |
| Miscellaneous | Shutdown Grace Period, default indefinitely. Desktop Heap for some types, typically 512 KB to 2048 KB. GC Server enabled or disabled. APL Session Pool Size, the maximum APL sessions in the pool for one instance. Maximum Concurrent User Sessions per instance. |
| Tracing | Application trace definition for this service. |
| Scaling | Minimum and maximum instances. Only for the Calculation service and worker services. |

Section 7.1, pages 80 and 81.

## Capability checks

A service can only start on agents where its capability checks are valid. When
the platform starts a service it matches required capabilities against the agents
to pick one. Two worked examples from the manual: restrict a service to specific
machines through a registry key check, and restrict web enabled dashboard
services to machines holding a valid certificate.

Define them in the Service Capability Checks window:

- **Name** and **Description**.
- **Check type**, one of Certificate Exists, Environment Variable Exists, File
  Present Check, Registry Key Exists, Windows Service Started.
- **Check argument**, for example a certificate thumbprint or a file location.

Apply them on the Capabilities tab of the Service Type Configuration window, by
right clicking the grid and inserting a capability. Open Capabilities in the
Configuration ribbon opens the checks window from there. The In use check box
marks checks that are used somewhere, and those cannot be deleted.

Re-evaluate all checks with Update Capabilities in the Platform ribbon group, or
from the Service Control Utility. Section 7.3, pages 82 and 83.

**Capabilities are the first thing to check when a service starts on one agent
and not another.** `ScdSvcCtl.exe service explain` prints the capabilities an
agent satisfies.

### Online certificate verification

The Certificate Exists check verifies the certificate against the certificate
revocation list online by default, which requires internet access from the server
where the agent runs. Without internet the check can take minutes and delay agent
start up. Turn it off in System Environment Configuration, Services tab, by
clearing Online certificate verification in the Capability checks section, after
which only the certificate validity time is checked. The equivalent cnf.ini
parameter is `SVCOnlineCertVerification`, 1 enabled and 0 disabled, and the per
agent command line arguments are `-onlinecertificateverification+` and
`-onlinecertificateverification-`, aliased `-OCSP+` and `-OSCP-`. Settings in
System Environment Configuration are saved to cnf.ini, so write access to that
file is required. Section 7.3.1, pages 83 to 86.

### Parameter variables in check arguments

A variable inside hashtags can stand in for a path that varies between
installations, for example `#MYDIRECTORY#\thisfile.txt` expanding to
`C:\myfolder\thisfile.txt` when `MYDIRECTORY=C:\myfolder`. Define variables in
System Environment Configuration, Directories tab, Additional definitions
section. A variable can also take an environment variable as its value. No
restart of SimCorp Dimension is needed, the update applies when capability checks
are updated. Section 7.3.2, page 86.

## Service tag mapping

Binds service types and configurations to groups of agents, set at deployment
time.

```
ScdSvcAgent.exe -install -serviceagenttag:MARKETDATASERVER
```

Then in the Service Tag Mapping window, press enter to load, right click, Append
row, choose Service type, optionally a Configuration with F4, and enter the Tag.

**Tags are exclusive.** A tagged agent will not run any service that does not
require the tag. That makes hardware use less efficient, and installing several
agents on the same machine is the documented workaround. SimCorp says to use tag
mapping for exceptional cases only, because it reduces the platform's ability to
manage the system, and recommends capability checks instead, with one exception:
**for the new Order Manager architecture service tag mapping is recommended.**
Sections 2.5 and 7.2, pages 14, 15, 81 and 82.

## Garbage collection

Workstation garbage collection is designed for desktop applications, collecting
more often with shorter pauses. Server garbage collection is optimised for high
throughput, using more memory but processing more data before collecting. GC
server is enabled by default for all services, but whether a given service type
uses it is a per type default defined by SimCorp. Set it on the Miscellaneous tab
of the Service Type Configuration window as Default, Enabled or Disabled. The GC
server column in the service catalogue shows the per type default. Remove the
functionality system wide by changing `allowgcserver` in cnf.ini from 1 to 0.
Section 7.5, pages 87 and 88.

## Rebalancing

Redistributes reschedulable services without configuration across agents, based
on load index, recalculating every 60 seconds.

What happens: a reschedulable service running on an agent whose load index is
high to very high, yellow to red, is moved to a comparable agent in the low to
very low range, blue or green. The move appears in Pending Actions with action
type Move, and the service being moved has management mode Transitional while the
move runs. The new instance starts on the receiving agent, the old instance
finishes its current job before stopping, then the started service resumes its
normal management mode and inherits the nickname. When the old instance stops the
Move action disappears from Pending Actions.

To enable:

1. Service Manager applet in System Manager.
2. OPERATION MODE ribbon group, select Maintenance mode. **Rebalancing cannot be
   enabled or disabled in production mode.**
3. REBALANCING ribbon group, select Enable.

Set the load index thresholds first, in Service Options, Service platform tab,
Service agent thresholds. Disable rebalancing when no reschedulable service
should move during a maintenance period. Command line equivalents are
`rebalancing enable`, `rebalancing disable` and `rebalancing getmode`.
Sections 6.3 and 6.3.1, pages 65, 66 and 67.

Which services are reschedulable is shown in the Reschedulable column of the
service catalogue.

## Scaling

A model can specify a minimum and maximum number of running instances so the
Automation service scales within that range, for example four to 20 Calculation
service instances. Instances start when workload rises past the capacity of the
running ones and stop when it falls, keeping the minimum. The platform checks
workload once a minute. The range appears on the arrow in the Graph system view.

**The Elastic Services sales module is a prerequisite.** Currently available for:

- Calculation service without specified configuration
- APL worker service
- Pricing and key ratios worker service
- Data clean-up service
- Configuration service

Set it in the Service Dependency Editor: open the model, select the service on
the Content tab, click Edit, and set the Minimum field and the maximum.
Section 6.4, pages 67 to 69.
