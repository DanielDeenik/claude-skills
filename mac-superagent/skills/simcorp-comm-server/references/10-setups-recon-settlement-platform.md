# 10 — Setup cards: reconciliation, settlement, outbound transport, performance, platform

Five of these share one parameter set: **`SE_CUST_ADDON`** (Settlement/Reconciliation –
Custodian Add-on, Production, Ignore OK messages, log `SE_CUST_ADDON_L`) with
`AS_PAID_TAX_RCL`, `RC_ASH_RECEIVER`, `RC_CASH_BAL`, `RC_PEND_TAX_RCL`,
`SE_ENH_TRD_STAT` all Active. Operational consequence: **one Mediator service carries all
five**. Restarting it for one interface stops the other four, and they share one log
directory — say so before advising a restart.

---

## RC_CASH_BAL — Cash balance reconciliation

Type **0 General**. PFD `RC_CASH_BAL`, `Config.RC-CashBalance.xml`.

Parameters: `RC_CB_IN_FOLDER = @confparam(Directory, INTERFACES)In\SFTP\RC_CASH_BALANCE\
Working`, `RC_CB_ARCHIVE_FOLDER = …\Archive`, `RC_CB_FILE_PATTERN_IN = *.csv`,
`RC_CB_FILE_PATTERN_OUT = BNYM_cash_recon_`,
`RC_CB_RECON_IN_DIR = @confparam(Directory,RECONCILIATION)BNYM\`,
`RC_CB_BNYM_FILE_VERSION = NEXEN`, `RC_CB_RECON_VERBOSE = NO`.

Support: the flow is Working → transform → `RECONCILIATION\BNYM\` → Archive. Missing
recon: check which of the three folders the file stopped in. `RC_CB_BNYM_FILE_VERSION =
NEXEN` pins the expected BNYM layout — a custodian format change breaks parsing here
first. `RC_CB_RECON_VERBOSE = NO` can be flipped to get more detail (local parameter,
applies live). **This setup has no dead letter, no retry, no alert of any kind** (12 §C):
failures are visible only in the shared `SE_CUST_ADDON_L` log.

---

## RC_PEND_TAX_RCL — Pending tax reclaim reconciliation

Type **0 General**. Two config rows, the *same file name* in two PFDs:
`Config.RC-PendTaxReclm.xml` @ `RC_PTR_BNYM` and @ `RC_PTR_JPM`. That is deliberate — one
solution, one config per custodian.

Four custodians are parameterised, though only two have their own PFD:

| Custodian | Pattern in | Pattern out | Recon dir |
|---|---|---|---|
| BNYM | `Pending*.csv` (version `NEW`) | `BNYM_pending_tax_reclaim_` | `…RECONCILIATION\BNYM\` |
| JPM | `Tax Reclaims*.csv` | `JPM_pending_tax_reclaim_` | `…\JPM\` |
| BNP | `*DAILY_TAX_RECLAIM*.csv` | `BNP_pending_tax_reclaim_` | `…\BNP\` |
| HSBC | `HSBC_Pending_reclaims*.csv` | `HSBC_pending_tax_reclaim_` | `…\HSBC\` |

Shared: `RC_PTR_IN_FOLDER = …In\SFTP\RC_PEND_TAX_RECL\Working`, `RC_PTR_ARCHIVE_FOLDER`.

Support: file naming is the whole game here — four custodians, four patterns, one inbox.
A renamed custodian file lands in Working and is never claimed. Also no error handling
configured (12 §C).

---

## AS_PAID_TAX_RCL — Paid tax reclaim (asset servicing)

Types **0 General, 3 MQ, 7 Data Extractor**. PFD `AS_PAID_TAX_RECL`, three config files:
`Config.AS-PTR-00General.xml`, `-01BNYM.xml`, `-02JPM.xml` — the "00 General + per
custodian" pattern.

Parameters: per-custodian `AS_AD_IN_FOLDER_BNYM|JPM` (`…\AS_PTR_BNYM|JPM\Working`),
`AS_AD_ARCHIVE_FOLDER_*`, `AS_FILE_PATTERN_* = *.csv`, `AS_SEARCH_STRING_BNYM = BNYM` /
`_JPM = JPM`, plus `AS_PTR_INPUT_QUEUE = AS_PTR`, `AS_PTR_ALERTS = Yes`,
`AS_ENABLE_VERBOSE_LOGGING = Yes`.

Support: both custodians use `*.csv`, so routing depends on `AS_SEARCH_STRING_*` matching
content/name — a file that matches neither is ignored silently. `AS_PTR_ALERTS = Yes` means
this one *does* alert; `AS_ENABLE_VERBOSE_LOGGING = Yes` is already on, so the shared log
should carry detail.

---

## RC_ASH_RECEIVER — ASH queue receiver

**No message types.** PFD `RC_ASH_RECEIVER`, `Config_ASHReceiver.xml`. Parameters:
`RC_ASH_RECEIVER_DIR = @confparam(Directory,RECONCILIATION)ASH\`,
`RC_ASH_RECEIVER_FILE_PATTERN = SIM_msg_`.

Support: pure file receiver into the reconciliation ASH folder; with no message type it
exchanges nothing with Dimension by label. Check the folder and the `SIM_msg_` prefix.

---

## SE_ENH_TRD_STAT — Enhanced trade status (settlement)

Types **0 General, 13 Batch Jobs**. PFD `SE_ENH_TRADE_STAT`, three configs
(`-00General`, `-01BNYM`, `-02JPM`).

Parameters: BNYM in `…\SE_ENH_TRD_STAT_BNYM\Working`, pattern `*.csv`, out
`enhanced_trade_status_BNYM`; JPM in `…\SE_ENH_TRD_STAT_JPM\Working`, pattern **`*.xml`**
(different format), out `enhanced_trade_status_JPM`; both feed
`@confparam(Directory, INTERFACES)In\Direct\ETS\`; then batch job group
`SE_ETS_SCBI_BJG = SE_CUST_ADDON_BI` on queue `SE_ETS_SCBI_BATCHQUEUE = SO_BATCH`.

Support: statuses not updating → did the `SE_CUST_ADDON_BI` group reach `SO_BATCH`
(02 §E)? BNYM is CSV and JPM is XML — do not apply one custodian's parsing assumption to
the other. No error handling configured (12 §C), and this one feeds downstream batch
logic, which makes the absence of a failure path worth raising.

---

## FNDS_SFTP_AVISO — Outbound SFTP transport to Aviso

Type **15 Extract data – Point-2-Point** via configurable message type `SFTP_AVISO`. PFD
`FNDS_SFTP_SRV`, `config.aviso.xml` (the same PFD also holds `config.ssc.xml` and
`config.xml` for other counterparties, all sharing `cartridge.sftp.xml`). Parameter set
`FNDS_SFTP_AVISO` (Production, Ignore OK, **no log directory**).

Parameters: `FTP_SERVER_AVISO = sftp1.aviso.ca:22`, user `nicola-aviso-simcorp`, key
`sshprivatekey_aviso.ppk`, `FTP_UPLOAD_PATH_AVISO` empty (root),
`DEX_FILE_PATH_AVISO = @confparam(Directory,ACTIVEDATA)Interfaces\Out\SFTP\OutboundFiles\
Aviso`, and the file whitelist
`DEX_FILE_PATTERN_AVISO = SecurityTransfer_*.csv|CashTransfer_*.csv|ForwardDeal_*.csv|
SpotDeal_*.csv|OptionDeal_*.csv|MutualFund_*.csv`. Mail:
`EMAIL_SMTP_SERVER = smtp.simcorpcloud.com`, from `donotreply@simcorpcloud.com`, to
`MAILBOX_AMOPS` only (amops@ + erifki@nicolawealth.com). `MAILBOX_FUNDADMIN`
(fundaccounting@ + erifki@) is declared here but **not used** by `cartridge.sftp.xml`.

Flow (`cartridge.sftp.xml`) resolves ports **at runtime** from the message
(`PORT_SUFFIX` → `UPLOAD_FILE_<suffix>` / `FTP_<suffix>`), then `<receiveall>` the local
files, `<send>` each over SFTP, write a local `SENT-<timestamp>-<name>` copy, log via
`SCIn_LogMessage`, and e-mail confirmation. On `<catch>`: e-mail the error, write
`PUT_<timestamp>.error` next to the files, and re-`<throw>`.

Support: this is the **cleanest error handling in the environment** — a failure produces an
e-mail *and* a `.error` file *and* a re-thrown exception. So: no e-mail and no `.error`
file means the flow never started (check `DEX_FILE_PATTERN_AVISO` and that the extract
actually wrote into the folder). A `SENT-` copy means the upload succeeded. Note the FTP
port in `config.aviso.xml` is declared with `Listen="False"` and `RetryConnection="10"` —
it is push-only, driven by the message, not polling.

---

## PE_F_IAS — Performance, Investment Analytics Service (MDATaaS)

Type **17 Connectivity monitor**. Interface package origin **2446** (`pIFCPKGORG`, SimCorp-supplied). Three
config rows across PFDs `PE_F_CONMON` (`Config.MDATaaS_ConMon.xml`) and `PE_F_CORE`
(`Config.MDATaaS_Core_ManagedIdentity.xml` Active; `…_ServicePrincipal.xml` **Inactive**)
— i.e. authentication is by **managed identity**, not service principal, which is why
`MDATAAS_CLIENT_ID` and `MDATAAS_CLIENT_SECRET` are empty. Do not populate them to "fix"
an auth error without switching the active config file.

Parameters: `MDATAAS_TENANT_ID = 12dcf0d8-fc71-4abe-a06c-2d2bc1c6d3f0`, storage account
`stperfaasnicolatstpub`, containers `perfaas-data-pub` / `perfaas-status`, dirs
`fromscd` / `toscd`, status prefix `CMON`, local dirs
`@confparam(Directory,INTERFACES)\In|Out\Direct\PE_F_IAS\DataIn|DataOut\`, queues
`MDATaaS_ConMonMsgParams_Queue_PE_F_IAS`, `MDATaaS_FromScdToAzureControl_Queue_PE_F_IAS`,
`MDATaaS_FromScdToAzureData_Queue_PE_F_IAS`, solution id `PE_IAS`.

Support: transport is `<AzureBlobStorage>`. Failures split cleanly into (a) blob/auth —
SimCorp Cloud and Azure side, and (b) file production — SimCorp Dimension side. Because it
is a licensed interface package, do not modify locked components; raise with SimCorp
(02 §J). Cross-check with `simcorp-performance-specialist` for what the service consumes.

---

## SO_ODA — Operational Data Assistant server  *(owner: SimCorp)*

Type **0 General**. PFD `SimCorp/SCDRCONNECT`, `config.ODA.xml`. Parameter set `SO_ODA`
(Production, log mode Normal, no log directory).

Parameters: `ODA_SERVICE = https://remoteconnect.simcorp.com/remoteconnectgateway/
service.svc?wsdl`, `ODA_USER = scdremoteconnect`, password masked, and four transfer
switches — `TRANSFER_ERRORLOG`, `TRANSFER_PATCHAPPLY`, `TRANSFER_PING`, `TRANSFER_SCMETA`,
all `yes`. Transport: `<WebRequest>` (SOAP) — the only web-service port in the environment.

Support: this is SimCorp's own remote-connect channel (it ships error logs, patch-apply
results, pings and metadata to SimCorp). **Owner = SimCorp** — do not modify it. If it is
down, SimCorp loses visibility of the installation; raise it with them rather than
changing switches. Its presence also means SimCorp already receives the error logs you
would otherwise have to attach to a ticket.
