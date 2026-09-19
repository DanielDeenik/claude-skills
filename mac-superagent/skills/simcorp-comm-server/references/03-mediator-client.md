# 03 — The Mediator client: what each tab is for in a support situation

Source: `commserv.pdf` §3.5, §6. Start it from the Communication Server Setups window
(Functions → *Show Setup*) or from Communication Server Parameter Sets.

## A. Connection modes decide what you can do (§3.5)

| Mode | How | Tabs available |
|---|---|---|
| DISCONNECTED (offline) | Started from Setups / Parameter Sets window | Configuration, Ports, Editor, Visual, Sandbox, Testbench, Help |
| CONNECTED to Production | Attaches to a running production server | Switchbox log, Configuration, Ports, **Dead Letter Port**, Help, Visual, Sandbox, Testbench — no editing, testing or debugging |
| CONNECTED to Test | Attaches to a server whose parameter set is in test mode | All of the above **plus** Message Tester, Editor (needs the PFD status = Edit), Debug |

Consequence for support: **you cannot debug a production server.** To debug you need the
parameter set in test mode. In offline mode all ports are created as memory ports and no
connection is made to internal or external ports — safe to open a live solution without
sending anything anywhere.

## B. Configuration tab — first stop for "what is this solution wired to"

Tree of every config file listed on the setup plus the files they reference. Files that
are referenced but not found are shown **in red, marked "Not found"** — this is the
fastest way to see a broken `<Cartridge>` or `apply=` reference (see 12 for the ones
already known in this environment). The Configuration Parameters node shows Local /
Global / Directory / Standard values as actually resolved. Free-text search (plain or
regex) runs across every file in the solution; double-click a file to find references to
it. Right-click → Edit opens it on the Editor tab.

## C. Dead Letter Port tab — the recovery tool (§6.5)

"Messages are sent to a dead letter port when the messages fail to be handled, and there
is a dead letter port specified. The messages are sent to the dead letter port if any of
the handlers fail during the execution."

- Pick the port in the **Dead Letter Port** field. Messages are stored chronologically and
  **cannot be edited** here.
- **Delete First Message** — "Remove a message that is no longer valid, for example when
  the data is incorrect."
- **Resend First Message** — "Resend the message to its original destination, for example
  when a server is down." Use only after the cause is fixed.
- **Delete All Messages** — clears the selected port.

Bulk drain pattern (manual §8.2): add a `<Dimension Name="DeadLetterRead" Listen="yes"
Queue="@const(DLQueue)" …>` port plus a `<File Name="DLOutput" AutoCreate="yes"
Path="@confparam(Directory, DUMP)"/>` port, and a one-handler cartridge with
`label="(Default)"` that sends each message to `DLOutput`. That empties a dead letter
queue to disk for inspection/reprocessing instead of clicking through the tab.

Which ports here even have a dead letter: only 7 config files declare `DeadletterPort`
(STDACKNAK, DA_GAIN_REQUEST ×3, TP_CTM_TMPL, DA_CAM, DA_BLOOMBERG). Everything else
relies on `<try>/<catch>` + `scdAlert_Create`, or has no failure path at all — see 12.

## D. Switchbox log tab — what actually arrived (§6.9)

Every message on any listening port appears in the Message Event List. Clicking one shows:
time of arrival, the port it was received on, **the cartridge used to process it**, the
label attached, and whether processing succeeded. Tick *Ignore Success messages* to cut
noise. The same content is what gets written to the parameter set's log directory when one
is configured — if the parameter set has no log directory, the Switchbox log is the only
place it exists, and it is not retained.

**Reload** (available from every tab) reloads all configuration, cartridge and XSLT files
of the loaded solution without restarting the server.

## E. Ports tab — is it listening?

Shows the global settings, the enabled port technologies and the query timeout ("seconds
to wait for queries to get answered in a synchronous call"). Selecting a port shows the
attributes from the config file **plus the defaults that were omitted but still apply** —
use this rather than reading the XML when a default is in question.
*Listen – Stop* / *Listen – Start* let you stop a single port without stopping the
service (equivalent to the `<portstop>` / `<portstart>` CDL statements). Useful when you
want to stage a file without the Mediator picking it up.

## F. Visual tab — reading an unfamiliar solution fast

Graphical message flow. Blue = ports, yellow = SimCorp Dimension interactions, green =
files, pink = labels for message types **not implemented** (marked inactive — an
immediately useful defect signal). Arrows are CDL statements; click one to list them and
jump into the cartridge at that statement. Options worth switching on when investigating:
*Include references inside error handling* (shows what happens in `<catch>`), *Markup dead
letter ports*, *Include dynamic references* (resolves `@var`/`@msg`), *Show handlers*.
Exports to JPEG or WMF — a fast way to document a flow for a ticket.

## G. Message Tester — inject at any step (§6.7)

Select a port and a label, paste a message body, Send. "It is possible to insert a message
into any part of the flow" — the documented technique is to take the known-good output of
step 9 and use it as the input to test step 10, instead of re-running the whole chain.
Messages sent to a listening port appear in the Switchbox log; a failed message can be
edited there and resent. Optional fields depending on port: Correlation, Delay,
Expiration, Priority.

## H. Debug tab — only against a test-mode service (§6.8)

Select the port, set a breakpoint, trigger the flow (Message Tester, a batch job moving a
file into the listen folder, or the real external trigger). Data elements can be viewed as
text, hex or XML **and changed mid-run**. Attribute functions are evaluated and shown
before the statement executes. `F11` steps backwards on any breakpoint except a handler's
first line — but note "the data variables do not change to their old values". Stepping
back inside `<foreach>`/`<receiveall>` jumps out to the start of the loop, not to the
previous iteration. Debugging slows execution measurably; do not benchmark in a debugger.

## I. Sandboxes — isolate one mechanism (§6.10)

| Sandbox | Diagnoses |
|---|---|
| CDL | Any CDL statement; *Allow interaction* controls whether it touches live ports |
| Extract | `<extractdata>` — delimited/flat text → XML (the CSV parsers in ORDERMATCH, NBIN) |
| Regex | `<regexreplace>` — date reformatting, filename extraction |
| Schema | `<schemacheck>` — XML vs XSD (SCCORE import structure) |
| Swift | `<convert>` — SWIFT text ⇄ SWIFT XML, with per-tag help |
| Webservice | Browsing a WSDL to build a `<WebRequest>` port (SCDRCONNECT/ODA) |
| Xmldiff | `<ifxmlequal>` — compare two XML payloads |
| XPath | The XPath in `<if>`, `<ifelse>`, `<select>`, `<foreach>`, `<getvalue>` |
| Xslt | `<transform>` — apply a stylesheet to a payload |

From a breakpoint, "Jump to…" pushes the live values straight into the matching sandbox.
This is the fastest way to answer "is the XSLT wrong or is the input wrong".

## J. Testbench — regression-proof a change (§6.11)

Test cases attach to handlers, run **offline**: "the handler is run with the specified
input, but all port connections are disabled and dummy results are returned" (mock
objects). Test cases are XML files stored in the Protected File Directories and declared
in a config file as `<Testcase File="…" Port="…" Label="…" />`. Assert types: XPath,
Contains, ContainsNot, RegexMatch, Schema, Equals, XMLEqual. Coverage colouring: green =
executed, red = not executed.

Caution: **the testbench executes file operations**. A test case containing `<writefile>`
really writes the file — put such statements in *Skipped statements* on the Details tab.

Scheduled regression: batch task **Communication Service Testbench - Execute**, pointed at
either a parameter set or a Communication Service setup, with a Result file (reference
file, XML output). The batch job **fails** if any test case fails, or if the whole
scenario takes more than **20 minutes**.
