# LLM Router — Intelligent Model Routing Skill

## Trigger

Activate when the user mentions: "LLM router", "model routing", "route prompts", "cost optimization LLM", "cheaper API calls", "RouteLLM", "NadirClaw", "LLMRouter", "model selection", "smart routing", "reduce LLM costs", "balance quality and cost", "proxy for LLMs", or any request about intelligently routing prompts to different AI models based on complexity/cost.

## Purpose

Guide the user through selecting, setting up, and configuring an intelligent LLM routing system that analyzes prompt complexity and routes to the optimal model — cheap models for simple tasks, premium models for complex ones. Typical cost reduction: 40-85%.

## Knowledge Base

### The Three Major Open-Source Routers

---

### 1. RouteLLM (by LMSYS)
**The Data-Driven Traffic Cop**

- **Repo:** https://github.com/lm-sys/RouteLLM
- **What it does:** Drop-in OpenAI client replacement. Analyzes prompts using trained classifiers and routes to strong vs. weak model.
- **Cost savings:** Up to 85% reduction while maintaining 95% of GPT-4 performance.
- **Pre-trained routers included:**
  - `sw_ranking` — Weighted Elo calculation based on prompt similarity
  - `bert` — BERT classifier trained on preference data
  - `causal_llm` — LLM-based classifier tuned on preference data
  - `mf` — Matrix factorization on preference data
- **Best for:** Teams already using OpenAI-compatible APIs who want plug-and-play routing with proven benchmarks.
- **Trained on:** GPT-4-1106-preview vs Mixtral-8x7B, but generalizes to other model pairs.

**Quick Start:**
```python
pip install "routellm[serve,eval]"

import os
from routellm.controller import Controller

os.environ["OPENAI_API_KEY"] = "your-key"

client = Controller(
    routers=["mf"],
    strong_model="gpt-4-1106-preview",
    weak_model="mixtral-8x7b-instruct-v0.1",
)

response = client.chat.completions.create(
    model="router-mf-0.11593",  # threshold after the router name
    messages=[{"role": "user", "content": "What is the capital of France?"}]
)
```

**As OpenAI-compatible server:**
```bash
python -m routellm.openai_server \
  --routers mf \
  --strong-model gpt-4-1106-preview \
  --weak-model mixtral-8x7b-instruct-v0.1
```

---

### 2. NadirClaw
**The Lightning-Fast Proxy**

- **Repo:** https://github.com/doramirdor/NadirClaw
- **What it does:** OpenAI-compatible proxy that classifies prompts in ~10ms and routes simple ones to cheap/local models.
- **Cost savings:** 40-70% depending on workload.
- **Key features:**
  - 10ms classification latency
  - Context Optimize: compacts bloated context (JSON, tool schemas, chat history) saving 30-70% input tokens
  - Works with Claude Code, Cursor, and any OpenAI-compatible client
  - Runs fully local — no third-party proxy, no subsidized tokens
  - MIT licensed, free, self-hostable
- **Best for:** Solo developers and small teams who want a lightweight local proxy, especially those using Ollama for free local models.
- **Typical routing split:** 60-70% of coding prompts are simple enough for cheap models.

**Quick Start:**
```bash
# Clone and run
git clone https://github.com/doramirdor/NadirClaw.git
cd NadirClaw
# Follow README for Docker or local setup
# Point Claude Code / Cursor to localhost proxy
```

**Docker + Ollama (zero-cost local routing):**
See: https://dev.to/dor_amir_dbb52baafff7ca5b/how-to-set-up-nadirclaw-with-docker-ollama-for-zero-cost-local-llm-routing-357a

---

### 3. LLMRouter (by UIUC)
**The Machine Learning Matchmaker**

- **Repo:** https://github.com/ulab-uiuc/LLMRouter
- **What it does:** Uses ML classifiers (KNN, SVM, MLP, Matrix Factorization, BERT, Elo Rating, graph-based) to dynamically select the best model per query.
- **16+ routing models** across 4 categories:
  - Single-round routers (KNN, SVM, MLP, MF, Elo)
  - Multi-round routers
  - Agentic routers
  - Personalized routers
- **11 benchmark datasets** included for training/evaluation
- **Best for:** ML-savvy teams who want to train custom routing logic on their own data, or researchers exploring routing strategies.
- **Features:**
  - Unified CLI for training, inference, and interactive chat
  - Gradio-based visual UI
  - Plugin system for custom routing logic
  - Batch processing support

**Quick Start:**
```bash
git clone https://github.com/ulab-uiuc/LLMRouter.git
cd LLMRouter
pip install -e .
# Train a router
llmrouter train --model knn --dataset mmlu
# Run inference
llmrouter infer --model knn --query "Explain quantum computing"
```

---

## Decision Framework

When the user asks which router to use, guide them through this matrix:

| Factor | RouteLLM | NadirClaw | LLMRouter |
|--------|----------|-----------|-----------|
| **Setup time** | 5 min | 15 min | 30+ min |
| **Pre-trained?** | Yes (4 routers) | Yes | Needs training |
| **Local/self-hosted** | Server mode | Fully local | Local |
| **OpenAI compatible** | Yes (drop-in) | Yes (proxy) | CLI/API |
| **Custom training** | Possible | Rules-based | Full ML pipeline |
| **Best cost savings** | Up to 85% | 40-70% | Varies by training |
| **Works with Ollama** | Yes | Yes (native) | Yes |
| **Visual UI** | No | No | Yes (Gradio) |
| **Ideal user** | Production teams | Solo/small teams | ML teams/researchers |

## Workflow

### When user asks about LLM routing:

1. **Ask 3 clarifying questions:**
   - Are you routing for a production app, local dev environment, or Claude Code/Cursor usage?
   - How many models do you want to route between? (2 specific models vs. dynamic pool)
   - Do you want plug-and-play, or are you willing to train custom routing logic?

2. **Recommend one primary option** based on their answers, with brief mentions of the other two as alternatives.

3. **Provide step-by-step setup** for their chosen router, including:
   - Installation commands
   - Configuration for their specific model pair
   - How to validate it's working (test with a simple vs. complex prompt)
   - Cost monitoring setup

4. **Give a "you'll know it's working when..."** checkpoint:
   - Simple prompts (e.g., "What's 2+2?") route to cheap model
   - Complex prompts (e.g., "Design a distributed caching system") route to premium model
   - Dashboard/logs show the routing split

## Related Resources

- Awesome AI Model Routing: https://github.com/Not-Diamond/awesome-ai-model-routing
- Router-R1 (reinforcement learning routing): https://github.com/ulab-uiuc/Router-R1
- GraphRouter (graph-based routing): https://github.com/ulab-uiuc/GraphRouter
