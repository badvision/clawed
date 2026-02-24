# CLAWED: Claude Agent Workflow Execution Delegation

**Production-tested multi-agent orchestration framework for Claude-powered development workflows**

## What is CLAWED?

CLAWED (Claude Agent Workflow Execution Delegation) is a systematic framework for coordinating specialized Claude agents to deliver high-quality software through enforced quality gates, role separation, and systematic failure mode prevention.

Born from real-world production use, CLAWED solves the fundamental challenges of AI-assisted development:
- **Documentation bloat** from agents over-documenting temporary work
- **Scope creep** when agents exceed their expertise boundaries
- **Test coverage oversight** when agents focus on implementation over validation
- **Context handoff failures** between specialized work phases
- **Human escalation confusion** about when to stop and ask vs. forge ahead

## Why CLAWED?

Traditional AI coding assistants treat Claude as a single generalist. CLAWED recognizes that systematic thinking requires **role specialization** with **enforced coordination**.

### The CLAWED Difference

**Without CLAWED:**
- Single agent tries to do everything
- Documentation becomes cluttered with temporary artifacts
- Tests cover implementation details, not user requirements
- Agents reinvent solutions instead of using existing patterns
- Work requires constant human supervision

**With CLAWED:**
- Specialized agents with clear responsibilities
- Systematic separation of temporary vs. permanent documentation
- Quality gates enforce test coverage and requirement validation
- STOP protocol ensures existing patterns are reused
- Orchestrator handles coordination, humans handle decisions

## Key Benefits

### For Development Teams
- **Systematic quality:** Quality gates catch common oversights before review
- **Clear ownership:** Each agent has defined responsibilities and boundaries
- **Reduced supervision:** Orchestrator enforces workflow, freeing humans for decisions
- **Knowledge preservation:** Proper documentation tier classification maintains clean docs

### For Anthropic and Frontier AI Research
CLAWED demonstrates **systematic thinking at scale** through:
- **Multi-agent coordination** with enforced role boundaries
- **Quality gate enforcement** catching failure modes automatically
- **Context management** across complex, long-running workflows
- **Human-in-the-loop escalation** at appropriate decision points

Production deployment shows Claude can:
- Self-coordinate across specialized roles
- Maintain quality standards without constant oversight
- Distinguish temporary from permanent artifacts
- Know when to escalate vs. proceed autonomously

## Quick Start

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/badvision/clawed.git
cd clawed

# Run the setup script to symlink agents, commands, and skills into ~/.claude
./setup.sh
```

### Minimal Configuration

CLAWED requires:
1. **Claude Code CLI** installed and configured
2. **Issue tracker integration** (GitHub Issues, Jira, etc.) — optional, degrades gracefully
3. API keys for any LLM Council researcher agents you want to use (see `skills/research/SETUP.md`)

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup instructions.

### Slash Commands

CLAWED provides five primary slash commands for workflow orchestration:

```bash
# Start discovery workflow (planning without implementation)
/discover

# Pick up and implement the next issue
/work-next

# Or work on specific issue
/work-next ISSUE-123

# Orchestrate any complex workflow
/orchestrate

# Search existing work before starting (prevents duplication)
/search-work "authentication"

# Purify a prompt before sending it to an ensemble (removes false premises and framing bias)
/plato "Why is microservices always better than monoliths?"
```

The orchestrator coordinates:
1. Issue context analysis and requirements validation
2. Delegation to specialized agents in proper sequence
3. Quality gate enforcement at each phase transition
4. Handoff coordination between agents
5. Human escalation when decisions needed

## Core Concepts

### Workflow Commands

CLAWED provides slash commands that invoke coordinated agent workflows:

- **`/discover`**: Guided discovery for planning and analysis without implementation
  - Requirements gathering with mandatory architecture assessment
  - Technical design documentation when needed
  - Work breakdown into properly-sized stories with acceptance criteria
  - Issue tracker integration for epic/story creation

- **`/work-next`**: Automated issue selection and implementation workflow
  - Query issue tracker for highest priority work
  - Requirements clarity check with escalation if needed
  - Architecture checkpoint (mandatory 6-question assessment)
  - Implementation coordination with parallel agent support
  - QA validation and final workflow completion

- **`/orchestrate`**: General-purpose workflow orchestration
  - Coordinates any complex multi-phase development work
  - Enforces quality gates at each phase transition
  - Manages agent handoffs and dependencies
  - Handles exception escalation and recovery

- **`/search-work`**: Cross-repository search before starting
  - Searches issue tracker, documentation, and git history
  - Prevents duplicate work and reinventing solutions
  - Discovers prior art and architectural decisions
  - Mandatory first step for technical-analyst agent

- **`/plato`**: Socratic prompt purification pipeline
  - Surfaces and removes false premises, leading framing, and presupposition traps
  - Reconstructs a clean, epistemically neutral version of the prompt
  - Computes framing sensitivity score and flags residual risks
  - Ideal for preparing prompts before ensemble or research workflows

### Specialized Agents

CLAWED coordinates specialized agents across two categories:

**Core Development Workflow (6 agents):**
- **Technical Analyst**: Requirements analysis with mandatory /search-work and 6-question architecture assessment
- **Software Architect**: Design decisions, STOP protocol enforcement, documentation integration
- **Product Owner (Task Planner)**: Dual-mode operation (discovery vs implementation), work breakdown with complexity-based coordination
- **TDD Software Engineer**: Test-first implementation, parallel work coordination when deployed as multiple agents
- **QA Test Validator**: Comprehensive validation, test coverage verification, project health assessment
- **Product Owner (Validator)**: Final validation, git workflow completion, PR creation, issue status updates

**LLM Council Research Team (6 agents):**
- **Research Lead**: Orchestrates multi-model research — decomposes queries, selects appropriate researcher agents, synthesizes findings
- **Claude Researcher**: Answers queries using Claude's own reasoning; strong at nuanced synthesis
- **OpenAI Researcher**: Queries OpenAI with chain-of-thought scaffolding and structured output
- **Gemini Researcher**: Queries Gemini via Vertex AI; strong at multimodal reasoning and long-context analysis
- **Perplexity Researcher**: Citation-backed, web-grounded research with source attribution
- **Peer Reviewer**: Evaluates anonymized model responses for accuracy, depth, and usefulness; avoids self-review bias

**Support Agent:**
- **Self-Review Checklist**: Quality checklist for agent self-assessment before completion

### Skills

CLAWED includes reusable skill packs that extend agent capabilities:

- **`socratize`** / **`brainstorm`**: Multi-perspective Socratic deliberation — coordinates personality-diverse agents to debate and resolve complex decisions
- **`concilize`**: Hybrid analysis combining Socratic deliberation with LLM Council multi-model grounding
- **`research`**: Full LLM Council pipeline — parallel queries to Claude, OpenAI, Gemini, and Perplexity with peer review synthesis

### Documentation Tiers

CLAWED enforces three documentation tiers:

- **Tier 1: Issue Tracker** (GitHub Issues, Jira, etc.) - Temporary work artifacts
- **Tier 2: Ephemeral Workspace** - Working notes for current iteration
- **Tier 3: Repository Docs** - Permanent system documentation

Agents must classify all documentation and clean up temporary artifacts.

### Quality Gates

Every phase has defined completion criteria:
- Requirements must be complete before design
- Design must pass STOP protocol before implementation
- Implementation must have passing tests before validation
- All tier-2 artifacts must be archived before completion

### Orchestration Enforcement

The orchestrator actively enforces workflow:
- Agents cannot skip phases
- Quality gates must pass before proceeding
- Role boundaries are enforced (no architecture changes by engineers)
- Documentation tier violations trigger cleanup

## Real-World Results

CLAWED evolved from 3+ months of production use in enterprise environments, handling:
- 15+ feature implementations through issue-driven workflow
- Complex multi-phase migrations with artifact tracking
- E2E test suite optimization and quality improvements
- Documentation reorganization at scale
- Parallel agent coordination for complex stories

Key achievements:
- **Zero documentation bloat** - Systematic tier-2 cleanup eliminated artifacts
- **Improved test quality** - Focus shifted from "no errors" to "validates requirements"
- **Pattern reuse** - STOP protocol and /search-work prevented redundant implementations
- **Sustained velocity** - Quality gates maintained standards without slowing delivery
- **Failure mode prevention** - Architecture assessment catches design needs, complexity-based coordination prevents over-decomposition

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Orchestration patterns and system design
- **[EVOLUTION.md](EVOLUTION.md)** - Journey from beta to production
- **[FAILURE_MODES.md](FAILURE_MODES.md)** - Systematic failure prevention (critical reading)
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Installation and configuration guide

## Examples

See [/examples](examples/) directory for:
- Simple orchestration flow
- Multi-agent coordination patterns
- Quality gate enforcement examples
- Documentation tier classification examples

## Contributing

CLAWED is production-tested but evolving. Contributions welcome in:
- Additional agent specializations
- Quality gate refinements
- Issue tracker integrations
- Documentation improvements

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

## Acknowledgments

CLAWED was developed through real-world use, discovering and solving actual coordination challenges. Special thanks to Anthropic for Claude's remarkable ability to maintain role boundaries and systematic thinking across complex workflows.

---

**Production-tested. Systematically coordinated. Ready for your development workflow.**
