# Git Hooks

This directory contains Git hooks that help maintain code quality and prevent common errors.

## Pre-Commit Hook

**Location:** `.git/hooks/pre-commit`

### Purpose

Validates YAML frontmatter in agent markdown files before allowing commits. This prevents commits with invalid YAML that would cause agent loading failures in Claude Code.

### What It Checks

1. **YAML Frontmatter Structure**
   - Validates presence of `---` delimiters
   - Checks for required fields: `name` and `description`

2. **Common YAML Errors**
   - Detects unquoted values containing colons (like `description: Examples include: when...`)
   - Validates that field values are non-empty

3. **Agent Naming Conventions**
   - Ensures `name` field uses only lowercase letters and hyphens
   - Example: `technical-analyst`, `tdd-software-engineer`

### Example Error Output

```
❌ YAML Validation Failed!

  agents/my-agent.md:
    Line 3: Field 'description' has unquoted value containing colon.
             Value: Use this agent when you need: analysis
             💡 Wrap the entire value in double quotes: description: "Use this agent when you need: analysis"

💡 Common fixes:
  - Wrap descriptions with colons in double quotes
  - Escape single quotes or wrap entire value in double quotes
  - Ensure 'name' uses lowercase letters and hyphens only
  - Check that --- delimiters are on their own lines

Commit aborted. Please fix the errors and try again.
```

### How to Fix Common Issues

#### Unquoted Colons

**❌ Wrong:**
```yaml
description: Examples include: when a user says 'do this'
```

**✅ Correct:**
```yaml
description: "Examples include: when a user says 'do this'"
```

#### Invalid Agent Names

**❌ Wrong:**
```yaml
name: Technical_Analyst
name: TechnicalAnalyst
name: technical analyst
```

**✅ Correct:**
```yaml
name: technical-analyst
```

#### Missing Delimiters

**❌ Wrong:**
```yaml
name: my-agent
description: Does stuff
model: sonnet
```

**✅ Correct:**
```yaml
---
name: my-agent
description: Does stuff
model: sonnet
---
```

### Bypassing the Hook (Not Recommended)

If you absolutely need to bypass the validation:

```bash
git commit --no-verify -m "Your message"
```

**Warning:** This may result in agents that fail to load in Claude Code.

### Troubleshooting

If the hook isn't running:

1. Check that it's executable:
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

2. Verify Python 3 is available:
   ```bash
   python3 --version
   ```

3. Test the hook manually:
   ```bash
   .git/hooks/pre-commit
   ```
