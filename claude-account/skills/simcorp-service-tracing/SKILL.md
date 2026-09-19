---
name: simcorp-service-tracing
description: "Guide and verify the SCD Service Manager tracing workflow: stop AMMSG calc services, restart with APL, DB and application tracing at startup, then stop tracing and fetch the files."
---

# SimCorp service tracing via the Service Manager

Source procedure: SimCorp (Sauli Niemi, 31 Aug 2026 Teams thread) plus Dan's recorded run on 31 Aug 2026. SimCorp Dimension runs inside a Citrix HTML5 canvas, so Claude cannot drive it; the operator performs the steps, Claude supplies the sequence and checks the evidence that comes back.

The four key points: stop all services, start with the relevant tracing, stop tracing, fetch the files. Tracing set at service startup dies with the service. A service restart without re enabling tracing silently produces nothing (this is exactly what happened on 31 Aug: services restarted at 11 CET, no tracing re enabled, nothing saved). After any restart, re enable before testing.

## Part A. The operator sequence

1. **Open the Service Manager.** System Manager, Service Manager tab, Services Pivot view, model NICOLAPFW. The pivot shows service type rows against agent host columns; the Service details pane below lists Configuration, Agent, Instance and State per service.
2. **Stop the AMMSG calculation services.** Select the Calculation service row, use Stop Filtered or Stop Selected, filter the stop grid by Configuration = AMMSG, and stop all listed instances. Read the panel "Services that cannot be stopped" and record any instance named there; those keep running and must be reported with the day's evidence.
3. **Start a replacement service with tracing on, per service.** Start service dialog, Tracing tab, all three sections in one pass (activation does not need two steps, it can all be set at startup):
   - **Database tracing.** Trace file id: unique per service, and at most 30 characters or the dialog refuses to save. Use the day's convention, for example PERF_TEST_3108 or CALC1 style suffixes when tracing several services. Trace level: SQL (level 1).
   - **Function tracing.** Function to trace: the prefix list for the investigation, for example ord*;fund*;. Threshold in percent and Threshold in seconds: as agreed for the day (the 31 Aug run used 1 and 1.0; the dialog defaults are 5 and 5.0).
   - **Application tracing.** Define Configuration, load or paste the trace XML (the project copy is ApplicationTraceForOrders.xml, which lists the FrontOfficeData and MWB OutBox assemblies). The Filename inside the XML and the Log filename field must be a path the SERVICE HOST can reach, not a client path: use the TEST ActiveData share, \\TEST-activedata.private-nicola.simcorpcloud.com\TEST-ActiveData\ActiveData\Tmp\<name>.log. A wrong path shows "Ensure that the entered path is available from the process hosting the service" or a native path error in the service log.
   Then Start, and wait for the new instance to come Online in the Service details pane.
4. **Verify activation before testing.** Open the new instance's service log and confirm the entry "Trace file successfully activated for the APL session ... Trace file is successfully activated for the CSharp session", plus "Function trace enabled for N function(s)". No entry means no trace; fix before running anything. Record which instance numbers are the traced ones (for example 215-6 Online traced, 215-4 and 215-5 Closed) so the test's work can be tied to the right instance.
5. **Run the day's tests.**
6. **Stop tracing.** Select the traced service, ribbon, SUPPORT TOOLS group, Tracing dropdown: Application Tracing, Database Tracing and Function Tracing each in turn, choose Disable tracing, OK. The trace file id shown when stopping DB tracing can be ignored; it stops the trace started under the other name.
7. **Verify deactivation and note the file paths.** The service log shows the deactivation entries and the function trace log's full path.
8. **Fetch the files.** DB traces: Database Trace Files window, Refresh then Get, note where they are saved. Function and application traces: the ActiveData Tmp share above.

## Part B. What Claude does with the evidence

When screenshots, logs or trace files come back: confirm activation entries exist for every traced service and flag any service listed as not stoppable or still Closed; check the trace file ids match the day's naming so files can be attributed; check the service log timestamps bracket the test window, and flag any service restart inside the window as a tracing loss; list which expected files (DB, function, application, per service) are present and name the missing ones as not captured, never assumed. Log the day per the pre test capture skill and the test plan workbook conventions.

## Grounding rules

Never invent a service name, instance number, trace id or path; use what the operator's evidence shows. Numbers enter reports only with a log line or screenshot behind them. The environment is TEST (custid NICOLA); do not apply this to production without explicit instruction.