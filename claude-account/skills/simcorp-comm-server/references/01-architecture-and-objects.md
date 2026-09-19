# 01 — Architecture, windows and objects

Sources: `commserv.pdf` (Communication Server, Sept 2025) §2–§3, §5; `commseri.pdf`
(Gateway) §11.1. Section numbers below are that manual's.

## What the server is made of (§2.1)

Two components, started as two separate services against the **same parameter set**:

- **SCD Gateway** — "responsible for access to the database". Exposes the standard APIs
  through the `SCIn` and `SCOut` ports (import via a message queue, run a data extract,
  queue a batch job group). §11.1 of the Gateway manual: "The SCD Gateway is the
  Communication Server component that executes SimCorp Dimension functions on request by
  the Mediator. It then sends the results back to the Mediator for further processing."
- **Mediator** — the workflow processor. Sends/receives messages, applies workflow logic,
  transforms data with XSLT.

Distributed, asynchronous, queue-based. A solution is defined by its **configuration
file(s)** (the ports) and **cartridge file(s)** (the handlers/business logic), optionally
with **XSLT** stylesheets and **XSD** schemas. Configuration lives both in the SimCorp
Dimension database *and* on the server as XML files.

Full version vs run-time version (§2.2): in the run-time version the user has read-only
access to the windows and cannot change the interface configuration. SimCorp consultants
always have full edit access.

## Prerequisites (§2.4)

- Oracle Advanced Queuing installed and running on the database server, and a **database
  user schema** for the Communication Server (Maintenance → *Database User Schemas
  Administration*, Schema type = *Communication server user schema*; you are prompted for
  a default tablespace and a password on save).
- Queue contents are viewable/manageable in **Database User Schemas Contents**, which
  handles: Dimension port, Sequencer port, Persistence port, RAW Queue, JMS TEXT Queue,
  XML Type Queue. Limits: the Persistence port supports show/save but **not** Drop Queue
  or Delete Messages; RAW/JMS TEXT/XML Type queues support Drop Queue, Delete Message and
  List Messages but **not** Save Messages or Display Message.
- Interface packages arrive through the **Configuration Transport System**; parts are
  locked. In this environment only `PE_F_IAS` carries an interface package number (2446)
  and only `SO_ODA` has owner = SimCorp; every other setup is owner = Customer.

## Communication Server Options (§3.1)

Maintenance → System Maintenance → System Options → Service Options → Communication Server.

| Field | Meaning |
|---|---|
| User schema | The Oracle user schema used for the queueing technology. **The server cannot run without it.** |
| Base directory (protected solutions) | Where protected file directories live; set under System Environment Configuration → Directories |
| Global configuration parameters | Constants for all solutions in the installation; optionally installation-specific. Read anywhere with `@confparam(Global, <PARAMETERID>)`. The Parameter ID argument must be UPPERCASE. Tick *Password* to hide a value. |

Parameter scopes readable with `@confparam()`: **Local** (this solution's setup),
**Global** (Service Options), **Directory** (System Environment Configuration →
Directories, plus standard params such as `MEDIATORSC`), **Standard** (installation info,
e.g. `@confparam(Standard,STATE)` / `VERSTXTSHORT`). This environment uses all four.

## Protected File Directories (§3.2)

Hold and protect the solution files. Physical path created on save:
`[SimCorp Dimension directory]\ComSrv\[Base directory]\[Subdirectory]`.

- Status: **Edit** → creates `<Subdirectory>.edit` with no write protection; **Test** →
  validates the files (on failure a warning appears and status stays Edit); **Protected**
  → accepts changes, moves files to production, deletes the `.edit` directory.
- **Production setups must be Protected.** Files must not be changed directly in the
  directory structure — changes made that way "can be ignored and overwritten".
- Insert via Functions → *Insert File* (multi-select allowed); *Update File* updates a
  file without changing directory status.
- Size limit: any inserted file ≤ **3000 KB**, and its compressed form ≤ **1500 KB**.
- If a **validated** setup references the directory you must clear the validation first
  (Communication Server Setups → Functions → *Validated Files*).

All 35 protected file directories in this export are status **Protected**. Base
directories in use: `1 (General)` ×33, `5 (Bloomberg)` ×1, `6 (SimCorp)` ×1.

## Communication Server Setups (§3.3)

Defines one **solution** by binding protected file directories to it.

- **Configuration parameters** — local constants. The *Installation* field makes a value
  state-specific: "Configuration parameters are only defined, if the text in this field
  matches the current STATE (for example PROD or TEST)." Tick *Password* to mask.
- **Message types** — the gate. "If you send a message to a label that is not enabled by
  the message type, then the message is discarded." Each row has an *Active* checkbox and
  may point at a **Configurable Message Type**.
  Message distribution types: *Point-2-point* (only ONE production server with this type
  per installation), *Point-2-Point Configurable*, *Subscribe Configurable* (all servers
  with the type receive), *Broadcast* (used by the General type for log messages and stop
  server commands).
- **Configuration files** — Subdirectory (F4) + File name. Config files must be XML with a
  `config` prefix. A **dash `-`** in File name references a protected file directory
  without naming a config file (shared libraries such as `SCLIB`), or an external
  directory holding `.dll`/`.exe` (e.g. `\\server\common files\-`).
- **Functions**: *Setup Server References* (which parameter sets and server administration
  setups use this setup), *Validated Files* (view/update/clear validation, Export Files),
  *Validate Setup* (basic requirement checks; slow on big solutions), *Show Setup* (starts
  the Mediator client on this solution).
- **Instance restriction** (§5.1.1): *No restriction* | *One Gateway Instance* | *One
  Mediator Instance* | **One Instance Only** (default). Cannot be changed while a Gateway
  or Mediator service using the setup is running. Every setup in this environment is
  *One Instance Only*.

### Changing a setup while it runs (§3.3.6) — hard rule
Local **Configuration parameters** can be changed while the Mediator/Gateway service runs.
**Message types and Configuration files cannot.** Those take effect only after restarting
the Communication Mediator service or reloading through a connected Mediator client.

## Communication Server Parameter Sets (§3.4)

- **Server type**: *Inactive* (temporarily disabled) | *Production* (normal; all files
  must be Protected and setups valid) | *Production test* (starts without validating the
  included setups) | *User test* (bound to a user ID; only effective while the server is
  up; used for local development so other users' messages are not consumed).
- **Log mode**: *Normal* (all messages logged) | *Ignore OK messages* (only notifications
  and errors). **Log directory** = a Reference File Name (F4). Leave empty and messages
  appear only in the Switchbox log. Manual's own warning: Normal mode "can result in
  excessive use of space and can have a negative impact on the performance"; create a new
  directory per day so old files can be purged.
- Oracle AQ names appear automatically in *Queue information*, prefixed with the parameter
  set name.
- Only **Active** setups load at start. Active/inactive can prepare a fail-over pair.
- Functions → *Show Parameter Set Log* and *Show Parameter Set History* give the combined
  view across all scaled services using that parameter set (§5.1.3).

## Starting the server (§3.5, §3.6)

System Manager → Service Manager → Start, service type **Communication gateway service**
and **Communication mediator service**, both on the same parameter set. Behaviour when a
port protocol (e.g. a folder for a file port) is unavailable:

| Parameter set mode | At start-up | Losing a port while running |
|---|---|---|
| Production | Mediator **shuts down** | Reconnects a number of times, then shuts down; Service Platform restarts it if configured |
| Production test / test | Starts in **stale state** — monitor shows "running", nothing is processed | Same reconnect/shutdown, but it will restart even if the port is still unavailable |

The *Communication Mediator Service* type ignores "Number of start-up attempts before
blacklisting"; the *Communication Gateway Service* type honours Recovery & Blacklisting.

## Scaling (§5)

Multiple instances of both services can run on one parameter set. The parameter set takes
the **most restrictive** instance restriction of its active setups. Load balancing needs
two or more services running the same solution — but **file-oriented ports do not support
it**, and neither do ports with `listen="yes"`. Parallel message processing is a port
attribute (`ProcessingMode="Parallel"`); breakpoints are disabled on such ports, order is
not guaranteed, and `<criticalsection>` (Oracle `DBMS_LOCK`; needs `grant execute on
SYS.DBMS_LOCK`) is the way to force single threading around a shared file or variable.
