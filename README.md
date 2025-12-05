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
git clone https://github.com/yourusername/clawed.git
cd clawed

# Install dependencies
npm install

# Configure for your environment
cp .env.example .env
# Edit .env with your settings
```

### Minimal Configuration

CLAWED requires:
1. **Issue tracker integration** (GitHub Issues, Jira, etc.)
2. **Agent definitions** in `.claude/agents/`
3. **Orchestration command** in `.claude/commands/`
4. **Quality gate definitions** in `.claude/templates/`

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup instructions.

### First Orchestration

```bash
# Invoke the orchestrator (Claude Code CLI)
/orchestrate

# Or for specific issue
/orchestrate --issue STORY-1
```

The orchestrator will:
1. Read issue context and requirements
2. Delegate to specialized agents in sequence
3. Enforce quality gates at each phase
4. Coordinate handoffs between agents
5. Escalate to humans when needed

## Core Concepts

### Specialized Agents

CLAWED coordinates five specialized agents:

- **Product Owner (Task Planner)**: Breaks down work, validates requirements
- **Technical Analyst**: Requirements analysis, acceptance criteria definition
- **Software Architect**: Design decisions, STOP protocol enforcement
- **TDD Software Engineer**: Implementation with test-first approach
- **QA Test Validator**: Comprehensive validation and quality verification

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

CLAWED evolved from production use on a personal PWA project (bee-organized), handling:
- 15+ feature implementations through issue-driven workflow
- Complex multi-phase migrations with artifact tracking
- E2E test suite optimization and quality improvements
- Documentation reorganization at scale

Key achievements:
- **Zero documentation bloat** - Systematic tier-2 cleanup eliminated artifacts
- **Improved test quality** - Focus shifted from "no errors" to "validates requirements"
- **Pattern reuse** - STOP protocol prevented redundant implementations
- **Sustained velocity** - Quality gates maintained standards without slowing delivery

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
