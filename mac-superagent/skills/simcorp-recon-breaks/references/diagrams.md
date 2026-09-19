# The diagram set

Nine diagrams, drawn in this order: architecture, then flow, then state, then decision, then
sequence. Every node is source tagged to a manual section or a verified client object. A step
that cannot be tagged does not become a node; it goes to the open questions list.

Shared styling. Near monochrome with one accent. Use this class block in every diagram so the
set reads as one system.

```
classDef ext fill:#F2F4F7,stroke:#9AA4B2,color:#3A3A4A
classDef scd fill:#E4E9F2,stroke:#5B6B8C,color:#1E2761
classDef act fill:#FFFFFF,stroke:#1E2761,color:#1E2761
classDef ctl fill:#FBF3E2,stroke:#A66E08,color:#7A5206
```

Use `ext` for anything outside SimCorp, `scd` for SimCorp objects, `act` for a human decision,
`ctl` for a control that can block progress. Never colour by counterparty or by domain; the
skeleton stays identical across domains and the difference is written in a rule bar of text
above the diagram.

## D1. Solution architecture, six layers

```mermaid
flowchart TB
  subgraph L1[1 Source]
    A1[Holdings, cash management data,<br/>portfolio calculation, transactions]:::scd
    A2[Custodian, fund administrator<br/>and legacy files]:::ext
  end
  subgraph L2[2 Delivery]
    B1[Reconciliation folder<br/>per counterparty]:::ext
    B2[Archive batch job group]:::scd
    B3[Reference Files setup<br/>Opening mode Read only]:::scd
  end
  subgraph L3[3 Configuration]
    C1[General Reconciliation Fields]:::scd
    C2[General Reconciliation Rules<br/>field type drives deviation maths]:::scd
    C3[General Reconciliation Lines]:::scd
    C4[General Reconciliation setup<br/>tracking, classification, statistics]:::scd
  end
  subgraph L4[4 Execution]
    D1[Manual execute]:::scd
    D2[Batch job]:::scd
    D3[Portfolio event]:::scd
    D4[Fund event]:::scd
    D5[Portfolio calculation<br/>position lines only]:::scd
  end
  subgraph L5[5 Exception handling]
    E1[Reconciliations applet]:::scd
    E2[Results Monitor]:::scd
    E3[Deviation Details]:::scd
    E4[Alerts Inbox]:::scd
    E5[Classify, comment,<br/>match, deactivate]:::act
  end
  subgraph L6[6 Reporting and automation]
    F1[View General Reconciliations]:::scd
    F2[Dashboard widgets]:::scd
    F3[Reconciliation APIs v1 and v2]:::scd
  end
  A2 --> B1 --> B2 --> B3 --> L4
  A1 --> L4
  C1 --> C2 --> C3 --> C4 --> L4
  D5 --> D1
  L4 --> L5 --> L6
```

## D2. Daily custodial run, one counterparty

```mermaid
flowchart LR
  S1[File received<br/>naming convention checked]:::ext
  S2{File closed and<br/>in the right folder}:::ctl
  S3[Archive job moves file<br/>to Archive folder]:::scd
  S4{Reference file flagged<br/>as processed}:::ctl
  S5[Portfolio calculation<br/>position lines only]:::scd
  S6[Reconciliation batch job group<br/>imports and matches]:::scd
  S7[Run log: matched,<br/>deviation, no match]:::scd
  S8{Error List empty}:::ctl
  S9[Results Monitor<br/>population frozen]:::scd
  S1 --> S2
  S2 -- no --> X1[Classify FED-01<br/>fix delivery and re run]:::act
  S2 -- yes --> S3 --> S4
  S4 -- yes --> X2[Toggle the processed flag<br/>classify FED-02]:::act
  S4 -- no --> S5 --> S6 --> S7 --> S8
  S8 -- no --> X1
  S8 -- yes --> S9
```

## D3. Break status assignment, how the engine decides

```mermaid
flowchart TB
  R0[Record pair evaluated<br/>against the rule set]:::scd
  R1{Any rule violated}:::scd
  R2[Automatic match]:::scd
  R3{Can it pair at all}:::scd
  R4[No match]:::scd
  R5[Level 1 test<br/>strictest]:::scd
  R6[Level 2 test]:::scd
  R7[Level 3 and 4 tests]:::scd
  R8[Deviation]:::scd
  R9[Derived match<br/>same Break ID matched]:::scd
  R10[Manual match<br/>user overrules]:::act
  R0 --> R1
  R1 -- no --> R2
  R1 -- yes --> R3
  R3 -- no --> R4
  R3 -- yes --> R5
  R5 -- no match --> R6
  R6 -- no match --> R7
  R7 -- no match --> R8
  R4 --> R10
  R8 --> R10
  R2 --> R9
```

## D4. Execution lifecycle, which is not the record status

```mermaid
stateDiagram-v2
  [*] --> Open: execution created
  Open --> Closed: Close, needs authorisation
  Closed --> SignedOff: Sign off, needs authorisation
  Closed --> Open: Re open
  SignedOff --> Open: Re open
  Open --> [*]: Delete
  note right of Closed
    Results can no longer be
    recalculated or changed.
    Alerts set to Resolved.
  end note
  note right of Open
    Never sign off while
    Re execution started at
    is populated.
  end note
```

## D5. Straight through processing control

```mermaid
flowchart TB
  P1[General reconciliation<br/>portfolio or fund event]:::scd
  P2[Step 1 import internal data]:::scd
  P3{Import only<br/>internal data}:::ctl
  P4[Snapshot kept,<br/>event terminates]:::scd
  P5[Step 2 import external file]:::scd
  P6[Step 3 match]:::scd
  P7{All records at or above<br/>Approval status}:::ctl
  P8[Event created Approved]:::scd
  P9[Event created Generated]:::scd
  P10{Breaks prevent raise<br/>selected}:::ctl
  P11[User cannot raise to Approved<br/>until every break is addressed]:::act
  P1 --> P2 --> P3
  P3 -- yes --> P4
  P3 -- no --> P5 --> P6 --> P7
  P7 -- yes --> P8
  P7 -- no --> P9 --> P10
  P10 -- yes --> P11
```

## D6. The ten stage process

```mermaid
flowchart TB
  T1[1 Confirm the run is valid]:::act
  T2[2 Freeze and export]:::act
  T3[3 Triage by status, value, age]:::act
  T4[4 Classify every break]:::act
  T5[5 Investigate by code]:::act
  T6[6 Disposition and fix<br/>at the causing layer]:::act
  T7[7 Document four things]:::act
  T8[8 Re execute and re verify]:::act
  T9[9 Close, approve, sign off]:::act
  T10[10 Control recurring<br/>and ageing population]:::act
  T1 -- run invalid --> T1
  T1 --> T2 --> T3 --> T4 --> T5 --> T6 --> T7 --> T8
  T8 -- break did not move,<br/>classification was wrong --> T4
  T8 --> T9 --> T10
  T10 -- code seen in three<br/>consecutive runs --> T6
```

## D7. Sequence, custodial cash break with a missing transaction

```mermaid
sequenceDiagram
  participant C as Counterparty file
  participant R as Reconciliation Manager
  participant A as Reviewer
  participant D as Dealer or Cash Management
  C->>R: closing balance for the account
  R->>A: Deviation on the cash line
  A->>R: Cash Integrity on the internal record
  R-->>A: net balance, netted payments, residual difference
  A->>R: Show Holdings then View Holdings
  R-->>A: last booked movement predates the file
  A->>C: compare the counterparty activity file
  C-->>A: the movement the internal book is missing
  A->>A: classify QTY-01, disposition D3
  A->>D: book the transaction
  A->>R: comment, then request re execution
  R-->>A: refreshed result, line matches
```

## D8. Sequence, alternatives market value break

```mermaid
sequenceDiagram
  participant R as Reconciliation Manager
  participant M as Alternative Investments Manager
  participant S as Statement
  participant A as Reviewer
  R->>A: Deviation or Match level 2 on the holding
  A->>M: open the investment, default layout
  A->>M: position, then Business Transactions, All Active
  M-->>A: active transactions after the valuation date
  A->>M: valuation history
  M-->>A: latest valuation and its date
  A->>S: compare valuation and each component
  S-->>A: capital call or distribution breakdown
  A->>A: classify PRC-04 or MET-01
  A->>R: comment with cause, remediation, outcome
  A->>R: copy comments out, then request refresh
```

## D9. Sequence, migration opening balance break

```mermaid
sequenceDiagram
  participant X as Counterparty position file
  participant R as Reconciliation Manager
  participant A as Reviewer
  participant T as Test environment
  participant L as Delta file
  X->>R: position the internal book does not carry
  R->>A: No match, Break ID and age
  A->>A: read the notice and the opening balance
  A->>A: classify MIG-01, MIG-02 or MIG-03
  A->>T: replicate the fix
  T-->>A: fix confirmed
  A->>L: add the record or the correction
  L->>R: next load
  A->>R: re execute and confirm the break cleared
```
