# Nicola Wealth: the FO_PREP_HOLDING group and the open questions

Source: Configuration Export by LGARNIER on 22-May-2026, TEST, version 25.10
SP0, in `i. Client - Nicola Wealth/General & Architecture/Louis/Prep FO
Holdings/`. Group created by DDOKTER on 14-May-2026. Also NWM_SAAM_TAA
Walkthrough (How to Run Prepare) and the NWM250_A Sum to 1B resolution note.

## The group as exported

| Sort | Batch job | Batch task | Parameters in the export | Frequency | Active |
|---|---|---|---|---|---|
| 1 | FO_FND_DELETE_ALL | 520 Front Office Model Delete All Data | none | Every day | No |
| 2 | FO_FND_UPD_ALL_MP_COMP, name Update all MP components | 519 Front Office Model Update 'MP Components' Data | PARM1 = 1 (Yes), PARM2 = 0 (No), PARM3 model portfolio empty | Every day | Yes |
| 3 | FO_FND_UPD_CL_SPE_DATA, name Update all Client Specific data | 518 Front Office Model Update 'Client specific' Data | PARM1 = 0 (No), PARM2 = 0 (No), PARM3 portfolio empty, PARM4 segment empty | Every day | Yes |

Reference file SO_BATCH (Service Operation, Generic Batch Log). No stop on
error, no email on failure, no calendar.

## What the export does not tell you

The .cei carries parameter values but not their window labels. PARM1 on the
MP components job could be Update changes and errors (Front Office
Configuration 3.12.3 step 7) or something else; the manual does not print the
batch task parameter list. Read the labels from the Batch Jobs window with the
job open and record them here before interpreting the values.

## What the walkthrough says the manual run is

Batch Jobs, Prepare Front Office Holdings. Open the modelling setup
"Investment Structures - Model portfolio components", type Update All 'MP
components' Data. Then open the client specific setup, select the mandate or
all portfolios. Confirm the calculation and run the job locally. Check the
job log and verify synthetic holdings in Asset Manager. Prerequisites listed
in the same walkthrough: the pricing profile tied to the model portfolios has
prices for every component security, and FX rates are loaded for the day.

## Known related history

The NWM250 USD class not summing to 1B was resolved by the FX Rate Profile
CLOSE with Max age 0 and a same day USD/CAD rate, then a re run of Prepare
(reference_fx_rate_profile_fix). Missing prices or FX on the profile named on
the Modelling tab are therefore a proven failure mode at this client.

## Open questions to close before naming a cause (8-Sep-2026)

1. Which environment ran for hours, and which installation was the source of
   its refresh (PROD or GOLD) and when.
2. Which job in the group was open for hours: 519 MP components or 518 Client
   specific. Batch log start and end lines.
3. Service Manager state in that environment: automation model, Front office
   data service, count of Front office modelling calculation services, PKR.
4. Front Office Options Modelling tab in that environment: the pricing and FX
   profiles now set, and the Automatically recalculate erroneous interval.
5. Status Log colours and the first Error Log messages after the run.
6. Whether the client specific job is meant to cover every portfolio, or a
   segment of the mandates that use SAAM and TAA.
7. Whether database statistics were gathered after the restore.
