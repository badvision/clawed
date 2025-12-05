---
description: Engage task orchestrator to pick up and complete the next issue
---

# Issue Implementation Workflow

Automatically pick up the next available issue and coordinate specialized agents to complete it systematically with full progress tracking and documentation.

**⚠️ CRITICAL INSTRUCTION**: When this command is invoked, you MUST IMMEDIATELY invoke the `/orchestrate` slash command to activate the task orchestration workflow. DO NOT attempt to evaluate complexity or decide if the work is trivial. DO NOT attempt to do any work yourself. Your ONLY job is to invoke `/orchestrate` right away.

## Immediate Action Required

Use the SlashCommand tool to invoke `/orchestrate` with the implementation workflow instructions:

```
SlashCommand(
  command: "/orchestrate implementation [pass through any user-provided arguments like issue key or filters]"
)
```

The `/orchestrate` command will then coordinate the complete issue implementation workflow through specialized agents following this systematic quality-gated workflow with 8 phases:

**Phase 1: Issue Selection and Branch Setup**
- Select highest priority issue and create/checkout feature branch
- Delegate to product-owner-task-planner

**Phase 2: Requirements Clarity Check**
- Review story for requirements completeness
- IF acceptance criteria clear and complete → Proceed to Phase 3 (Architecture Assessment)
- IF requirements ambiguous/incomplete → Delegate to technical-analyst first:
  * Analyze story requirements and clarify acceptance criteria
  * Complete architecture assessment (6 questions)
  * Escalate if business decisions needed
- Ambiguity indicators: vague criteria, missing integration details, unclear scope, undefined edge cases

**Phase 3: Architecture Assessment and Design** (MANDATORY checkpoint)
- technical-analyst completes architecture assessment (6 questions) if requirements needed clarification
- IF ANY architecture question = "yes" → Delegate to software-architect for technical design
- IF ALL architecture questions = "no" → Document skip justification, proceed to planning

**Phase 4: Planning**
- product-owner-task-planner breaks down work into tasks based on requirements and architecture assessment
- Use Task tool to delegate to product-owner-task-planner

**Phase 5: Development**
- tdd-software-engineer implements with TDD practices
- Use Task tool to delegate to tdd-software-engineer

**Phase 6: QA**
- qa-test-validator verifies tests and quality standards
- Use Task tool to delegate to qa-test-validator

**Phase 7: Remediation** (if needed)
- Fix any issues found by QA (loop back to development if needed)
- Use Task tool to delegate back to tdd-software-engineer

**Phase 8: Completion**
- product-owner-validator finalizes git workflow (commit, push, PR), links artifacts, updates issue status
- Use Task tool to delegate to product-owner-validator
- If architectural decisions made, delegate to software-architect for documentation

Each phase has quality gates that must be satisfied before proceeding. The orchestrator coordinates all agent work and ensures proper documentation in issue tracker throughout.

**DO NOT DO ANYTHING ELSE**. Just invoke `/orchestrate` and let it coordinate the specialized agents.

## Command Usage Examples

```bash
# Pick up next highest priority issue assigned to current user
/work-next

# Work on specific issue key
/work-next ISSUE-123

# Work on next issue from specific project
/work-next project:MYPROJECT

# Work on next issue with specific priority
/work-next priority:Major
```
