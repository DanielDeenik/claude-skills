# The Order Manager service family on the Service Platform

Sources: Service Configuration user manual March 2026 chapter 2. Front Office
Configuration user manual September 2025, sections 16.10, 17.19, 17.20, 17.20.1
and chapter 21. Copying SimCorp Dimension user manual September 2025, section 3.2.

The new Order Manager architecture is the one part of the platform where SimCorp
departs from its own general advice, so treat it as a special case.

## The services

| ID | Service | Configuration | Instance restriction |
|---|---|---|---|
| 64 | Order Manager - Order service | See catalogue | See catalogue |
| 67 | Order Manager - Management service | None | Single |
| 70 | Order Manager - Elvin service | None | Single |
| 205 | Order cache service | Mandatory | Multiple |
| 217 | Order Manager message service | See catalogue | See catalogue |
| 307 | Order Manager - Cache | None | Single |
| 328 | Order Manager - Workflow service | See catalogue | See catalogue |
| 329 | Order Manager - Data Store service | None | Multiple |
| 340 | Order Manager - Position Status service | See catalogue | See catalogue |
| 342 | Order Manager - Message Broker service | None | Multiple |
| 343 | Order Manager - Transformation service | See catalogue | See catalogue |
| 348 | Order Manager - Data Extract Service | None | Single |
| 349 | Order Manager - API Service | Mandatory | Multiple |
| 353 | Order Manager - Automation Service | None | Single |
| 376 | Order Manager - External Integration service | Mandatory | Multiple |
| 385 | Order Manager - FIX Router | None | Multiple |
| 397 | Order Manager - FIX API Service | Mandatory | Multiple |

Read the catalogue for the columns marked "see catalogue" rather than assuming.
Service Configuration chapter 2, pages 31 to 34.

## What each one does, in dependency terms

The Message Broker service handles message exchange between the Workflow,
Transformation, Position Status, Order, Management, Trade Status, FIX Router,
FIX API, FIX.NET and External Integration services. The Data Store service is the
storage engine for the Workflow service, using event sourcing over a cluster of
nodes. The Data Extract service depends on the Data Store service. The FIX Router
communicates with the other services through the Message Broker service. The new
architecture also uses the Compliance order manager integration service, which
provides communication with the Compliance pre-trade service so Order Manager can
monitor the pre-trade service state. Front Office Configuration chapter 21,
pages 259 to 261, and section 17.19, page 240.

## Service tag mapping is recommended here

The general recommendation is capability checks. The single documented exception
is the new Order Manager architecture, where service tag mapping is recommended.
Service Administration sections 2.5 and 7.2, pages 15 and 81.

## The three integration services and their start rules

The API service streams trading data such as orders and comments. The External
Integration service streams non trading data such as users, dealing desks,
aggregation rules, brokers and counterparties. The FIX API service streams FIX
session definitions and FIX session states.

To enable streaming, in System Manager click Start, then on the Parameters tab
select the service type, then select the configuration created in the Order
Manager API Service Configuration window, then click Start.

Four documented start rules, all from Front Office Configuration section 17.20.1,
pages 243 and 244:

1. **Before starting the Order Manager - External Integration service, ensure the
   Order Manager - Management service is running.**
2. **Only one instance of an integration service with the same configuration can
   run at a time.** This is narrower than the catalogue's Instance restriction
   Multiple. Multiple instances are possible only across different
   configurations.
3. **If you start the API service and the trading data subscription is not
   included in the configuration, or you start the External Integration service
   and the non trading data subscription is not included in the configuration,
   the service fails to start.**
4. **Ports 5671, 5672, 443 and 4222 must be open on the agent where the service
   runs.**

For the FIX API service specifically, it must have been added to the service
model before streaming can be enabled.

The streaming API uses Azure Service Bus for asynchronous messaging and supports
protobuf and JSON binary payloads. Setting it up means choosing the Azure Service
Bus authentication method and messaging entity mode, configuring Azure Service
Bus messaging in an integrated environment, then enabling streaming for Order
Manager. The first three steps are documented in the System Administrator's
Manual, which is not held locally. Section 17.20, page 243.

## Certificates

| Service | Where the certificate is configured |
|---|---|
| Order Manager - Elvin service | Order Manager Configuration window, Advanced Parameters tab, Elvin certificate thumbprint field |
| Order Manager - Message Broker service | Order Manager Configuration window, Parameters tab, Certificate name field |
| Order Manager - Workflow service | Workflow Server Parameters tab, Client to server certificate name field |
| Order Manager - Data Store service | Workflow Server Parameters tab, Server to server certificate name field |
| Order Manager - API service and Order Manager - External Integration service | OM API Service Configuration window |

**If a service cannot find a correctly configured security certificate, it fails
to start, and an error message is logged in the service log which is readable
from System Manager.** A certificate can be given as a thumbprint, a subject
distinguished name or a certificate specification string. SimCorp Dimension looks
in both the user certificate store and the machine store, and where several match
it takes the most recently issued with the longest expiration.

Certificates are mandatory for the Workflow service and the Data Store service,
and for the API, External Integration and FIX API services in single tenant and
multi tenant app registrations where a client secret is not used. They are
optional but strongly recommended for the Elvin and Message Broker services, and
running those two without certificates means their communication is neither
encrypted nor authenticated.

SimCorp Dimension does not create or maintain certificates. They must be signed
by a CA trusted by both the machine hosting the agents and the end user machine
running SimCorp Dimension, the purpose must be digital signature or key
encipherment, and the Extended Key Usage must include the required values.
Section 17.19, pages 240 to 242.

## Copying an environment breaks Order Manager in specific ways

When a target installation has been copied or refreshed from another environment,
check all four of these before blaming the model. Copying SimCorp Dimension
section 3.2, pages 11 and 12.

1. **Certificates are not copied.** They live in the Windows certificate
   repository, not in the SimCorp Dimension installation. The certificate name
   configuration in Workflow Server Parameters is copied, so the names arrive
   pointing at certificates that may not exist. "If certificates with the correct
   names are not set up in the Windows Certificate repository, and you try to
   start the target installation, the relevant services generate an error log for
   the missing certificate, and will fail to start."
2. **The Data Store service password and encryption key are copied**, stored in
   the SimCorp Dimension password vault at the same database location as the
   FIX.NET SQL server database password. After copying, the Data Store service
   password must be changed in the target installation, which can only be done
   from a machine with access to the Data Store service HTTP port, by default
   2113. The encryption key must not be changed, because a mismatch makes
   existing data inaccessible.
3. **Hostnames, directory paths and communication ports live in cnf.ini** and
   must be updated to point at the target installation.
4. **Source folder structures copied by accident break the Data Store service.**
   The error is "The data store configuration appears to be out of date for this
   installation", logged in the Data Store service log. Fix it by ensuring
   `OM_DATASTOREHOSTNAMES` and `OM_DATASTOREPATHS` in cnf.ini reflect the target,
   and that the hostname and directory path parameters in the Order Manager
   Configuration window are correct.

Also relevant when copying: the Data Store files must always be copied, the Data
Store and Workflow services must be shut down before copying the source files,
and each source node's data files go to the corresponding destination node's
storage location. The External notification uri configuration parameter for the
API sits in cnf.ini and may need copying too.

## Where the deeper troubleshooting lives

Front Office Operations user manual, section 6.5, carries named Order Manager
failures including Management service does not start with a missing directory,
Management service does not start with a Counterparty Manager error, FIX session
does not start on request, FIX.NET Server does not start, and Operations Console
fails to start. Open that manual when the failing service is one of those.
