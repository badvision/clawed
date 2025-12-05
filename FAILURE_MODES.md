# CLAWED Failure Modes and Prevention

## Overview

This document catalogs real failure modes discovered during CLAWED's evolution from beta to production, and the systematic solutions that prevent their recurrence.

**Every failure mode here is real.** Each came from actual development work, caused real problems, and taught specific lessons.

## Critical Failure Modes

### 1. Documentation Bloat

**Severity:** HIGH - Accumulates over time, eventually makes repository unmaintainable

#### The Failure

**What Happened:**
Architecture documentation directory accumulated 683 lines of temporary implementation artifacts:
- `documentation-migration-mapping.md` (171 lines) - temporary cross-reference tracking
- `documentation-reorganization-implementation.md` (512 lines) - implementation plan details

**Why It Happened:**
- Agents naturally create documents to communicate findings and decisions
- No clear rule about temporary vs. permanent documentation
- No enforcement of cleanup before issue completion
- Future value unclear at time of creation

**Real Impact:**
- Future developers would need to read 683 lines of irrelevant content
- Cross-references pointing to temporary artifacts would break
- Architecture docs mixed permanent patterns with transient implementation details
- Search results cluttered with temporary artifacts

**Example of Bloat:**
```markdown
# Documentation Migration Cross-Reference Mapping

*Created: 2025-09-26*
*Migration for: GitHub Issue #1 - Documentation Organization*

This document maps the cross-reference changes made during
the documentation reorganization...

## Migrated to GitHub Issues (Tier 2)

| Original File | New Location | GitHub Issue | Notes |
|---------------|--------------|--------------|-------|
| `box-position-fix.md` | GitHub Issue #7 | I-6 | Complete content migrated |
...
```

**Why This is Tier-2 Not Tier-3:**
- Created for specific issue (#1)
- Migration process is one-time, not recurring
- Details about "what moved where" irrelevant 6 months later
- Belongs in issue comments, not permanent architecture docs

#### The Solution

**Tier Classification System with Enforcement:**

**Tier 1: Issue Tracker (GitHub/Jira)**
- Purpose: Temporary work artifacts, coordination, searchable history
- Content: Progress updates, decisions made during work, STOP analysis
- Lifecycle: Permanent record in issue tracker, not in repository

**Tier 2: Ephemeral Workspace**
- Purpose: Working notes for current iteration
- Location: `/tmp/claude/{project}/iteration-{N}/`
- Content: Agent notes, scratch analysis, handoff context
- Lifecycle: Current iteration only, naturally cleaned by OS

**Tier 3: Repository Documentation**
- Purpose: Permanent system knowledge
- Location: `/docs/` in repository
- Content: Architecture, patterns, requirements, decisions
- Lifecycle: Maintained with code, long-lived

**The Question:** "Would a developer care about this 6 months from now?"
- Yes → Tier 3
- No → Tier 1 or 2

**Enforcement Mechanisms:**

**1. Immediate Artifact Tagging**
When agent creates any document:
```markdown
## 📋 Tier-2 Artifact Created

**File**: `/tmp/claude/gs-12345/iteration-1/stop-analysis.md`
**Purpose**: STOP protocol analysis for authentication approach
**Agent**: Software Architect
**Created**: 2025-09-15
**Action Required**: Archive to issue and remove before completion
```

**2. Product Owner Review**
Before issue completion:
- Review ALL issue comments for artifact references
- Verify classification of all created documents
- Ensure tier-2 artifacts archived to issue comments
- Authorize cleanup only after validation

**3. Automated Validation**
CI/CD pipeline checks:
- Documents in `/docs/` for tier-2 indicators (issue numbers, dates, "implementation")
- Commit messages for documentation additions
- Pull requests for tier classification justification

**Result:**
- Zero documentation bloat in repository
- Clear separation of temporary vs. permanent
- Natural cleanup through ephemeral workspace
- Searchable history preserved in issue tracker

### 2. Test Coverage Oversight

**Severity:** HIGH - Tests exist but don't validate actual requirements

#### The Failure

**What Happened:**
Issue #6 (Inspection History System) marked "complete" with tests passing, but feature didn't work for users.

**Test Coverage Metrics:**
- Unit tests: 73% coverage
- Integration tests: 42% coverage
- All tests: PASSING

**But in production:**
- Inspection history not displaying for existing hives
- Date formatting incorrect
- Navigation broken from history to detail view

**Why It Happened:**
- Tests focused on "does code execute without errors"
- Coverage measured lines executed, not requirements validated
- Test assertions checked implementation details, not user requirements
- No validation phase separate from implementation phase

**Real Test Example (The Problem):**
```javascript
describe('InspectionHistoryService', () => {
  it('should fetch inspection history', async () => {
    const result = await service.getHistory('hive-123');
    expect(result).toBeDefined();
    expect(Array.isArray(result)).toBe(true);
    // Test passes if array returned, regardless of correctness
  });
});
```

**What This Test Validates:**
- Method doesn't throw error
- Returns an array

**What This Test DOESN'T Validate:**
- Correct inspections returned for hive
- Historical order preserved
- All required fields present
- Date formatting meets requirements
- Navigation data included

#### The Solution

**Multi-Phase Validation with Requirement Focus:**

**Phase 1: Implementation (TDD Engineer)**
- Write tests that encode acceptance criteria
- Tests fail initially (Red)
- Implement until tests pass (Green)
- Refactor (Blue)

**Phase 2: QA Validation (QA Validator)**
- Separate agent validates against original requirements
- Not just "do tests pass" but "do requirements work"
- Integration testing with actual user workflows
- Edge case validation separate from implementation

**Quality Gate:**
```yaml
QA_validation_gate:
  cannot_proceed_until:
    - all_acceptance_criteria_demonstrably_met: true
    - integration_tests_validate_user_workflows: true
    - edge_cases_tested_with_real_data: true
    - no_regressions_in_existing_functionality: true
```

**Real Test Example (The Solution):**
```javascript
describe('Inspection History - User Requirements', () => {
  describe('Acceptance Criteria: Display inspection history for hive', () => {
    it('should show all inspections for selected hive in reverse chronological order', async () => {
      // Given: Hive with 3 inspections on different dates
      const hive = await createTestHive('test-hive-001');
      const inspection1 = await createInspection(hive, '2025-01-15');
      const inspection2 = await createInspection(hive, '2025-02-20');
      const inspection3 = await createInspection(hive, '2025-03-10');

      // When: User views inspection history
      const history = await service.getHistory(hive.identifier);

      // Then: All inspections shown, newest first
      expect(history).toHaveLength(3);
      expect(history[0].id).toBe(inspection3.id); // Newest first
      expect(history[1].id).toBe(inspection2.id);
      expect(history[2].id).toBe(inspection1.id); // Oldest last

      // And: Required fields present for navigation
      expect(history[0].hiveIdentifier).toBe(hive.identifier);
      expect(history[0].inspectionDate).toBe('2025-03-10');
      expect(history[0].navigationData).toBeDefined();
    });
  });
});
```

**What This Test Validates:**
- Actual requirement: "show all inspections"
- Actual requirement: "reverse chronological order"
- Actual requirement: "for selected hive"
- Fields needed for user workflow (navigation)

**Testing Philosophy Shift:**

**Before:**
- Question: "Does the code work?"
- Focus: Technical correctness
- Validation: No errors thrown

**After:**
- Question: "Does it meet the requirement?"
- Focus: User requirements
- Validation: Acceptance criteria demonstrable

**Result:**
- Bug escape rate dropped from 18% to <3%
- Test rework decreased (tests stay valid longer)
- Confidence in "passing tests" increased dramatically

### 3. Orchestration Drift ("Stick to the Script")

**Severity:** MEDIUM - Agents exceed boundaries, requiring human intervention

#### The Failure

**What Happened:**
TDD Engineer, while implementing navigation feature, decided existing architecture "wasn't optimal" and redesigned component hierarchy without architect involvement.

**Result:**
- Implementation took 4 days instead of planned 1 day
- Broke existing integrations
- Introduced technical debt (inconsistent with project patterns)
- Required architect to review and refactor
- Total cost: 6 days (4 implementation + 2 remediation) vs planned 1 day

**Why It Happened:**
- No clear boundary enforcement
- Agent felt "empowered" to make improvements
- Opportunistic refactoring seemed beneficial at the time
- No mechanism to catch out-of-scope work until completion

#### The Solution

**Explicit Decision Boundaries with Enforcement:**

**Each Agent Has:**

**Autonomous Decision Boundaries** - What they CAN decide alone:
```yaml
TDD_Engineer_can_decide:
  - Implementation approach within assigned task scope
  - Code structure following established project patterns
  - Test strategy and test case selection
  - Bug fixes not affecting external interfaces
  - Performance optimizations using standard techniques
  - Error handling following project conventions
```

**Mandatory Escalation Criteria** - What they MUST escalate:
```yaml
TDD_Engineer_must_escalate:
  - Architectural changes not in scope
  - Pattern deviations requiring new approaches
  - External API dependencies unavailable
  - Security vulnerabilities needing assessment
  - Performance issues beyond standard optimization
  - Breaking changes affecting existing functionality
```

**Orchestrator Enforcement:**

**Pre-Implementation Check:**
```yaml
orchestrator_validates:
  - task_scope_clear: "Engineer knows boundaries"
  - acceptance_criteria_defined: "Success criteria explicit"
  - patterns_identified: "Existing patterns documented"
  - escalation_criteria_understood: "Agent knows when to stop"
```

**During Implementation:**
```yaml
orchestrator_monitors:
  - files_changed: "Only expected files modified"
  - scope_boundaries: "No architectural changes attempted"
  - escalation_signals: "Agent reports blockers appropriately"
```

**Real Escalation Example:**
```markdown
## 🚨 Exception Report - TDD Software Engineer

**Exception Type**: DESIGN_ISSUE
**Severity**: HIGH
**Category**: ARCHITECTURE

### Issue Description
Implementation of navigation feature requires changes to component hierarchy
to maintain consistency with existing patterns. Current architecture has
HiveDetail as parent of InspectionHistory, but requirement needs reverse
relationship.

### Impact Assessment
- **Timeline Impact**: Cannot complete in allocated 1 day
- **Scope Impact**: Requires architectural decision outside task scope
- **Quality Impact**: Proceeding would create inconsistent patterns

### Resolution Options

**Option 1: Refactor component hierarchy**
- Pros: Clean architecture, follows new pattern
- Cons: Affects multiple components, requires architect review
- Timeline: 3-4 days total
- Resources: Software Architect, TDD Engineer

**Option 2: Adapter pattern for current architecture**
- Pros: Stays within scope, minimal changes
- Cons: Technical debt, pattern inconsistency
- Timeline: 1 day (on schedule)
- Resources: TDD Engineer only

### Recommended Action
ESCALATE_ARCHITECTURE_REVIEW

**Reasoning:** Option 2 can complete task but creates technical debt.
Option 1 is proper solution but requires architect involvement to ensure
consistency across system.

---
*Work paused pending architectural decision*
```

**Orchestrator Response:**
1. Acknowledges escalation
2. Engages Software Architect
3. Makes decision with proper expertise
4. Updates task scope if needed
5. Engineer resumes with clear direction

**Result:**
- Engineers work within scope
- Architectural decisions made by architects
- Escalations happen early (before wasted effort)
- Human decisions prepared with clear options

### 4. STOP Protocol Violations (Pattern Reinvention)

**Severity:** MEDIUM - Wasted effort implementing existing solutions

#### The Failure

**What Happened:**
Multiple navigation bugs caused by using database IDs instead of business identifiers (serial numbers).

**Pattern:**
- Existing codebase used `identifier` field for navigation
- New features repeatedly used `id` (database primary key)
- Users confused when URLs contained numeric IDs instead of readable serials
- Each new feature required bug fix to use correct pattern

**Why It Happened:**
- No systematic "search for existing patterns" step
- Engineers started implementing without researching codebase
- Faster to implement than research (in short term)
- Pattern documentation not comprehensive

**Real Example:**
```javascript
// NEW FEATURE (wrong pattern)
function navigateToHiveDetail(hive) {
  router.push(`/hive/${hive.id}`); // Using database ID
}

// EXISTING PATTERN (correct)
function navigateToHiveDetail(hive) {
  router.push(`/hive/${hive.identifier}`); // Using business identifier
}
```

**Impact:**
- 5 separate navigation bugs over 3 months
- Each requiring bug fix and test updates
- User confusion from inconsistent URLs
- Wasted ~2 days per bug (10 days total)

#### The Solution

**STOP Protocol Enforcement Before Implementation:**

**STOP = Search, Think, Outline, Prove**

**Architect Quality Gate:**
```yaml
cannot_approve_design_until:
  stop_protocol_completed: true
  stop_analysis_documented: true
  stop_findings_justify_approach: true
```

**Search:** Find existing solutions
```markdown
## Search Phase

**Existing Navigation Patterns:**
- HiveDetail: Uses `hive.identifier` in URL
- BoxManagement: Uses `box.serialNumber` in URL
- FrameDetail: Uses `frame.identifier` in URL

**Pattern Identified:** Business identifiers for navigation, not database IDs

**Libraries Available:**
- React Router v6 with useParams hook
- Custom `useBusinessIdentifier` hook for resolution
```

**Think:** Why existing insufficient
```markdown
## Think Phase

**Why New Implementation Needed:**
- Inspection history needs navigation to historical state
- Existing navigation assumes current state
- Need to pass inspection date with identifier

**Why Existing Pattern Sufficient:**
- Can extend URL pattern: `/hive/:identifier/inspection/:date`
- Business identifier still correct
- Just add date parameter to existing pattern

**Conclusion:** Existing pattern IS sufficient with minor extension
```

**Outline:** Integration approach
```markdown
## Outline Phase

**Integration with Existing Patterns:**
- Extend HiveDetail route: `/hive/:identifier/inspection/:date?`
- Use existing `useBusinessIdentifier` hook for hive resolution
- Add new `useInspectionDate` hook for date parameter
- Consistent with all other navigation patterns

**Configuration Consistency:**
- Router configuration in `src/routes/index.js`
- Pattern documented in `/docs/patterns/navigation.md`
```

**Prove:** Justify necessity
```markdown
## Prove Phase

**Business Justification:**
- User requirement: View historical inspection details
- Must maintain identifier pattern for consistency
- Extension is simplest approach meeting requirement

**Simplicity Validation:**
- Reuses 90% of existing navigation code
- No new libraries or dependencies
- Follows established project patterns

**Supporting Evidence:**
- All existing navigation uses business identifiers
- User feedback requests readable URLs
- Technical debt from database IDs in previous features
```

**Enforcement Mechanism:**

**1. Architect Must Document STOP:**
Workspace must contain `stop-analysis.md` with all four sections before design approved.

**2. Orchestrator Validates:**
- Search findings present and comprehensive
- Think analysis shows evaluation of existing
- Outline shows integration, not replacement
- Prove shows business justification

**3. Engineer Receives:**
- Design with STOP analysis attached
- Clear guidance on patterns to use
- Justification for custom code (if any)

**Result:**
- Navigation pattern used consistently
- No more "identifier vs ID" bugs
- Existing solutions reused appropriately
- Custom implementations justified

### 5. Context Loss Between Attempts

**Severity:** MEDIUM - Repeated mistakes, wasted learning

#### The Failure

**What Happened:**
Issue #6 (Inspection History) completed three separate times:
1. First attempt: Implemented but didn't meet requirements
2. Second attempt: Fixed critical issues but still not complete
3. Third attempt: Finally achieved actual success

**What Was Repeated:**
- Same requirements misunderstanding in attempts 1 and 2
- Same integration issues discovered twice
- Same edge cases missed in initial testing
- Learning from attempt 1 lost by attempt 2

**Why It Happened:**
- Agents read issue description, not issue history
- Prior attempt context lost in comment stream
- No systematic "read everything first" protocol
- Assumption that latest comment has full context

**Impact:**
- 12 days total vs. planned 4 days
- Frustration from repeating discoveries
- Quality perception damaged (multiple "completions")

#### The Solution

**Comprehensive Context Protocol Before Starting:**

**Mandatory Pre-Work Steps:**
```yaml
before_any_work_begins:
  step_1:
    action: "Read issue title and description"
    purpose: "Understand initial requirements"

  step_2:
    action: "Read ALL existing comments in chronological order"
    purpose: "Understand complete history and prior attempts"

  step_3:
    action: "Identify prior work and lessons learned"
    purpose: "Don't repeat mistakes or discoveries"

  step_4:
    action: "Document assumptions and open questions"
    purpose: "Clarify before proceeding"
```

**Orchestrator Enforcement:**
```yaml
orchestrator_validates:
  - agent_read_full_context: "Confirmed by agent report"
  - prior_attempts_acknowledged: "Agent references prior work"
  - lessons_learned_integrated: "Agent shows awareness of past issues"
  - new_questions_documented: "Agent asks about unclear aspects"
```

**Agent Context Report Template:**
```markdown
## 📖 Context Review Complete

**Issue**: STORY-1 - Inspection History System
**Review Date**: 2025-09-20
**Agent**: Technical Analyst

### Prior Attempts Reviewed
1. **Attempt 1 (2025-09-15)**: Implementation incomplete
   - **Lesson**: Didn't validate chronological ordering
   - **Integration issue**: Date formatting inconsistent
   - **Will avoid**: Implementing without date format specification

2. **Attempt 2 (2025-09-17)**: Critical issues fixed
   - **Lesson**: Edge case with zero inspections not tested
   - **Integration issue**: Navigation data missing
   - **Will avoid**: Proceeding without edge case test plan

### Open Questions for Clarification
1. Should empty history show message or empty list?
2. Date format: ISO or localized display?
3. Pagination: How many inspections per page?

### Context-Informed Approach
Based on prior attempts, will:
- Specify date formats explicitly in requirements
- Include edge cases in acceptance criteria
- Validate navigation data in test plan
- Confirm empty state handling upfront
```

**Result:**
- Issues completed in single attempt (>90%)
- Prior learning preserved and applied
- Reduced rework from 58% to 8%
- Faster to actual completion despite more thorough preparation

## Human Escalation Guidelines

### When to Escalate Immediately (STOP Work)

**Business Decisions:**
- Conflicting business priorities affecting task sequencing
- Scope changes that affect project commitments
- Resource constraints that affect feasibility
- External dependencies with undefined timelines

**Technical Decisions Requiring Senior Expertise:**
- New technology stack introduction
- Architecture changes affecting system fundamentals
- Security decisions affecting compliance
- Performance requirements needing infrastructure changes

**Blockers Preventing Progress:**
- External APIs unavailable or broken
- Test failures indicating fundamental design problems
- Requirements contradictions not resolvable at agent level

### When to Escalate with Continued Work (STANDARD)

**Clarifications Needed But Workarounds Possible:**
- Implementation complexity exceeding estimates (continue with simpler approach)
- Domain expertise gaps (continue with researched best practices)
- Testing environment issues (continue with unit tests, flag integration issues)

**Trade-offs Requiring Business Input:**
- Quality vs. timeline decisions
- Performance vs. maintainability trade-offs
- User experience alternatives needing product input

### When NOT to Escalate (Autonomous Decisions)

**Within Agent Expertise and Scope:**
- Implementation approaches following established patterns
- Code structure and organization decisions
- Test strategy and test case selection
- Standard optimizations and refactoring
- Bug fixes not affecting external interfaces
- Documentation improvements and clarifications

**Guideline:** If it's in your autonomous decision boundary, proceed. If it affects architecture, scope, or requires business judgment, escalate with options.

## Prevention Checklist

### Before Starting Any Issue

- [ ] Read issue title and description
- [ ] Read ALL existing comments
- [ ] Review any prior attempts and lessons learned
- [ ] Identify applicable existing patterns (STOP protocol)
- [ ] Confirm autonomous decision boundaries
- [ ] Document assumptions and open questions

### During Requirements Phase

- [ ] All requirements have acceptance criteria
- [ ] Success metrics defined and measurable
- [ ] Dependencies identified and documented
- [ ] Risk assessment completed
- [ ] Tier classification determined for any artifacts created

### During Design Phase

- [ ] STOP protocol completed and documented
- [ ] Existing patterns researched and evaluated
- [ ] Integration points specified
- [ ] Design validated against requirements
- [ ] Custom implementations justified

### During Implementation Phase

- [ ] Tests written before implementation (TDD)
- [ ] Tests validate requirements, not implementation
- [ ] Code follows established patterns
- [ ] No architectural changes outside scope
- [ ] All tier-2 artifacts tagged immediately

### During Validation Phase

- [ ] All acceptance criteria demonstrably met
- [ ] Tests focus on user requirements
- [ ] Edge cases covered with real data
- [ ] No regressions in existing functionality
- [ ] Integration validated with actual workflows

### Before Completion

- [ ] All tier-2 artifacts identified and archived
- [ ] Documentation classification validated
- [ ] Quality gates passed
- [ ] Product owner reviewed ALL comments
- [ ] Cleanup authorized

---

**Every failure mode here cost real time and effort. Every prevention mechanism emerged from actual pain. Learn from these mistakes without repeating them.**
