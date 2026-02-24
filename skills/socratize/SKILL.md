---
name: socratize
description: Perform multi-perspective analysis and deep-research of a problem to arrive at a well-considered proposed solution
---

# Socratize

**⚠️ CRITICAL INSTRUCTION**: When this command is invoked, you MUST IMMEDIATELY invoke the `/orchestrate` slash command. DO NOT attempt to do any work yourself. Your ONLY job is to invoke `/orchestrate` right away.

## Immediate Action Required

Use the Skill tool to invoke `/orchestrate`:

```
Skill(
  skill: "orchestrate"
)
```

The `/orchestrate` command will coordinate the Socratic dialogue process described below.

## Overview

The `/socratize` command orchestrates a Socratic dialogue process with multiple analyst and architect agents, each with unique personalities and perspectives, to thoroughly analyze complex software problems and build consensus on solutions.

**Architecture**: The orchestrator spawns a product owner who facilitates the dialogue. The product owner CANNOT directly spawn or manage analyst/architect agents - it must request the orchestrator to perform these actions and relay messages between agents.

## Core Responsibilities

**CRITICAL: As the orchestrator, you are responsible for:**
- **Agent lifecycle management**: Only you can spawn analyst and architect agents using the Task tool
- **Message relay**: Pass information between product owner and analysts/architects
- **Coordination**: Execute the product owner's requests for agent spawning and communication
- **DO NOT** read files, grep, or analyze problems yourself - that's for the agents
- Let the product owner determine when the process is complete

**CRITICAL: The product owner CANNOT:**
- Use the Task tool to spawn agents directly
- Communicate with analysts/architects directly
- Must request all agent operations through you (the orchestrator)

## Process Workflow

### Phase 1: Problem Clarification

**Orchestrator spawns** a product owner who then **requests** the orchestrator to deploy a technical analyst to ensure clarity on:
- **[PROBLEM]**: What needs to be solved?
- **[CONTEXT]**: What background information is relevant?
- **[EXPECTED OUTCOME]**: What does success look like?

**Message flow**: Orchestrator → Product Owner → (requests analyst spawn) → Orchestrator spawns analyst → Analyst works → Orchestrator relays results to Product Owner

If any element is unclear or ambiguous, **ESCALATE TO USER IMMEDIATELY**. Do not assume anything.

### Phase 2: Determine Agent Counts

**Product owner analyzes** the problem scope and **requests** the orchestrator to spawn **[NUM_ANALYSTS]** and **[NUM_ARCHITECTS]** (range: 3-10 each):

**Small scope (3-3):**
- Simple feature additions
- Local code changes
- Single-module modifications
- Needs: Local source analysis, git history, maybe wiki docs

**Medium scope (5-5):**
- Multi-module features
- Cross-cutting concerns
- Integration changes
- Needs: Multiple codebases, API contracts, deployment considerations

**Large scope (10-10):**
- Application-wide changes
- Architecture overhauls
- System-wide refactoring
- Needs: Comprehensive codebase understanding, extensive documentation review, multiple integration points

### Phase 3: Deploy Agent Flock

**Product owner requests** and **orchestrator spawns** **[NUM_ANALYSTS]** analysts and **[NUM_ARCHITECTS]** architects, each with:
- **Unique name** (e.g., "Marcus", "Elena", "Raj")
- **Personality disposition** (ranging from optimistic to skeptical, plus other dimensions like risk-averse/risk-tolerant, detail-oriented/big-picture, pragmatic/idealistic)

**Message flow**: Product Owner designs agent specs → Orchestrator spawns agents → Orchestrator relays outputs back to Product Owner

**Agent instruction format:**
```
You are [NAME] and your style is [PERSONALITY DISPOSITION].

[PROBLEM]: <problem statement>
[CONTEXT]: <context information>
[EXPECTED OUTCOME]: <expected outcome>

For analyst agents, include:
- Use the issue-tracker integration to query and read issues
- Use the documentation integration to access wiki documentation
- Leverage other relevant skills as needed for your research

<agent-specific instructions>
```

**Analyst agent tasks:**
- Collect information from wiki, Jira, PRs, documentation
- **Use issue-tracker integration** for querying issues and reading issue details
- **Use documentation integration** for accessing wiki documentation and proposals
- Provide annotated research with light analysis
- Focus on understanding [PROBLEM] thoroughly
- Report if insufficient information found (escalate to user)

**Architect agent tasks:**
- Review analyst findings
- Synthesize solutions for [EXPECTED OUTCOME]
- Ask analysts for additional data if needed
- Propose and critique peer proposals
- Vote on solutions

### Phase 4: Socratic Dialogue (Facilitated by Product Owner via Orchestrator)

The product owner facilitates dialogue **through the orchestrator**:

1. **Initial Information Gathering**: Product owner requests orchestrator spawn analysts in parallel
2. **Synthesis**: Product owner requests orchestrator relay analyst findings to architects
3. **Clarification Round**: Product owner requests orchestrator relay architect questions to analysts (if ambiguous, escalate to user)
4. **Proposal Phase**: Product owner requests orchestrator collect architect proposals
5. **Deliberation Rounds**: Up to 5 rounds of peer review and voting (orchestrator relays messages)

**Between rounds:**
- Product owner organizes architect feedback
- **Orchestrator relays** feedback and voting requests to architects
- **Orchestrator relays** architect votes back to product owner
- Continue until 2/3 majority agreement on one solution

**Message flow example**:
```
Product Owner → Orchestrator: "Spawn 5 analysts with these specs..."
Orchestrator → Spawns analysts → Relays results to Product Owner
Product Owner → Orchestrator: "Share analyst findings with architects..."
Orchestrator → Relays to architects → Collects responses → Returns to Product Owner
```

**Escalation rules:**
- If analysts report insufficient information → product owner escalates to user for more [CONTEXT]
- If architects cannot reach 2/3 consensus after 5 rounds → product owner escalates to user with summary of disagreements

### Phase 5: Completion

Process ends when product owner declares consensus reached or escalates deadlock to user.

## Example Usage

**Small feature example:**
```
User: "We need to add rate limiting to the API endpoints"

Orchestrator workflow:
1. Spawn product-owner-task-planner
2. Product owner requests: "Spawn technical-analyst to clarify problem"
3. Orchestrator spawns technical-analyst → relays results to product owner
4. Product owner analyzes scope: "Spawn 5 analysts and 5 architects with these specs..."
5. Orchestrator spawns agents:
   - Marcus (optimistic): Use issue-tracker integration to find related issues
   - Elena (skeptical): Use documentation integration to review existing rate-limit docs
   - Raj (detail-oriented): Review codebase for current implementations
   - Sofia (pragmatic): Check PR history for similar work
   - Chen (risk-averse): Analyze potential failure modes
   + 5 architects (same personality range)
6. Product owner coordinates dialogue through orchestrator message relay
7. Orchestrator relays messages between product owner and agents until 2/3 consensus
```

**Large architectural change example:**
```
User: "We need to migrate from monolith to microservices"

Orchestrator workflow:
1. Spawn product-owner-task-planner
2. Product owner requests: "Spawn technical-analyst to clarify problem"
3. Orchestrator spawns technical-analyst → relays results to product owner
4. Product owner analyzes scope: "Spawn 10 analysts and 10 architects..."
5. Orchestrator spawns 10 analysts, product owner specifies tasks:
   - Use issue-tracker integration to search for related epics and tech debt issues
   - Use documentation integration to review architecture documentation
   - Analyze codebase structure and dependencies
   - Review deployment and infrastructure docs
6. Orchestrator spawns 10 architects with diverse personalities
7. Product owner coordinates up to 5 deliberation rounds via orchestrator relay
8. If no consensus, product owner escalates disagreements to user
```

## Agent Personality Examples

**Optimistic**: "This approach has great potential. We can build on our existing infrastructure..."
**Skeptical**: "I see several risks with this approach. What about edge cases like..."
**Risk-averse**: "We should prioritize stability. Let's consider the safest path..."
**Risk-tolerant**: "This is an opportunity to modernize. We should embrace the newer approach..."
**Detail-oriented**: "Looking at line 47 of the auth module, I notice..."
**Big-picture**: "Stepping back, this aligns with our broader platform strategy..."
**Pragmatic**: "Given our timeline and resources, the most practical solution is..."
**Idealistic**: "If we do this right, we can set a new standard for..."

## Critical Rules

1. **Never assume** - If ambiguous, escalate to user
2. **Orchestrator does NOT do work** - Only spawns agents and relays messages
3. **Product owner determines completion** - Not the orchestrator
4. **Product owner CANNOT spawn agents** - Must request orchestrator to spawn/manage
5. **All agent communication flows through orchestrator** - Product owner → Orchestrator → Agents → Orchestrator → Product owner
6. **2/3 majority required** - If not reached in 5 rounds, escalate
7. **Early escalation on missing info** - Don't proceed with gaps
