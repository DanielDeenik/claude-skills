# 09 — Setup cards: trade capture and orders

---

## ORDERMATCH — General Order Match  *(high traffic, DEX-heavy)*

Types **7 Data Extractor, 9 Order General Match**. PFD `ORDERMATCH`,
`Config.ORDERMATCH.xml` (4 cartridges, 15 XSLTs). Parameter set `ORDERMATCH`
(**Production Test**, log mode Normal, log reference file `ORDERMATCH`).

Parameters: `MATCH_DIR = @confparam(Directory,ACTIVEDATA)\Interfaces\OrderMatch`,
`MATCH_STP_QUEUE = FO_OM_STP`, `MATCH_AUX_MSG_EXT_ID = ORDMATCH`,
`TIMEZONE_OFFSET = -PT4H`, alert `ASN_ORDERMATCH = ORDERMATCH`, and four extraction
definitions used as live lookups:

| Parameter | DEX | Looks up |
|---|---|---|
| `MATCH_DEX_SECURITY_ID` | `OM_CSVR_SECURITY_ID` | security |
| `MATCH_DEX_PORTFOLIO` | `OM_CSVR_PORTFOLIO` | portfolio |
| `MATCH_DEX_ORDER_NO` | `OM_CSVR_ORDER_NO` | existing order |
| `MATCH_DEX_FX_RATE` | `OM_CSVR_FX_RATE` | FX rate (only when trade, quotation and settlement currencies do not all match) |

Flow: `cartridge.FileIn.xml` passes the payload to `MatchIn`.
`cartridge.IncomingRecords.xml` backs the raw file up to
`MATCH_DIR\BackUp\<date>\<id>.txt`, parses CSV with `<extractdata delimiter=","
textqualifier="&quot;">`, then per record: `CalculatePrice.xslt` (fills price when column 9
is blank: `abs(Column8/Column7)`) → `ValidatePrice.xslt` (rounding reconciliation) → three
**synchronous** `<query … label="SCIn_DataExtractExecute">` lookups → when the trade, quotation
and settlement currencies do not all match, `DEXQuery_FXRate.xslt` +
`FXAdjustPrice_1.xslt` → `MatchRequestCommand.xslt`.
`cartridge.CreateOrderMatch.xml` formats with `OrderGeneralMatchFormat_Wealth.xslt`,
validates with `scCheckIncomingFields.xslt`, applies an XSLT from **outside the PFD**
(`@confparam(Directory,MEDIATORSC)/FIX_Receive2AplXml.xslt`) and sends
`label="SCIn_OrderGeneralMatch"`.

Support:
- Slow matching is expected behaviour, not a bug: three synchronous `<query>` calls per
  record block the port (02 §G, `commserv.pdf` §7.2.6). Volume, not code, is usually the
  cause.
- A lookup returning nothing fails the record — reproduce the DEX in the Data Extractor
  before touching the cartridge (`simcorp-dex-validator`).
- The raw file is always backed up under `MATCH_DIR\BackUp\<date>` — use it to replay
  through the Message Tester instead of asking for a resend.
- `cartridge.SCOut.xml` has **only** an `scdLog` — no try/catch, no dead letter, no alert
  (12 §C). A failure on the response leg is silent. Treat "the order match request went out
  but nothing came back" as a known blind spot: check SimCorp side directly.
- `FIX_Receive2AplXml.xslt` lives outside the exported tree; its presence cannot be
  verified from the PFD. If the Configuration tab shows it red/"Not found", the
  `MEDIATORSC` directory parameter is the thing to check, not the cartridge.

---

## TP_NBIN_TRANS — Trade Capture satellite (NBIN transactions)

Types **0 General, 3 MQ, 7 Data Extractor, 19 Filter Tool Box**. PFD `TP_NBIN_TRANS`,
`Config.xml` (4 cartridges, 17 XSLTs, 5 lookup `.txt` files). Parameter set
`TP_NBIN_TRANS` (Production, log mode Normal, log `TP_NBIN_TRANS_LG`).

Parameters: `FILE_IN = @confparam(Directory,INTERFACES)\In\SFTP\NBIN\Transactions\Working`,
`ARCHIVE_FILE = …\Transactions\Archive`,
`TC_FILE_IN = @confparam(Directory,INTERFACES)In\TRADE_CAPTURE\FILE_IN`,
`MQ = TP_TRADE_CAPTURE-CFD`, and `WEBSPHERE_MANAGER` / `WEBSPHERE_QUEUE` **both empty** —
the WebSphere path is configured but not populated in TEST. Do not assume MQ connectivity
exists here.

Support: Working vs Archive tells you whether a file was consumed. `Cartridge_TC_Split.xml`
calls `check_completeness.xslt`, which is **missing from the directory** (12 §B) — a split
that fails on completeness checking is a known gap, not a data problem.

---

## TP_TC_APL — Trade Capture, APL-relevant trades

Types **3 MQ, 7 Data Extractor, 19 Filter Tool Box**. Configs `Config.xml` (PFD
`TP_TC_APL`) + `config.scDLSLink.xml` (PFD `DM_DLS_LINK`). Parameter set `TP_TC_APL`
(Production, Ignore OK, log `TP_TC_AP_CS`). 12 cartridges, 18 XSLTs.

Parameters: `DEAL_ALLOCATION = Yes`, `LINKED_TRADE_TIMEOUT = 300`, and the lineage block
`DLS_SOLUTION = Trade_Capture`, `DLS_SRC_SYSTEM = SCD`, `DLS_DEST_SYSTEM = External`,
`DLS_DATA_BACKUP = Yes`.

`LINKED_TRADE_TIMEOUT` (300) feeds `<Sequencer Name="LinkedTrade" LifeSpan="300"
MessageFailTreatment="AutoDeleteMessages">`. That is the key operational fact: **a linked
trade whose partner does not arrive within 300 seconds is auto-deleted from the sequencer**
— it does not dead-letter and it does not alert. "Half a linked trade went through" is
explained by this parameter, and raising it is a local-parameter change (live-applicable).

Queues declared here: `TC_2APL`, `TC_2RFR`, `TRADELINK`, `WINDOWMAPPING`,
`SPECIALHANDLING`, `DEALALLOC`, `EXTCLIENTTRADE`, `BLOCKALLOC`, `ALLOCONLY`,
`TRADEIMPORT`, `LINKEDTRADE`. Direction is outbound (SCD → External). `CANCELMODIFY` and
`CANCELREQUEUE` belong to `TP_TC_CANC_MOD`, not here.

Support: as with DM_ALTS, `DLSLink` is declared only in `DM_DLS_LINK` — that config row
must stay Active.

---

## TP_TC_CANC_MOD — Cancel/New treated as Modify  *(no parameter set)*

Types **3 MQ** and **15 Extract data – Point-2-Point** via configurable message type
`TP_TC_CANCEL_REQUEUE`. PFD `TP_TC_CANC_MOD`, `Config.xml`. Parameters:
`CANCEL_MODIFY = @confparam(Directory,INTERFACES)IN\TRADE_CAPTURE\CANCEL_MODIFY` and
`ARCHIVE_CANCEL_MODIFY = …\ARCHIVE_CANCEL_MODIFY`.

**Not in any parameter set in this export.** Before answering "why is a cancel/new not
being turned into a modify", the first check is whether this setup is deployed at all in
the environment being asked about. Its Point-2-Point configurable type also means only one
production server per installation may carry it.

---

## TP_TC_X_ASH — Trade Capture ASH connector  *(no message types, no parameter set)*

PFD `TP_TC_X_ASH`, `Config_ASHtoTC.xml`, no local configuration parameters, no message
types, not in any parameter set. It is one of a family of bridge configs in the tree
(`TP_TC_X_FILE`, `TP_TC_X_QUEUE`) that move messages between a transport and the trade
capture process using the generic `<Port Type="…">` style. Treat it as a transport shim:
if trades from ASH are missing, the live path is more likely `RC_ASH_RECEIVER`
(card 10) or `TP_NBIN_TRANS`.

---

## Not in this export but present on disk

`NW_NBIN`, `NW_NBIN_TRX`, `TP_TC_TM`, `TP_TC_RFR`, `TP_CTM_TMPL`, `SIM_CTM_CONNECT`,
`DM_RMS_OM`, `DM_RMS_REQ_SEC`, `NW_OP_SYNC`, `NW_BULK_FEE` all have full config/cartridge
sets in the `ComSrv` tree, and `NW_MAIN` references `NW_NBIN`, `NW_NBIN_TRX` and
`NW_BULK_FEE` as setups — but those setups were not part of this 27-setup export. The
NBIN batch-chain pattern they use is described in 02 §E, and the gap is logged in 12 §A.
Re-export with those setups selected before supporting them in detail.
