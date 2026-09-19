# Brain Topology — 5-Layer Cognitive Architecture

The shared cognitive architecture that powers all MiroFish agents. Derived from first
principles across neuroscience and AI systems design.

## The Irreducible Insight

The architecture is a **closed loop**, not a pipeline. Action generates prediction error →
which updates the World Model → which reshapes Memory consolidation → which sharpens the
next Perception pass. Remove any one link and you don't have a weaker agent — you have a
fundamentally different (broken) one.

---

## The 5-Layer Stack

| Layer | Brain Analog | Key Mechanism | Agent Component |
|-------|-------------|---------------|-----------------|
| **L0 Perception** | Sensory cortex | Multi-modal → unified feature vectors | Signal collectors, doc parsers, API ingest |
| **L1 Memory** | Hippocampus | AAAK compression + spatial hierarchy + temporal graph | Persistent JSON memory + KuzuDB knowledge graph |
| **L2 World Model** | PFC / DMN | 4 paradigms: Implicit / Explicit / Simulator / Hybrid | Mosaic assembler / domain model builder |
| **L3 Planning** | Basal ganglia + PFC | Multi-scale: Reflex → Episode → Strategy → Meta | Specialist routing + confidence scoring + thesis formation |
| **L4 Action** | Motor cortex + cerebellum | Tools + agent delegation + feedback loop | HITL controls, Notion writes, doc generation, position execution |

---

## Layer Details

### L0 — Perception

**Purpose**: Convert raw multi-modal inputs into unified, queryable signal vectors.

**Neuroscience analog**: The sensory cortex doesn't store raw pixels — it extracts features
(edges, motion, color) and passes them upstream in a compressed, structured format. The
agent does the same: raw documents become chunked embeddings, raw market data becomes
signal vectors, raw conversations become extracted entities.

**Implementation patterns**:
- Document ingestion: chunk → embed → store in ChromaDB with domain metadata
- Entity extraction: during ingestion, extract entities + relationships → KuzuDB graph
- Signal normalization: every input source produces the same schema regardless of origin
- Context prefix: every chunk carries its source domain, doc type, and confidence weight

### L1 — Memory

**Purpose**: Store, compress, recall, and consolidate knowledge across time.

**Neuroscience analog**: The hippocampus doesn't store memories — it indexes them. It links
spatial location (where was this?), temporal position (when was this?), and associative
connections (what relates to this?). During sleep, it replays important memories to
consolidate them into long-term cortical storage.

**Implementation patterns**:
- **Persistent specialist memory** (memory_manager.py): JSON files per specialist in
  `memory/specialists/`. Keyword-based recall. Each memory entry has: content, timestamp,
  keywords, source, confidence.
- **Knowledge graph** (KuzuDB): Entity-relationship graph for structural queries. Nodes are
  concepts/modules/configs. Edges are relationships (depends_on, configures, overrides).
- **AAAK Compression**: When memory fills, compress by: Abstracting (generalize), Anchoring
  (link to existing knowledge), Associating (connect related), Killing (drop low-value).
- **Temporal decay**: Recent memories get higher recall weight. Old memories that haven't
  been accessed decay in priority.

### L2 — World Model

**Purpose**: Assemble perceived signals and recalled memories into a coherent model of
reality that can be queried and simulated.

**Neuroscience analog**: The prefrontal cortex and default mode network maintain an internal
simulation of the world. You can "imagine" a conversation before having it. The world model
enables counterfactual reasoning: "if X were true, what would we expect to see?"

**Four paradigms**:
1. **Implicit**: Pattern-matching from training data (the LLM's base knowledge)
2. **Explicit**: Stated rules and constraints (config contracts, business logic)
3. **Simulator**: Run forward projections ("if we configure X, what happens to Y?")
4. **Hybrid**: Combine all three — use implicit for gaps, explicit for constraints, simulator for validation

### L3 — Planning

**Purpose**: Given the world model, decide what to do at multiple timescales.

**Multi-scale planning**:
- **Reflex** (milliseconds): Immediate pattern match → cached answer
- **Episode** (minutes): Single question → route to specialist → generate answer
- **Strategy** (hours): Multi-question campaign → identify knowledge gaps → plan ingestion
- **Meta** (days): Review agent performance → update specialist prompts → retrain

### L4 — Action

**Purpose**: Execute the plan using available tools, then capture feedback.

**The feedback loop is what makes the agent learn**:
1. Execute action (write answer, generate doc, update config)
2. Capture human response (approve, reject, correct)
3. Generate prediction error (expected outcome vs actual)
4. Feed error back to L2 World Model (update beliefs)
5. Trigger L1 Memory consolidation (store the correction)
6. Sharpen L0 Perception (adjust signal weighting for next pass)

---

## Applying the Topology

Different agent types emphasize different layers:

| Agent Type | Heavy Layers | Light Layers |
|-----------|-------------|-------------|
| **SimCorp Super Agent** | L0 (doc parsing), L1 (accumulated customization knowledge), L3 (specialist routing) | L2 (domain model is built incrementally) |
| **MiroFish Research Agent** | L0 (multi-source signals), L2 (mosaic assembly), L3 (arbitrage scoring) | L1 (research is ephemeral, not accumulated) |
| **Overnight Ops Agent** | L3 (autonomous planning), L4 (build execution), L1 (learning from failures) | L0 (signals are pre-defined) |
