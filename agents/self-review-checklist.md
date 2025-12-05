# Agent Self-Review Checklist

This checklist should be completed by development agents (tdd-software-engineer, software-architect, etc.) BEFORE submitting work to QA or product owner validation.

## Purpose

Catch quality issues early through systematic self-review, reducing rework cycles and improving first-time quality.

## When to Use

Complete this checklist after finishing development work, before marking tasks as "done" or submitting to QA.

## Self-Review Process

### Step 1: Code Review (Read Your Own Diff)

- [ ] I have reviewed every line of code I changed
- [ ] I understand why each change was necessary
- [ ] I have removed any debug code, console.logs, or temporary changes
- [ ] I have not left any commented-out code without explanation

### Step 2: Code Cleanliness

- [ ] No unused imports remain in any file
- [ ] No unused variables, parameters, or properties exist
- [ ] All defined properties/methods are actually used
- [ ] All logger instances actually log something
- [ ] No TODO/FIXME comments without tracking tickets

### Step 3: Test Quality

- [ ] Every test validates behavior, not just existence
- [ ] No tests only assert `toBeDefined()` or `toBeTruthy()`
- [ ] Tests cover happy path, edge cases, and error conditions
- [ ] Test names clearly describe what is being tested
- [ ] Tests are meaningful and would catch real bugs

### Step 4: Documentation

- [ ] Documentation is in the correct location (`/docs/` vs component directory)
- [ ] Code comments explain "why", not "what"
- [ ] Complex logic has explanatory comments
- [ ] Public APIs have JSDoc documentation
- [ ] README updates reflect new functionality

### Step 5: Error Handling

- [ ] All error cases are handled appropriately
- [ ] Error messages are clear and actionable
- [ ] No silent failures or swallowed errors
- [ ] Logging provides sufficient debugging information

### Step 6: Integration

- [ ] Changes integrate properly with existing code
- [ ] No breaking changes to existing APIs (or properly documented if intentional)
- [ ] Dependencies are up-to-date and appropriate
- [ ] Configuration changes are documented

### Step 7: Testing

- [ ] All tests pass locally
- [ ] No flaky tests introduced
- [ ] Test coverage meets project standards
- [ ] Integration tests cover critical paths

## Reporting

When submitting work, include:
```
✅ Self-review completed
- Code diff reviewed
- No unused code remains
- All tests are meaningful
- Documentation in correct location
- All tests passing
```

## Red Flags (Stop and Fix)

If you answer "no" to any of these, STOP and fix before submitting:
- Are all tests meaningful and behavior-focused?
- Is all code actually used?
- Is documentation in the right place?
- Do all tests pass?

## Remember

**The best code review is the one you do yourself first.** Catching issues at this stage saves multiple round-trips through QA and code review.
