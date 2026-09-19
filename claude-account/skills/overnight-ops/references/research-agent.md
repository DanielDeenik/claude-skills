# Research Agent — Phase 2

## Objective
Deepen Social Arb's intelligence by researching the top opportunities identified in Phase 1 (COLLECT). The goal is to accumulate context that makes the platform smarter over time.

## Detailed Steps

### Step 1: Identify Research Targets
1. Call `social_arb_get_mosaics` with action="build_thesis" to get the strongest signals
2. Call `social_arb_get_theses` with status="pending_review" to see what's awaiting decision
3. Sort by divergence_strength descending — highest divergence = biggest information gap
4. Pick the top 3 symbols as research targets

### Step 2: Web Research (per symbol)
For each target symbol:

**Public markets (stocks):**
- Search for recent earnings reports, analyst upgrades/downgrades
- Check for M&A activity, insider trading, institutional flows
- Look for product launches, regulatory changes, patent filings
- Search Reddit (r/wallstreetbets, r/stocks) for retail sentiment shifts

**Crypto:**
- Check protocol governance proposals, TVL changes
- Search for bridge exploits, audit completions, major integrations
- Look for regulatory news (SEC, EU MiCA)
- Check DeFi Llama for TVL trends vs. token price

**Private companies:**
- Search for funding round announcements, valuation changes
- Check job postings (hiring velocity = growth signal)
- Look for partnership announcements, customer wins
- Search GitHub for commit velocity on open-source repos

### Step 3: Synthesize
For each symbol, produce a structured research note:

```
## {SYMBOL} Research Note — {date}
**Divergence:** {score} | **Coherence:** {score} | **Lifecycle:** {stage}

### Key Findings
1. [Most important finding with source]
2. [Second finding]
3. [Third finding]

### Signal vs. Market Gap
[Explain why social signals diverge from market price]

### Thesis Implication
[Does this strengthen or weaken the existing thesis?]

### Recommended Action
[approve/reject/defer the pending thesis, or investigate further]
```

### Step 4: Persist
1. Save research notes to auto-memory as project-type memories
2. Update existing memories if the research updates prior findings
3. If the research changes your view on a thesis, note it in the briefing
4. Do NOT auto-approve or auto-reject theses — that's Dan's HITL decision

## What NOT to Do
- Don't make trading decisions
- Don't modify the database directly
- Don't spend more than 30 minutes on research per cycle
- Don't research symbols that aren't in the configured symbol lists
