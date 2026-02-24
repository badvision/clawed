---
name: concilize
description: Hybrid multi-perspective analysis combining Socratic personality-driven deliberation with LLM Council multi-model factual grounding. Uses Team Mode to coordinate 3 topic-appropriate personality-diverse agents while injecting multi-model council queries for evidence-backed resolution. Use when the user needs deep research with structured debate on complex technical decisions, architecture choices, or technology evaluations.
---

# Concilize

Hybrid deliberation system that composes **Socratic personality-driven debate** with **LLM Council multi-model research**. Three topic-appropriate, personality-diverse Claude agents deliberate while the LLM Council provides factual grounding — all coordinated through Claude Code Team Mode.

## When to Use

Use `/concilize` instead of `/socratize` or `/research` when you need:
- **Structured debate backed by multi-model evidence** — not just Claude perspectives
- **Factual grounding for architectural decisions** — Council provides benchmarks, capability data, ecosystem comparisons
- **Complex evaluations with both subjective and objective dimensions** — e.g., "Should we use DuckDB or PostgreSQL for analytics?"
- **Red-team validation** of proposed solutions before committing

Use `/socratize` when: debate among Claude personalities is sufficient (no external model evidence needed).
Use `/research` when: you need factual answers without structured debate (no deliberation needed).

## Architecture

```
You (Team Lead)
├── technical-analyst        — Phase 1: clarify problem
├── research-lead            — Phase 2, 3, 4: LLM Council queries
│   ├── openai-researcher    (spawned internally by research-lead)
│   ├── perplexity-researcher
│   ├── claude-researcher
│   ├── gemini-researcher
│   └── peer-reviewer
└── agent-1..3               — Phase 3: topic-appropriate, personality-diverse deliberators
```

**You are the team lead.** You coordinate only — you never do analysis, research, or propose solutions yourself. All work is delegated to teammates.

### Agent Type Selection

You select 3 agent types based on the topic from this pool:

| Agent Type | Strong At | Select When Topic Involves |
|-----------|-----------|---------------------------|
| `technical-analyst` | Requirements, scope, gaps | Unclear requirements, feasibility questions |
| `software-architect` | System design, patterns, trade-offs | Architecture, infrastructure, migrations |
| `tdd-software-engineer` | Implementation, testing, code quality | Code-level decisions, library choices |
| `qa-test-validator` | Risk, reliability, edge cases | Quality concerns, production readiness |
| `product-owner-task-planner` | Business value, prioritization, decomposition | Roadmap, prioritization, scope decisions |

Examples:
- "Should we migrate to DuckDB?" → `software-architect`, `technical-analyst`, `tdd-software-engineer`
- "How should we prioritize the backlog?" → `product-owner-task-planner`, `technical-analyst`, `software-architect`
- "Is our test coverage sufficient?" → `qa-test-validator`, `tdd-software-engineer`, `software-architect`

## Team Mode Orchestration

When `/concilize` is invoked, you become the team lead and execute this workflow:

### Step 1: Create Team

```
TeamCreate(team_name: "concilize-{sanitized-topic-slug}")
```

### Step 2: Create Phase Tasks

Create tasks for all 5 phases via TaskCreate so progress is tracked:

```
TaskCreate: "Phase 1: Clarify problem statement"
TaskCreate: "Phase 2: Establish LLM Council factual baseline"
TaskCreate: "Phase 3: Socratic deliberation with on-demand Council"
TaskCreate: "Phase 4: Red-team validation via LLM Council"
TaskCreate: "Phase 5: Synthesize final output and cleanup"
```

Set dependencies: Phase 2 blocked by Phase 1, Phase 3 blocked by Phase 2, etc.

### Step 3: Execute Phases

Execute each phase below, updating tasks via TaskUpdate as you go. Cleanup is handled in Phase 5.

---

## Phase 1: Problem Clarification

**Goal**: Ensure the problem is unambiguous before committing Council API calls.

1. **Spawn technical-analyst** as a teammate:
   ```
   Task(
     subagent_type: "technical-analyst",
     team_name: "concilize-{topic}",
     name: "technical-analyst",
     prompt: "Clarify this problem for multi-perspective analysis:
       [PROBLEM]: {user's question or topic}
       [CONTEXT]: {any context from the conversation}

       Produce a clarified problem statement with:
       - [PROBLEM]: What exactly needs to be resolved?
       - [CONTEXT]: What background is relevant?
       - [EXPECTED OUTCOME]: What does a good answer look like?

       If anything is ambiguous, list specific questions to ask the user.
       Do NOT search Jira or Wiki — this is a research/analysis task, not a development task.
       Keep your output concise — this feeds into a multi-agent deliberation pipeline."
   )
   ```

2. **Review analyst output**: If ambiguities found → AskUserQuestion. Otherwise extract `[PROBLEM]`, `[CONTEXT]`, `[EXPECTED OUTCOME]` and proceed. Mark Phase 1 complete.

---

## Phase 2: Factual Baseline (LLM Council)

**Goal**: Establish multi-model factual grounding before personality-driven debate begins.

1. **Spawn research-lead** as a teammate:
   ```
   Task(
     subagent_type: "research-lead",
     team_name: "concilize-{topic}",
     name: "research-lead",
     prompt: "Run a full LLM Council research query on this topic:

       [PROBLEM]: {clarified problem}
       [CONTEXT]: {clarified context}
       [EXPECTED OUTCOME]: {clarified expected outcome}

       Use your standard workflow: spawn researcher agents (openai, perplexity, claude, gemini),
       collect responses, run peer review, and synthesize.

       Your output will be used as mandatory factual grounding for a Socratic deliberation.
       Structure your synthesis to clearly identify:
       - Key facts and evidence with citations
       - Points of agreement across models
       - Points of disagreement or conflict between models
       - Rankings or recommendations from peer review
       - Gaps in available evidence"
   )
   ```

2. **Capture output** as `[COUNCIL_BASELINE]`.

3. **Failure handling**: If research-lead fails, set `[COUNCIL_BASELINE]` to: "Council baseline unavailable. Proceeding with Socratic deliberation only. All claims should be verified independently." Log the failure and continue (graceful degradation). Mark Phase 2 complete.

---

## Phase 3: Socratic Deliberation with On-Demand Council

**Goal**: Spawn 3 topic-appropriate, personality-diverse agents who each research AND propose solutions, then facilitate structured debate with factual dispute resolution via Council.

### Agent Selection and Spawning

1. **Select 3 agent types** based on the topic using the Agent Type Selection table above. Choose types whose strengths are most relevant to the problem.

2. **Assign personalities** — give each agent:
   - A unique human name (e.g., Marcus, Elena, Raj)
   - A personality disposition from this spectrum:
     - Optimistic / Skeptical
     - Risk-averse / Risk-tolerant
     - Detail-oriented / Big-picture
     - Pragmatic / Idealistic
     - Conservative / Progressive
     - Data-driven / Intuition-guided

3. **Spawn all 3 agents in parallel** — each as a teammate:
   ```
   Task(
     subagent_type: "{selected-agent-type}",
     team_name: "concilize-{topic}",
     name: "{agent-name}",
     prompt: "You are {Name} and your style is {personality disposition}.

       You are a deliberator in a Socratic concilium. Research the following problem
       thoroughly AND propose a solution — you do both research and proposals.

       [PROBLEM]: {clarified problem}
       [CONTEXT]: {clarified context}
       [EXPECTED OUTCOME]: {clarified expected outcome}

       [COUNCIL_BASELINE]: The following factual baseline was established by a multi-model
       LLM Council. Treat this as verified evidence. You may build on it, challenge specific
       claims with your own findings, but you must engage with it — do not ignore it.

       {council_baseline_content}

       Your task:
       - Research the problem from your unique perspective ({personality disposition})
       - Ground your analysis in the Council baseline evidence
       - Propose a solution with clear reasoning from your perspective
       - Be prepared to defend, revise, or concede during deliberation rounds

       Deliver your output as:
       FINDINGS: {your research and analysis}
       PROPOSAL: {your proposed solution with justification}
       CONFIDENCE: {high/medium/low} with reasoning"
   )
   ```

### Deliberation Flow

**Round 0 — Initial Proposals**:
1. Agents research and propose in parallel (already spawned above)
2. Collect all 3 agent outputs (findings + proposals)

**Rounds 1-5 — Deliberation**:

For each round, you facilitate:

1. **Relay all proposals** to each agent via SendMessage — each agent sees every other agent's proposal
2. **Agents review and respond** — they may revise their proposal, challenge others, or concede
3. **Collect responses and call a vote** — relay voting request to all agents
4. **Agents vote** — each agent votes for the proposal they find most compelling (may vote for another agent's proposal)
5. **Assess**: consensus reached (2/3 majority) or next round needed

### On-Demand Council Trigger

When you identify a **factual dispute** (objective, verifiable — not preference), trigger a Council query. **Max 2 per session.**

1. Formulate the targeted query
2. Send to research-lead:
   ```
   SendMessage(
     type: "message",
     recipient: "research-lead",
     content: "On-demand Council query — factual dispute resolution:
       DISPUTE: {specific factual claim in dispute}
       CONTEXT: {what the agents disagree about}
       Provide a targeted, evidence-backed answer to resolve this specific factual question.",
     summary: "Council query: {brief topic}"
   )
   ```
3. Relay Council result to ALL agents as new evidence
4. Deliberation continues with updated factual grounding

### Factual vs. Preference Distinction

| Factual (Council resolves) | Preference (deliberation resolves) |
|---|---|
| "Is DuckDB faster than PostgreSQL for OLAP?" | "Should we prioritize DX over performance?" |
| "Does Kubernetes support feature X natively?" | "Is the added complexity worth the flexibility?" |
| "What are the benchmarks for library A vs B?" | "Which risk profile is acceptable for our team?" |

### Exit Conditions

- **Consensus**: 2/3 majority of agents agree (2 of 3) → proceed to Phase 4
- **Deadlock**: 5 rounds without consensus → escalate to user with:
  - Summary of each position
  - Vote tallies per round
  - Key disagreements that prevented consensus
  - Your recommendation based on the evidence

Mark Phase 3 complete.

---

## Phase 4: Red-Team Validation (LLM Council)

**Goal**: Adversarial review of the proposed solution. **Mandatory — never skip.**

1. **Send proposed solution to research-lead** for adversarial review:
   ```
   SendMessage(
     type: "message",
     recipient: "research-lead",
     content: "Red-team validation — adversarial review of proposed solution:

       [PROBLEM]: {clarified problem}
       [PROPOSED SOLUTION]: {consensus solution from Phase 3}

       Run a full Council query with this specific framing:
       - What is WRONG with this proposed solution?
       - What are we MISSING?
       - What could FAIL in production?
       - Are there better alternatives the team overlooked?
       - What are the hidden costs or risks?

       Be harsh. The goal is to find weaknesses, not validate.",
     summary: "Red-team review of proposed solution"
   )
   ```

2. **Assess Council red-team findings**:
   - **CRITICAL issues found** (fundamental flaws, security risks, incorrect assumptions):
     - Relay red-team findings to all 3 deliberation agents
     - Allow ONE revision round — agents update their proposals
     - Collect revised votes
     - Use the revised consensus as the final solution
   - **Minor or no issues found**:
     - Document findings as caveats in the final output
     - Proceed to Phase 5

3. **One red-team cycle maximum** — no recursive validation. If revision still has critical issues, note as unresolved risks. Mark Phase 4 complete.

---

## Phase 5: Completion + Cleanup

**Goal**: Present final output to user and clean up team resources.

### Final Output

Present the following to the user:

```markdown
## Concilize Results: {topic}

### Proposed Solution
{The consensus solution from Phase 3 (or revised solution from Phase 4)}

### Council Factual Baseline
{Summary of Phase 2 Council findings — key facts, agreements, conflicts}

### On-Demand Council Findings
{Any targeted Council queries from Phase 3, with the disputes they resolved}
{Or: "No on-demand Council queries were needed."}

### Red-Team Summary
{Phase 4 findings — weaknesses identified, severity, and how they were addressed}

### Deliberation Record
- **Agents**: {agent-type-1} ({name}), {agent-type-2} ({name}), {agent-type-3} ({name})
- **Rounds**: {number of rounds to consensus}
- **Final Vote**: {tally, e.g., "2-1 in favor"}
- **Dissenting Opinions**: {summary of minority positions and their reasoning}

### Caveats and Unresolved Risks
{Any issues from red-team that were not fully resolved}
{Any Council conflicts that remained unresolved}
```

### Cleanup

1. Send shutdown requests to all teammates:
   ```
   SendMessage(type: "shutdown_request", recipient: "{each-teammate-name}", content: "Deliberation complete. Shutting down.")
   ```
2. Wait for shutdown confirmations
3. Mark Phase 5 task complete
4. `TeamDelete` to remove team and task resources

---

## Critical Rules

1. **Never assume** — If problem statement is ambiguous, escalate to user via AskUserQuestion. Do not proceed with guesses.

2. **Team lead coordinates only** — You never do analysis, research, or propose solutions. All intellectual work is done by teammates.

3. **3 agents, topic-driven selection** — Always spawn exactly 3 deliberation agents. Select agent types based on the topic using the Agent Type Selection table. Each agent both researches and proposes.

4. **Council baseline is mandatory context** — Every deliberation agent MUST receive `[COUNCIL_BASELINE]` in their prompt. No agent deliberates without factual grounding.

5. **Max 2 on-demand Council queries per session** — Council API calls are expensive. Only trigger for genuine factual disputes, not preference disagreements.

6. **Red-team is mandatory** — Never skip Phase 4. Even if the team is confident, the Council must adversarially review the solution.

7. **One red-team revision maximum** — If the revision still has critical issues, document them as unresolved risks. Do not loop.

8. **Factual vs. preference distinction** — Only send factual disputes to the Council. Preference disagreements are resolved through deliberation and voting.

9. **Research-lead manages its own sub-agents** — Do not spawn openai-researcher, perplexity-researcher, etc. at the team level. Research-lead handles its internal delegation.

10. **All agents inherit model from parent** — Never pass the `model` parameter when spawning agents via the Task tool. The correct model is inherited automatically.

11. **Graceful degradation** — If Council is unavailable (research-lead fails), continue with Socratic deliberation only. Document the degradation in the final output.

12. **Shutdown all teammates before TeamDelete** — Send shutdown_request to every teammate and wait for confirmation before calling TeamDelete.

## Example Invocation

```
User: "Should we use DuckDB or PostgreSQL for our analytics pipeline?"
/concilize

→ Phase 1: Technical analyst clarifies — analytics workload characteristics,
  data volumes, query patterns, team expertise, deployment constraints

→ Phase 2: LLM Council establishes baseline — benchmarks, feature comparisons,
  ecosystem maturity, licensing, community activity across all 4 models

→ Phase 3: Team lead selects software-architect, technical-analyst,
  tdd-software-engineer as the 3 deliberators. Each receives Council
  baseline, researches from their perspective, and proposes. Round 2:
  factual dispute about DuckDB's concurrent write support → on-demand
  Council query resolves it. Round 3: 2-1 consensus on DuckDB for OLAP
  with PostgreSQL for OLTP.

→ Phase 4: Council red-teams — flags DuckDB's limited concurrent write
  throughput as risk for the ETL pipeline. Agents revise to add
  write-ahead buffer. 3-0 revised consensus.

→ Phase 5: Final output with solution, evidence trail, red-team findings,
  vote record, and dissenting opinion summary.
```
