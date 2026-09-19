# 06 — Catalogue of the environment (TEST export, 2026-08-18)

Provenance: SimCorp Dimension 26.04 SP0, track `IMPL`, state `TEST`, `custno=10055`,
`custid=NICOLA`, exported by DDEENIK 2026-08-18T14:53–14:55Z. Regenerate with
`scripts/parse_comsrv_cei.py` after any fresh export — do not hand-edit these tables.

## A. Message type codes seen in this environment

| Code | Message type | Used by |
|---|---|---|
| 0 | General | AS_BDL_CONVERT, AS_PAID_TAX_RCL, NW_AI_SKILL, NW_BULK_TRADES, RC_CASH_BAL, RC_PEND_TAX_RCL, SE_ENH_TRD_STAT, SO_ODA, TP_NBIN_TRANS |
| 3 | MQ | ARCHON, AS_COACSRV, AS_PAID_TAX_RCL, DA_CAM, DM_ALTS, NW_ACC_SYNC, NW_AI_SKILL, NW_BULK_TRADES, SIM_ALTS, TP_NBIN_TRANS, TP_TC_APL, TP_TC_CANC_MOD |
| 5 | Bloomberg | DA_BLOOMBERG |
| 7 | Data Extractor | ARCHON, AS_BDL_CONVERT, AS_COACSRV, AS_PAID_TAX_RCL, DA_CAM, NW_ACC_SYNC, NW_AI_SKILL, NW_BULK_TRADES, ORDERMATCH, TP_NBIN_TRANS, TP_TC_APL |
| 9 | Order General Match | ORDERMATCH |
| 12 | Corporate action manager | AS_BDL_CONVERT, DA_CAM |
| 13 | Batch Jobs | ARCHON, DM_ALTS, DM_COPP_CLARK, NW_ACC_SYNC, SE_ENH_TRD_STAT, SIM_ALTS |
| 15 | Extract data – Point-2-Point | AS_COACSRV (`GAIN_REQUEST`), FNDS_SFTP_AVISO (`SFTP_AVISO`), TP_TC_CANC_MOD (`TP_TC_CANCEL_REQUEUE`) |
| 17 | Connectivity monitor | PE_F_IAS |
| 19 | Filter Tool Box | DM_ALTS, SIM_ALTS, TP_NBIN_TRANS, TP_TC_APL |
| 21 | Data Import | ARCHON, DM_ALTS, NW_ACC_SYNC, SIM_ALTS |
| 30 | Export alert data | NI_ALERT_EXPORT |

Four setups have **no message type at all**: `DM_RMS_GAIN`, `DM_RMS_GAIN_AZ`,
`RC_ASH_RECEIVER`, `TP_TC_X_ASH`. They cannot exchange anything with SimCorp Dimension via
labels — they are file/queue-only or outbound-API-only solutions. That is a design fact to
confirm before "fixing" it.

## B. The 27 setups → their parameter set and log

| Setup | Name | Parameter set (server type) | Log reference file |
|---|---|---|---|
| ARCHON | Cash Activity Between Archon & SCD | ARCHON (Production Test) | ARCHON_LOG |
| AS_BDL_CONVERT | Bloomberg CA Files converter | AS_BDL_CONVERT (Production) | AS_BDL_CONV_CS |
| AS_COACSRV | COAC Solution Server | AS_COACSRV (Production) | AS_CA_PS_COAC |
| AS_PAID_TAX_RCL | Asset Servicing – Paid Tax Reclaim | SE_CUST_ADDON (Production) | SE_CUST_ADDON_L |
| DA_BLOOMBERG | Bloomberg – Data License Requester | DA_BLOOMBERG (Production) | — none — |
| DA_CAM | Corporate Action General Interface | DA_CAM (Production) | AS_CA_PS_CAM |
| DM_ALTS | Alternative Investments – Data Mgmt | DM_ALTS (Production) | DM_ALTS_LOG |
| DM_COPP_CLARK | Copp Clark Interface | DM_COPP_CLARK (Production) | — none — |
| DM_RMS_GAIN | RMS to GAIN | **none** | — |
| DM_RMS_GAIN_AZ | RMS to GAIN – Azure API | **none** | — |
| FNDS_SFTP_AVISO | SFTP – Outbound Transport – Aviso | FNDS_SFTP_AVISO (Production) | — none — |
| NI_ALERT_EXPORT | Nicola – Alert Export | **none** | — |
| NW_ACC_SYNC | Wealth Account Sync | NW_ACC_SYNC (Production Test) | NW_ACC_SYNC_LOG |
| NW_AI_SKILL | Wealth – AI Skill | NW_AI_SKILL (Production Test, active) **and** NW_MAIN (inactive) | — none — |
| NW_BULK_TRADES | Wealth – Bulk Trades | NW_BULK_TRADES (Production, **inactive**) and NW_MAIN (**inactive**) | — none — |
| ORDERMATCH | General Order Match | ORDERMATCH (Production Test) | ORDERMATCH |
| PE_F_IAS | Performance – Investment Analytics Service | PE_F_IAS (Production, pkg-org 2446) | — none — |
| RC_ASH_RECEIVER | Reconciliation – ASH queue receiver | SE_CUST_ADDON (Production) | SE_CUST_ADDON_L |
| RC_CASH_BAL | Reconciliation – Cash Balance | SE_CUST_ADDON (Production) | SE_CUST_ADDON_L |
| RC_PEND_TAX_RCL | Reconciliation – Pending Tax Reclaim | SE_CUST_ADDON (Production) | SE_CUST_ADDON_L |
| SE_ENH_TRD_STAT | Settlement – Enhanced Trade Status | SE_CUST_ADDON (Production) | SE_CUST_ADDON_L |
| SIM_ALTS | SIM – Alternatives Decomposition | SIM_ALTS (Production) | SIM_ALTS_CS_LOG |
| SO_ODA | Operational Data Assistant Server (**owner SimCorp**) | SO_ODA (Production) | — none — |
| TP_NBIN_TRANS | Trade Capture Satellite Setup | TP_NBIN_TRANS (Production) | TP_NBIN_TRANS_LG |
| TP_TC_APL | Trade Capture APL relevant trades | TP_TC_APL (Production) | TP_TC_AP_CS |
| TP_TC_CANC_MOD | Trade Capture – Cancel/New as Modify | **none** | — |
| TP_TC_X_ASH | Trade Capture ASH Connector | **none** | — |

All 27 are `pCSPARALLEL = 0 (One Instance Only)`; all owner = Customer except `SO_ODA`
(SimCorp). Only `PE_F_IAS` carries a non-blank interface package origin (`pIFCPKGORG=2446`);
`pIFCPKGNO` is blank on all 27.

## C. The 19 parameter sets

| Parameter set | Server type | Log mode | Setups (active?) |
|---|---|---|---|
| ARCHON | Production Test | Normal | ARCHON ✓ |
| AS_BDL_CONVERT | Production | Ignore OK | AS_BDL_CONVERT ✓ |
| AS_COACSRV | Production | Ignore OK | AS_COACSRV ✓ |
| DA_BLOOMBERG | Production | Normal | DA_BLOOMBERG ✓, DM_BLB_UNK_UNDE ✓ |
| DA_CAM | Production | Ignore OK | DA_CAM ✓ |
| DM_ALTS | Production | Ignore OK | DM_ALTS ✓ |
| DM_COPP_CLARK | Production | Ignore OK | DM_COPP_CLARK ✓ |
| FNDS_SFTP_AVISO | Production | Ignore OK | FNDS_SFTP_AVISO ✓ |
| NW_ACC_SYNC | Production Test | Normal | NW_ACC_SYNC ✓ |
| NW_AI_SKILL | Production Test | Ignore OK | NW_AI_SKILL ✓ |
| NW_BULK_TRADES | Production | Ignore OK | NW_BULK_TRADES ✗ |
| NW_MAIN | Production Test | Ignore OK | NW_AI_SKILL ✗, NW_BULK_FEE ✓, NW_BULK_TRADES ✗, NW_NBIN ✗, NW_NBIN_TRX ✗ |
| ORDERMATCH | Production Test | Normal | ORDERMATCH ✓ |
| PE_F_IAS | Production | Ignore OK | PE_F_IAS ✓ |
| SE_CUST_ADDON | Production | Ignore OK | AS_PAID_TAX_RCL ✓, RC_ASH_RECEIVER ✓, RC_CASH_BAL ✓, RC_PEND_TAX_RCL ✓, SE_ENH_TRD_STAT ✓ |
| SIM_ALTS | Production | Ignore OK | SIM_ALTS ✓ |
| SO_ODA | Production | Normal | SO_ODA ✓ |
| TP_NBIN_TRANS | Production | Normal | TP_NBIN_TRANS ✓ |
| TP_TC_APL | Production | Ignore OK | TP_TC_APL ✓ |

`NW_MAIN` is the only multi-solution Wealth parameter set and in this TEST snapshot **four
of its five setups are inactive** — only `NW_BULK_FEE` would load. `NW_BULK_TRADES` is
inactive in both parameter sets that contain it, so it does not run at all here.

## D. Reference File Names used as log directories (11)

`ARCHON_LOG`, `AS_BDL_CONV_CS`, `AS_CA_PS_COAC`, `AS_CA_PS_CAM`, `DM_ALTS_LOG`,
`NW_ACC_SYNC_LOG`, `ORDERMATCH`, `SE_CUST_ADDON_L`, `SIM_ALTS_CS_LOG`, `TP_NBIN_TRANS_LG`,
`TP_TC_AP_CS`. They are built from components — e.g. `ARCHON_LOG` = SimCorp Dimension
directory `log` + static text `Servers\` + `YYYY` + `MM` + `DD` — i.e. **a new folder per
day**, which is exactly the manual's recommendation for purging. Open mode "Create or
overwrite", charset Windows (ANSI), Create directory = Yes.

Eight parameter sets have **no** log directory: DA_BLOOMBERG, DM_COPP_CLARK,
FNDS_SFTP_AVISO, NW_AI_SKILL, NW_BULK_TRADES, NW_MAIN, PE_F_IAS, SO_ODA. For those, the
Switchbox log in a connected Mediator client is the only view of message history — plan
the investigation accordingly (attach before reproducing, not after).

## E. Configurable Message Types (3) — all type 15, Extract data – Point-2-Point

| ID | Name | Consumed by |
|---|---|---|
| `GAIN_REQUEST` | GAIN_REQUEST | AS_COACSRV |
| `SFTP_AVISO` | SFTP Execute – Aviso | FNDS_SFTP_AVISO |
| `TP_TC_CANCEL_REQUEUE` | Trade Capture – Cancel/New as Modify flow | TP_TC_CANC_MOD |

Because type 15 is Point-2-Point, only one production server per installation may hold
each of these. Duplicating one of these setups into a second production parameter set is
a configuration error.

## F. Protected File Directories (35, all status Protected)

Base `General` (33): ARCHON, AS_BLOOM_CONVERTER, AS_CA_SCLIB, AS_PAID_TAX_RECL, COAC,
COAC_CSD_LIB, DA_CAM, DA_GAIN_REQUEST, DM_ALTS, DM_COPP_CLARK, DM_DLS_LINK, DM_RMS_GAIN,
DM_RMS_GAIN_AZ, FNDS_SFTP_SRV, NI_ALERT_EXPORT, NW_ACC_SYNC, NW_AI_SKILL, NW_BULK_TRADES,
ORDERMATCH, PE_F_CONMON, PE_F_CORE, RC_ASH_RECEIVER, RC_CASH_BAL, RC_PTR_BNYM, RC_PTR_JPM,
SCLIB, SE_ENH_TRADE_STAT, SIM_ALTS, STDACKNAK, TP_NBIN_TRANS, TP_TC_APL, TP_TC_CANC_MOD,
TP_TC_X_ASH. Base `Bloomberg` (1): DA_BLOOMBERG. Base `SimCorp` (1): SCDRCONNECT.

Shared libraries referenced with `-` instead of a config file name: `AS_CA_SCLIB`,
`COAC_CSD_LIB`, `SCLIB` (and functionally `DM_DLS_LINK`, `TP_CTM_LIB`,
`TP_TC_SIM_CONV_MAP` in the file tree). Editing one of these affects every solution that
mounts it — check *Setup Server References* before touching them.

The on-disk `ComSrv` tree contains **55** solution folders — 20 more than the 35 exported
directories, because folders such as `NW_NBIN`, `NW_NBIN_TRX`, `NW_BULK_FEE`, `NW_OP_SYNC`,
`DM_DLS`, `TP_TC_TM`, `TP_TC_RFR`, `TP_CTM_TMPL`, `SIM_CTM_CONNECT`, `DM_RMS_*`,
`NI_BLB_UNK_UDLY` exist on disk but are not referenced by any of the 27 exported setups.
See 12 §A before concluding anything from that.
