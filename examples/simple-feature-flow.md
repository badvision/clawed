# Simple Feature Orchestration Example

## Scenario

**Feature:** Add user profile avatar upload
**Complexity:** Low
**Estimated Time:** 30-45 minutes with orchestration

### User Story
As a user, I want to upload a profile avatar so I can personalize my account.

### Acceptance Criteria
1. User can select image file from device
2. Image preview shown before upload
3. Supported formats: JPG, PNG (max 5MB)
4. Avatar displayed in user profile
5. Error handling for invalid files

## Orchestration Flow

### Phase 1: Task Planning

**Agent:** Product Owner (Task Planner)

**Input:**
- User story and acceptance criteria
- No prior context (new feature)

**Activities:**
```yaml
Requirements Validation:
  - Review acceptance criteria for completeness
  - Identify missing details (e.g., avatar dimensions)
  - Check for ambiguities

Task Breakdown:
  - Backend: File upload endpoint
  - Frontend: Upload component
  - Integration: Profile display update
  - Testing: Unit, integration, E2E

Dependencies:
  - Existing authentication system
  - User profile data model
  - Image storage service
```

**Output (Issue Comment):**
```markdown
## 📋 Product Owner - Requirements Validation

**Status**: Requirements reviewed and validated

### Requirements Completeness
✅ User story clear and actionable
✅ Acceptance criteria specific and testable
⚠️ Need clarification on avatar dimensions

### Task Breakdown
1. **Backend Task**: File upload API endpoint
   - Duration: 4 hours
   - Dependencies: Authentication, storage service

2. **Frontend Task**: Avatar upload component
   - Duration: 6 hours
   - Dependencies: Backend endpoint, UI component library

3. **Integration Task**: Profile display update
   - Duration: 2 hours
   - Dependencies: Backend and frontend complete

4. **Testing Task**: Comprehensive validation
   - Duration: 3 hours
   - Dependencies: All implementation complete

### Open Questions
1. Avatar dimensions: Square? Aspect ratio?
2. Storage location: S3? Local filesystem?
3. Existing avatar: Replace or keep history?

**Next Phase**: Technical Analyst for requirements clarification
```

**Quality Gate:**
```yaml
Product_Owner_Gate:
  ✅ requirements_reviewed: true
  ✅ task_breakdown_complete: true
  ✅ dependencies_identified: true
  ⚠️ clarifications_needed: true (dimensions, storage)
```

**Orchestrator Decision:** Proceed to Technical Analyst for clarification.

### Phase 2: Requirements Analysis

**Agent:** Technical Analyst

**Input:**
- Product Owner's task breakdown
- Open questions identified
- Acceptance criteria

**Activities:**
```yaml
Requirements Clarification:
  - Research standard avatar dimensions (200x200, 400x400)
  - Review existing storage patterns (finds S3 used elsewhere)
  - Check profile data model (avatar_url field exists)

Acceptance Criteria Refinement:
  - Add specific dimensions
  - Specify storage approach
  - Define replacement behavior

Dependency Analysis:
  - Authentication: Required, available
  - Storage service: S3 client configured
  - Profile model: Needs avatar_url field migration
```

**Output (Issue Comment):**
```markdown
## 🔍 Technical Analyst - Requirements Analysis

**Status**: Requirements clarified and complete

### Clarifications Resolved
1. **Avatar dimensions**: 400x400 pixels (matches existing UI patterns)
2. **Storage**: S3 bucket (consistent with document uploads)
3. **Replacement**: Single avatar, replaces existing (simplest approach)

### Updated Acceptance Criteria
1. User can select image file from device
2. Image preview shown before upload
3. Supported formats: JPG, PNG (max 5MB)
4. Image resized to 400x400 on server
5. Avatar stored in S3 with user-scoped key
6. Avatar URL saved to user profile
7. Avatar displayed in user profile (400x400)
8. Error handling for invalid files
9. Loading state during upload

### Dependencies Confirmed
✅ Authentication system (JWT middleware)
✅ S3 storage service (aws-sdk configured)
✅ User profile model (avatar_url field)
⚠️ Need database migration for avatar_url field

### Risk Assessment
- **Low Risk**: Standard file upload pattern
- **Medium Risk**: Image processing on server (memory usage)
- **Mitigation**: Stream processing, size limits enforced

**Next Phase**: Software Architect for design specification
```

**Quality Gate:**
```yaml
Technical_Analyst_Gate:
  ✅ requirements_complete: true
  ✅ acceptance_criteria_refined: true
  ✅ dependencies_documented: true
  ✅ risk_assessment_complete: true
  ✅ next_phase_ready: true
```

**Orchestrator Decision:** Proceed to Software Architect.

### Phase 3: Architecture Design

**Agent:** Software Architect

**Input:**
- Refined requirements and acceptance criteria
- Dependency analysis
- Risk assessment

**Activities:**
```yaml
STOP Protocol Execution:
  Search:
    - Existing file upload patterns (finds document upload)
    - Image processing libraries (finds sharp library)
    - S3 integration patterns (finds upload helper)

  Think:
    - Existing document upload handles PDFs, not images
    - Need image-specific processing (resize, format conversion)
    - S3 helper reusable with minor extension

  Outline:
    - Extend existing upload pattern for images
    - Add image processing middleware
    - Reuse S3 helper with new bucket path
    - Follow established API patterns

  Prove:
    - Business need: User avatar requirement
    - Simplicity: Extends existing patterns (minimal custom code)
    - Evidence: Similar pattern in document upload successful
```

**Output (Issue Comment):**
```markdown
## 🏗️ Software Architect - Design Specification

**Status**: Design complete, ready for implementation

### STOP Protocol Analysis

**Search Findings:**
- ✅ File upload pattern exists (document upload service)
- ✅ S3 integration helper available
- ✅ Image processing library (sharp) already in dependencies

**Think Analysis:**
- Existing upload pattern 80% reusable
- Need image-specific middleware (resize, validate)
- S3 helper needs extension for avatar bucket path

**Outline Integration:**
```typescript
// Extend existing upload service
class AvatarUploadService extends FileUploadService {
  // Reuse: Authentication, multipart handling, error handling
  // Add: Image validation, resize to 400x400, format conversion
}

// Reuse S3 helper with avatar-specific path
s3Helper.upload(file, { bucket: 'user-avatars', key: `${userId}/avatar.jpg` });
```

**Prove Necessity:**
- Business requirement: User personalization
- Simplest approach: Extend existing patterns
- Evidence: Document upload pattern proven in production

### Design Specification

**API Endpoint:**
```
POST /api/user/avatar
Content-Type: multipart/form-data

Request:
  - file: image file (JPG/PNG, max 5MB)

Response:
  - avatar_url: string (S3 URL)
  - status: success | error
```

**Implementation Sequence:**
1. Image validation middleware
2. Image processing (resize to 400x400)
3. S3 upload with avatar-specific path
4. Database update (avatar_url field)
5. Frontend upload component
6. Profile display update

**Integration Points:**
- Authentication: JWT middleware (existing)
- Storage: S3 helper (extend for avatars)
- Database: User model (add avatar_url field)
- Frontend: File input component (new)

**Next Phase**: TDD Software Engineer for implementation
```

**Quality Gate:**
```yaml
Software_Architect_Gate:
  ✅ stop_protocol_complete: true
  ✅ existing_patterns_identified: true
  ✅ integration_approach_documented: true
  ✅ implementation_sequence_defined: true
  ✅ design_validated: true
```

**Orchestrator Decision:** Proceed to TDD Engineer.

### Phase 4: Implementation

**Agent:** TDD Software Engineer

**Input:**
- Design specification
- Implementation sequence
- Acceptance criteria

**Activities:**
```yaml
Test-Driven Development:
  Red Phase:
    - Write test: Avatar upload succeeds
    - Write test: Invalid file rejected
    - Write test: Image resized correctly
    - Write test: S3 upload called
    - Write test: Database updated
    - Run tests: ALL FAIL (no implementation yet)

  Green Phase:
    - Implement AvatarUploadService
    - Add image validation middleware
    - Integrate sharp for resizing
    - Update S3 helper call
    - Add database migration
    - Run tests: ALL PASS

  Refactor Phase:
    - Extract validation logic
    - Add error handling
    - Optimize image processing
    - Add logging
    - Run tests: ALL PASS (no regression)
```

**Output (Issue Comment):**
```markdown
## ⚙️ TDD Software Engineer - Implementation Complete

**Status**: All acceptance criteria implemented and tested

### Test-Driven Development Results

**Red Phase (Tests First):**
- ✅ 7 unit tests written (all failing initially)
- ✅ 3 integration tests written (all failing initially)
- ✅ Tests encode acceptance criteria

**Green Phase (Implementation):**
- ✅ AvatarUploadService implemented
- ✅ Image validation middleware added
- ✅ Resize functionality (sharp library)
- ✅ S3 upload integration
- ✅ Database migration (avatar_url field)
- ✅ All tests passing (10/10)

**Refactor Phase (Quality Improvement):**
- ✅ Validation logic extracted to helper
- ✅ Error handling added
- ✅ Logging integrated
- ✅ Tests remain passing (10/10)

### Test Coverage
- Unit tests: 92% (7/7 passing)
- Integration tests: 100% (3/3 passing)
- Overall coverage: 89% (exceeds 80% threshold)

### Code Quality
- Cyclomatic complexity: 6 (below 10 threshold)
- No linting errors
- Follows project patterns
- Documentation comments added

### Implementation Notes
- Extended FileUploadService (reused 80% of code)
- S3 helper required minor extension (avatar bucket path)
- Database migration tested in isolation
- Error handling covers all edge cases

**Next Phase**: QA Test Validator for comprehensive validation
```

**Quality Gate:**
```yaml
TDD_Engineer_Gate:
  ✅ tests_written_first: true
  ✅ all_tests_passing: true (10/10)
  ✅ coverage_threshold_met: true (89% > 80%)
  ✅ code_quality_standards: true
  ✅ scope_boundaries_respected: true (no architecture changes)
  ✅ implementation_complete: true
```

**Orchestrator Decision:** Proceed to QA Validator.

### Phase 5: QA Validation

**Agent:** QA Test Validator

**Input:**
- Implementation with passing unit/integration tests
- Acceptance criteria
- Test coverage report

**Activities:**
```yaml
Comprehensive Validation:
  Acceptance Criteria Verification:
    - Test each criterion with real data
    - Verify edge cases not in unit tests
    - Validate integration with existing system

  Test Suite Execution:
    - Run all tests (unit, integration, E2E)
    - Verify meaningful validation (not just coverage)
    - Check for test quality issues

  Regression Testing:
    - Verify existing features unchanged
    - Test authentication flow still works
    - Confirm profile display remains functional
```

**Output (Issue Comment):**
```markdown
## ✅ QA Test Validator - Validation Results

**Status**: All acceptance criteria met, ready for deployment

### Acceptance Criteria Validation

1. ✅ User can select image file from device
   - Tested: File input component functional
   - Edge case: Multiple file selection rejected

2. ✅ Image preview shown before upload
   - Tested: Preview displays correctly
   - Edge case: Invalid file shows error, not preview

3. ✅ Supported formats: JPG, PNG (max 5MB)
   - Tested: JPG and PNG accepted
   - Edge case: GIF, BMP rejected with clear error
   - Edge case: 6MB file rejected with size error

4. ✅ Image resized to 400x400 on server
   - Tested: Various sizes all become 400x400
   - Edge case: Already 400x400 processed correctly
   - Edge case: Non-square images cropped to square

5. ✅ Avatar stored in S3 with user-scoped key
   - Tested: S3 upload successful
   - Verified: Key format correct (userId/avatar.jpg)
   - Edge case: Concurrent uploads handled

6. ✅ Avatar URL saved to user profile
   - Tested: Database updated correctly
   - Edge case: Update failure rolls back upload

7. ✅ Avatar displayed in user profile
   - Tested: Profile shows new avatar
   - Edge case: Missing avatar shows default

8. ✅ Error handling for invalid files
   - Tested: All error cases show user-friendly messages
   - Edge case: Network errors handled gracefully

9. ✅ Loading state during upload
   - Tested: Spinner shown during upload
   - Edge case: Fast upload still shows state change

### Test Suite Results
- Unit tests: 7/7 passing
- Integration tests: 3/3 passing
- E2E tests: 2/2 passing (added for avatar flow)
- Total: 12/12 passing (100%)

### Regression Testing
✅ Authentication flow unchanged
✅ Profile display functionality intact
✅ Existing file uploads unaffected
✅ No performance degradation detected

### Quality Metrics
- Test coverage: 89% (exceeds threshold)
- Code quality: No linting errors
- Performance: Upload completes <3 seconds (good)
- Security: File validation prevents exploits

**Next Phase**: Product Owner Validator for final sign-off
```

**Quality Gate:**
```yaml
QA_Validator_Gate:
  ✅ acceptance_criteria_met: true (9/9)
  ✅ test_suites_passing: true (12/12)
  ✅ no_regressions: true
  ✅ edge_cases_covered: true
  ✅ quality_metrics_satisfied: true
```

**Orchestrator Decision:** Proceed to Product Owner Validator.

### Phase 6: Final Validation

**Agent:** Product Owner (Validator)

**Input:**
- QA validation results
- All phase artifacts
- Issue comment history

**Activities:**
```yaml
Final Review:
  - Verify all acceptance criteria demonstrably met
  - Confirm quality standards satisfied
  - Review all issue comments for tier-2 artifacts
  - Validate documentation tier classification
  - Authorize cleanup and completion
```

**Output (Issue Comment):**
```markdown
## 🎬 Product Owner - Final Validation

**Status**: Feature complete, ready for deployment

### Final Review Results

**Acceptance Criteria:** 9/9 met
**Quality Gates:** 6/6 passed
**Test Coverage:** 89% (target: 80%)
**Regressions:** 0 detected

### Documentation Tier Classification

**Tier 1 (Issue Comments):**
- ✅ All agent progress reports (6 comments)
- ✅ STOP protocol analysis (in comment, not repo)
- ✅ Task breakdown and planning (in comment)

**Tier 2 (Ephemeral Workspace):**
- ✅ No artifacts created (simple feature, no workspace needed)

**Tier 3 (Repository):**
- ✅ No permanent documentation changes required
- ✅ Code comments sufficient for this feature

**Artifact Review:** No tier-2 artifacts in repository (clean)

### Deployment Readiness
✅ All tests passing
✅ Code reviewed and approved
✅ No outstanding issues
✅ Documentation appropriate

**Issue Status:** Closing as complete

---

**Total Time:** 42 minutes (orchestration) + 15 minutes (development)
**Quality:** All gates passed on first attempt
**Rework:** 0 iterations required
```

**Quality Gate:**
```yaml
Product_Owner_Gate:
  ✅ acceptance_criteria_validated: true
  ✅ quality_standards_met: true
  ✅ no_tier2_artifacts: true
  ✅ documentation_classified: true
  ✅ ready_for_deployment: true
```

**Orchestrator Decision:** Close issue, update metrics.

## Orchestration Outcomes

### Summary Statistics

```yaml
Feature: User Profile Avatar Upload
Duration: 57 minutes total (orchestration + development)
Phases: 6/6 completed
Quality Gates: 6/6 passed on first attempt
Tests: 12/12 passing
Coverage: 89%
Regressions: 0
Escalations: 0
Rework Iterations: 0
```

### Artifacts Created

**Tier 1 (Issue Comments):**
- 6 agent progress reports
- Task breakdown and planning
- Requirements clarification
- STOP protocol analysis
- Implementation notes
- Validation results

**Tier 2 (Ephemeral Workspace):**
- None (simple feature didn't require workspace)

**Tier 3 (Repository):**
- AvatarUploadService.ts (new)
- imageValidationMiddleware.ts (new)
- avatar-upload.test.ts (new)
- Migration: AddAvatarUrlToUser.sql (new)
- Frontend: AvatarUpload.tsx (new)

### Key Takeaways

**What Worked:**
- Systematic progression through phases
- Quality gates caught potential issues early
- STOP protocol prevented reinvention
- Test-first approach ensured correctness
- Documentation remained clean (no bloat)

**Time Comparison:**

**Without Orchestration:**
- Initial implementation: 3 hours
- Bug fixes after testing: 2 hours
- Rework for missed requirements: 4 hours
- Documentation cleanup: 1 hour
- **Total: 10 hours**

**With Orchestration:**
- Systematic workflow: 57 minutes
- No rework needed
- Documentation clean from start
- **Total: 57 minutes**

**Savings: 9 hours (90% reduction)**

The savings come from:
- Upfront requirements clarity
- No missed acceptance criteria
- No architectural surprises
- No documentation rework
- Single-pass implementation
