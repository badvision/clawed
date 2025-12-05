# CLAWED Architecture

## Overview

CLAWED implements a **systematic multi-agent orchestration architecture** where specialized agents coordinate through enforced handoffs, quality gates, and workspace management to deliver production-quality software.

This architecture emerged from production use, solving real coordination challenges rather than theoretical abstractions.

## Core Architectural Principles

### 1. Agent Specialization with Role Enforcement

**Principle:** Each agent has a narrow expertise domain and cannot exceed it.

**Implementation:**
- Agents have explicit **autonomous decision boundaries** - what they can decide alone
- Agents have explicit **mandatory escalation criteria** - what requires orchestrator/human input
- Orchestrator enforces boundaries by rejecting out-of-scope work

**Why It Matters:**
- Prevents scope creep (engineer trying to redesign architecture)
- Ensures appropriate expertise applied to each problem
- Creates clear escalation points for human decisions

**Example:**
```yaml
# TDD Software Engineer boundaries
CAN decide autonomously:
  - Implementation approach within task scope
  - Code structure following project patterns
  - Test strategy and test case selection
  - Bug fixes not affecting external interfaces

MUST escalate:
  - Architectural changes not in scope
  - External dependencies unavailable or broken
  - Security vulnerabilities needing assessment
  - Performance issues beyond task scope
```

### 2. Documentation Tier Classification

**Principle:** All documentation is either temporary (working notes) or permanent (system knowledge).

**Three-Tier System:**

**Tier 1: Issue Tracker (GitHub/Jira)**
- Purpose: Communication and coordination during active work
- Content: Progress updates, decisions made, context for current issue
- Lifecycle: Permanent record, searchable archive
- Responsibility: All agents contribute during their phases

**Tier 2: Ephemeral Workspace**
- Purpose: Working notes, scratch analysis, iteration artifacts
- Content: STOP protocol analysis, temporary findings, agent handoff notes
- Lifecycle: Current iteration only, naturally cleaned by OS
- Responsibility: Agents create as needed, don't commit to git

**Tier 3: Repository Documentation**
- Purpose: Permanent system knowledge for future developers
- Content: Architecture, patterns, requirements, decisions
- Lifecycle: Long-lived, maintained with code
- Responsibility: Architects and analysts maintain

**Critical Rule:** "Would a developer care about this 6 months from now?"
- Yes → Tier 3
- No → Tier 1 or 2

**Workspace Structure:**
```
/tmp/claude/{project-id}/iteration-{N}/
  ├── agent-notes/           # Agent working notes
  ├── stop-analysis/         # STOP protocol findings
  ├── test-results/          # Validation artifacts
  └── IMPORTANT-{topic}.md   # Escalation-worthy findings
```

**Why This Pattern:**
- Prevents documentation bloat in repository
- Natural cleanup (OS handles /tmp/)
- Clear iteration boundaries
- Forces intentional elevation to permanent docs

### 3. Quality Gates and Systematic Validation

**Principle:** Work cannot proceed to next phase until current phase meets objective criteria.

**Quality Gate Structure:**

Each agent phase has three types of gates:

**Completion Gates** (objective criteria):
```yaml
Technical Analyst:
  - All requirements have acceptance criteria
  - Dependencies identified and documented
  - Risk assessment completed
  - Next phase readiness confirmed

Software Architect:
  - STOP protocol completed (Search, Think, Outline, Prove)
  - All integration points specified
  - Implementation sequence defined
  - Design validated against requirements

TDD Engineer:
  - All tests passing with meaningful validation
  - Code coverage meets project standards
  - No introduction of technical debt
  - Implementation matches requirements exactly

QA Validator:
  - All acceptance criteria demonstrably met
  - Test suites passing (unit, integration, E2E)
  - No regressions in existing functionality
  - Documentation updated appropriately
```

**Autonomous Decision Boundaries:**
- Clear criteria for what agent can decide alone
- Reduces unnecessary escalation
- Speeds autonomous phases

**Mandatory Escalation Triggers:**
- Objective criteria for when human input required
- Prevents agents "forging ahead" inappropriately
- Ensures human-in-the-loop at decision points

**Why It Matters:**
- Catches common oversights (test coverage, scope creep)
- Creates checkpoints for validation
- Prevents downstream problems from upstream issues
- Objective criteria reduce ambiguity

### 4. STOP Protocol for Pattern Reuse

**Principle:** Before implementing custom solutions, prove existing approaches insufficient.

**STOP = Search, Think, Outline, Prove**

**Search:**
- Existing solutions in codebase
- Standard libraries and frameworks
- Established patterns in documentation

**Think:**
- Why existing solutions insufficient
- What constraints prevent reuse
- Technical gaps requiring custom code

**Outline:**
- How custom solution integrates with existing patterns
- Configuration consistency (logging, metrics, etc.)
- Adherence to established conventions

**Prove:**
- Business justification for custom implementation
- Simplicity validation (simplest approach chosen)
- Supporting evidence for decisions

**Enforcement:**
- Architects must document STOP analysis in workspace
- Analysis reviewed before approving implementation
- Prevents "reinventing the wheel"

**Real Example from Beta:**
Navigation bug caused by using database IDs instead of existing "identifier/serialNumber" pattern. STOP protocol would have caught this by finding existing navigation patterns first.

### 5. Orchestrator-Driven Coordination

**Principle:** Human focuses on decisions, orchestrator handles coordination.

**Orchestrator Responsibilities:**

**Phase Management:**
- Sequence agents in correct order
- Validate quality gates before phase transitions
- Manage parallel vs. sequential work
- Handle phase-specific context handoffs

**Exception Handling:**
- Receive structured exception reports from agents
- Apply recovery strategy decision matrix
- Escalate to humans with prepared options
- Track resolution and update workflow

**Artifact Tracking:**
- Monitor tier-2 artifact creation
- Enforce documentation classification
- Coordinate cleanup before completion
- Validate archival completeness

**Quality Enforcement:**
- Verify autonomous decision boundaries respected
- Catch scope creep and role violations
- Ensure STOP protocol compliance
- Validate test coverage and quality metrics

**Human Escalation:**
- Business decisions affecting scope/priority
- Technical decisions requiring senior expertise
- Resource constraints or dependency blockers
- Compliance or security considerations

**Why This Pattern:**
- Humans freed from coordination overhead
- Systematic enforcement of standards
- Consistent handling of exceptions
- Clear escalation with prepared options

## Agent Coordination Patterns

### Sequential Phase Workflow

Standard issue workflow:

```mermaid
Product Owner (Task Planner)
    ↓ (requirements validation)
Technical Analyst
    ↓ (requirements analysis)
Software Architect
    ↓ (STOP protocol + design)
TDD Software Engineer
    ↓ (implementation + tests)
QA Test Validator
    ↓ (comprehensive validation)
Product Owner (Validator)
    ↓ (final sign-off)
Completion
```

**Key Coordination Points:**

**Task Planner → Technical Analyst:**
- Handoff: Initial requirements, acceptance criteria
- Validation: Requirements completeness check
- Gate: All requirements reviewable, gap analysis complete

**Technical Analyst → Software Architect:**
- Handoff: Complete requirements, dependency map, risk assessment
- Validation: Architecture review needed or proceed to implementation?
- Gate: Sufficient detail for design phase

**Software Architect → TDD Engineer:**
- Handoff: Technical design, integration specifications, implementation sequence
- Validation: Design completeness, STOP protocol documented
- Gate: Design approved, ready for implementation

**TDD Engineer → QA Validator:**
- Handoff: Implementation, test suite, coverage metrics
- Validation: All tests passing, quality standards met
- Gate: Code ready for comprehensive validation

**QA Validator → Product Owner:**
- Handoff: Validation results, quality metrics, integration test results
- Validation: All acceptance criteria met, no regressions
- Gate: Ready for production deployment decision

### Parallel Task Management

When issue has independent components:

```yaml
orchestrator_identifies:
  - task_a: Can proceed independently
  - task_b: Can proceed independently
  - task_c: Depends on task_a completion

execution_strategy:
  phase_1:
    parallel:
      - delegate task_a to engineer_instance_1
      - delegate task_b to engineer_instance_2
  phase_2:
    sequential:
      - await task_a completion
      - delegate task_c to engineer_instance_3
  phase_3:
    integration:
      - qa_validator tests all components together
```

### Remediation Workflow

When quality gate fails:

```yaml
failure_detected:
  agent: "QA Test Validator"
  issue: "Integration test failures in HiveNavigation"

orchestrator_analysis:
  severity: HIGH
  category: INTEGRATION
  affected_phase: Implementation

recovery_decision:
  strategy: TARGETED_REMEDIATION
  approach:
    - re_engage_engineer: true
    - scope: "Fix integration issues only"
    - prevent_scope_creep: "No refactoring, no feature additions"
    - validation: "QA validates fix before proceeding"

execution:
  - TDD Engineer receives: test failures, expected behavior, scope limits
  - TDD Engineer fixes: specific integration issues
  - QA Validator verifies: targeted fix, no new issues, original criteria met
  - Orchestrator proceeds: to next phase
```

## Workspace and Context Management

### Ephemeral Workspace Pattern

**Path Structure:**
```
/tmp/claude/{project-identifier}/iteration-{N}/
```

**Components:**

**Project Identifier:**
- Issue key (STORY-1) for tracked work
- Descriptive name (auth-spike) for ad-hoc exploration

**Iteration Number:**
- Sequential: 1, 2, 3... (never FINAL, LAST, COMPLETE)
- Each iteration = one attempt/revision
- Natural versioning through path structure

**Content Guidelines:**

**DO create:**
- Working notes for analysis
- STOP protocol documentation
- Test result artifacts
- Agent handoff context
- IMPORTANT-{topic}.md for escalation-worthy findings

**DON'T create:**
- Permanent documentation (use Tier 3)
- Meta-documentation about the work (use issue comments)
- Version numbers (iteration provides versioning)
- Completion markers (always assume more iterations)

**Lifecycle:**
- Created by orchestrator, communicated to agents
- Agents write as needed during their phase
- Orchestrator reviews for escalation-worthy content
- OS naturally cleans up over time
- Product owner elevates worthy artifacts to issue tracker

### Context Handoff Protocol

**Problem:** Agents lose context between phases.

**Solution:** Structured handoff via issue comments.

**Handoff Template:**
```markdown
## 🔄 Phase Complete: {Agent Name}

**Phase**: {Technical Analysis | Architecture Design | Implementation | Validation}
**Status**: {COMPLETE | COMPLETE_WITH_NOTES | BLOCKED}

### Deliverables
- {Specific artifact 1}
- {Specific artifact 2}

### Key Decisions Made
- **{Decision Category}**: {What was decided and why}

### Context for Next Phase
**What next agent needs to know:**
- {Critical context 1}
- {Critical context 2}

**Potential Challenges:**
- {Anticipated issue 1}
- {Suggested approach}

### Workspace Artifacts
- `/tmp/claude/{project}/iteration-{N}/{file}` - {Purpose}

**Next Phase**: {Agent Name} - {What they should focus on}
```

**Why This Works:**
- Explicit knowledge transfer
- Searchable issue history
- Clear phase boundaries
- Reduced context loss

## Exception Handling and Recovery

### Structured Exception Reporting

**Required Information:**
```yaml
exception_type: [BLOCKER | CLARIFICATION | ASSUMPTION]
severity: [CRITICAL | HIGH | MEDIUM | LOW]
category: [REQUIREMENTS | TECHNICAL | RESOURCE | BUSINESS | INTEGRATION]

description: "Clear description of what is blocking or unclear"

impact_assessment:
  timeline: "How this affects delivery schedule"
  scope: "Whether this affects planned deliverables"
  quality: "How this affects quality standards"
  resources: "Additional resources or skills needed"

resolution_options:
  - option: "Option 1 description"
    pros: ["Advantage 1", "Advantage 2"]
    cons: ["Risk 1", "Risk 2"]
    timeline: "Estimated resolution time"
    resources: ["Who needs to be involved"]

  - option: "Option 2 description"
    pros: ["Advantage 1"]
    cons: ["Risk 1"]
    timeline: "Estimated resolution time"
    resources: ["Who needs to be involved"]

recommended_action: [ESCALATE_IMMEDIATE | ESCALATE_STANDARD | PROCEED_WITH_ASSUMPTIONS]
```

### Recovery Strategy Matrix

**CRITICAL + REQUIREMENTS:**
- Pause all work immediately
- Escalate to product owner and stakeholders
- Document context and decision options
- Schedule alignment session within 24 hours

**CRITICAL + TECHNICAL:**
- Assess impact on other work streams
- Emergency architecture review
- Evaluate workarounds vs. proper fixes
- Set 48-hour maximum for technical decision

**HIGH + BUSINESS:**
- Continue non-blocked work
- Document business decision matrix with trade-offs
- Schedule business review within 3 days
- Prepare for multiple scenarios

**MEDIUM + INTEGRATION:**
- Document dependency status
- Identify workarounds or task resequencing
- Engage external teams proactively
- Continue with mockups/stubs while awaiting real integration

## Quality Metrics and Health Monitoring

### Documentation Health Score

**Components:**
- **Coverage**: Code with appropriate documentation references (target: >80%)
- **Accuracy**: Valid vs broken documentation links (target: 100%)
- **Freshness**: Documentation updated within review cycles (target: <1 week lag)
- **Compliance**: Documents following template standards (target: 100%)

**Composite target:** >85% health score

### Orchestration Effectiveness Metrics

**Phase Transition Success Rate:**
- Percentage of phases passing quality gates on first attempt
- Target: >90%

**Exception Handling Efficiency:**
- Time from exception report to resolution decision
- Target: <24 hours for CRITICAL, <72 hours for HIGH

**Agent Boundary Violations:**
- Count of agents attempting out-of-scope work
- Target: <5% of phases

**Documentation Tier Violations:**
- Count of tier-2 artifacts in tier-3 locations
- Target: 0 (caught before completion)

### Success Indicators

**Systematic Thinking Demonstrated:**
- STOP protocol compliance: 100% for architecture phase
- Quality gate pass rate: >90% on first attempt
- Exception reports: Structured and actionable
- Handoffs: Complete context transfer

**Human-in-the-Loop Optimization:**
- Escalation appropriateness: >95% (not too early, not too late)
- Decision preparation: Options presented with clear trade-offs
- Resolution efficiency: Decisions made quickly with good information

**Sustained Quality:**
- Test coverage: >80% with meaningful validation
- Code quality metrics: Meeting or exceeding standards
- Regression rate: <2% of deployments
- Documentation accuracy: >95% links valid

## Integration Points

### Issue Tracker Integration

**Required Capabilities:**
- Create and read issues
- Add and read comments
- Update issue status
- Create links between issues
- Search with query language

**Supported Platforms:**
- GitHub Issues
- Jira
- Generic REST API (with adapter)

### CI/CD Integration

**Quality Gate Enforcement:**
```yaml
documentation_validation:
  - Validate tier classification
  - Check cross-references
  - Verify documentation coverage
  - Generate health report

test_validation:
  - Run all test suites
  - Check coverage thresholds
  - Validate meaningful assertions
  - Detect test quality issues

code_quality:
  - Lint and format checks
  - Static analysis
  - Complexity metrics
  - Security scanning
```

### Development Environment Integration

**Claude Code CLI:**
- Slash commands invoke orchestration
- Agent definitions in `.claude/agents/`
- Quality gates in `.claude/templates/`
- Orchestration logic in `.claude/commands/`

**Cursor IDE:**
- Rules enforce workflow during development
- Templates guide agent interactions
- Validation runs on git hooks

## Future Architecture Considerations

### Multi-Project Orchestration
- Share agent definitions across projects
- Project-specific quality gate customization
- Cross-project pattern library

### Learning and Adaptation
- Pattern success/failure tracking
- Quality gate threshold optimization
- Exception recovery strategy refinement

### Advanced Coordination
- Parallel multi-issue orchestration
- Cross-team dependency management
- Resource allocation optimization

---

**This architecture emerged from production use, solving real coordination challenges. Every pattern addresses a discovered failure mode.**
