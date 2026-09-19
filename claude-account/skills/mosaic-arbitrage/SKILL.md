---
name: mosaic-arbitrage
description: >
  Apply Chris Camillo's mosaic theory and information arbitrage framework to identify
  asymmetric investment opportunities — across stocks, dropshipping/e-commerce, and crypto —
  before the mainstream market prices them in. Use this skill whenever the user asks to:
  research a trend, evaluate a product opportunity, build an investment thesis, identify
  market vulnerabilities, find undervalued niches, analyse social sentiment vs. ad spend,
  score a product with STEPPS, time a "gold rush" lifecycle, create a trend radar, generate
  a risk simulation, or produce research reports and interactive dashboards for arbitrage plays.
  Trigger on any mention of: "information arbitrage", "mosaic theory", "Camillo", "trend radar",
  "dropshipping thesis", "market vulnerability", "gold rush", "STEPPS", "pre-suasion", or
  "10X simulator".
---

# Mosaic Theory & Information Arbitrage Skill

A framework for identifying asymmetric opportunities by connecting non-obvious signals —
inspired by Chris Camillo's edge: spotting cultural shifts in social data *before* Wall Street,
analysts, or competitor dropshippers notice.

---

## Core Philosophy (First Principles)

1. **Information Arbitrage**: The edge exists in the *gap* — between rising social sentiment
   and flat institutional/competitor awareness. The gap = your alpha window.

2. **Mosaic Theory**: No single data point is the signal. The thesis emerges from assembling
   fragments: a Reddit complaint thread + a stagnant Google Trends curve + zero Facebook Ad
   Library spend + weak brand loyalty = confirmed opportunity.

3. **Trend Confirmation, Not Speculation**: Only act on *confirmed* trends (multi-week
   directional consistency). Flash signals are noise. Sustained shifts are alpha.

4. **Friction Is the Enemy of Margin**: Returns, heavy logistics, brand moats, and saturated
   ad markets all destroy ROI. Eliminate them structurally, not reactionally.

---

## The Four Frameworks — When to Apply Each

| Framework | Use When |
|---|---|
| **Mosaic Theory** | Building an investment thesis from fragmented signals |
| **Information Arbitrage Radar** | Identifying opportunities before mainstream pricing |
| **STEPPS Scoring** | Evaluating viral/sharing potential of a product or trend |
| **Gold Rush Lifecycle** | Timing entry/exit in a trend or niche |

---

## Module 1 — The Arbitrage Radar (Opportunity Discovery)

### What it does
Continuously scans for the *spread* between rising social signal and flat market response.

### Signal Sources to Analyse (or instruct user to check)
- **Reddit / TikTok / Twitter**: rising complaint threads, DIY workarounds, wish-list posts
- **Google Trends**: directional slope over 4–12 weeks (confirm, don't lead)
- **Amazon / AliExpress reviews**: negative review velocity on top-selling products
- **Facebook Ad Library**: competitor ad spend volume as saturation proxy

### The Arbitrage Signal Formula
```
Signal Strength = (Social Chatter Growth %) − (Competitor Ad Spend Growth %)
```
- Signal > 200%: Strong arbitrage window. Act.
- Signal 50–200%: Monitor. Confirm next week.
- Signal < 50% or negative: Market has priced it in. Pass.

### Vulnerability Detection (Moat Analysis)
A product is exploitable when:
- Top 3 sellers have consistent 1–2 star reviews citing the *same* flaw
- No recognisable brand dominates (generic suppliers)
- Consumer switching cost is zero (utility item, no ecosystem lock-in)
- The flaw is fixable by sourcing a marginally better supplier version

**Output format**: Produce a ranked opportunity table:
```
| Product Niche | Signal Strength | Vulnerability Type | Recommended Fix | Moat Score (1–10) |
```

---

## Module 2 — STEPPS Scoring

Score every opportunity against Jonah Berger's 6 STEPPS triggers. Higher scores = more
viral potential = lower CAC.

| Trigger | Question to Ask | Score (1–5) |
|---|---|---|
| **S**ocial Currency | Does owning/using this make people look good or smart? | |
| **T**riggers | Is there a daily cue that reminds people they need this? | |
| **E**motion | Does it produce strong feeling (anxiety relief, delight, pride)? | |
| **P**ublic | Is the product visible in use? Does it signal identity? | |
| **P**ractical Value | Does it solve a clear, recurring problem cheaply? | |
| **S**tories | Is there a narrative or transformation arc people share? | |

**Total STEPPS Score** (max 30): 
- 22–30: High virality. Low-spend ads can work.
- 14–21: Moderate. Needs strong creative.
- Below 14: Hard sell. Reconsider.

---

## Module 3 — Gold Rush Lifecycle Timing

### The Three Rings (weeks/months timeline)

```
[OUTER RING — Emerging: 3–6 months out]
  Social chatter rising. Google Trends flat. No ad spend.
  Action: Watch. Add to watchlist.

[MIDDLE RING — Validating: 1–3 months out]
  Google Trends confirms upward slope. Ad spend beginning.
  Action: Test with minimum budget ($200–500).

[CENTRE — Confirmed: Act Now]
  Social + Search aligned. Ad spend still below saturation.
  Action: Deploy full budget. Set exit trigger.
```

### Exit Signal
When Facebook Ad Library spend *growth* outpaces social chatter growth for 2 consecutive
weeks → Gold Rush ending. Reduce spend. Prepare to pivot.

### "Boring but Lucrative" Heatmap Logic
When sexy trends saturate, the system should surface:
- Consistent search volume (flat but sustained 12+ months)
- Near-zero competitor ad presence
- B2B adjacent, hobbyist, ergonomic, or safety-adjacent categories
These segments have lower peaks but *longer windows* and lower churn risk.

---

## Module 4 — The 10X or Zero Simulator

### Inputs
- Supplier unit cost (€/£/$)
- Shipping weight class (< 500g preferred)
- Target markup multiple (aim 4–6x for digital-physical)
- Daily ad budget
- Target demographic (age, platform, geography)
- Fragility / return risk flags: contains glass? requires sizing? perishable?

### Risk Penalty System
| Flag | Return Rate Penalty |
|---|---|
| Requires sizing (S/M/L) | +15% return assumption |
| Contains glass/fragile | +12% return assumption |
| Electronics with setup | +10% return assumption |
| Fabric/utility, no sizing | 0% penalty (ideal) |

### Simulation Output (Monte Carlo logic — simplified)

Run 3 scenarios:

**Bear Case** (20th percentile):
- Ad CPM at 90th percentile of niche
- Conversion rate: half of benchmark
- Return rate at maximum penalty

**Base Case** (50th percentile):
- Ad CPM at median
- Conversion rate: niche benchmark
- Return rate at minimum penalty

**Bull Case** (80th percentile):
- Ad CPM at 30th percentile
- Conversion rate: 1.5x benchmark
- Return rate: near zero (ideal product)

**Output verdict**:
- If Bull/Base > 5x ROI and Bear < −80%: "High risk / high reward. Micro-test only ($200)."
- If Bull > 3x and Bear > −30%: "Proceed. Strong asymmetry."
- If Bear < −80% and Bull < 3x: "Pass. Unfavourable risk/reward."

---

## Output Formats — What to Produce

Match the output to the request:

| Request Type | Output |
|---|---|
| "Research a trend / product" | Mosaic thesis doc: signal sources, STEPPS score, moat analysis, recommendation |
| "Build a dashboard / radar" | Single-file HTML with interactive trend radar (BMW-style lattice), heatmap, and simulator UI |
| "Investment thesis" | Structured markdown/docx report: signal data, STEPPS, lifecycle stage, unit economics, risk verdict |
| "Scraping agent / code" | Python agent scaffolding for Reddit/Google Trends/Ad Library monitoring |
| "Simulate this product" | Run Module 4 and return verdict table with Bear/Base/Bull scenarios |

---

## HTML Dashboard Guidelines

When producing an interactive HTML dashboard:

- **Dark mode** with neon accent colours (consistent with Nexus v4 aesthetic if applicable)
- **Trend Radar**: Concentric rings (Emerging / Validating / Confirmed). Clickable nodes.
  Click → detail panel showing: STEPPS score, vulnerability summary, lifecycle stage,
  signal strength metric.
- **Heatmap panel**: 2D scatter — Y axis = social chatter volume, X axis = ad spend saturation.
  Colour: green (low saturation / high signal), red (saturated).
- **Simulator panel**: Sliders for cost inputs. Auto-calculates Bear/Base/Bull. Displays dial
  or verdict badge.
- All panels in one file. Use vanilla JS + CSS or D3 if needed. No external dependencies
  except cdnjs.

---

## Asset Classes — Framing Differences

### Stocks / Equities
- Signal: social chatter about a *behaviour change* that benefits a company before earnings
- Mosaic: combine niche forum posts + hiring data + supply chain signals + sentiment delta
- Exit: institutional coverage begins = arbitrage window closing

### Dropshipping / E-commerce
- Signal: complaint threads about existing product flaws + rising search intent
- Mosaic: Amazon review velocity + Facebook Ad Library + AliExpress supplier availability
- Exit: CPM spike + declining CTR = saturated

### Crypto / Web3
- Signal: developer activity + early community chatter before exchange listings
- Mosaic: GitHub commits + Discord growth rate + wallet concentration data
- Exit: mainstream media coverage = late-stage, reduce position

---

## Reference Files

- `references/stepps-deep-dive.md` — Extended STEPPS examples by product category
- `references/signal-sources.md` — Full list of data sources, URLs, and scraping notes
- `references/unit-economics-templates.md` — Markup/CAC/LTV calculation templates

Read these when the user needs deeper detail in any specific area.
