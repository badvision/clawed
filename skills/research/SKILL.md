---
name: research
description: LLM Council - 3-stage multi-model research pipeline (collect, peer review, synthesize). Queries OpenAI, Perplexity, Claude, and Gemini in parallel, has them anonymously critique each other, then synthesizes a final answer. Keywords: research, code review, architecture, multi-model consensus, LLM council, peer review, technology comparison.
---

# Research Skill

LLM Council: 3-stage multi-model research using OpenAI, Perplexity, Claude, and Gemini.

## How It Works

1. **Collect** - Query all models in parallel
2. **Peer Review** - Each model anonymously critiques and ranks the others
3. **Synthesize** - Chairman produces a final answer from all responses and reviews

9 API calls per query with all 4 models (4 collect + 4 review + 1 synthesis). Gracefully degrades if models are unavailable.

The chairman is selected based on task type: Perplexity leads research queries, Gemini leads code reviews, bug analysis, and comparisons.

## Usage Modes

### Monolithic (full council pipeline)

Runs all 3 stages with every available provider:

```bash
python -m research research "Python async best practices"
python -m research review src/server.py "security focus"
python -m research compare LanceDB Pinecone Weaviate
python -m research bug src/client.py "Connection timeout"
python -m research design src/arch.py "scalability requirements"
python -m research validate "Use DuckDB" "analytics pipeline" PostgreSQL ClickHouse
python -m research comprehensive src/auth.py "authentication best practices"
```

### Per-agent (single provider query)

Query a single provider directly. Used by model-agent definitions in multi-agent workflows:

```bash
python -m research query openai "Python async best practices"
python -m research query gemini "Compare DuckDB and PostgreSQL" --task-type comparison
python -m research query perplexity "Latest WASM runtime benchmarks" --context "Performance research"
python -m research query anthropic "Review this approach" --task-type code-review
```

### Peer review (on collected responses)

Run peer review on a JSON file of previously collected responses:

```bash
python -m research review-responses "Python async best practices" responses.json
```

The responses file should be a JSON array of objects with `provider`, `model`, and `content` fields.

## Programmatic

```python
import asyncio
from research import run_council, query_single

# Full council pipeline
result = asyncio.run(run_council("Python async best practices", "Research query"))
print(result.synthesis)

# Single provider query
response = asyncio.run(query_single("gemini", "Explain WASM", "Research query"))
print(response.content)
```

## Setup & Verification

See `SETUP.md` for detailed provider configuration, agent symlink verification, and troubleshooting. When users ask about configuring this skill or debugging provider issues, refer to that document.

## Environment

```bash
# Required (at least one)
OPENAI_API_KEY=sk-proj-...
PERPLEXITY_API_KEY=pplx-...
ANTHROPIC_API_KEY=sk-ant-...

# Gemini via Vertex AI
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=global          # CRITICAL: use "global" for Gemini 3.x
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Override models (optional — defaults are set in council.py)
OPENAI_MODEL=<model-id>
PERPLEXITY_MODEL=<model-id>
ANTHROPIC_MODEL=<model-id>
GEMINI_MODEL=<model-id>
```

## Multi-Agent Research Team

This skill supports two orchestration modes:

### CLI mode (single process)

Run `python -m research research "topic"` to execute all 3 stages in one process. Simple but inflexible — always uses the same models regardless of task type.

### Team mode (recommended)

The `research-lead` agent orchestrates a team of specialized agents. All agents inherit their model from `~/.claude/settings.json`.

| Agent | Role |
|-------|------|
| `research-lead` | Orchestrator: decomposes queries, selects which model-agents to spawn, synthesizes |
| `openai-researcher` | Queries OpenAI via `query openai` — chain-of-thought scaffolding |
| `perplexity-researcher` | Queries Perplexity via `query perplexity` — citation-backed answers |
| `claude-researcher` | Answers directly (no API key needed) — nuanced synthesis with codebase access |
| `gemini-researcher` | Queries Gemini via `query gemini` — multimodal reasoning |
| `peer-reviewer` | Evaluates anonymized responses via `review-responses` — avoids self-review bias |

The research-lead selects agents based on task type:

| Task | Agents Selected |
|------|----------------|
| research | All 4 researchers |
| review | OpenAI, Claude, Gemini |
| compare | Perplexity, Claude, Gemini |
| bug | OpenAI, Claude |
| validate | All 4 researchers |

## Dependencies

`httpx` and `google-genai`. Install: `pip install httpx google-genai`
