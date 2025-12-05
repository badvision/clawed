---
description: Guided discovery workflow for planning and analysis without implementation
---

# Guided Discovery Workflow

Systematically analyze requirements, prepare technical designs, and create organized work items through an orchestrated interview and planning process. **NO CODE IMPLEMENTATION, TESTS, OR PULL REQUESTS** - strictly for planning, analysis, and communication.

**⚠️ CRITICAL INSTRUCTION**: When this command is invoked, you MUST IMMEDIATELY invoke the `/orchestrate` slash command to activate the discovery workflow. DO NOT attempt to do discovery work yourself. Your ONLY job is to invoke `/orchestrate` right away.

## Immediate Action Required

Use the SlashCommand tool to invoke `/orchestrate` with the discovery workflow instructions:

```
SlashCommand(
  command: "/orchestrate discovery [pass through any user-provided arguments like topic, issue key, or mode preference]"
)
```

The `/orchestrate` command will then coordinate the complete discovery workflow for planning and analysis through specialized agents following this systematic workflow with 7 phases:

**Phase 1: Requirements Discovery and Architecture Assessment**
- technical-analyst conducts interview (interactive or document-guided mode) to clarify all requirements
- technical-analyst completes MANDATORY architecture assessment (6 questions)
- Use Task tool to delegate to technical-analyst
- Wait for analyst completion before proceeding

**Phase 2: Architecture Checkpoint Decision**
- Review analyst's architecture assessment results
- IF ANY architecture question = "yes" → Proceed to Phase 3 (Technical Design)
- IF ALL architecture questions = "no" → Skip to Phase 4 (Work Decomposition with documented justification)

**Phase 3: Technical Design** (if architecture assessment requires it)
- software-architect creates technical design based on assessment results
- Use Task tool to delegate to software-architect
- Wait for architect completion before proceeding

**Phase 4: Documentation** (if design warrants)
- software-architect uses project documentation tooling (if configured) to create documentation
- Documentation created before proceeding to decomposition

**Phase 5: Work Decomposition** (if actionable work items identified)
- product-owner-task-planner breaks down into epics and stories
- Use Task tool to delegate to product-owner-task-planner

**Phase 6: Issue Tracker Integration** (if work items created and user approves)
- product-owner-task-planner creates issue tracker tickets with full context
- Links stories to epics, documentation, and related issues

**Phase 7: Final Summary and Handoff**
- Compile complete discovery package for user
- Include: requirements summary, architecture assessment, technical design, documentation links, issue links, next steps

**CRITICAL CONSTRAINTS:**
- Sequential execution REQUIRED - each agent needs previous agent's output
- NEVER run dependent agents in parallel
- Architecture assessment (6 questions) is MANDATORY - cannot skip to decomposition without assessment
- NO CODE IMPLEMENTATION - discovery and planning only
- NO TESTS, NO PULL REQUESTS

Each phase has quality gates that must be satisfied before proceeding. The orchestrator coordinates all agent work sequentially and ensures proper handoffs between phases.

**DO NOT DO ANYTHING ELSE**. Just invoke `/orchestrate` and let it coordinate the specialized agents.

## Command Usage Examples

```bash
# Start guided discovery from scratch
/discover

# Start discovery for specific issue (provide context)
/discover ISSUE-123

# Start discovery with preferred mode
/discover interactive
/discover document-guided

# Start discovery for specific topic area
/discover "user authentication redesign"
```

## Integration with Work-Next

Discovery output feeds directly into implementation workflow:

```
/discover              →  Creates issue tracker stories with full context
                          Links to documentation
                              ↓
/work-next STORY-KEY  →  Implements per technical design
                          References documentation
```

This separation ensures requirements are thoroughly understood and properly planned before coding begins.
