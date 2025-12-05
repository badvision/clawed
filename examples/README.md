# CLAWED Examples

This directory contains working examples demonstrating CLAWED orchestration patterns.

## Available Examples

### 1. Simple Feature Orchestration
**File:** `simple-feature-flow.md`
**Demonstrates:** End-to-end orchestration for a straightforward feature implementation
**Complexity:** Basic
**Time:** ~30 minutes to complete

Key concepts:
- Issue-driven workflow
- Sequential agent coordination
- Quality gate enforcement
- Documentation tier classification

### 2. Multi-Agent Coordination
**File:** `multi-agent-coordination.md`
**Demonstrates:** Parallel task execution with dependency management
**Complexity:** Intermediate
**Time:** ~2 hours to complete

Key concepts:
- Task decomposition
- Parallel vs. sequential execution
- Dependency coordination
- Integration validation

### 3. STOP Protocol Application
**File:** `stop-protocol-example.md`
**Demonstrates:** Pattern reuse before custom implementation
**Complexity:** Intermediate
**Time:** ~45 minutes to complete

Key concepts:
- Search for existing solutions
- Think about necessity
- Outline integration approach
- Prove business justification

### 4. Quality Gate Enforcement
**File:** `quality-gate-enforcement.md`
**Demonstrates:** How quality gates catch common oversights
**Complexity:** Basic
**Time:** ~20 minutes to complete

Key concepts:
- Objective completion criteria
- Automated validation
- Failure detection and remediation
- Escalation handling

### 5. Documentation Tier Classification
**File:** `tier-classification-example.md`
**Demonstrates:** Proper classification of temporary vs. permanent documentation
**Complexity:** Basic
**Time:** ~15 minutes to complete

Key concepts:
- Three-tier system
- Immediate artifact tagging
- Ephemeral workspace usage
- Cleanup authorization

## Running Examples

Each example includes:

1. **Scenario description** - The problem to solve
2. **Agent interactions** - How agents coordinate
3. **Quality gates** - What gets validated
4. **Outcomes** - Expected results and artifacts

### Prerequisites

- CLAWED installed and configured
- Issue tracker integration active
- Agent definitions in place
- Quality gate templates configured

### Usage Pattern

```bash
# 1. Read the example markdown file
cat examples/simple-feature-flow.md

# 2. Create test issue with example scenario
gh issue create --title "Example: User Profile Avatar" --body "$(cat examples/simple-feature-flow.md)"

# 3. Run orchestration
/orchestrate --issue STORY-1

# 4. Observe agent coordination and quality gates
# Watch issue comments for agent progress

# 5. Review outcomes
# Check workspace artifacts and documentation
```

## Learning Path

**For beginners:**
1. Start with `simple-feature-flow.md`
2. Understand sequential coordination
3. Learn quality gate enforcement

**For intermediate users:**
4. Try `multi-agent-coordination.md`
5. Practice parallel task management
6. Master dependency handling

**For advanced usage:**
7. Study `stop-protocol-example.md`
8. Implement custom quality gates
9. Optimize orchestration patterns

## Contributing Examples

Have a useful orchestration pattern? Contribute an example!

**Requirements:**
- Real scenario from production or realistic use case
- Clear demonstration of CLAWED concepts
- Step-by-step explanation
- Expected outcomes documented

See [CONTRIBUTING.md](../CONTRIBUTING.md) for submission guidelines.
