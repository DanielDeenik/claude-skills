# The Order Manager Data Store cluster

Sources: Front Office Configuration September 2025 section 16.4 with 16.4.1,
16.4.2, 16.4.5 to 16.4.7 and 16.4.10, pages 161 to 168. Service Configuration
March 2026 chapter 2 and chapter 4. Copying SimCorp Dimension September 2025
section 3.2. Log signatures marked observation come from the Nicola export of
7 September 2026.

## The rules, verbatim where it matters

- The Data Store "remains available for data (event) write operations when at
  least half the nodes are available and connected." (16.4, page 161)
- "You can run the Order Manager - Data Store services on a single node in UAT
  and development modes. For production mode, however, a minimum of three nodes
  is required to form an event stream-clustered environment. The new
  architecture continues to operate even if one node is stopped." (16.4)
- "If two nodes are stopped, then the Order Manager - Workflow service can still
  read data available on the one remaining node. However, no new data (any
  action or event that results in the update of existing data or creation of
  new data such as the arrival of new orders in the new Order Manager
  architecture) is written in the Data Store cluster." (16.4)
- No maximum node count, provided the number is odd. Production: as many as
  possible, still odd. (16.4)
- Sizing table, service 329: three instances in every installation size, with
  the footnote "For installations not in production, only a single service is
  required." (Service Configuration chapter 4, page 54 and 57)
- Instance restriction Multiple, configuration None, category Business.
  Catalogue text: "in a production environment, a minimum of three instances
  must be running. In test installations, only one service is required."
  (Service Configuration chapter 2)
- Recommended model start order: Data Store, then Workflow, then Order service.
  Messages sent while Workflow is still starting can be lost. (16.4 note)
- Network encryption with certificates is not supported for the Data Store in
  cluster mode of three or more nodes. Certificates remain mandatory between
  client, Order service and Workflow service. (16.4.5, page 164)

## Operating the cluster from the Service Platform (16.4.6, page 165)

1. Workflow Server Parameters tab of the Order Manager Configuration window:
   one machine name per row in Hostname, one directory path per node in
   Directory path. These land in cnf.ini as omwsdatastorehostnames and
   omwsdatastoredirectorypaths.
2. Each node runs on its own dedicated machine, with its own service agent.
3. Dedicate the node controllers with a service tag (Service Tag Mapping in the
   Service Administration manual).
4. Set the agents to `-maxrunningservices=1` so each agent starts one service.

Consequence for the automation model: service 329 needs a Count equal to the
number of hostnames, one instance per tagged machine, in a group that starts
before Workflow. A Count of one on a three hostname configuration is a
production cluster with two nodes stopped by design.

## Storage, ports, password

- The service fails to start if the configured directory does not contain valid
  EventStore files. On first setup, create the directory with a marker file
  carrying the `.start` extension. (16.4.1, page 162)
- TCP and HTTP ports are entered once and apply to every hostname. Open the TCP
  port and the TCP port minus one on the firewall, for example 1113 and 1112.
  (16.4.2, page 162)
- Password default is `changeit`; change it only after all other parameters are
  applied and the service restarted; the encryption key can never be changed.
  Deleting the database requires a successful restart and then a password
  change. (16.4.4, pages 163 and 164)
- Registry error "Access to the registry key 'Global' is denied" is a user
  permission problem on the agent account. (16.4.10, page 168)
- After copying an environment: certificates are not copied, the Data Store
  password and encryption key are copied and the password must be changed,
  hostnames and paths in cnf.ini must point at the target, and a copied source
  folder structure gives "The data store configuration appears to be out of
  date for this installation" in the Data Store log. (Copying SimCorp
  Dimension 3.2, pages 11 and 12)

## Log signatures (observation, Data Store 329-1, 7 September 2026)

The service log is an EventStore node log wrapped by the Service Platform.
Lines seen, in order, with what they establish:

| Line pattern | What it establishes |
|---|---|
| `Starting 'FirstGeneration' service 'Order Manager - Data Store service' as '329-1' requested using 'Dependency Strategy' by 'DOMAIN\ACCOUNT' from 'host'` | Who started it: the automation model, from the named agent host |
| `Starting EventStore at 10.x.x.x i.e. hostname` | Which node this instance is |
| `Other host: hostname` (one line per other node) | The configured cluster membership. Count these lines plus one: that is the node count the model must satisfy |
| `Service Starting on Tcp : 1113 Http : 2113` | Ports in use; compare with the Workflow Server Parameters tab |
| `WRITER CHECKPOINT`, `CHASER CHECKPOINT`, `EPOCH CHECKPOINT`, `TRUNCATE CHECKPOINT: -1` | Database position on this node. Equal writer and chaser means nothing pending on this node |
| `The exception(s) occured when scanning for message types: Could not load file or assembly ...` at Information level | Assembly load exceptions during message type scan. Seen with the service still reporting started. Cause status: NOT VERIFIED, do not name it as a fault or as harmless without SimCorp confirmation |
| `Service Started`, `Service is successfully started` | The Service Platform considers the process up. This is the green cell in the pivot. It says nothing about quorum |
| `SYSTEM INIT`, `SYSTEM START`, `IS UNKNOWN`, `New State Unknown` | Node has no cluster role yet. Whether a later line announces a leader role on a healthy cluster is NOT MEASURED locally; capture a healthy node log before using its absence as evidence |
| `Looks like node [10.x.x.x:3113] is DEAD (Gossip send failed)` | The named node is unreachable on the gossip port. One such line per missing node |
| `External TCP connection accepted ... Client connection name: 'ES-...'` | A client connected on the TCP port. The client IP tells you which machine, typically the Workflow host |
| `ES TcpConnection closed ... Close reason: [ConnectionReset] Socket receive error` | That client connection was dropped. Repeated at a fixed interval it is a client reconnecting to a node that cannot serve it |

Reading rule: two DEAD lines on a three host membership plus a state that stays
Unknown plus periodic ConnectionReset on the client is the log shape of
"fewer than half the nodes available". The manual sentence in 16.4 is the
finding; the log lines are the evidence; the other two node logs and the model
Count for 329 are the confirmation still required.

## What a healthy cluster must show before you call it fixed

- One "Starting EventStore" line per node, each on its own machine.
- No DEAD lines after the first minute.
- Workflow service log without connection resets.
- A newly released order visible in Order Manager and its Order Outbox row
  without the "not received" warning.
