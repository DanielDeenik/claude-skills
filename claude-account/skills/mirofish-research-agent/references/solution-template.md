# Solution Document Template

Use this template for every MiroFish research agent mission. Copy and fill in all sections.
Sections marked [REQUIRED] must be completed before any code is written.

---

```markdown
# MiroFish Mission: [Mission Name]

**Created:** [date]
**Asset Class:** [equity / private / crypto / cross-asset]
**Status:** [DRAFT → APPROVED → IN-PROGRESS → COMPLETE]

---

## 1. Problem Statement [REQUIRED]

### What information asymmetry are we targeting?
[One paragraph: what does the market believe, and why is that wrong?]

### Who benefits from this asymmetry?
[Who holds the mispriced position? Retail? Institutional? Both?]

### What's the time horizon?
[When does the arbitrage window likely close?]

---

## 2. Brain Topology Mapping [REQUIRED]

| Layer | Component | Data Source | Refresh Cadence | Output Format |
|-------|-----------|-------------|-----------------|---------------|
| L0 Perception | [collectors] | [APIs/sources] | [interval] | Signal JSON |
| L1 Memory | [knowledge store queries] | [DB tables] | [on-signal] | Entity links |
| L2 World Model | [assembly logic] | [signal + memory] | [on-batch] | Mosaic JSON |
| L3 Planning | [scoring formula] | [mosaic + config] | [on-assembly] | Thesis JSON |
| L4-L5 Action | [HITL controls] | [thesis + human] | [on-gate] | Decision JSON |

### Feedback Loop
[How does the Action layer feed back into Perception? What prediction errors
get generated? How does the World Model update?]

---

## 3. Signal Architecture [REQUIRED]

### Input Signals
| Signal | Source | Category | Confidence Method | Config Key |
|--------|--------|----------|-------------------|------------|
| [name] | [API/scrape] | [fund/struct/behav/sent] | [how scored] | [config.key] |

### Assembly Rules
[How do fragments combine into a mosaic? What's the minimum? What triggers conflict?]

### Scoring Formula
```
Signal Strength = [formula]
```
[Explain each variable and where its value comes from (config/computed/user-input)]

---

## 4. HITL Gates [REQUIRED]

| Gate # | Phase | Trigger Condition | Human Options | Timeout Behavior | Config Key |
|--------|-------|-------------------|---------------|------------------|------------|
| 1 | Solution Review | Doc created | Approve/Edit | Block | — |
| 2 | Test Review | Tests written | Approve/Add | Block | — |
| 3 | UI Review | Agent running | Approve/Adjust | Auto-defer 24h | hitl_timeout |
| 4 | Final Verify | Checks pass | Ship/Revise | Block | — |

### Decision Capture
[Every HITL decision is stored with: verdict, reasoning text, timestamp, conviction score]

---

## 5. UI Specification [REQUIRED]

### Layout (ASCII wireframe)
```
+------------------------------------------+
| MISSION HEADER                           |
| [Asset] [Class Badge] [Hypothesis]  [TS] |
+-------------------+----------------------+
| SIGNAL GRID       | THESIS PANEL         |
| ┌─Fund──┐ ┌─Str─┐ | Consensus: ...       |
| │       │ │     │ | Misframing: ...      |
| └───────┘ └─────┘ | Reality: ...         |
| ┌─Behav─┐ ┌─Sent┐ | Score: [bar]         |
| │       │ │     │ | Conviction: [meter]  |
| └───────┘ └─────┘ |                      |
+-------------------+----------------------+
| CATALYST CHAIN    | RISK MATRIX          |
| 1. [event]→[date] | [risk]→[probability] |
+-------------------+----------------------+
| HITL: [APPROVE] [DEFER] [REJECT]  [text] |
+------------------------------------------+
```

### Component Tree
```
MissionAgent
├── MissionHeader (asset, class, hypothesis, timestamp)
├── SignalGrid
│   ├── SignalCategory (fundamental)
│   ├── SignalCategory (structural)
│   ├── SignalCategory (behavioral)
│   └── SignalCategory (sentiment)
├── ThesisPanel
│   ├── ConsensusBlock
│   ├── MisframingBlock
│   ├── RealityBlock
│   ├── ArbitrageScore
│   └── ConvictionMeter
├── CatalystChain
├── RiskMatrix
└── HITLControls
    ├── VerdictButtons
    └── ReasoningInput
```

### Data Flow
[What API endpoints does this hit? What state does it manage? What refreshes?]

### Design Tokens
[Reference: bloomberg-ui.md — specify any mission-specific overrides]

---

## 6. Test Plan [REQUIRED]

### Backend (pytest)
| Test File | What It Covers | Key Assertions |
|-----------|---------------|----------------|
| test_{name}_config.py | No hardcoded values | AST scan, config key coverage |
| test_{name}_signals.py | Signal collection | Required fields, staleness, rate limit |
| test_{name}_assembly.py | Mosaic assembly | Min fragments, diversity, conflicts |
| test_{name}_scoring.py | Arbitrage formula | Formula correctness, threshold mapping |
| test_{name}_hitl.py | HITL gates | Trigger conditions, reasoning capture |

### Frontend (vitest)
| Test File | What It Covers | Key Assertions |
|-----------|---------------|----------------|
| {Name}.test.jsx | Rendering | All states, categories, HITL controls |
| {Name}.api.test.js | API calls | Endpoint correctness, error handling |
| {Name}.keyboard.test.js | Shortcuts | Key bindings, focus management |

### Integration
| Scenario | Steps | Expected Outcome |
|----------|-------|-----------------|
| Full pipeline run | Collect → Assemble → Score → Gate | Thesis produced, HITL triggered |
| Empty signals | No data from any source | Graceful empty state, no crash |
| Conflicting signals | Bull + bear in same mosaic | Conflict flag, raised to HITL |

---

## 7. Config Contract [REQUIRED]

| Key | Default | Source | Description |
|-----|---------|--------|-------------|
| flag_threshold | 50 | config | Score above which to FLAG for deep dive |
| monitor_threshold | 30 | config | Score above which to MONITOR |
| min_mosaic_fragments | 3 | config | Minimum signals to form a mosaic |
| min_signal_categories | 2 | config | Minimum distinct categories required |
| signal_max_age_hours | 24 | config | Signals older than this are filtered |
| hitl_conviction_threshold | 7 | config | Conviction score that triggers HITL gate |
| hitl_timeout_hours | 24 | config | Hours before unresolved HITL auto-defers |
| rate_limit_per_minute | 60 | config | Max API calls per minute per source |
| [add mission-specific keys] | | | |

---

## 8. Extension Points

### What existing modules does this touch?
| Module | How Extended | Files Modified |
|--------|-------------|---------------|
| [existing module] | [what's added] | [file paths] |

### What new modules does this create?
| Module | Purpose | Depends On |
|--------|---------|-----------|
| [new module] | [what it does] | [existing deps] |

### Migration Notes
[Any DB schema changes? New tables? Columns added to existing tables?]
```

---

## Usage Notes

- Every `[bracketed]` section must be filled in. Don't leave placeholders.
- The Config Contract (section 7) is the source of truth. Tests verify against it.
- The Test Plan (section 6) maps 1:1 to actual test files. Every row = a file.
- The UI Specification (section 5) should be detailed enough that another developer
  could build the component without asking questions.
- Extension Points (section 8) exist to enforce "extend, never rewrite."
