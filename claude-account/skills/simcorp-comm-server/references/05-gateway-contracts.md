# 05 — SCIn/SCOut message contracts and error semantics

Source: `commseri.pdf` (Communication Server Gateway, Sept 2025). Use this when reading a
response payload, or when wiring a new call into SimCorp Dimension.

## A. The internal ports (commserv §4.5.4)

| Port | Direction |
|---|---|
| `SCIn` | Mediator → Gateway (requests into SimCorp Dimension) |
| `SCOut` | Gateway → Mediator (responses out of SimCorp Dimension) |
| `SCInDeadLetter` / `SCOutDeadLetter` | Failures the cartridge did not handle, plus messages whose label matched no handler — see 02 §D for the manual's own contradiction about the `IgnoreUnhandledMessages` value that triggers this |

They are generated automatically at start-up and bound to the Oracle AQs named on the
parameter set. `SCOut` listens, so **at least one `SCOut` handler must exist** in the
solution. The `(Mediator)` internal port carries `Start`, `Stop` and Notification events —
that is where a controlled-shutdown or version-check handler lives (§8.3).

## B. Which message type gates which label

The message type on the setup is the gate; the label is the routing key.

| Integration | Message type on the setup | Request label | Response label |
|---|---|---|---|
| Data Extractor | Data Extractor | `SCIn_DataExtractExecute` | `SCOut_DataExtractResponse` |
| Filter Tool Box | Filter Tool Box | `SCIn_FilterAction` | per `<Label>` node |
| Batch Queue | Batch Jobs | `SCIn_BatchQueue` | per `<Label>`, `SCOut_*` |
| Message Queue / STP (new) | not stated in §6 (MQ is stated only for the old integration, §8.1) | `SCIn_MsgQueueUpdate`, `SCIn_StpQueueUpdate` | `SCOut_MqResponse`, `SCOut_StpResponse` |
| Message Queue (old) | MQ | `dWEBMSGIN_MQFILTER`, `dWEBMSGIN_MQFILTERRESP`, `dWEBMSGIN_MQSTPINSERT` | `dWEBMSGOUT_MQPROCESS` |
| Fund actions | Fund actions | `SCIn_FundAction` | per `<Label>` |
| FO missing security | — | `SCOut_EdmFoRequest` (out) | `SCIn_EdmFoResponse` (in) |
| Logging | General | `SCIn_LogMessage` | — |
| Stop the server | General (Broadcast) | `SCIn_StopServer` | — |

`<Label>` conventions used across the Gateway contracts: a value starting `SCOut_` = an
**asynchronous** response; the literal `Respond` = **synchronous**; `-` = **no response**.

## C. Request shapes worth knowing

**Data Extractor** — root `<ExtractCommand Description=… type="asynchronous|synchronous|
noresponse">`, with `<Extract>` holding exactly one of `<ExtractionDefinition>`,
`<ExtractionSetup>` or `<ExporterDefinition>`, plus `<ID>`, `<ReturnFormat>` (xml|text),
`<RecCnt>` (a count or an interval such as `0-10000`; the manual does not state the
out-of-range behaviour for this node — the `Reccnt` attribute on `sc:definequery` in §2.3.2
that *does* raise an error is a different construct), and
`<Variables><UseDefaults>` (set `no` and missing variables are reported as errors).
There is a **record limit** on what the server can return: for large volumes use an
extracts exporter definition writing to a file, not an inline response.

**Batch Queue** — root `<BatchCommand>`, mandatory `<Label>` and `<BatchQueue>`, then one
or more `<InsertGroup><BatchJobGroup>` (and/or `<UpdateGroup>` keyed on `<ExtRef>`).
Optional `<Priority>` (`dPRIORITY_LOW|MED|HIGH`, default MED), `<WaitTo>` (`hhmm` or
`YYYYMMDDhhmm`, **not validated before execution**), `<Status>` (`dMSGSTAT_QUEUED` default,
or `dMSGSTAT_ONHOLD` to park it). `<UpdateGroup>` only touches entries whose status is
`dMSGSTAT_ONHOLD`, `_QUEUED` or `_ERROR`; anything else is ignored, and multiple matches on
the same `<ExtRef>` are **all** updated.

**Filter Tool Box** — root `<FilterCommand>` with one of `<DfsImport>`, `<DfsReformat>`,
`<DfsScFmtImport>`, `<DirectFilterImport>`, `<DirectFilterDfsImport>`, `<FilterImport>`,
`<FilterDfsImport>`. Mandatory mapping keys per action: `<pFILTER>` (direct filter),
`<pDFSETUP>` (data format setup), `<pDIRDFSINT>`, `<pFILTERDFSINT>`. `<ErrorFile>` is
mandatory unless `<ID>` is given — that is where rejected records land.

**Message Queue (new)** — root `<MqCommand>` with `<InsertMessages>` and/or
`<UpdateMessages>`. `<ID>` is mandatory and names the sub-node where results come back.
`<RespMode>`: `Clear` | `KeepIfError` | `Keep` controls how long response state is kept.
`<fpWAITTO>` / `<fpWAIT_MIN>` delay processing. Update needs `<pMSGQUE>` + `<pMSGIK>`.

**Fund actions** — `<FundActionCommand>` with `<ActionTrigger ID=…><FundAction>` = one of
`dFUNDACT_ENQUEUE`, `_DEQUEUE`, `_RAISEEV`, `_HOLD`, `_RELEASE` (two-person: first call
sets *Release requested*), `_DIRRELEASE` (single-person), `_DELEV`.

## D. Reading a response — the error surface

| Where | What it tells you |
|---|---|
| `<Status><State>` | `OK` or `Error`/`ERROR` — the overall verdict |
| `<Status><Action>` / `<Message>` / `<Time>` | What was attempted and when |
| `<Information>` per action node: `<ID>`, `<State>`, `<Result>` | Per-action outcome when one command carried several |
| `<Log><Error>` / `<Log><Msg>` | Per-action log lines and error text |
| Per record: `pMSGSTAT` + `pERRMSG` | The record-level verdict. Real example from the manual: `pMSGSTAT=dMSGSTAT_ERROR`, `pERRMSG=Unknown Exchange (#150: Exchange: [Exchange]) (MEB_BOND7;0;04-04-2001;Ask;DKK)` |
| `pMSGIK`, `pMSGQUEIK`, `BatchQueueIK` | The keys to quote when asking someone to look in the queue |

Message status domain (`tMSGQUEUE`): `dMSGSTAT_QUEUED`, `_ONHOLD`, `_ERROR`, `_REMOVED`,
`_DELETED`, `_SKIPPED`, plus `_FINISH` seen on successful processing. For the external STP
queue (`tSTPMSGEXTQUEUE`) only `_QUEUED`, `_ONHOLD`, `_ERROR`, `_DELETED` apply.

`<pERRSTOP>` (Boolean, default `no`) is the abort-on-error switch: set `yes` to stop
processing the following action nodes once one fails. Fund actions aggregate instead —
"When all messages succeed, the overall state is ok. If one or more actions fail, the
overall status is error and information on how many actions failed is added."

Partial success is therefore the normal case for imports: an overall `OK` does **not**
mean every record loaded. Always read the per-record statuses before telling a user the
import worked.

## E. SWIFT converter: warning vs exception (§2.2)

The converter validates format, character type and field length — **not** business
content. Recoverable problems are logged in a `<WarningList>` and the offending content is
usually stripped: `FieldOverrunError`, `SubFieldOverrunError`, `SubFieldLineOverrunError`,
`BlockOverrunError`, `BlockIdentifierError`, `UnknownFormatError`, `TruncationError`,
`LegalCharacterError` (illegal characters auto-converted, e.g. `Ø` → `OE`). Two are logged
but **not** removed from the converted message: `TooManyDecimalsError` and `NoDecimalError`
— those will reach the counterparty. Unrecoverable parse failures throw exceptions (e.g.
tag 50K missing its subfield structure; tag 30F date not exactly 8 numeric characters).
The `From` attribute on a mandatory SWIFT field is what gets sent back as the **NAK reason
code** — that is why mandatory-field metadata matters operationally.

## F. What the Gateway manual does NOT define

No retry/backoff policy, no request timeout, no redelivery semantics, no numeric return
code table, and no per-Gateway-command parameter documentation. It also never mentions
Oracle AQ or WebSphere MQ — its "message queue" means SimCorp's own table-backed queues.
Retry and dead-lettering are **port-level config concerns** (see 04), not Gateway
behaviour. Do not promise a retry that is not configured on the port.
