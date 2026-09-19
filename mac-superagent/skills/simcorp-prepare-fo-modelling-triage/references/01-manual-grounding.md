# Manual grounding, verbatim by section

Source editions: Front Office Configuration September 2025 (foconfig.pdf),
Front Office Operations September 2025 (foops.pdf), Service Configuration
March 2026 (srvicconf.pdf), Copying SimCorp Dimension September 2025
(copyscd.pdf), Service Administration March 2026 (srvicad.pdf). All live in
`ii. Manuals & Documentation/PDFs`. Dash punctuation inside quotes is
normalised to colons per house style; wording is otherwise verbatim.

## Front Office Configuration 3.12 Configuring modelling data for Asset Manager

"The Front office modelling calculation and Front office data services ensure
that model portfolio weights are calculated when necessary for use in Asset
Manager. The Front Office modelling calculation service type performs the
following actions: Updates the status of model and client-specific portfolios.
Automatically recalculates the weights of the model portfolio components
online when changes occur. The Front office data service service type queues
and then recalculates portfolios. In addition, there are a set of batch jobs
which handle preparation of modelling data for Asset Manager. These jobs offer
the same functionality, but a different approach."

## Front Office Configuration 3.12.1 Configure modelling settings

"The pricing and FX rate profiles that you specify on the Modelling tab of the
Front Office Options window are used to calculate weights across the Front
Office. Therefore, they are also used to calculate the model portfolio data
that is specified in the Strategic Asset Allocation and Mandates (SAAM) and
Tactical Asset Allocation (TAA) windows."

Step 5: "To use pricing and FX rate profiles from your model portfolios, that
is for specific clients, select the Use profiles from model portfolios check
box. The Pricing profiles and FX rate profiles fields are then closed for
input. If you select this check box, make sure you use the same pricing and FX
rate profile for each model portfolio defined in a Tactical Asset Allocation
setup. Otherwise, the model weights calculation can fail."

Step 7: "To recalculate the client-specific data whenever there is a change to
the model portfolio or to the model portfolio components that are attached to
the Tactical Asset Allocation, select the Automatically recalculate client
specific weights check box. Changes to model portfolio components trigger a
recalculation of the weights of that model's components (the model is set for
recalculation and is then recalculated). After that, all the portfolios that
have this model in their Tactical Asset Allocation are recalculated."

Step 8 and note: "To recalculate all erroneous model portfolio components and
client-specific data within the time that you specify in the Time interval in
minutes between attempts to recalculate erroneous field, select the
Automatically recalculate erroneous check box. Note: SimCorp recommends that
you set the time interval to at least 60 minutes. If you do not, the service
can be kept permanently busy trying to recalculate erroneous models. This is
useful if errors appear because of missing prices and new prices are then
imported."

## Front Office Configuration 3.12.2 Set up the Front Office modelling calculation service

"The Front Office modelling service is a specific service job type of the
Calculation service which you must set up to run on the Service Platform. The
Front Office modelling calculation service is specified in the Calculation
service configuration window, within the Service Manager applet. Note: In the
Calculation service configuration window, you can run multiple Front office
modelling calculation services simultaneously. This optimises performance when
there are large amounts of model portfolio and client-specific data for
calculation."

## Front Office Configuration 3.12.3 Configure preparation of modelling data

"1. Open the Prepare Front Office Modelling window. 2. In the Show ribbon menu,
select the Actions applet. 3. Press Ctrl + N to enable the fields. 4. Enter an
ID and a Name. 5. In the Type field, select Update 'MP components' Data from
the drop-down list. 6. Select a model portfolio, client portfolio, or portfolio
segment. 7. Select the Update changes and errors check box if only those model
portfolios/portfolios which were previously calculated and which are now
changed/updated are to be recalculated when you click Execute. 8. Save your
changes, and click Execute."

3.12.3.1: "To view the status, open the Status Log applet. Red: An attempt was
made to recalculate the model, but errors occurred. Yellow: The model requires
recalculation. Green: The model was calculated successfully."

3.12.3.2: "To view the errors, open the Error Log applet. No error message: If
you made changes to the model portfolio components and prices were found, no
messages are shown in the error log. If no prices/FX rates are found for
changed or new components, errors that state this are displayed. Model
portfolio has been changed. Tactical Asset Allocation has been changed. No
Tactical Asset Allocation exists before or at dd-mm-yyyy. Portfolio has been
changed."

## Front Office Operations 3.6 Run the Front Office Prepare model portfolio data batch jobs

"The batch jobs basically work in the same way as the Prepare Front Office
Modelling window. However, the status and error logs make it easier for you to
get an overview of what was calculated. The four batch jobs are: Front Office
Model Update 'MP Components' Data: Calculates/updates the model portfolio
component weights in the Front Office Holdings table. Queues portfolios for
recalculation. Front Office Model Execute: This job does the same as the
Prepare Front Office Modelling window. It takes the parameter Prepare Front
Office Modelling ID. Front Office Model Update 'Client specific' Data:
Calculates individual model portfolio weights according to TAA/SAAM for the
included portfolios. Front Office Model Delete All Data: Deletes the model
portfolio data from the Front Office Holdings table."

## Front Office Operations 3.5 Run the Front Office Data Update batch job

"The batch job does not perform the actual update. Instead, it marks all
portfolios for update by the service. The Front office data services then
start to update Front Office Holdings, one portfolio at a time." Events that
require a full update include "You change any global option on the Front
office holdings tab of the Front Office Options window." Authorisations: "The
batch user (and service user) that you use to run the job (and service) must
be authorised to all the portfolios that you specify in the Front office
holdings portfolio segment."

## Front Office Operations 5.4.1 and 6.1 Diagnostics

5.4.1: "A set of performance counters are available specifically for the Front
office data service which you can generate by using the Service Manager
applet. You can use these counters to gauge: How much work is queued on the
Front office data service. How often the Front Office holdings data is
updated. How other services and data consumers are impacted by the updates."

6.1: "The trace log records details about: Found positions. Skipped (waited)
positions. Processed positions." Configured in Support Tool Options, Front
Office tab, Trace file directory, Advanced logging of service messages.

## Front Office Operations 6.4 Slow actions and pricing

6.4.2: "If the Execution type of the security in question is No execution, the
security is not included in the monitored securities segment of the Pricing
and Key Ratios Services setup. Modify the segment and restart the service."

6.4.3: "Update the database statistics if compliance validations and other
actions are running slowly to see if it resolves the issue: If you recently
upgraded your SimCorp Dimension installation. If you recently implemented
Front Office solutions. If neither of these cases apply but you are
experiencing the problem."

6.4.5: "There is a risk that this can generate a high number of zero holdings
which can negatively impact the performance of the Front Office solutions."

## Service Configuration, installation guidelines, service 215

Calculation service, job type Front office modelling calculation: Minimum 1
service, 1 CPU, 500 MB workspace, 4 GB RAM. Standard 2 services. Large 3
services with 1000 MB workspace. Service catalogue entry 57 Front office
modelling calculation: "Updates the status of model and client-specific
portfolios and automatically recalculates the weights of the model portfolio
components online when changes occur."

## Copying SimCorp Dimension chapter 4

4.1.9 and 4.2.15: "The automation model is automatically unloaded as part of
the RESET_AFTER_COPY job. Optionally, you can set the automation model to one
that matches the test environment: scdsvcctl.exe maint on, scdsvcctl.exe aut
load <model_name>."

4.2.18: "The first time you restore a SimCorp Dimension installation to a
target destination, you must run through the system options and change all
the parameters required to prevent the installation from corrupting the source
installation."

4.2.20: "Optionally, you can close all blacklists because they might not apply
in your test environment: scdsvcctl.exe blacklist closeall."

## Not documented anywhere in the 119 PDF corpus (swept 8-Sep-2026)

No manual states an expected duration for the Prepare jobs. No release note
(2510, 2601, 2604) mentions the Prepare Front Office Modelling window. The
parameter labels of batch tasks 518, 519 and 520 are not printed in any
manual; read them from the Batch Jobs window.
