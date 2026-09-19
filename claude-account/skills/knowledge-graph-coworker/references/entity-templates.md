# Entity Templates

Markdown templates for all knowledge graph entity types.
Copy and fill when creating new entities.

---

## People

```markdown
---
type: person
name: "{full_name}"
role: "{analyst|executive|insider|founder|researcher}"
organization: "[[Companies/{org_name}]]"
email: "{email}"
aliases: ["{nickname}", "{abbreviation}"]
first_seen: "{YYYY-MM-DD}"
source: "{signal|email|meeting|manual}"
confidence: {0.0-1.0}
---

## Role Context
{What this person does, why they matter to our research}

## Key Signals
- [[Signals/{signal_id}]] — {context}

## Relationships
- Works at: [[Companies/{org}]]
- Connected to: [[People/{other_person}]]
- Expert in: [[Topics/{topic}]]
```

## Companies

```markdown
---
type: company
name: "{company_name}"
class: "{public|private|crypto}"
ticker: "{SYMBOL}"  # if public
sector: "[[Sectors/{sector_name}]]"
market_cap: {number}  # if public, in USD
stage: "{seed|series_a|series_b|series_c|growth|public}"  # if private
last_funding: "{YYYY-MM-DD}"  # if private
valuation: {number}  # if private, last known
domain: "{company.com}"
aliases: ["{abbreviations}"]
first_seen: "{YYYY-MM-DD}"
tracked: {true|false}  # for live notes
---

## Current Thesis
{One paragraph: current investment thesis or research angle}

## Consensus Narrative
{What the market currently believes about this company}

## Misframing (if any)
{Why the consensus might be wrong}

## Key Signals
- [[Signals/{signal_id}]] — {context}

## Relationships
- Sector: [[Sectors/{sector}]]
- Competitors: [[Companies/{competitor}]]
- Partners: [[Companies/{partner}]]
- Key People: [[People/{person}]]

## Catalysts
1. {event} — {date} — {expected magnitude}
```

## Sectors

```markdown
---
type: sector
name: "{sector_name}"
parent_sector: "[[Sectors/{parent}]]"  # if subsector
keywords: ["{keyword1}", "{keyword2}"]
aliases: ["{alt_names}"]
---

## Overview
{What this sector covers, current dynamics}

## Key Companies
- [[Companies/{company1}]] — {brief context}
- [[Companies/{company2}]] — {brief context}

## Themes
- [[Topics/{theme1}]]
- [[Topics/{theme2}]]

## Signals
- [[Signals/{signal_id}]] — {context}
```

## Topics

```markdown
---
type: topic
name: "{topic_name}"
keywords: ["{keyword1}", "{keyword2}", "{keyword3}"]
aliases: ["{alt_names}"]
gold_rush_stage: "{emerging|validating|confirmed|saturated}"
first_seen: "{YYYY-MM-DD}"
---

## Overview
{What this topic/theme is about}

## Related Companies
- [[Companies/{company}]] — {how related}

## Related People
- [[People/{person}]] — {how related}

## Signal History
- {date}: [[Signals/{signal_id}]] — {context}
```

## Signals

```markdown
---
type: signal
id: "{unique_id}"
source: "{reddit|yfinance|sec|google_trends|email|manual}"
category: "{fundamental|structural|behavioral|sentiment}"
timestamp: "{ISO-8601}"
companies: ["[[Companies/{company}]]"]
topics: ["[[Topics/{topic}]]"]
confidence: {0.0-1.0}
value: {numeric_value}
---

## Signal Content
{The actual signal data/observation}

## Context
{Why this signal matters, what it might indicate}

## Related Signals
- [[Signals/{related_id}]] — {relationship: confirms|contradicts|extends}
```

## Theses

```markdown
---
type: thesis
id: "{unique_id}"
asset: "[[Companies/{company}]]"
asset_class: "{equity|private|crypto}"
created: "{ISO-8601}"
conviction: {1-10}
signal_strength: {number}
verdict: "{APPROVE|DEFER|REJECT}"
status: "{active|closed|invalidated}"
---

## Consensus Narrative
{What the market believes}

## Misframing
{Why the consensus is wrong}

## Reality (from mosaic)
{What assembled signals show}

## Arbitrage Gap
- Signal Strength: {score}
- True Growth: {%}
- Market Awareness: {%}

## Mosaic Fragments
### Fundamental
- [[Signals/{id}]] — {context}

### Structural
- [[Signals/{id}]] — {context}

### Behavioral
- [[Signals/{id}]] — {context}

### Sentiment Delta
- [[Signals/{id}]] — {context}

## Catalyst Chain
1. {event} — {timeline} — {magnitude}

## Risk Matrix
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|

## HITL Decisions
- {date}: {verdict} — "{reasoning}"
```

---

## Notes on Templates

- All `{bracketed}` values must be filled from config or data, never hardcoded
- Confidence scores are 0.0-1.0 floats
- Dates use ISO-8601 format
- Backlinks use `[[Category/Name]]` Obsidian syntax
- Entity IDs should be generated (UUID or hash), not sequential integers
- `tracked: true` entities get live notes (auto-updating)
