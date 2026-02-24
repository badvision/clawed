# AI-Assisted Research with Claude Code

Three complementary skills for structured analysis: personality-driven deliberation, multi-model factual grounding, and both combined.

## /socratize — The Senate

Type `/socratize` in Claude Code and it spawns a team of personality-diverse Claude agents — an optimist, a skeptic, a pragmatist, a detail-oriented analyst, a big-picture thinker — each playing a distinct role. They research the problem from their perspective, propose solutions, challenge each other, and vote. A product owner facilitates the rounds, tracks consensus, and declares when 2/3 majority is reached or deadlock after 5 rounds.

Think of it as the Roman Senate: structured deliberation with genuine disagreement, arriving at a decision through debate and voting.

It works well for subjective questions — architectural trade-offs, design approaches, prioritization — where there is no single right answer and the value comes from hearing multiple perspectives argue it out.

But every voice is Claude. Same training data. Same knowledge cutoff. Same blind spots. When the Senate agrees unanimously, you have to wonder: is it consensus or echo chamber?

## /research — The Oracle Network

Type `/research` and something different happens. Instead of Claude debating with itself, a `research-lead` agent dispatches the question to four independently trained models in parallel:

| Model | What It Brings |
|-------|---------------|
| **OpenAI** | Systematic chain-of-thought reasoning. Thorough, structured analysis |
| **Perplexity** | Real-time web search with citations. The only Council member that looks things up live — source URLs included |
| **Claude** (Anthropic) | Nuanced synthesis. The only Council member with direct access to your codebase via Read/Glob/Grep. No API key needed — it IS the host model |
| **Gemini** (Google, via Vertex AI) | Multimodal reasoning with large context windows. Handles big inputs well |

Then three stages execute:

1. **Collect** — All 4 models receive the same question and answer independently. No model sees another's response. (4 API calls)
2. **Peer Review** — Responses are anonymized as "Response A", "Response B", etc. Each model critiques and ranks the others without knowing who wrote what. This surfaces genuine disagreements rather than deferring to authority. (4 API calls)
3. **Synthesize** — A chairman model (selected by task type — Perplexity for research, Gemini for code reviews) reads all responses and all reviews, then produces a definitive synthesis weighted by the peer rankings. (1 API call)

Nine API calls total. Four independently trained minds instead of one repeated four times. Where the Senate gives you deliberation, the Oracle Network gives you evidence — facts, benchmarks, citations, current data.

But the oracles don't *debate*. They answer once, in isolation. If two models contradict each other, nobody presses them to reconcile. You get evidence without deliberation.

## /concilize — The Concilium

From Latin *concilium* (council, assembly). What if the Senate could consult the oracles AND debate among themselves?

`/concilize` composes both systems into a 5-phase workflow with 3 topic-appropriate agents:

1. **Clarify** — A technical analyst examines the question and makes sure it's unambiguous before any API calls are spent. If something is unclear, it asks you
2. **Oracle Baseline** — The LLM Council runs a full `/research` query. Four models. Peer-reviewed. Citations. This establishes a factual baseline that all subsequent debate must engage with
3. **Deliberate** — The team lead selects 3 agent types based on the topic (from technical-analyst, software-architect, tdd-software-engineer, qa-test-validator, product-owner-task-planner) and spawns them with distinct personalities. Each agent receives the Council baseline as mandatory reading, researches from their perspective, AND proposes a solution — no analyst/architect split. The Senate debates in structured rounds. When a *factual* dispute arises, they can send a runner back to the oracles — max 2 on-demand Council queries per session. Matters of *preference* stay in the Senate. Rounds continue until 2/3 consensus or 5-round deadlock
4. **Red Team** — Mandatory, never skipped. The Oracle Council is asked to attack the proposed solution: "What is wrong with this plan? What will fail? What are we missing?" If critical flaws are found, the agents get one revision round
5. **The Decree** — Final output with the decision, all oracle evidence, dispute resolutions, the adversarial review, vote tallies, and any dissenting opinions preserved

The Senate without oracles produces eloquent consensus that may be wrong. The oracles without a Senate produce accurate evidence that no one debates. The Concilium produces evidence-grounded consensus that has survived adversarial review.

## When to Use Which

| Skill | Best For | Example | External API Calls |
|-------|----------|---------|-------------------|
| `/socratize` | Subjective questions where structured debate is the value | "How should we structure our component library?" | 0 |
| `/research` | Factual questions where multi-model evidence matters | "What are the current benchmarks for DuckDB vs PostgreSQL OLAP?" | ~9 |
| `/concilize` | Complex decisions with both factual and subjective dimensions | "Should we migrate our analytics pipeline from PostgreSQL to DuckDB?" | ~18 |

## Architecture

```
research-lead (orchestrator, never queries LLMs directly)
├── openai-researcher (shells out to OpenAI API)
├── perplexity-researcher (shells out to Sonar API)
├── claude-researcher (answers directly, has codebase access)
├── gemini-researcher (shells out to Vertex AI)
└── peer-reviewer (evaluates anonymized responses)
```

The `research-lead` coordinates but never queries models itself. It decomposes questions, selects which models to consult based on task type, collects responses, and hands off to the peer-reviewer for evaluation.

The outer researcher agents (openai, perplexity, gemini) are thin wrappers that shell out to `python -m research query <provider>` and return the result. The research-lead, claude-researcher, and peer-reviewer do substantive reasoning. All agents inherit their model from `~/.claude/settings.json`.

## Setup

See `SETUP.md` for detailed provider configuration, agent symlink verification, per-provider verify commands, and troubleshooting.

## Usage

```bash
# Within Claude Code — the recommended way
/research          # LLM Council: 4 models, peer review, synthesis
/concilize         # Full Concilium: Council + Socratic debate + red-team
/socratize         # Socratic debate only (Claude personalities, no external models)

# CLI mode (monolithic, runs all 3 stages in one process)
cd ~/.claude/skills/research
python -m research research "DuckDB vs PostgreSQL for analytics"
python -m research compare LanceDB Pinecone Weaviate

# Single provider query (used internally by agent team mode)
python -m research query perplexity "Latest WASM runtime benchmarks"
```

## Dependencies

See `SETUP.md` for installation and verification steps.
