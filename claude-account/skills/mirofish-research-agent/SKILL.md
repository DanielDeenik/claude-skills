---
name: mirofish-research-agent
description: >
  Build MiroFish super-agent research missions — Bloomberg-terminal-style JSX agents running
  the 5-layer brain topology to discover asymmetric opportunities across equities, private
  companies, and crypto. Produces solution docs BEFORE code, enforces TDD (pytest + vitest),
  HITL gates, zero hardcoded values. Trigger on: "MiroFish", "research agent", "super agent",
  "brain topology", "investment research", "mosaic research", "financial dashboard",
  "Bloomberg style", "arbitrage agent", "ticker research", "private company research",
  "crypto research", or any request to build an interactive research tool for Social Arb.
---

# MiroFish Research Agent Skill

Build production-grade, interactive research agents that implement Chris Camillo's mosaic
theory through Social Arb's 5-layer cognitive architecture. Every agent ships with a
solution design doc, full test coverage, HITL gates, and a Bloomberg-terminal-style UI.

---

## Why This Skill Exists

Social Arb's edge is assembling fragmented signals into investment theses before mainstream
pricing catches up. The MiroFish research agent is the human-facing interface to that edge —
it runs the full brain topology loop (Perception → Memory → World Model → Planning → Action)
as an interactive experience where the human stays in the loop at every decision point.

The skill enforces three non-negotiable constraints Dan has set:

1. **No hardcoded values** — every threshold, URL, ticker, config value comes from
   config/env/DB or user input. Zero magic numbers.
2. **Extend, never rewrite** — every feature extends existing Social Arb modules. Check
   what exists before creating anything new.
3. **TDD + HITL** — tests first, human approval at gates. No code ships without both.

---

## Workflow: 5 Phases (mirrors the brain topology)

Every research agent build follows this sequence. Do not skip phases.

### Phase 0: PERCEIVE — Understand the Mission

Before writing anything, gather the research context:

1. **What asset class?** Public equity / private company / crypto / cross-asset
2. **What's the hypothesis seed?** (Can be blank — agent forms its own)
3. **What signals matter?** Map to existing Social Arb collectors or identify new ones needed
4. **What's the HITL surface?** Where does the human make decisions?

Read the existing codebase to understand what's already built:
- Check `social_arb/agents/` for existing agent patterns
- Check `social_arb/ui/src/pages/` for existing UI components
- Check `social_arb/api/routes/` for existing API surface
- Check `social_arb/engine/` for intelligence layer modules

### Phase 1: REMEMBER — Solution Design Document

**Create `docs/SOLUTION_<mission-name>.md` before any code.**

The solution doc is the contract between the agent and the human. It must contain:

```markdown
# MiroFish Mission: [Name]

## 1. Problem Statement
What information asymmetry are we targeting?

## 2. Brain Topology Mapping
| Layer | Component | Data Source | Output |
|-------|-----------|-------------|--------|
| L0 Perception | What collectors/APIs | Specific sources | Signal format |
| L1-L2 Memory→World Model | How signals assemble | Assembly logic | Mosaic format |
| L3 Planning | Decision framework | Scoring formula | Thesis format |
| L4-L5 Action | What the human does | HITL gates | Position/pass |

## 3. Signal Architecture
- Input signals (with source, refresh cadence, config keys)
- Assembly rules (how fragments become mosaics)
- Scoring formula (with all thresholds as config values)

## 4. HITL Gates
| Gate | Trigger | Human Decision | Timeout Behavior |
|------|---------|---------------|-----------------|

## 5. UI Specification
- Layout wireframe (ASCII or description)
- Component tree
- Data flow (what API calls, what state)
- Bloomberg terminal design tokens (see references/bloomberg-ui.md)

## 6. Test Plan
- Backend: pytest test file names and what they cover
- Frontend: vitest test file names and what they cover
- Integration: end-to-end scenarios

## 7. Config Contract
Every configurable value listed with:
| Key | Default | Source (env/config/DB/user-input) | Description |
```

**HITL Gate 1:** Present the solution doc to the human. Do NOT proceed to code until
approved. Ask: "Does this solution design capture what you want? Any changes before I
write tests?"

### Phase 2: MODEL — Write Tests First (TDD)

After solution doc approval, write tests BEFORE implementation.

**Backend (pytest):**
```
tests/test_<mission>_signals.py    — Signal collection and validation
tests/test_<mission>_assembly.py   — Mosaic assembly logic
tests/test_<mission>_scoring.py    — Thesis scoring and arbitrage formulas
tests/test_<mission>_config.py     — Config loading, no hardcoded values
```

**Frontend (vitest):**
```
ui/src/__tests__/<Mission>.test.jsx  — Component rendering
ui/src/__tests__/<Mission>.api.test.js — API integration
```

Test writing rules:
- Every threshold/magic number in tests must reference a config constant, not a literal
- Test the HITL gate triggers (when does the agent pause for human input?)
- Test the scoring formula with edge cases (zero signals, max signals, conflicting signals)
- Test that the UI renders in all states (loading, error, empty, populated, HITL-waiting)

**HITL Gate 2:** Show the test file structure and key test cases to the human. Ask:
"These are the tests I'll write first. Missing anything?"

### Phase 3: PLAN — Implement Against Tests

Now build the code to make tests pass. Follow red-green-refactor:

1. **Red:** Run tests, confirm they fail (they should — no implementation yet)
2. **Green:** Write minimal code to pass each test
3. **Refactor:** Clean up while keeping tests green

Implementation order:
1. Config/constants first (the contract)
2. Backend data logic (signals, assembly, scoring)
3. API routes (extend existing `social_arb/api/routes/`)
4. Frontend components (extend existing `social_arb/ui/src/pages/`)
5. Wire into existing pipeline (extend, don't replace)

**Extension rules:**
- New API routes go in existing route files if they fit, new file only if truly new domain
- New UI pages must be wired into `App.jsx` routing AND sidebar navigation
- New collectors must register with the existing Sentinel agent pattern
- All new DB tables go through `init_db()` in the existing schema

### Phase 4: ACT — Bloomberg Terminal UI

The UI is the human's interface to the research agent. It must feel like a Bloomberg
terminal — dense, data-rich, professional.

**Read `references/bloomberg-ui.md` for the full design system.**

Key principles:
- Dark background (#0a0e17), high-contrast data
- Monospace for numbers/data, sans-serif for labels
- Dense information layout — no wasted whitespace
- Color encodes meaning: green=bullish, amber=neutral, red=bearish, cyan=information
- Every interactive element has a keyboard shortcut
- Real-time feel: pulse animations on live data, timestamps on everything

Component patterns for research agents:
- **Mission Header:** Asset name, class badge, hypothesis seed, mission timestamp
- **Signal Grid:** 4-column mosaic fragment display (Fundamental / Structural / Behavioral / Sentiment)
- **Thesis Panel:** Structured output with arbitrage score, conviction meter, catalyst chain
- **HITL Controls:** Prominent approve/defer/reject buttons with reasoning textarea
- **Drill Panel:** Expandable detail on any signal fragment

**HITL Gate 3:** Show the running agent to the human. Ask: "How does this look and feel?
Any UI adjustments before we finalize?"

### Phase 5: VERIFY — Quality Gate

Before marking complete, run the full verification:

1. **All tests pass** — `pytest` and `vitest` both green
2. **No hardcoded values** — grep the new code for magic numbers/strings
3. **Extension integrity** — no orphaned pages, no dead API methods, all routes wired
4. **HITL gates functional** — the agent actually pauses for human input at each gate
5. **Config contract honored** — every value in the solution doc's config table is
   actually configurable

```bash
# Hardcoded value check
grep -rn "http://" new_files/ | grep -v "config\|env\|test"
grep -rn "[0-9]\{2,\}" new_files/ | grep -v "config\|test\|import"
```

**HITL Gate 4 (final):** Present verification results. Ask: "All checks pass. Ready to
commit?"

---

## The 5-Layer Brain Topology — How It Maps to Code

The research agent IS the brain topology made interactive:

| Layer | Brain Analog | Agent Component | What It Does |
|-------|-------------|-----------------|-------------|
| **L0 Perception** | Sensory cortex | Signal collectors | Multi-source data → unified signal vectors |
| **L1 Memory** | Hippocampus | Knowledge store | AAAK compression + temporal knowledge graph |
| **L2 World Model** | PFC / DMN | Mosaic assembler | 4 paradigms: Implicit / Explicit / Simulator / Hybrid |
| **L3 Planning** | Basal ganglia | Thesis scorer | Multi-scale: Reflex → Episode → Strategy → Meta |
| **L4-L5 Action** | Motor cortex | HITL controls + executor | Tools + agent delegation + feedback loop |

The closed loop is critical: Action generates prediction error → updates World Model →
reshapes Memory consolidation → sharpens next Perception pass. The UI must make this loop
visible to the human.

---

## Asset Class Adaptations

### Public Equities
- **Perception:** Earnings data, hiring signals, supply chain, social sentiment, SEC filings
- **Mosaic:** Combine niche forum posts + analyst consensus gaps + institutional flow
- **Scoring:** Signal Strength = True Growth % - Market Awareness %
- **Arbitrage window closes when:** Institutional coverage begins

### Private Companies / Startups
- **Perception:** Funding rounds, partnership announcements, adjacent market signals, job posts
- **Mosaic:** Bloomberg integration signals + ecosystem positioning + TAM validation
- **Scoring:** Adjacent Market Validation = Confirmed Integrations × TAM Growth Rate
- **Arbitrage window closes when:** Series B narrative ceiling gets priced in

### Crypto / Web3
- **Perception:** Developer activity, wallet concentration, exchange flow, community growth
- **Mosaic:** GitHub commits + Discord growth + on-chain metrics + whale behavior
- **Scoring:** Signal Strength = Dev Activity Growth % - Mainstream Media Coverage %
- **Arbitrage window closes when:** Mainstream media coverage = late-stage

---

## Arbitrage Scoring (Universal Formula)

```
Signal Strength = (True Growth %) - (Market Awareness %)
```

Where:
- True Growth comes from mosaic assembly (the reality the market hasn't priced)
- Market Awareness comes from analyst coverage, media mentions, ad spend, institutional flow

| Score | Interpretation | Action |
|-------|---------------|--------|
| > 50 | Strong divergence | FLAG for deep dive |
| 30-50 | Moderate divergence | MONITOR, gather more fragments |
| < 30 | Weak or no divergence | PASS unless catalyst imminent |

All thresholds (50, 30) must be config values, not hardcoded.

---

## Misframing Detection (Phase 1 of Every Research Run)

Before assembling the mosaic, the agent must surface:
1. **What the market consensus narrative is** (how is this asset currently framed?)
2. **Why that framing might be wrong** (what signals contradict it?)
3. **What the reframing would look like** (if reality ≠ consensus, what's the true story?)

This is the Bachem insight generalized: "The market frames X as Y. But the data says X is
actually Z. The gap between Y and Z is the arbitrage."

---

## MiroFish Thesis Output Format

Every research run must produce this structured output:

```
╔══ MIROFISH THESIS ══╗
║ Asset: [name]
║ Class: [equity/private/crypto]
║ Mission: [timestamp]
╠══════════════════════╣
║ CONSENSUS NARRATIVE
║ [What the market currently believes]
║
║ MISFRAMING
║ [Why the consensus is wrong or incomplete]
║
║ REALITY (from mosaic)
║ [What the assembled signals actually show]
║
║ ARBITRAGE GAP
║ Signal Strength: [score]
║ True Growth: [%] | Market Awareness: [%]
║
║ MOSAIC FRAGMENTS
║ Fundamental: [signals]
║ Structural: [signals]
║ Behavioral: [signals]
║ Sentiment Delta: [signals]
║
║ CATALYST CHAIN
║ 1. [event] — [timeline] — [magnitude]
║ 2. ...
║
║ RISK MATRIX
║ [key risks with probability estimates]
║
║ VERDICT: [APPROVE / DEFER / REJECT]
║ Conviction: [1-10]
║ Next HITL Gate: [what triggers re-review]
╚══════════════════════╝
```

---

## Reference Files

Read these when you need deeper detail:

- `references/brain-topology.md` — The shared 5-layer cognitive architecture (Perception →
  Memory → World Model → Planning → Action) with neuroscience analogs. This is the same
  architecture used by the SimCorp Super Agent — both agents share the brain topology but
  emphasize different layers. Read when designing new research missions or debugging the
  feedback loop between Action and Perception.
- `references/bloomberg-ui.md` — Full Bloomberg terminal design system: colors, typography,
  component patterns, animation specs, keyboard shortcuts
- `references/solution-template.md` — Complete solution document template with examples
- `references/tdd-patterns.md` — pytest + vitest patterns for financial data, config
  validation, HITL testing

### Sister Skill: SimCorp Super Agent
The `simcorp-super-agent` skill shares the same brain topology but is optimized for
consulting: document analysis, Notion pipeline integration, and accumulated client-specific
customization learning. If a research mission involves SimCorp Dimension or fund
administration, the SimCorp Super Agent is the better tool.

---

## Checklist (verify before completing any MiroFish build)

- [ ] Solution doc created and approved by human
- [ ] Tests written BEFORE implementation
- [ ] All tests passing (pytest + vitest)
- [ ] Zero hardcoded values (grep verified)
- [ ] All new routes wired in App.jsx + sidebar
- [ ] All new API routes have corresponding api.js methods
- [ ] HITL gates functional (agent pauses for human)
- [ ] Bloomberg terminal aesthetic applied
- [ ] Mosaic fragments displayed in 4-category grid
- [ ] Thesis output follows MiroFish format
- [ ] Config contract matches solution doc
- [ ] Extends existing modules, no orphaned code
