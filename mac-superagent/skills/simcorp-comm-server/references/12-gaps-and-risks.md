# 12 — Verified gaps and risks in this environment

Everything here was found by inspecting the 2026-08-18 TEST export and the `ComSrv` tree.
Each item says what was checked, so it can be re-verified rather than believed.

## A. Coverage gaps in the export itself — read before drawing conclusions

- The setups export contains **27** setups. The parameter sets reference **four setups that
  are not in it**: `DM_BLB_UNK_UNDE` (in parameter set `DA_BLOOMBERG`), `NW_BULK_FEE`,
  `NW_NBIN`, `NW_NBIN_TRX` (all in `NW_MAIN`). Their configuration parameters, message
  types and config-file lists are therefore **unknown** — the file tree shows what they do,
  not how they are wired.
- Five exported setups sit in **no parameter set**: `DM_RMS_GAIN`, `DM_RMS_GAIN_AZ`,
  `NI_ALERT_EXPORT`, `TP_TC_CANC_MOD`, `TP_TC_X_ASH`. Configured, not deployed here.
- The `ComSrv` tree holds **55** solution folders against 35 exported Protected File
  Directories. Folders with no exported PFD row include `NW_NBIN`, `NW_NBIN_TRX`,
  `NW_BULK_FEE`, `NW_OP_SYNC`, `DM_DLS`, `TP_TC_TM`, `TP_TC_RFR`, `TP_CTM_TMPL`,
  `TP_CTM_LIB`, `TP_TC_SIM_CONV`, `TP_TC_SIM_CONV_MAP`, `TP_TC_X_FILE`, `TP_TC_X_QUEUE`,
  `SIM_CTM_CONNECT`, `DM_RMS_OM`, `DM_RMS_REQ_SEC`, `DM_RMS_ULTUMUS`, `NI_BLB_UNK_UDLY`, `DM_BLB_UNK_UNDERLY`,
  `FNDS_FILE_MGMT`, `RC_PTR_BNYM`/`RC_PTR_JPM` (these two *are* exported).
- **This is a TEST snapshot.** Nothing here proves what PROD does. Re-export before
  answering a PROD question.

## B. Broken or missing file references (would fail at run time)

Found by resolving every `<Cartridge>` and `apply=` reference against the actual tree.
The Mediator's Configuration tab shows these in red as "Not found".

| Where | Missing | Impact |
|---|---|---|
| `DA_GAIN_REQUEST/config.gain_oraq.xml`, `config.gain_webspheremq.xml` | `cartridge.scGainRequestIn.xml`, `cartridge.scGainRequestDex.xml` | 2 of 6 declared cartridges absent |
| `DM_RMS_REQ_SEC/cartridge.OM.xml` | `OM_TranslateIdType.xslt`, `OM_CreateOpenFigiRequest.xslt`, `OM_TranslateInstType.xslt`, `OM_CreateRequest.xslt`, `OM_CreateResponse.xslt` | **Live wiring** — the OpenFIGI security-mapping flow fails if invoked |
| `AS_BLOOM_CONVERTER/Cartridge.xml` | `Bdl_conv_DEL_.xslt` (the `DEL_` flow is in the valid list) | a Bloomberg `DEL_` corporate-action record cannot resolve its transform |
| `TP_NBIN_TRANS/Cartridge_TC_Split.xml` | `check_completeness.xslt` | split completeness check fails |
| `TP_CTM_TMPL/cartridge.scRepoProcessing.xml` | 5 XSLTs (`scFormatTMRepoRec`, `scInitDmCmd`, `scInitFilterCommand`, `scFilterResponse`, `scDMImportResponse`) | repo processing path |
| `STDACKNAK/cartridge.scStdAckNak.xml` | `scMakeUniqeMetaData.xslt` | shared ack/nak library |
| `DM_DLS/cartridge.scGeneral.xml` | calls `connMon_query.xslt`; the file present is `ConMon_Query.xslt` | different string, not just case — fails on a case-sensitive filesystem |
| `COAC/cartridge.scTest.xml` | 5 XSLTs | developer harness only, wired into `Config.sc-Test.xml` |
| `DA_CAM/configCorpactMq.xml`, `configCorpactFile.xml` | 3 cartridges each | **orphaned legacy** (2012 headers, paths outside the PFD); not in the active setup — ignore, or propose deletion |

Also: **34** `apply=` / `<Cartridge>` references differ from the on-disk filename **only by
letter case** (COAC, DM_RMS_ULTUMUS, DA_GAIN_REQUEST, DM_DLS, TP_CTM_TMPL, DA_CAM,
TP_TC_CANC_MOD, TP_TC_APL, TP_TC_TM, TP_NBIN_TRANS, TP_TC_RFR, PE_F_CONMON). Harmless on
Windows; a landmine if the tree is ever compared, deployed or diffed on a case-sensitive
system. The **PE_F_CONMON** one is the serious one — it is cartridge-level and inside the
live `PE_F_IAS` Production setup: `Config.MDATaaS_ConMon.xml` declares
`<Cartridge>cartridge.MDATaaS_ConMon.xml</Cartridge>` while the file on disk is
`cartridge.MDATaas_ConMon.xml`. Separately, the `DA_BLOOMBERG` **setup** registers its
config file as `config.sc-ftp.xml` while the PFD holds `Config.sc-Ftp.xml` — a
setup-to-PFD case mismatch that the reference-scan above does not cover.

## C. Solutions with no failure path at all

Scanned every config + cartridge for `deadletter|error|retry|acknak|alert|mailsender`:

- `RC_CASH_BAL` — cash balance reconciliation
- `RC_PTR_BNYM` and `RC_PTR_JPM` — pending tax reclaim
- `SE_ENH_TRADE_STAT` — enhanced trade status (and it feeds downstream batch logic)

No dead letter, no retry, no alert, no e-mail. A failure in any of these is visible only
in the shared `SE_CUST_ADDON_L` log — and that parameter set runs log mode *Ignore OK
messages*, so there is no positive confirmation of success either. These are custodian
cash and tax-reclaim feeds; the absence of a failure path is worth raising with the
environment owner as a finding, not just a note.

Narrower case: `ORDERMATCH/cartridge.SCOut.xml` contains only an `scdLog` — no try/catch,
no dead letter, no alert — even though the rest of ORDERMATCH does use `<try>/<catch>` and
declares `ASN_ORDERMATCH`. The response leg of order matching is unmonitored.

## D. Cross-solution dependencies that are invisible from one file

`DM_ALTS`, `SIM_ALTS`, `TP_TC_APL`, `TP_TC_RFR` and `TP_TC_TM` all `send … port="DLSLink"`
but none declares that port. It is declared once, in
`DM_DLS_LINK/config.scDLSLink.xml` as `<Memory Name="DLSLink" Listen="true" />`.
Those solutions therefore only work when `DM_DLS_LINK` is loaded into the **same**
Communication Server. `DM_ALTS`, `SIM_ALTS` and `TP_TC_APL` do include that config row —
`TP_TC_RFR` and `TP_TC_TM` are not exported setups, so their wiring is unverified.
Removing the `DM_DLS_LINK` row from a setup silently breaks its lineage logging.

Similarly, `AQ_PACKAGE`, `AQ_CONNECT` and `AQ_ENCODING` are used via `@const()` in almost
every Dimension/Oraq config but declared in none — SimCorp Dimension injects them at
start-up. Not a gap; do not "fix" it.

`ORDERMATCH` applies `@confparam(Directory,MEDIATORSC)/FIX_Receive2AplXml.xslt` from
**outside** the protected tree. Its presence cannot be verified from the export, and it is
not under Protected File Directory control — an unmanaged dependency on a live path.

## E. Configuration risks worth flagging to the owner

1. **Eight parameter sets have no log directory** (06 §D). For those interfaces there is no
   retained message history at all — only a live Switchbox log. That includes
   `DA_BLOOMBERG`, `FNDS_SFTP_AVISO`, `PE_F_IAS` and `SO_ODA`.
2. **`NW_MAIN` has four of five setups inactive**, and `NW_BULK_TRADES` is inactive in both
   parameter sets that reference it. Either that is intentional staging or the Wealth bulk
   path is dark. Confirm before anyone says "bulk trades broke".
3. **Fixed `-PT4H` timezone offsets** in `DM_COPP_CLARK`, `NW_AI_SKILL`, `ORDERMATCH`.
   These do not follow daylight saving; the effective run/stamp time shifts by an hour at
   each DST boundary.
4. **`TP_NBIN_TRANS` has empty `WEBSPHERE_MANAGER` / `WEBSPHERE_QUEUE`** — the MQ path is
   declared but unconfigured in TEST.
5. **`DM_RMS_GAIN_AZ` has empty `COMSERVCLIENTID`, `COMSERVSECRET`, `TOKEN_URL`.** Not
   deployable as exported.
6. **`TP_TC_APL`'s `LINKED_TRADE_TIMEOUT = 300`** auto-deletes an unmatched linked trade
   from the sequencer (`MessageFailTreatment="AutoDeleteMessages"`) with no dead letter and
   no alert. Silent data loss by configuration.
7. Passwords appear masked (`********`) in the CEI export, but `.ppk` private key files
   (`bbsftpnonprod.ppk`, `sshprivatekey_aviso/ssc/bmo.ppk`) are **inside the exported
   tree**. Treat any copy of that export as a credential-bearing artefact.

## F. Questions this export cannot answer

- What the Mediator Help tab lists as available ports, port attributes, metadata, message
  types and Gateway command parameters — both manuals deliberately delegate these.
- Whether PROD matches TEST in any respect.
- The wiring of `NW_NBIN`, `NW_NBIN_TRX`, `NW_BULK_FEE`, `DM_BLB_UNK_UNDE`.
- Whether `@confparam(Directory,MEDIATORSC)` resolves on the live server.
- Whether any of the missing files in §B were deliberately retired or are genuine breakage
  — that needs the person who built the solution.
