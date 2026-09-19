# 04 — Config files, ports and CDL, as they actually appear in this environment

Manual references `commserv.pdf` §4; counts and snippets from the `ComSrv` tree exported
2026-08-18 (71 config XML, 241 cartridge XML, 711 XSLT, 55 solution folders).

## A. The three file types (§4.2)

| File | Role | Naming in this tree |
|---|---|---|
| Configuration file | Container for the solution: declares ports, reads configuration parameters, lists cartridge files and test cases | must be XML with a `config` prefix; here `Config.xml`, `config.Alts.xml`, `Config_NW_NBIN.xml`, `Config.sc-Ftp.xml` … |
| Cartridge file | Handlers = business logic + data flow, written in CDL | `cartridge.*.xml`, `Cartridge_*.xml` |
| Style sheet | XSLT transformation, called by `<transform apply="…">` | `*.xslt` (711 of them) |
| Schema | XSD validation via `<schemacheck>` | 3 in the tree |

Config skeleton, as used by every solution here:

```xml
<Config Version="x.y">
  <Constant Name="…" Value="@confparam(Local,…)" />   <!-- or @const(…) chaining -->
  <File|Dimension|Oraq|Ftp|Webspheremq|Memory|Persistence|Sequencer|Timer|
       MailSender|AzureBlobStorage|WebRequest|Port  Name="…" … />
  <Cartridge>cartridge_x.xml</Cartridge>              <!-- order = load order -->
</Config>
```

Every port needs a `Name` — that is the identifier CDL uses in `<send>`. Ports over an
external queuing technology also need the physical `Queue` name. `Listen="yes"` means the
port is monitored and at least one handler must exist for it.

## B. Port/adapter census — what this environment actually uses

Counted across the 71 config files (files using it / total occurrences):

| Element | Files | Occurrences | Note |
|---|---|---|---|
| `<Dimension>` | 53 | 213 | The SimCorp gateway/AQ port — dominant type |
| `<File>` | 46 | 170 | Drop/poll/archive/log ports |
| `<Oraq>` | 13 | 27 | Raw Oracle AQ interop (GAIN, CAM, TP_TC_RFR) |
| `<Persistence>` | 13 | 18 | In-flight state (`Lifespan`, `RemoveAtStartup`) |
| `<Memory>` | 6 | 19 | Internal chaining, `DLSLink` |
| `<Port Type="file\|dimension">` | 6 | 21 | Legacy generic style (DA_CAM CorpAct, TP_TC_X_*) |
| `<Sequencer>` | 5 | 6 | Ordering/packing (`MessageFailTreatment`) |
| `<Webspheremq>` | 5 | 11 | IBM MQ |
| `<Ftp>` + `<FtpSSH>` | 5 | 5 | SFTP — only DA_BLOOMBERG's has a `DeadletterPort`; FNDS_SFTP_SRV ×3 and DM_COPP_CLARK have none |
| `<Timer>` | 3 | 5 | Polling (`Period`, `PeriodUnit="sec"`) |
| `<MailSender>` | 2 | 2 | SMTP for `<sendemail>` |
| `<AzureBlobStorage>` | 2 | 4 | MDATaaS / PE_F_CORE |
| `<WebRequest>` | 2 | 2 | SOAP (SCDRCONNECT → ODA) |

There is **no** `<Http>`, `<WebService>` or `<Sftp>` element anywhere: SFTP is always
`<Ftp><FtpSSH …/></Ftp>`, and the only web-service port type is `<WebRequest>` (SOAP —
no REST/JSON port exists in this environment).

Port categories the manual defines (§4.5): Message Oriented Middleware (queueing,
guaranteed delivery, Submit **and** Listen), File Oriented Middleware (Submit/Listen but
no queueing — **cannot load-balance**), Web Request (query only, no Listen), Auxiliary
(special purpose, may support only one direction).

## C. Parameter resolution — how a value gets into a port

```
@confparam(Local,  NAME)   ← Communication Server Setup, Configuration parameters (462 uses)
@confparam(Global, NAME)   ← Service Options → Communication Server
@confparam(Directory, NAME)← System Environment Configuration → Directories (19 uses,
                              e.g. MEDIATORSC, ACTIVEDATA, INTERFACES, RECONCILIATION)
@confparam(Standard, NAME) ← installation info (3 uses, e.g. STATE, VERSTXTSHORT)
@const(NAME)               ← a <Constant> declared earlier in the same config file
```

`AQ_PACKAGE`, `AQ_CONNECT`, `AQ_ENCODING` are consumed via `@const()` in nearly every
Dimension/Oraq config **without being declared in the file** — SimCorp Dimension generates
them into the solution at start-up. Do not "fix" them by hand-declaring them.

## D. Cartridge structure and CDL (§4.2.2, §4.8)

```xml
<cartridge Version="1.2">
  <inputport port="PortName">
    <handler label="SomeLabel" output="msg"> … CDL … </handler>
    <handler label="(Default)" output="msg"> … </handler>
  </inputport>
</cartridge>
```

CDL is XML, **case-sensitive**, must be well-formed or the Mediator throws on load.
Commands are elements; parameters are attributes; attribute functions look like
`@function(args)`. Data variables are created by `output=` attributes and are **local to
the handler** — they cannot be used before they are initiated. `@vartype()` tests the type.

Statements you will meet in this environment:

| Statement | Use |
|---|---|
| `<send input= port= label= />` | Fire-and-forget. Preferred |
| `<query …>` | Synchronous — blocks the port until answered. Limit its use (§7.2.6) |
| `<transform input= apply= output= engine=>` | Apply XSLT. `engine="Automatic"` is the manual's value for enabling XSLT 2.0; `engine="XmlPrime"` is used in this environment's cartridges but is not documented in either manual |
| `<extractdata input= output= delimiter= columntitlenames=>` | Flat/CSV → XML |
| `<getvalue>` / `<setvalue>` / `<loadfile>` | Read XPath / set a value / load a file |
| `<select><case><default>` , `<if>` , `<ifelse><then><else>` , `<foreach>` | Control flow |
| `<try><do><catch exception="…">` , `<throw>` | Error handling — the main pattern here |
| `<notify message=…>` | Writes to the Switchbox log event list |
| `<criticalsection><lock><timeout>` | Force single threading (Oracle `DBMS_LOCK`) |
| `<portstart>` / `<portstop>` | Start/stop listening on one port from a handler |
| `<movefile> <copyfile> <writefile> <deletefile> <appendfile> <createdir> <xmlfilesplit>` | File operations |
| `<sendemail fromaddress= toaddress= server= subject= body=>` | Uses a `<MailSender>` port |
| `<receiveall port= output= received=>` | Drain a port (the FNDS_SFTP pattern) |

## E. Gateway commands — the modern way to call SimCorp Dimension

Instead of hand-building the XML `<Command>` structure and sending it to `SCIn`, a handler
can call a Gateway command directly. The full list (`commseri.pdf` §11.1):

`scdAlert_Create` · `scdDataMapper_Execute` · `scdDex_ExtractionDefinition` ·
`scdDex_ExtractionSetup` · `scdDex_ExtractsExport` · `scdFtb_DfsImportBaseFilter` ·
`scdFtb_DfsImportDirectFilter` · `scdFtb_DfsImportUserFilter` · `scdLog` ·
`scdMsgQ_InsertMessages` · `scdMsgQ_UpdateMessages` · `scdStpQ_InsertMessages` ·
`scdStpQ_UpdateMessages`

Per-command parameters are **not** in either manual (§11.2 is a stub) — they are on the
Mediator **Help tab**. Say so rather than guessing a signature.

House error pattern in this environment (Nicola-built solutions):

```xml
<catch exception="except">
  <scdLog message="***[ERROR]: @var(except)" />
  <scdAlert_Create errorMessage="Error in Port '@msg(port)' with label '@msg(label)'.
                   Please investigate. Error: @var(except)"
                   systemName="@const(AlertSystemName_NW_NBIN)" flowStep="@unique()" />
</catch>
```

13 of the 55 solution folders declare an `AlertSystemName_*` constant fed by an `ASN_*`
local parameter — that constant is the link between a Comm Server failure and the alert
the operations team sees. If an interface fails silently, check whether it has one.

## F. Two rules that catch people out

1. **Cartridges are transport-agnostic.** `DA_CAM` binds the *same* `cartridge.scCamGain.xml`
   from a WebSphere MQ config and an Oracle AQ config. Re-pointing an interface between
   transports is a config-file change, not a logic change.
2. **A referenced port need not be declared locally.** `DM_ALTS`, `SIM_ALTS`, `TP_TC_APL`,
   `TP_TC_RFR` and `TP_TC_TM` all `send … port="DLSLink"` but none declares it — it is
   declared in `DM_DLS_LINK/config.scDLSLink.xml` as `<Memory Name="DLSLink" Listen="true"/>`.
   Those solutions only work when that directory is loaded into the same server. Removing
   `DM_DLS_LINK` from a setup silently breaks the lineage logging of five interfaces.
