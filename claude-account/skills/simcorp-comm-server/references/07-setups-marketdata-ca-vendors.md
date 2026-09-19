# 07 — Setup cards: market data, corporate actions, vendor feeds

Each card: what it does · how it moves data · the parameters you will need · the failure
modes that are real for *this* configuration. Values are from the 2026-08-18 TEST export
and the `ComSrv` tree; anything not there is marked unknown, not guessed.

---

## DA_BLOOMBERG — Bloomberg Data License Requester  *(high traffic)*

Message type **5 Bloomberg** only. PFD `Bloomberg/DA_BLOOMBERG`, config registered as
`config.sc-ftp.xml` (the file on disk is `Config.sc-Ftp.xml` — a case mismatch, harmless on
Windows only). Parameter set `DA_BLOOMBERG` (Production, log mode Normal, **no log
directory**) — which also loads `DM_BLB_UNK_UNDE`, a setup absent from this export (12 §A).

Transport: `<Ftp><FtpSSH>` to `sftp.bloomberg.com`, key file
`@confparam(Directory,ACTIVEDATA)\Configuration\ComSrv\bbsftpnonprod.ppk`
(`PRIVATEKEYPASSWORD` and `PASSWORD` both empty in TEST — key-only auth). Files land in
`BLOOM_DIR = @confparam(Directory,INTERFACES)Data\BDL`, out via `BLOOM_DIR_OUT`. Request
files are prefixed `PREFIX = D_`; the port's `InputFilePattern` accepts `D_*.out`,
`D_*.err`, `D_*.out.gz`.

Flow: `cartridge.scBloombergIn.xml` logs the raw payload to `BloomFtpLog`, builds a status
envelope with `scBloomStatusInit.xslt`, branches on `.err`, then
`send … port="SCIn" label="dWEBMSGIN_BLOOMSTATUS"`. Outbound
`cartridge.scBloombergOut.xml` handles `dWEBMSGOUT_BLOOMREQUEST` on `SCOut`, pushes the
request over SFTP and reports dispatch status back with the same label.

This is the **best-instrumented** solution in the environment: dead letter port
(`BloombergDeadletter` → `…/Deadletter`), `Sleep=5`, `FtpTimeOut=30`,
`RetryCommand=50`, and three passive audit ports (`BloomFtpLog`, `BloomInLog`,
`BloomOutLog`).

Support:
- Nothing arriving → check the `.out`/`.err` naming against `PREFIX`; then the Deadletter
  folder; then the three log ports (they hold the raw traffic even when parsing failed).
- A `.err` file **is** a Bloomberg-side rejection, not a Comm Server fault — the cartridge
  routes it deliberately.
- Key/host changes: `SERVER`, `PRIVATEKEYFILE`, `PRIVATEKEYPASSWORD` are local parameters,
  so they can be changed while the service runs (11 §B).
- A commented-out `<File Name="BloombergFtp">` block exists as a deliberate failover to a
  file port when SFTP is unavailable. Uncommenting it is a **config file** change ⇒ needs
  a Mediator restart or Reload, and PFD status Edit→Test→Protected.

---

## AS_BDL_CONVERT — Bloomberg corporate-action file converter

Types **0 General, 7 Data Extractor, 12 Corporate action manager**. PFD
`AS_BLOOM_CONVERTER`, `Config.xml`, 1 cartridge + 25 XSLTs. Parameter set
`AS_BDL_CONVERT` (Production, Ignore OK, log `AS_BDL_CONV_CS`).

Parameters: working folder `CS_FLD` and `FLD_TEST` both
`@confparam(Directory,INTERFACES)\In\SFTP\BDL_Convert`; security lookup extracts
`DEX_SEC_LOOKUP = AS_BDL_ISIN_LOOKUP`, `DEX_SEC_LOOKUP_BLB = AS_BDL_ISIN_LOOKUP_BLB`;
identification systems `IDSYS_MAIN_SEC = FIGI`, `IDSYS_UND_SEC = FIGI`.

`Cartridge.xml` dispatches dynamically: `transform apply="Bdl_conv_@var(currentFlowName).xslt"`.
Known defect: the valid-flow list includes `DEL_` but **`Bdl_conv_DEL_.xslt` does not
exist** — a Bloomberg "DEL_" corporate-action record will fail to resolve its transform
(12 §B). 20 other flows are present (BIDS_, BONU_DVSE_, CHAN_, CHAN_NM_, CHOS_, DVCA_Mand_,
DvcaOthr_Mand_, EXRI_, INCR_, ISIN.mainsec, ISIN.spinoff, LIQU_Mand_, MRGR_, Ndiv_Mand_,
PRIO_, RHDI_, RHTS_, SOFF_, SPLT_, TEND_, plus `_generic`).

Support: a single CA event type failing while others succeed almost always means a missing
or misnamed `Bdl_conv_*.xslt` — check the Configuration tab for red "Not found" entries,
and use the **Xslt sandbox** with the actual record to confirm before changing anything.
Security lookup failures point at the two DEX names above, not at the converter.

---

## DA_CAM — Corporate Action General Interface  *(high traffic)*

Types **3 MQ, 7 Data Extractor, 12 Corporate action manager**. Config files span four
PFDs: `-@AS_CA_SCLIB`, `-@COAC_CSD_LIB`, `-@SCLIB` (libraries, dash-referenced) plus
`config.cam-gain-file.xml` and `config.cam.xml` in `DA_CAM`. Parameter set `DA_CAM`
(Production, Ignore OK, log `AS_CA_PS_CAM`).

Parameters: `CAM_DIRECT_IN` / `CAM_DIRECT_OUT` come from **Global** scope
(`@confparam(Global,…)`) — not from this setup; `CAM_MSGQUEUE = AS_CA_MQ`;
`MESSAGEQUEUE = COM_SERVER_MQ`; GAIN folders `GAIN_IN_DIR`, `GAIN_OUT_DIR`,
`GAIN_ACK_NAK_DIR` (all under the Global CAM directories); `GAIN_ACK_NAK_USE_OAQ = no`;
`KEY_STORE = @confparam(Directory,NETROOT)MQKeystore`; `SCLIB = ..\SCLIB`;
`DEXONESHOTREQUEST = 0`.

Transport variants matter: the same `cartridge.scCamGain.xml` is bound by a WebSphere MQ
config **and** an Oracle AQ config. Switching transports is a config-file swap, not a
logic change (04 §F).

Support:
- Ack/nak not appearing → `GAIN_ACK_NAK_DIR` and `GAIN_ACK_NAK_USE_OAQ`; the shared
  `STDACKNAK` library is the module that formats them.
- Dead letters exist here (`WorkflowDeadLetter`, `MessageStorageDeadLetter`) — check them
  before assuming loss.
- `configCorpactFile.xml` / `configCorpactMq.xml` in this directory are **orphaned legacy**
  (2012-era headers, cartridges missing, paths pointing outside the PFD). They are not in
  the setup's active config list. Do not troubleshoot against them (12 §B).

---

## AS_COACSRV — COAC Solution Server (SWIFT corporate actions)

Types **3 MQ, 7 Data Extractor, 15 Extract data – Point-2-Point** via configurable message
type `GAIN_REQUEST`. Six config entries across `AS_CA_SCLIB`, `COAC_CSD_LIB`, `COAC`
(`Config.sc-File.xml`, `Config.sc-OracleAQ.xml`), `DA_GAIN_REQUEST`
(`config.gain_file.xml`) and `STDACKNAK` (`config.scStdAckNak.xml`). Parameter set
`AS_COACSRV` (Production, Ignore OK, log `AS_CA_PS_COAC`).

Notable parameters: `BYPASS_MT566 = NO`, `COAC_MANUALINPUTALLOWED = Yes`,
`COAC_SEND_TO_SWIFTSIM = No`, `MULTITENANCY = Yes`, `WRITEACK = Yes`, `WRITENACK = Yes`,
`USEMSGSTATISTICS = YES`, `CIPHER = TLS_RSA_WITH_AES_256_CBC_SHA`,
`KEY_STORE = @confparam(Directory,NETROOT)MQKeystore`, `RESPONSE_PORT = Workflow`,
`USE_COAC_CSD_LIB = COAC_CSD_LIB`, `USEDEXPREQUERY`/`USEDEXPOSTQUERY = No`,
and a large-amount splitter: `USESPLITLARGEAMOUNT = No`, `SPLITAMTMAX = 50000000`,
`SPLITSIZE = 500`, `SPLITINPUTDIR`/`SPLITOUTPUTDIR`, `SPLITFILENAME = Splitfile`.

Support:
- SWIFT conversion problems are **warnings vs exceptions** (05 §E). `TooManyDecimalsError`
  and `NoDecimalError` are logged but **not stripped** — they reach the counterparty.
- NAK reason codes come from the `From` attribute on mandatory SWIFT fields.
- `Config.sc-Test.xml` and `cartridge.scTest.xml` are a developer harness with five missing
  XSLTs; ignore them unless someone activated the test config.
- Point-2-Point: only one production server per installation may hold `GAIN_REQUEST`.

---

## DM_COPP_CLARK — Copp Clark calendars

Type **13 Batch Jobs** only. PFD `DM_COPP_CLARK`, `Config_CoppClark.xml`. Parameter set
`DM_COPP_CLARK` (Production, Ignore OK, **no log directory**).

Parameters: SFTP `sftp.coppclark.com:22`, user `nicolawealth.hds`, password masked,
`FTP_FOLDER = /`, base dir `@confparam(Directory,INTERFACES)IN\Direct\CoppClark`,
`INPUT_FILE_NAMES = Placeholder.csv`, `ARCHIVE_ONLY_FILES = ExchangeTrading`,
`DOWNLOAD_DELAY_SECONDS = 90`, `TIMEZONE_OFFSET = -PT4H`, alert system name
`ASN_COPP_CLARK = COPP_CLARK`, and the scheduling pair
`BATCH_JOB_GROUP = DM_CPCLRK_CALENDARS` on `BATCH_QUEUE = SO_BATCH` at
`BATCH_JOB_GROUP_TIME_24H_HHMM = 2115`.

Support: calendars missing next morning → was the 21:15 group inserted on `SO_BATCH`?
Check the batch response, then the 90-second download delay, then the file name against
`INPUT_FILE_NAMES`. `TIMEZONE_OFFSET = -PT4H` is a **fixed** offset — it does not follow
daylight saving, so a DST change shifts the effective run time by an hour. Flag that at
the March/November boundaries rather than debugging the interface.

---

## DM_RMS_GAIN and DM_RMS_GAIN_AZ — RMS to GAIN (file API and Azure API)

**No message types, and no parameter set in this export** — they are configured but not
deployed here. `DM_RMS_GAIN`: `config.RMS_GAIN.xml`, `GAIN_URL = @confparam(Directory,
GAINURL)`, `REQUESTTYPE = Standard`. `DM_RMS_GAIN_AZ`: `config.RMS_GAINAZ.xml`, Azure
variant with `GAIN_AZURE_URL`, `TOKEN_URL`, `COMSERVCLIENTID`, `COMSERVSECRET` (all three
empty in TEST) and a `<Timer Name="Poll" Period="30" PeriodUnit="sec">`.

Support: before investigating "GAIN is not updating", establish **which** GAIN path is
live — the CAM/COAC GAIN folders (`DA_CAM`, `AS_COACSRV`) are a different mechanism from
these two RMS setups. If a ticket asks for the Azure API, the credentials are blank in
TEST and must come from whoever owns the Azure app registration; do not invent them.
