# 08 — Setup cards: Alternatives and Wealth (Nicola-built)

---

## DM_ALTS — Alternative Investments data management  *(high traffic)*

Types **3 MQ, 13 Batch Jobs, 19 Filter Tool Box, 21 Data Import**. Config files
`config.Alts.xml` (PFD `DM_ALTS`) **and** `config.scDLSLink.xml` (PFD `DM_DLS_LINK`).
Parameter set `DM_ALTS` (Production, Ignore OK, log `DM_ALTS_LOG`).

Nine inbound folders, all under `@confparam(Directory,ACTIVEDATA)\Interfaces\In\SFTP\`:

| Parameter | Folder | Content |
|---|---|---|
| `ALT_STATIC_IN` | `Alts_Static\Incoming` | static data |
| `ALT_COMMIT_IN` | `Alts_Commitments\Incoming` | commitments |
| `ALT_TRANS_IN` | `Alts_Transactions\Incoming` | transactions |
| `ALT_VALS_IN` | `Alts_Valuations\Incoming` | valuations |
| `ALT_INCEXP_IN` | `Alts_IncomeExpenses\Incoming` | income/expenses |
| `ALT_SECBUY_IN` | `Alts_SecondaryBuy\Incoming` | secondary buys |
| `ALT_SECSELL_IN` | `Alts_SecondarySell\Incoming` | secondary sells |
| `ALT_TRANSDECOMP_IN` | `Alts_TransactionDecomp\Incoming` | transaction decomposition |
| `ALT_DECOMPOS_LOOKTHR_IN` | `Alts_Decompositions_LookThrough\Incoming` | look-through decompositions |

Plus `DIR_UF_ERROR_LOG = …\Alts_Errorlog\`, `MQ_NAME = DM_ALTS`, and the data-lineage
block `DLS_SOLUTION = DM_ALTS`, `DLS_SRC_SYSTEM = EXTERNAL`, `DLS_DEST_SYSTEM = SCD`,
`DLS_DATA_BACKUP = YES`.

Flow: `cartridge.Alts_FileIn.xml` has one handler per folder; each logs metadata to
`DLSLink` then fans into the single queue `DM_ALT_Process`.
`cartridge.Alts_Processing.xml` branches by category and runs the matching transform —
`XMLtoDataImport.xslt`, `…InvestLink.xslt`, `…UnderAsset.xslt`, `…Decompos.xslt`, or the
DFS filter builders `XMLtoFilterDfsNetCallDist.xslt` / `…Migration.xslt`, or
`XMLtoMQ.xslt` → `StaticDataMQ.xslt` — then a second-stage `dataimport*.xslt`
(`engine="XmlPrime"`) before `send … port="SCIn" label="SCIn_DMImportQueue"` (or
`SCIn_DMImportExecute` on the decompose path). `cartridge.scOut.xml` evaluates six SCOut
labels through `ResponseEval.xslt` / `ReformatImportResponse.xslt` and logs the outcome
back to `DLSLink`.

Support:
- **The file that fails and the folder it sat in tell you the transform.** Map folder →
  parameter → transform using the table above before opening any XSLT.
- Rejected records: read the import response (05 §D) — overall `OK` does not mean every
  record loaded. `DIR_UF_ERROR_LOG` holds the unformatted error log.
- `DLSLink` is **not declared in this config** — it lives in `DM_DLS_LINK`. If that config
  file is removed from the setup, every handler here fails on the first `send`. Both
  config rows must stay Active.
- Nothing at all processing → is the file in `Incoming` and does its name match the port
  pattern? Then check `DM_ALT_Process` and the MQ message type being Active.

---

## SIM_ALTS — Alternatives decomposition (SIM subset)

Types **3 MQ, 13 Batch Jobs, 19 Filter Tool Box, 21 Data Import**. Configs
`config.Alts.xml` (PFD `SIM_ALTS`) + `config.scDLSLink.xml` (PFD `DM_DLS_LINK`).
Parameter set `SIM_ALTS` (Production, Ignore OK, log `SIM_ALTS_CS_LOG`).

Same cartridge names as `DM_ALTS` but **one** input folder:
`ALT_DECOMPOS_IN = …\Interfaces\In\SFTP\SIM_ALTS\Incoming`, error log
`…\SIM_ALTS\Alts_Errorlog\`, `DLS_SOLUTION = SIM_ALTS`. Only the decomposition chain
(`XMLtoDataImportDecompos.xslt` → `dataimportdecompos.xslt` →
`label="SCIn_DMImportExecute"`) is wired.

Support: this is a **derivative of DM_ALTS**, so a fix applied to one is not automatically
in the other — always check both directories when changing decomposition logic. The `scOut`
cartridge is structurally identical, so response-evaluation defects will show in both.

---

## NW_ACC_SYNC — Wealth Account Sync

Types **3 MQ, 7 Data Extractor, 13 Batch Jobs, 21 Data Import**. PFD `NW_ACC_SYNC`,
`Config.xml`. Parameter set `NW_ACC_SYNC` (**Production Test**, log mode Normal, log
`NW_ACC_SYNC_LOG`).

Parameters: `FILE_DIR_IN = @confparam(Directory,ACTIVEDATA)\Interfaces\In\SFTP\WealthSync\
Delta\PortfolioGroupStructure`, `CONTROL_FILE_PATTERN = *.ctl`,
`DATA_FILE_PATTERN = *.csv`, `SCDMQ_ID = NW_ACC_SYNC`.

Control-file pattern: the `.ctl` file is the trigger; the `.csv` is the payload. A `.csv`
sitting alone will never be picked up — that is the single most common "sync did not run"
cause for this shape of interface (`ARCHON` and `TP_NBIN_TRANS` share it).

Support: parameter set is *Production Test*, so it will start in **stale state** if the
WealthSync share is unreachable — the monitor will still say running (02 §A). There is no
`FILE_DIR_OUT` here (unlike ARCHON): this setup is inbound only.

---

## NW_AI_SKILL — Wealth AI Skill

Types **0 General, 3 MQ, 7 Data Extractor**. PFD `NW_AI_SKILL`,
`Config_NW_AI_SKILL.xml`. In parameter set `NW_AI_SKILL` (Production Test, Ignore OK, no
log directory) **and** in `NW_MAIN` where it is **inactive**.

Parameters: `AISK_DIRECTORY_BASE = @confparam(Directory,INTERFACES)In\SFTP\AISkill`,
`AISK_FILE_EXTENSION = .csv`, `AISK_MESSAGE_QUEUE = TP_WEALTH`,
`AISK_DEX_ORDERS_SELL_ALL = CSVR_NW_ASIK_SA`, `AISK_SWITCH = Yes`,
`AISK_TIMEZONE_OFFSET = -PT4H`, alert `ASN_NW_AI_SKILL = WEALTH_AI_SKILL`.

Support: `AISK_SWITCH` is the kill switch — set to anything but `Yes` and the flow stops
without an error. Check it before debugging. The sell-all extract `CSVR_NW_ASIK_SA` is a
DEX name: failures there belong to the extraction definition, not the Comm Server
(`simcorp-dex-validator`). Fixed `-PT4H` offset: same DST caveat as DM_COPP_CLARK.

---

## NW_BULK_TRADES — Wealth bulk trades  *(not running in this snapshot)*

Types **0 General, 3 MQ, 7 Data Extractor**. PFD `NW_BULK_TRADES`,
`Config_NW_BULK_TRADES.xml` (10 cartridges). **Inactive in both parameter sets that
reference it** (`NW_BULK_TRADES` and `NW_MAIN`) — so in this TEST environment it does not
load at all. Establish that before investigating "bulk trades stopped working".

Parameters: base `BT_DIRECTORY_BASE = @confparam(Directory,BUSINESSDATA)Wealth\BulkTrades`
with sub-folders `Orders`, `Cash`, `Transfers`, `ManualAccountTransactions`
(`BT_DIRECTORY_*`), `BT_FILE_EXTENSION = .csv`, `BT_MESSAGE_QUEUE = TP_WEALTH`,
`BT_DEX_ORDERS_SELL_ALL = CSVR_NW_BT_SA`, alert `ASN_NW_BULK_TRADES = WEALTH_BULK_TRADES`.

Note it shares the `TP_WEALTH` queue with `NW_AI_SKILL`. Two solutions on one queue is
fine, but they must not both be Point-2-Point-gated on the same type.

---

## NI_ALERT_EXPORT — Nicola alert export  *(no parameter set)*

Type **30 Export alert data**. PFD `NI_ALERT_EXPORT`, `Config_AlertExport.xml`. Single
parameter `ASN_NI_ALERT_EXPORT = ALERT_EXPORT`. **Not in any parameter set in this
export** — configured, not deployed. Relevant because the `scdAlert_Create` calls scattered
through the other solutions (04 §E) raise alerts *inside* SimCorp; exporting them onward
is this setup's job. If someone asks why alerts are not reaching an external tool, the
answer starts here, not in the raising solution.

---

## ARCHON — Cash activity between Archon and SimCorp Dimension

Types **3 MQ, 7 Data Extractor, 13 Batch Jobs, 21 Data Import**. PFD `ARCHON`,
`Config.xml` (1 cartridge, no XSLTs). Parameter set `ARCHON` (**Production Test**, log mode
Normal, log `ARCHON_LOG`).

Parameters: `FILE_DIR_IN = …\Interfaces\In\SFTP\Archon`,
`FILE_DIR_OUT = …\Interfaces\Out\SFTP\Archon`, `CONTROL_FILE_PATTERN = *.ctl`,
`DATA_FILE_PATTERN = *.csv`, `SCDMQ_ID = TP_ARCHON`.

Support: same `.ctl` + `.csv` control-file rule as `NW_ACC_SYNC`. Bidirectional, so check
both In and Out folders. Log mode Normal with a dated log folder (`ARCHON_LOG` builds
`log\Servers\YYYY\MM\DD`) means this one **does** leave a trail — start there.
