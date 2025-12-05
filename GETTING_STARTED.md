# Getting Started with CLAWED

## Overview

This guide walks through setting up CLAWED orchestration for your project, from initial installation through running your first coordinated workflow.

CLAWED requires:
1. Issue tracker integration (GitHub Issues or Jira)
2. Claude Code CLI or compatible environment
3. Agent definitions and orchestration logic
4. Quality gate templates

Estimated setup time: 2-4 hours for basic configuration.

## Prerequisites

### Required Tools

**Claude Code CLI:**
- Download from Anthropic
- Configure with your API keys
- Verify installation: `claude --version`

**Issue Tracker Access:**
- GitHub: Personal access token with repo and issue permissions
- Jira: API token with issue read/write permissions

**Git Repository:**
- Existing repository or new project
- Write access for committing agent configurations

### Environment Variables

Create `.env` file in project root:

```bash
# Issue Tracker Configuration
ISSUE_TRACKER_TYPE=github  # or 'jira'
ISSUE_TRACKER_URL=https://github.com/yourusername/yourproject
GITHUB_TOKEN=ghp_your_personal_access_token_here

# Or for Jira:
# JIRA_URL=https://yourcompany.atlassian.net
# JIRA_TOKEN=your_jira_api_token
# JIRA_EMAIL=your.email@company.com

# Claude Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key
```

**Token Setup:**

**GitHub:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (full control)
4. Copy token to `.env` as `GITHUB_TOKEN`

**Jira:**
1. Go to Jira Profile → Personal Access Tokens
2. Create new token with issue read/write permissions
3. Copy token to `.env` as `JIRA_TOKEN`

## Installation

### Step 1: Clone CLAWED Framework

```bash
# Clone the repository
git clone https://github.com/yourusername/clawed.git
cd clawed

# Install dependencies
npm install

# Verify installation
npm test
```

### Step 2: Copy Agent Definitions to Your Project

```bash
# In your project directory
mkdir -p .claude/agents
mkdir -p .claude/commands
mkdir -p .claude/templates

# Copy agent definitions
cp clawed/.claude/agents/* .claude/agents/

# Copy orchestration command
cp clawed/.claude/commands/orchestrate.md .claude/commands/

# Copy quality gate templates
cp clawed/.claude/templates/* .claude/templates/
```

### Step 3: Configure for Your Project

Edit `.claude/commands/orchestrate.md` to customize:

```markdown
# Orchestration Configuration

## Issue Tracker Integration
ISSUE_TRACKER: github  # or 'jira'
PROJECT_KEY: PROJ      # Your project abbreviation

## Agent Definitions
AGENTS_DIR: .claude/agents/

## Quality Gates
TEMPLATES_DIR: .claude/templates/

## Workspace Configuration
WORKSPACE_ROOT: /tmp/claude/{project}/iteration-{N}/
```

### Step 4: Initialize Documentation Structure

```bash
# Create documentation directories
mkdir -p docs/{architecture,patterns,requirements,decisions}

# Create README files for each tier
cat > docs/README.md << 'EOF'
# Project Documentation

This directory contains permanent system documentation (Tier 3).

See ARCHITECTURE.md for documentation tier classification.
EOF

cat > docs/architecture/README.md << 'EOF'
# Architecture Documentation

System architecture, component specifications, and integration patterns.
EOF

cat > docs/patterns/README.md << 'EOF'
# Development Patterns

Established patterns and conventions for this project.
EOF
```

## Configuration

### Agent Customization

Each agent definition in `.claude/agents/` can be customized:

#### Example: Technical Analyst Agent

```yaml
# .claude/agents/technical-analyst.md

Role: Technical Analyst
Specialization: Requirements analysis and acceptance criteria definition

Autonomous Decision Boundaries:
  - Technical complexity assessment (Low/Medium/High)
  - Whether architectural review is needed
  - Risk categorization and standard mitigation strategies
  - Reasonable assumptions for missing non-critical details
  - Standard acceptance criteria patterns

Mandatory Escalation Criteria:
  IMMEDIATE (Stop Work):
    - Business stakeholder input required for scope decisions
    - Conflicting requirements from different stakeholders
    - Legal/compliance requirements needing assessment
    - Budget/resource constraints affecting feasibility

  STANDARD (Continue with Documentation):
    - Domain expertise needed beyond agent knowledge
    - Industry-specific requirements unclear
    - Performance criteria needing business validation

Quality Gates:
  Requirements Completeness:
    - All functional requirements have acceptance criteria
    - Non-functional requirements identified
    - Success metrics and definition of done established
    - Scope boundaries explicitly defined

  Dependency Clarity:
    - All internal and external dependencies identified
    - Dependency impact and resolution timelines documented
    - Prerequisite work clearly defined

  Risk Assessment:
    - High and medium risks identified
    - Mitigation strategies defined for high risks
    - Technical complexity evaluation completed
```

**Customization Points:**
- Adjust quality gate thresholds for your project standards
- Add project-specific patterns to autonomous boundaries
- Customize escalation criteria for your organization
- Add domain-specific validation requirements

### Quality Gate Templates

Edit `.claude/templates/quality-gates.md`:

```yaml
# Project-Specific Quality Gates

Code Coverage Thresholds:
  unit_tests: 80%              # Adjust for your standards
  integration_tests: 70%
  e2e_tests: 50%

Code Quality Metrics:
  max_cyclomatic_complexity: 10
  max_function_length: 50      # lines
  max_file_length: 300         # lines

Documentation Requirements:
  business_logic_coverage: 80%  # % of business logic with doc comments
  api_documentation: 100%       # All public APIs documented
  architecture_updates: required # On architectural changes

Performance Standards:
  page_load_time: 2000          # milliseconds
  api_response_time: 500        # milliseconds
  build_time_max: 300           # seconds
```

### Issue Tracker Integration

#### GitHub Issues Configuration

Create `.claude/config/github.yaml`:

```yaml
github:
  repository: yourusername/yourproject
  issue_labels:
    orchestration:
      in_progress: "orchestration:in-progress"
      requirements: "phase:requirements"
      design: "phase:design"
      implementation: "phase:implementation"
      validation: "phase:validation"
      blocked: "status:blocked"

  issue_template: |
    ## Requirements
    <!-- Technical Analyst phase -->

    ## Design
    <!-- Software Architect phase -->

    ## Implementation Notes
    <!-- TDD Engineer phase -->

    ## Validation Results
    <!-- QA Validator phase -->
```

#### Jira Configuration

Create `.claude/config/jira.yaml`:

```yaml
jira:
  instance: yourcompany.atlassian.net
  project_key: PROJ

  custom_fields:
    orchestration_phase: customfield_10001
    quality_gate_status: customfield_10002

  issue_types:
    feature: Story
    bug: Bug
    task: Task

  workflows:
    standard:
      - To Do
      - Requirements Analysis
      - Design
      - In Progress
      - Validation
      - Done
```

## First Orchestration

### Example: Simple Feature Implementation

Let's orchestrate a simple feature from issue creation through completion.

#### Step 1: Create Issue

**GitHub:**
```bash
gh issue create \
  --title "Add user profile avatar upload" \
  --body "As a user, I want to upload a profile avatar so I can personalize my account." \
  --label "type:feature"
```

**Jira:**
```bash
curl -X POST \
  -H "Authorization: Bearer $JIRA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Add user profile avatar upload",
      "description": "As a user, I want to upload a profile avatar...",
      "issuetype": {"name": "Story"}
    }
  }' \
  "https://yourcompany.atlassian.net/rest/api/2/issue"
```

#### Step 2: Invoke Orchestration

```bash
# Using Claude Code CLI
claude /orchestrate --issue STORY-1

# Or from interactive session
> /orchestrate --issue STORY-1
```

#### Step 3: Observe Orchestration

**Orchestrator starts:**
```
🎯 Orchestration Started: STORY-1

📖 Reading issue context...
   ✓ Issue title and description read
   ✓ All comments reviewed (0 existing)
   ✓ No prior attempts detected

🔍 Phase 1: Requirements Analysis
   → Delegating to Technical Analyst...
```

**Technical Analyst phase:**
```
📋 Technical Analyst Working...

Analyzing requirements:
✓ Functional requirements identified
✓ Acceptance criteria defined
✓ Dependencies documented
✓ Risk assessment completed

Quality Gate Check:
✓ Requirements completeness: PASS
✓ Dependency clarity: PASS
✓ Risk assessment: PASS
✓ Next phase readiness: PASS

Adding analysis to issue comments...
```

**Software Architect phase:**
```
🏗️ Software Architect Working...

Executing STOP Protocol:
✓ Search: Existing file upload patterns found
✓ Think: Existing pattern suitable with extension
✓ Outline: Integration approach documented
✓ Prove: Business justification clear

Creating design specification...
Quality Gate Check:
✓ STOP protocol complete: PASS
✓ Integration points specified: PASS
✓ Design validated: PASS

Adding design to issue comments...
```

**TDD Engineer phase:**
```
⚙️ TDD Engineer Working...

Test-Driven Development:
✓ Tests written (7 unit, 3 integration)
✓ Implementation complete
✓ All tests passing (10/10)
✓ Code coverage: 87%

Quality Gate Check:
✓ Implementation complete: PASS
✓ Test coverage: PASS (87% > 80% threshold)
✓ Code quality standards: PASS
✓ Scope boundaries respected: PASS

Committing changes...
```

**QA Validator phase:**
```
✅ QA Test Validator Working...

Validation Results:
✓ All acceptance criteria met
✓ Test suites passing (10 unit, 3 integration, 2 e2e)
✓ No regressions detected
✓ Documentation updated

Quality Gate Check:
✓ Acceptance criteria: PASS (5/5)
✓ Quality standards: PASS
✓ Integration: PASS
✓ Documentation: PASS

Adding validation results to issue...
```

**Product Owner phase:**
```
🎬 Product Owner Validator Working...

Final Review:
✓ All phases completed successfully
✓ Quality gates passed
✓ No tier-2 artifacts in repository
✓ Ready for deployment

Updating issue status to Done...
```

**Orchestration complete:**
```
✅ Orchestration Complete: STORY-1

Summary:
- Phases: 5/5 completed
- Quality gates: 5/5 passed
- Time: 42 minutes
- Escalations: 0

Issue updated and ready for deployment.
```

## Troubleshooting

### Common Issues

#### Issue: "Cannot find agent definition"

**Symptom:**
```
Error: Agent definition not found: technical-analyst
```

**Solution:**
1. Verify `.claude/agents/technical-analyst.md` exists
2. Check file permissions (must be readable)
3. Validate YAML frontmatter in agent file

#### Issue: "Quality gate failed"

**Symptom:**
```
❌ Quality Gate Failed: Test coverage below threshold (65% < 80%)
```

**Solution:**
1. Review quality gate thresholds in `.claude/templates/quality-gates.md`
2. Adjust thresholds if overly strict for current phase
3. Add tests to meet threshold
4. Request remediation phase if needed

#### Issue: "Issue tracker authentication failed"

**Symptom:**
```
Error: GitHub API authentication failed (401)
```

**Solution:**
1. Verify `GITHUB_TOKEN` in `.env`
2. Check token has correct permissions (repo scope)
3. Regenerate token if expired
4. Test with: `curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user`

#### Issue: "Workspace path not found"

**Symptom:**
```
Error: Cannot create workspace at /tmp/claude/...
```

**Solution:**
1. Verify `/tmp/` directory exists and is writable
2. Check disk space available
3. On Windows, use different path (e.g., `C:\Temp\claude\`)
4. Update `WORKSPACE_ROOT` in orchestration config

### Getting Help

**Documentation:**
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design and patterns
- [FAILURE_MODES.md](FAILURE_MODES.md) - Common problems and solutions
- [EVOLUTION.md](EVOLUTION.md) - Background and lessons learned

**Community:**
- GitHub Discussions: Ask questions and share experiences
- Issue Tracker: Report bugs and request features
- Examples: See `/examples/` for working patterns

## Next Steps

### Customize for Your Project

1. **Define Project Patterns**
   - Document in `/docs/patterns/`
   - Add to agent autonomous boundaries
   - Reference in quality gates

2. **Establish Quality Standards**
   - Set coverage thresholds
   - Define code quality metrics
   - Configure CI/CD integration

3. **Train Your Team**
   - Share agent definitions and roles
   - Review orchestration workflow
   - Practice with small issues first

### Advanced Configuration

Once basic orchestration is working:

**Parallel Task Management:**
- Configure for issues with independent components
- Set up multi-agent coordination
- Define dependency management rules

**Custom Quality Gates:**
- Add project-specific validation
- Integrate with existing tools
- Configure automated enforcement

**Metrics and Monitoring:**
- Track orchestration effectiveness
- Monitor quality gate pass rates
- Measure time to completion

### Production Deployment

Before using CLAWED in production:

1. **Test with Small Issues**
   - Start with well-defined features
   - Validate agent coordination
   - Refine quality gate thresholds

2. **Establish Baseline Metrics**
   - Current time to completion
   - Current test coverage
   - Current rework rate

3. **Gradual Rollout**
   - One team first
   - Monitor effectiveness
   - Adjust based on feedback

4. **Team Training**
   - Agent roles and responsibilities
   - Quality gate expectations
   - Escalation procedures

---

**You're ready to orchestrate! Start with a small feature issue and observe the multi-agent coordination in action.**
