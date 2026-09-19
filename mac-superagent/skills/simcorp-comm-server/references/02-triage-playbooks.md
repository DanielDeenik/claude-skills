# 02 — Triage playbooks

Each playbook: what you are looking at → what to check, in order → what fixes it.
Manual references are `commserv.pdf` unless stated.

## A. Server will not start, or runs but processes nothing (§7.3.1, §3.6.1)

1. Can the solution logs be written? Check the **solution server log** and the
   **parameter set log** (the log directory named on the parameter set — see the
   Reference File Name in 06).
2. `service.log` in the **Log** folder of the installation directory holds error messages
   for **all** services.
3. Windows event log on the host. Unhandled Mediator exceptions go there; if the server
   cannot write to it, look for `MediatorErrorLogXXXX.log` in `%TEMP%`.
4. If the logs are empty or stale, check the **service histories** for Gateway and
   Mediator (System Manager). This is the manual's own next step, not a workaround.
5. **"Running but idle" is a specific, diagnosable state.** A port protocol was
   unreachable at start-up while the parameter set is in test mode (Production test / User
   test) → the server starts in **stale state**: the monitor shows running, nothing is
   processed. In *Production* it would have shut down instead. Fix the port target
   (folder, share, queue, SFTP host), then restart.
6. Production mode additionally requires **every** file in the solution to be status
   *Protected* and the setups to be **valid** (Functions → Validate Setup).
7. Both services must run against the same parameter set. One alone is not a server.

## B. A file was sent but nothing happened (§7.3.2)

Three possibilities, in the manual's own order: received but not handled (wrong file
name); received but errored; never created by the sender.

1. Log files first — errors or warnings naming the file.
2. Compare the actual file name against the port's `InputFilePattern` and the setup's
   pattern parameter (e.g. `DATA_FILE_PATTERN`, `RC_CB_FILE_PATTERN_IN`,
   `SE_ETS_FILE_PATTERN_IN_JPM`, `DEX_FILE_PATTERN_AVISO`). "A common error is to forget
   to handle a specific file name on a port that listens to all files."
3. Check the local folders used for transfer — the `FILE_DIR_IN` / `..._IN_FOLDER` /
   `Working` directory, and the `Archive` directory (already processed?).
4. Log on to the remote SFTP site and confirm the file is actually there; the address is
   a configuration parameter of the solution.
5. "The file can be written to a dead letter queue if there is an unhandled exception" —
   check the Dead Letter Port tab (03 §C).

## C. A message vanished with no error (§3.3.1, §4.4)

Two silent-discard rules, both by design:

- **Message type gate** — "If you send a message to a label that is not enabled by the
  message type, then the message is discarded." Open the setup, confirm the message type
  row exists **and** that *Active* is ticked.
- **No handler and no `(Default)`** — "If a port has no `(Default)` label defined and a
  message is received with a label that is not specified for the port, the message is
  discarded. An information log message is generated, and a notification is sent to the
  Switchbox log." So: open the Switchbox log, find the notification, then add a
  `(Default)` handler that raises an error rather than swallowing the message. The manual
  recommends every port has one.

## D. Dead letter queue is filling

Dead letters are messages that failed inside a handler, on a port that has a
`DeadletterPort` configured (`listen="yes"` ports only), plus messages whose label has no
handler. **The manual contradicts itself on the trigger value**: §4.5 says the attribute
`IgnoreUnhandledMessages` "defaults to false … if the attribute is false, and the port has
a dead letter port specified, the unhandled messages are sent to the dead letter port",
while §4.5.4 says the dead letter queue receives unmatched messages "if the attribute
IgnoreUnhandledMessages is set to True". Do not state either as fact — check the Mediator
Help tab or the live port before relying on it. The Dimension-side pair is `SCInDeadLetter` /
`SCOutDeadLetter`. Handling is in 03 §C. Rule: diagnose before resending — a resend into
an unchanged fault just returns the message to the queue.

## E. A batch-driven chain stalls part-way

The pattern used across this environment (clearest in `NW_NBIN`) is: build a batch command
with an XSLT → `send … port="SCIn" label="SCIn_BatchQueue"` → **wait for the stage's own
`BatchResponse` handler** (fed from `SCOut`) → only then trigger the next stage.

1. Identify the last stage that completed (parameter-set log / Switchbox log / the
   persistence port's tracker records).
2. Did the batch job group actually reach the batch queue? Check the queue named by the
   setup's `..._BATCH_QUEUE` parameter and the group named by `..._BATCH_JOB_GROUP_*`.
3. Read the batch response XML: `<Status><State>` and `<Message>`; the response also
   returns `<BatchQueueIK>`.
4. If the group ran but the chain did not advance, the `SCOut` response label is not being
   matched by a handler — check the SCOut cartridge for that stage's label.
5. `<Status>` on the request can be `dMSGSTAT_ONHOLD`, which parks the group deliberately
   until it is set to `dMSGSTAT_QUEUED`.

## F. Garbled characters, or XML that will not open (§7.3.5, §4.3)

- Every port must have an explicit `Encoding` — do not rely on defaults. Most solutions
  here use `ISO-8859-1`.
- "If your text files have an extra character (a period) for each character in the file,
  you have accidentally used a double-byte encoding scheme (for example utf-16) instead of
  a single-byte scheme (for example ISO-8859-1)."
- "If the XML file opens OK in Notepad, but will not open in your default browser, you
  likely have a mismatch between the XML header encoding scheme and the one used in the
  file."
- The Communication Server **ignores** `<xsl:output encoding="…">`. All messages are
  utf-16 inside handlers. To control the written header use
  `<xsl:output omit-xml-declaration="yes"/>` or the CDL `<setxmlencoding …>`.
- WebSphere MQ ports use `Encoding` **or** `CharSet` depending on text vs binary.

## G. Slow, or backing up (§7.2)

| Cause | Check | Fix |
|---|---|---|
| File port sorting | `sort="true"` on a file port | With >1000 files waiting this rescans on every pick-up. Set `sort="no"` unless sequence matters |
| Anti-virus | Input folder on a file server with active AV | Exclude the interface folders |
| Too many listening ports | Count of `Listen="yes"` ports | Each gets a thread; reduce ports, fan out internally by content, or split the solution across hosts |
| Log folders | Log directory with many files | Clean regularly; create log folders per date (this is what the `*_LOG` reference file names in 06 do) |
| Huge XML messages | Message size (§4.3, not §7.2) | Select relevant nodes / split with `<foreach>` / split the document. Size alone is not the rule: ">5 MB can process fine and one less than 500 KB can cause memory exception" — complex XSLT is often the real cost |
| Synchronous calls | `<query>` in cartridges | `<query>` blocks the port until answered; prefer `<send>`. Same for synchronous Data Extractor requests |
| Detailed logging | Parameter set log mode = *Normal* | Switch to *Ignore OK messages* |

## H. A change was made and nothing changed (§3.3.6, §6.9)

- Local **configuration parameters** apply while the service runs.
- **Message types** and **configuration files** do not. Restart the Communication Mediator
  service, or click **Reload** in a connected Mediator client (available from every tab —
  it reloads all configuration files of the loaded solution without a restart).
- File edits must go through the Protected File Directories window (Edit → change →
  Test → Protected). Editing files directly on disk "can be ignored and overwritten".
- If the setup is validated, clear the validation before inserting/updating files.
- XSL caching: **off** in test mode (each transform reloaded from disk — that is why test
  behaves differently), **on** in production mode.

## I. Duplicate or competing processing (§3.3.1, §5.2, §7.3.6)

- Only **one production Communication Server per installation** may hold a given
  Point-2-Point message type. Two production parameter sets carrying the same
  Point-2-Point type is a configuration error, not a race condition.
- File and FTP ports are **not re-entrant** — they cannot load-balance and two solutions
  must never point at the same physical folder.
- Multiple solutions on one machine share the same TEMP folder. If different SimCorp
  Dimension versions run on one host, set FTP/File port `workpath` to TMP (which includes
  the installation name) instead of the default TEMP.
- In a queue-based interface where order matters, do not scale to multiple Mediator or
  Gateway instances — order is not preserved.

## J. When to stop and escalate

Escalate to SimCorp / the hosted DBA when: the Oracle user schema or AQ is unavailable
(the server cannot run at all without it); WebSphere client/server version mismatch (the
manual defers to the System Administrators' Manual); an interface package component is
locked; or the failure is in a SimCorp-owned setup (`SO_ODA`) or a licensed interface
package (`PE_F_IAS`, package 2446).
