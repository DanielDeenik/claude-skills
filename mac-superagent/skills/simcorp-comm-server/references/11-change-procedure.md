# 11 — Changing a Communication Server safely

## A. Decide which level the change belongs to

| You want to change | Level | Live? |
|---|---|---|
| A directory, pattern, credential, switch, queue name, DEX name, timeout | Setup → **Configuration parameters** | **Yes** — applies while the service runs |
| A port, its attributes, a cartridge list, a test case | **Configuration file** in a Protected File Directory | No — restart Mediator service or Reload |
| Which labels the solution may exchange | Setup → **Message types** | No — restart or Reload |
| Which solutions run together, server type, log mode, log directory | **Parameter Set** | Restart the services |
| How many service instances may run | Setup → **Instance restriction** | Cannot change while any Gateway/Mediator service using the setup runs |
| Business logic, transformations | Cartridge / XSLT file in the PFD | Reload picks these up |

Design rule (`commserv.pdf` §7.1): keep solutions small and self-contained, and integrate
at the **Parameter Set** level rather than by stuffing several interfaces into one setup —
"a change to another physical server is simple to implement" and it is easier to maintain.
This environment mostly follows that (one setup per parameter set); `SE_CUST_ADDON` and
`NW_MAIN` are the two grouped exceptions.

## B. Changing a local configuration parameter (the safe, live change)

1. Communication Server Setups → open the setup → Configuration parameters.
2. Add/edit the Parameter ID and text. Tick *Password* for secrets; set *Installation* only
   when the value must differ by STATE (PROD vs TEST) — it is applied only when the text
   matches the current STATE.
3. Save. It is live for running services.
4. Verify in the Mediator client → Configuration tab → Configuration Parameters → Local.

Parameter IDs used in `@confparam(Global,…)` must be UPPERCASE.

## C. Changing a file (config, cartridge, XSLT, XSD, lookup)

1. If the setup is validated: Communication Server Setups → Functions → **Validated Files**
   → *Clear Validation* (this releases the files in the PFD).
2. Protected File Directories → select the directory → Status = **Edit**
   (creates `<Subdirectory>.edit`).
3. Edit through the Mediator (right-click file → Edit → change → Save) or
   Functions → *Insert File* / *Update File*. Never edit the folder on disk directly —
   such changes "can be ignored and overwritten". Max 3000 KB per file (1500 KB compressed).
4. Format and *Validate against schema* in the editor before saving.
5. Status = **Test** → validation runs; on failure a warning appears and status stays Edit.
6. Status = **Protected** → changes accepted, files moved to production,
   `.edit` directory deleted.
7. Re-validate the setup: Functions → **Validate Setup**.
8. Apply: click **Reload** in a connected Mediator client, or restart the Communication
   Mediator service. Config-file and message-type changes do **not** apply otherwise.

Remember which directories are shared (`SCLIB`, `AS_CA_SCLIB`, `COAC_CSD_LIB`,
`DM_DLS_LINK`, `TP_CTM_LIB`): check Functions → *Setup Server References* first to see
every parameter set and server administration setup you are about to affect.

## D. Adding a new solution — the four steps in order

1. **Protected File Directory** — subdirectory + base directory (`General` unless there is
   a reason), insert `config*.xml`, cartridges, XSLTs; set Protected.
2. **Communication Server Setup** — ID + name; local configuration parameters; message
   types (+ Active); configuration files (Subdirectory + File name, or `-` for a library);
   Save; Functions → *Validate Setup*.
3. **Communication Server Parameter Set** — ID + name; server type; log mode; log
   directory (a Reference File Name that builds a dated folder — copy the pattern of
   `ARCHON_LOG`: SimCorp directory `log` + `Servers\` + YYYY + MM + DD); add the setups and
   tick Active.
4. **Start** — System Manager → Service Manager → start a *Communication gateway service*
   **and** a *Communication mediator service* on that parameter set.

Then: *Show Setup* from the Setups window to open the Mediator on it, check the
Configuration tab for red "Not found" files, check the Ports tab, and drive a first message
through the Message Tester.

## E. Before promoting anything to Production

- Every file status **Protected**; setup validated.
- Server type Production requires both of those; *Production test* skips setup validation
  and is what most of the Nicola-built solutions run as in TEST — do not carry that habit
  into PROD without asking why.
- Check Point-2-Point collisions: only one production server per installation may hold a
  given Point-2-Point message type (here: `GAIN_REQUEST`, `SFTP_AVISO`,
  `TP_TC_CANCEL_REQUEUE`, and the Bloomberg/SWIFT standard types).
- Check no other solution already listens on the same physical folder or FTP path — file
  ports are not re-entrant.
- Give every listening port a `(Default)` handler that raises an error, and a
  `DeadletterPort` where the transport supports it. Silent discard is the default
  behaviour otherwise.
- Set an explicit `Encoding` on every port.
- Decide the log mode deliberately: *Normal* on a busy interface generates a large number
  of files and measurably slows the system.
- Add Testbench test cases for the handlers you changed, and consider scheduling the
  **Communication Service Testbench - Execute** batch task (20-minute ceiling for the whole
  scenario, and the job fails if any case fails).

## F. Scaling an interface

1. Setup → **Instance restriction**: *No restriction* / *One Gateway Instance* /
   *One Mediator Instance* / *One Instance Only*. Cannot be changed while services using
   the setup are running. Every setup here is currently *One Instance Only*.
2. Parameter set takes the **most restrictive** restriction among its active setups —
   check it on the Parameter Sets window (Restriction column) before starting instances.
3. Start additional service instances on the same parameter set from Service Manager.
4. Do not scale where message order matters — order is not preserved across instances.
5. File and FTP ports and any port with `listen="yes"` cannot load-balance.
6. Within one instance, `ProcessingMode="Parallel"` on a supporting port parallelises
   handler execution (depth = number of processors; breakpoints disabled). Guard shared
   files/variables with `<criticalsection>` — it uses Oracle `DBMS_LOCK`, so the schema
   user needs `grant execute on SYS.DBMS_LOCK` and `grant select on DBA_LOCK`.

## G. Rollback

There is no version history inside the Protected File Directories window beyond the
parameter-set history. Before step C, export the current files: Functions → *Validated
Files* → **Export Files**, and keep the CEI export of the setup/parameter set
(`scripts/parse_comsrv_cei.py` reads them back). That export **is** the rollback artefact —
take it first, not after.
