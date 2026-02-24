# Core Principles

## Communication Style

- Avoid repetitive validation phrases like "you're absolutely right" - use varied language
- Challenge technical assumptions when they need verification
- Prioritize accuracy over agreement

## Agent Documentation Behavior

**CRITICAL**: Agents (including you in orchestrator mode) should NOT create documents by default.

### The Minimal Documentation Rule

**Before creating ANY markdown file or documentation, ask:**

1. **Was documentation explicitly requested in the task?**
   - Yes → Create it (it's a deliverable)
   - No → Continue to #2

2. **Is it required by acceptance criteria?**
   - Yes → Create it (definition of done)
   - No → Continue to #3

3. **Is this a major revelation requiring human escalation?**
   - Yes → Create brief document in `/tmp/claude-research-{project}/`, note in completion report for issue tracker attachment
   - No → Continue to #4

4. **Does another agent truly need written context?**
   - First try: Include in completion report
   - If insufficient: Write to `/tmp/claude-research-{project}/` (ephemeral)
   - No → **DO NOT CREATE DOCUMENT**

**Default behavior: Include findings in completion report, pass to next agent via orchestrator.**

### Common Anti-Patterns to AVOID

**❌ Do NOT create:**
- "IMPLEMENTATION-COMPLETE.md" → Use completion report
- "ANALYSIS.md" → Include in completion report
- "EXECUTIVE-SUMMARY.md" → Not a deliverable unless explicitly requested
- "FINDINGS.md" → Pass to next agent in handoff
- "BUG-REPORT.md" → Document in issue tracker comment
- "PHASE-N-SUMMARY.md" → Status belongs in completion report

**✅ DO create:**
- Documentation explicitly requested in task
- Documentation required by acceptance criteria
- Wiki pages for formal architecture proposals (if wiki integration available)
- Final deliverables when research complete (and user asked for it)

### Ephemeral Workspace for Research/Scratch Work

**CRITICAL**: Orchestrator manages workspace paths and communicates them to agents. Agents MUST use the provided workspace path.

**Path Structure:**
```
/tmp/claude/{IDENTIFIER}/iteration-{N}/

Where:
- IDENTIFIER = Issue tracker key (STORY-1) OR adhoc name (error-handling, auth-spike)
- N = iteration number (1, 2, 3... NEVER use FINAL, LAST, COMPLETE)
```

**Agent Behavior:**
- **Orchestrator provides workspace path** in delegation prompt
- **Agents create directories as needed** within their workspace
- **Write ONLY if**:
  1. Task explicitly requires documentation
  2. Major revelation requiring human escalation (name: `IMPORTANT-{topic}.md`)
  3. Another agent needs written context (rare - try completion report first)

**Naming Rules:**
- ✅ `IMPORTANT-architecture-decision.md` - Signals importance to future Claude
- ✅ `test-results.json` - Descriptive, iteration-scoped by path
- ❌ `FINAL-report.md` - No FINAL (always assume more iterations)
- ❌ `analysis-v2.md` - No version numbers (iteration path provides versioning)
- ❌ `COMPLETE-summary.md` - No COMPLETE (never truly complete)

**Framing:**
When you write, remember: **You're writing for future Claude, not humans.**
- Frame as "echoes into the future"
- What would future-you need to know?
- Would this be important days/weeks later?
- If not important enough to name IMPORTANT-*.md, include in completion report instead

**Purpose**: Ephemeral storage, naturally cleaned up by OS
**Lifecycle**: Product owner reviews during PR phase, elevates worthy artifacts to issue tracker attachments
**Benefit**: No git/gitignore concerns, no workspace clutter, clear iteration boundaries

### Artifact Elevation

During PR review, product owner:
1. Reviews `/tmp/claude-research-{project}/` for worthy artifacts
2. Attaches important findings to issue tracker issue
3. Lists attachments in issue tracker comment with descriptions
4. Does NOT commit research artifacts to git (issue tracker is their home)

**Key Principle**: Agents communicate through completion reports, not documents. Documents are for explicit deliverables, human consumption (issue tracker/wiki), or major revelations only.

---

# Pull Request Guidelines

## CRITICAL: Always Create Draft Pull Requests

**⚠️ ALL PULL REQUESTS MUST BE CREATED AS DRAFTS ⚠️**

When creating pull requests using `gh pr create`, you MUST include the `--draft` flag. This is non-negotiable.

### Why Draft PRs?

- **Human-in-the-loop approval**: Only the human developer should decide when work is ready for peer review
- **Avoid notification spam**: Team members will be annoyed if they receive review requests for unfinished work
- **Allow for iteration**: Work may need additional commits, testing, or refinement before being ready
- **Respect team workflow**: The developer needs to verify the PR is complete and properly formatted before requesting reviews

### Correct Usage

**✅ CORRECT - Always use --draft:**
```bash
gh pr create --draft --title "feat: Add new feature" --body "$(cat <<'EOF'
## Summary
- Implemented feature X
- Added tests

## Test plan
- [ ] Unit tests pass
- [ ] Manual testing complete

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**❌ INCORRECT - Never omit --draft:**
```bash
# This will immediately notify reviewers - DO NOT DO THIS
gh pr create --title "feat: Add new feature" --body "..."
```

### Converting Draft to Ready

Once the human developer has reviewed the PR and confirmed it's ready, they can convert it to "ready for review" using:

```bash
gh pr ready <PR_NUMBER>
```

Or they can use the GitHub web interface to mark the PR as ready for review.

### Exception Handling

There are NO exceptions to this rule. Even if:
- The work seems complete
- All tests are passing
- The commit is small or trivial
- The user says "create a PR"

**ALWAYS** create as draft. Let the human decide when to mark it ready for review.
