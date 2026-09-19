---
name: simcorp-comm-server
description: >
  SimCorp Dimension Communication Server support for Nicola Wealth — triage interface
  incidents and configure or change any of the 27 Communication Server Setups in this
  environment. Covers the object chain (Protected File Directory, Setup, Parameter Set,
  Gateway and Mediator services), the Mediator client (dead letter port, Switchbox log,
  debug, sandboxes, testbench), config/cartridge/XSLT anatomy, CDL and Gateway commands,
  SCIn/SCOut message contracts, and a card per solution. Use when a file did not
  arrive, a message vanished, an import or batch chain stalled, a dead letter queue is
  filling, a Comm Server will not start or runs but processes nothing, characters are
  garbled, throughput is slow, or when adding or changing a setup, port, cartridge or
  configuration parameter. Trigger: comm server, communication server, ComSrv, Mediator,
  cartridge, CDL, dead letter, Switchbox, protected file directory, parameter set, SCIn,
  SCOut, DM_ALTS, NW_NBIN, ORDERMATCH, DA_BLOOMBERG, FNDS_SFTP.
---

# SimCorp Communication Server — support and configuration

Sisters: `simcorp-dex-builder` / `simcorp-dex-validator` (the extraction definitions this
server calls), `simcorp-database-tracing`, `simcorp-performance-toolkit`,
`simcorp-oracle-configuration` (Oracle/platform layer under the server). This skill owns
**the Communication Server itself** — its objects, its files, its message flow, and what to
do when an interface misbehaves.

## Ground rule

Never guess a window, field, port attribute, queue name, directory or parameter value.
Three authoritative sources, in this order:

1. **The environment export** — `references/06-setup-catalogue.md` and the per-family
   setup cards (07–10). Provenance: SimCorp Dimension **26.04 SP0**, track `IMPL`, state
   **TEST**, `custid=NICOLA`, exported by DDEENIK **2026-08-18T14:53–14:55Z**. Contents:
   27 Communication Server Setups, 19 Parameter Sets, 35 Protected File Directories, 3
   Configurable Message Types, 11 Reference File Names, plus the `ComSrv` file tree
   (1,064 files: 71 config XML, 241 cartridge XML, 711 XSLT, across 55 solution folders).
2. **The manuals** — `commserv.pdf` (Communication Server, Sept 2025) and `commseri.pdf`
   (Communication Server Gateway, Sept 2025) in `ii. Manuals & Documentation/PDFs/`.
   Section numbers are cited throughout the references.
3. **The Mediator's own Help tab** — the manuals deliberately delegate the full port list,
   port attributes, metadata, message-type list and Gateway-command parameters to it.
   If an answer needs one of those, say so and go read Help rather than inventing it.

If the answer is in none of the three, say "I don't know — this needs the Mediator Help
tab / a screenshot / SimCorp". An empty grep proves only that the string is absent from
what was exported.

## The object chain — get this right before anything else

```
Protected File Directory   files (config.xml, cartridge*.xml, *.xslt, *.xsd, lookups)
   ↓  referenced by
Communication Server Setup = ONE SOLUTION
        local Configuration parameters  (@confparam(Local,NAME))
        Message types                   (gate: wrong/inactive type ⇒ message discarded)
        Configuration files             (subdirectory + file name, or "-" for a library)
        Instance restriction            (default One Instance Only)
   ↓  grouped by
Communication Server Parameter Set
        Server type: Inactive | Production | Production test | User test
        Log mode: Normal | Ignore OK messages ; Log directory (Reference File Name)
        Which setups are Active
   ↓  started as TWO services on the Service Platform, same parameter set
Communication gateway service   +   Communication mediator service
```

A setup can sit in several parameter sets; a parameter set can hold several setups; a
protected file directory can serve several setups (that is how `SCLIB`, `AS_CA_SCLIB`,
`COAC_CSD_LIB`, `TP_CTM_LIB`, `DM_DLS_LINK` work — referenced with `-` as the file name).

## Triage — start here

| Symptom | First move | Detail |
|---|---|---|
| Server will not start | Solution + parameter-set logs writable? `service.log` in the installation `Log` folder, Windows event log, then Gateway/Mediator **service histories** | 02 §A |
| Service shows "running" but nothing is processed | Stale state: a port was unreachable at start-up and the parameter set is in **test** mode. In Production the Mediator shuts down instead | 02 §A |
| File dropped, nothing happened | Wrong file name vs `InputFilePattern`; received but errored; never sent. Check log, local folders, remote SFTP, dead letter | 02 §B |
| Message vanished with no error | Label has no handler **and** the port has no `(Default)` handler ⇒ discarded (info log + Switchbox notification). Or the message type is not enabled/active on the setup | 02 §C |
| Dead letter queue filling | Mediator **Dead Letter Port** tab → Resend First Message / Delete First Message / Delete All. Fix cause first | 03 §C |
| Import ran, records rejected | Read the response XML: `<Status><State>`, `<Log><Error>`, per-record `pMSGSTAT=dMSGSTAT_ERROR` + `pERRMSG` | 05 §D |
| Batch chain stalls mid-way | Stage waits on its `BatchResponse` handler; check the batch queue, the batch job group, and the SCOut response label | 02 §E, 07–10 |
| Garbled characters / XML will not open in a browser | Encoding: port `Encoding` attribute vs XML header; double-byte used where single-byte expected | 02 §F |
| Slow / backing up | File-port `sort`, anti-virus on the input folder, too many listening ports, huge log folders, `<query>` used instead of `<send>` | 02 §G |
| Change saved but no effect | Local config parameters apply live; **message types and configuration files do not** — restart the Mediator service or click **Reload** in a connected Mediator client | 02 §H, 11 |
| Duplicate processing / two servers fighting | Point-2-Point message types allow only one production server per installation; File/FTP ports do not load-balance and are not re-entrant | 02 §I |

## The 27 setups — pick the family, then the card

| Family | Setups | Card |
|---|---|---|
| Market & reference data, corporate actions, custody vendors | `DA_BLOOMBERG` `AS_BDL_CONVERT` `DA_CAM` `AS_COACSRV` `DM_COPP_CLARK` `DM_RMS_GAIN` `DM_RMS_GAIN_AZ` | 07 |
| Alternatives + Wealth (Nicola-built) | `DM_ALTS` `SIM_ALTS` `NW_ACC_SYNC` `NW_AI_SKILL` `NW_BULK_TRADES` `NI_ALERT_EXPORT` `ARCHON` | 08 |
| Trade capture & orders | `TP_NBIN_TRANS` `TP_TC_APL` `TP_TC_CANC_MOD` `TP_TC_X_ASH` `ORDERMATCH` | 09 |
| Reconciliation, settlement, outbound transport, performance, platform | `RC_CASH_BAL` `RC_ASH_RECEIVER` `RC_PEND_TAX_RCL` `AS_PAID_TAX_RCL` `SE_ENH_TRD_STAT` `FNDS_SFTP_AVISO` `PE_F_IAS` `SO_ODA` | 10 |

## References

| File | What is in it |
|---|---|
| `references/01-architecture-and-objects.md` | Windows, fields, statuses, options, prerequisites, service start-up |
| `references/02-triage-playbooks.md` | The nine playbooks referenced in the table above |
| `references/03-mediator-client.md` | Tabs, dead letter handling, debug, sandboxes, testbench, reload |
| `references/04-config-cdl-reference.md` | Config XML anatomy, port census in this environment, CDL statements |
| `references/05-gateway-contracts.md` | SCIn/SCOut labels, message contracts, status and error semantics |
| `references/06-setup-catalogue.md` | All 27 setups + 19 parameter sets + 35 directories, one index |
| `references/07..10-setups-*.md` | Per-setup support cards, by family |
| `references/11-change-procedure.md` | How to change a setup/PFD/parameter set safely, and scaling |
| `references/12-gaps-and-risks.md` | Verified gaps in this environment — broken references, missing error handling |
| `scripts/parse_comsrv_cei.py` | Re-parse a fresh CEI export into the catalogue tables; never hand-type them |

Refresh rule: the catalogue is a **dated snapshot of TEST**. Before answering anything
about current PROD behaviour, re-export and re-run the parser — do not present TEST facts
as PROD facts.
