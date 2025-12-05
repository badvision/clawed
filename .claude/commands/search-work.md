---
description: Search across issue tracker, documentation, and Git commits for existing work
allowed_tools: [Bash, Read, Write]
---

# Cross-Repository Work Search

Search for existing work across issue trackers, documentation systems, and Git commit history to discover prior art, existing solutions, and related documentation before starting new work.

## Purpose

**CRITICAL**: Always search before creating. This command prevents:
- Duplicate work (someone already solved this)
- Reinventing solutions (documentation has architectural decisions)
- Missing context (issue tracker has requirements discussions)
- Ignoring prior failures (git history shows what didn't work)

## Search Strategy

### 1. Issue Tracker Search
Search across:
- Issue summaries and descriptions
- Issue comments (where most context lives)
- Custom fields if relevant

**Implementation depends on your issue tracker (GitHub Issues, JIRA, Linear, etc.):**

```bash
# Example: GitHub Issues via gh CLI
gh issue list --search "SEARCH_QUERY" --limit 20 --json number,title,url,state,updatedAt

# Example: JIRA via REST API (if available)
curl -s -H "Authorization: Bearer ${ISSUE_TRACKER_TOKEN}" \
  "${ISSUE_TRACKER_URL}/rest/api/2/search?jql=text~\"SEARCH_QUERY\"&fields=key,summary,status,assignee,updated,comment&maxResults=20"
```

### 2. Documentation Search
Search across:
- Page titles
- Page content
- Comments and attachments

**Implementation depends on your documentation system (Confluence, Notion, GitHub Wiki, etc.):**

```bash
# Example: Confluence via REST API (if available)
curl -s -H "Authorization: Bearer ${DOCS_TOKEN}" \
  "${DOCS_URL}/rest/api/content/search?cql=space=${SPACE_KEY}+AND+text~\"SEARCH_QUERY\"&limit=20&expand=body.storage"

# Example: GitHub Wiki (search via local clone)
cd .wiki && git grep -i "SEARCH_QUERY" | head -20
```

**Common Documentation Locations to Search:**
- Architecture decision records (ADRs)
- Technical design documents
- Development standards and best practices
- System architecture documentation
- Service catalogs and component lists
- Detailed service/component documentation

### 3. Git Commit History Search
Search across:
- Commit messages
- File paths and changes
- Blame history for specific patterns

```bash
# Search git history for commits matching query
# Only search if in a git repository
if git rev-parse --git-dir > /dev/null 2>&1; then
  git log --all --grep="SEARCH_QUERY" --oneline -n 20 > /tmp/git_search_results.txt

  # Also search file paths
  git log --all --name-only --pretty=format: | grep -i "SEARCH_QUERY" | sort -u | head -20 >> /tmp/git_search_results.txt
fi
```

### 4. Pull Request Search (if using GitHub/GitLab)
```bash
# Search PRs if gh CLI is available
if command -v gh &> /dev/null; then
  gh pr list --search "SEARCH_QUERY" --limit 20 --json number,title,url,state,updatedAt > /tmp/pr_search_results.json
fi
```

## Search Execution Workflow

1. **Parse search query** from user input
2. **Execute parallel searches** across all available sources
3. **Parse and rank results**:
   - Recent activity weighted higher
   - Exact matches weighted higher than partial
   - Issues with links to documentation/PRs weighted higher
4. **Present unified results** with links and context
5. **Suggest next steps** based on what was found

## Result Presentation Format

```markdown
# Search Results for: "{query}"

## Issues ({count})
1. **[{key}]** {summary} - Status: {status}, Updated: {date}
   Link: {issue_url}
   Context: {first 200 chars of description or recent comment}

## Documentation ({count})
1. **{title}** - Updated: {date}
   Link: {doc_url}
   Context: {first 200 chars of content}
   Section: {ADRs | Architecture | Standards | etc}

## Git History ({count})
1. **{commit_hash}** {commit_message} - Date: {date}
   Files: {affected_file_paths}

## Pull Requests ({count})
1. **#{pr_number}** {title} - State: {state}, Updated: {date}
   Link: {pr_url}

## Recommendations
- If found related work: "Consider reviewing {issue/doc/pr} before proceeding"
- If found architectural decisions: "Read {doc} for context on this approach"
- If found nothing: "No prior work found - proceed with discovery"
```

## Implementation Script Template

Create a project-specific search script adapted to your tooling:

```python
#!/usr/bin/env python3
"""
Cross-repository work search
Adapt this template to your project's specific tooling
"""
import json
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

def search_issues(query, api_token=None, base_url=None):
    """
    Search issue tracker

    Adapt this for your issue tracker:
    - GitHub Issues: Use gh CLI or GitHub API
    - JIRA: Use JIRA REST API
    - Linear: Use Linear API
    - GitLab: Use GitLab API
    """
    # Example: GitHub Issues
    if not api_token or not base_url:
        return []

    try:
        # Adapt this command for your issue tracker
        result = subprocess.run(
            ['gh', 'issue', 'list', '--search', query, '--limit', '20',
             '--json', 'number,title,url,state,updatedAt'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except:
        pass
    return []

def search_docs(query, api_token=None, base_url=None):
    """
    Search documentation system

    Adapt this for your documentation:
    - Confluence: Use Confluence REST API
    - Notion: Use Notion API
    - GitHub Wiki: Use local git clone
    - MkDocs/Docusaurus: Use static site search or grep
    """
    # Implement based on your documentation system
    return []

def search_git(query):
    """Search git history"""
    try:
        # Check if in git repo
        subprocess.run(['git', 'rev-parse', '--git-dir'],
                      check=True, capture_output=True)

        # Search commit messages
        result = subprocess.run(
            ['git', 'log', '--all', f'--grep={query}', '--oneline', '-n', '20'],
            capture_output=True, text=True
        )
        return result.stdout.strip().split('\n') if result.stdout else []
    except:
        return []

def search_prs(query):
    """Search pull requests (GitHub/GitLab)"""
    try:
        result = subprocess.run(
            ['gh', 'pr', 'list', '--search', query, '--limit', '20',
             '--json', 'number,title,url,state,updatedAt'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except:
        pass
    return []

def format_results(issues, docs, git_commits, prs, query):
    """Format search results"""
    output = [f"# Search Results for: \"{query}\"\n"]

    # Issues
    if issues:
        output.append(f"\n## Issues ({len(issues)})\n")
        for issue in issues[:10]:
            # Adapt field names to your issue tracker
            num = issue.get('number', issue.get('key', '?'))
            title = issue.get('title', issue.get('summary', ''))
            status = issue.get('state', issue.get('status', {}).get('name', ''))
            updated = issue.get('updatedAt', issue.get('updated', ''))[:10]
            url = issue.get('url', '')

            output.append(f"- **[{num}]** {title}")
            output.append(f"  Status: {status}, Updated: {updated}")
            output.append(f"  Link: {url}\n")

    # Documentation
    if docs:
        output.append(f"\n## Documentation ({len(docs)})\n")
        for doc in docs[:10]:
            title = doc.get('title', '')
            url = doc.get('url', '')
            output.append(f"- **{title}**")
            output.append(f"  Link: {url}\n")

    # Git commits
    if git_commits:
        output.append(f"\n## Git Commits ({len(git_commits)})\n")
        for commit in git_commits[:10]:
            if commit.strip():
                output.append(f"- {commit}")
        output.append("")

    # Pull requests
    if prs:
        output.append(f"\n## Pull Requests ({len(prs)})\n")
        for pr in prs[:10]:
            num = pr.get('number', '?')
            title = pr.get('title', '')
            state = pr.get('state', '')
            updated = pr.get('updatedAt', '')[:10]
            url = pr.get('url', '')

            output.append(f"- **#{num}** {title}")
            output.append(f"  State: {state}, Updated: {updated}")
            output.append(f"  Link: {url}\n")

    return '\n'.join(output)

if __name__ == '__main__':
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    if not query:
        print("Usage: python3 search_work.py \"search query\"")
        sys.exit(1)

    # Get tokens from environment (adapt to your setup)
    issue_token = os.getenv('ISSUE_TRACKER_TOKEN')
    docs_token = os.getenv('DOCS_TOKEN')
    issue_url = os.getenv('ISSUE_TRACKER_URL')
    docs_url = os.getenv('DOCS_URL')

    # Execute searches
    issues = search_issues(query, issue_token, issue_url)
    docs = search_docs(query, docs_token, docs_url)
    git_commits = search_git(query)
    prs = search_prs(query)

    # Format and print results
    print(format_results(issues, docs, git_commits, prs, query))
```

## Command Usage

```bash
# Search for specific topic
/search-work "authentication"

# Search for feature name
/search-work "content marketing agent"

# Search for technical term
/search-work "context limit"

# Search for service name
/search-work "ContentProcessingService"
```

## Integration with Other Agents

### Technical Analyst Agent
**MUST** use `/search-work` during requirements discovery to:
- Find existing solutions or partial implementations
- Locate related issue discussions
- Discover architectural decisions in documentation

### Software Architect Agent
**MUST** use `/search-work` during architecture phase to:
- Find existing architectural patterns
- Locate similar system designs
- Discover prior technical decisions and rationale

### Documentation Specialist
**MUST** use `/search-work` when creating/updating documentation to:
- Find related documentation that should be linked
- Discover existing index pages to update
- Locate related proposals or architectural decisions

## Best Practices

1. **Search before creating**: Always search before writing new code or documentation
2. **Use multiple terms**: If first search fails, try synonyms or related terms
3. **Review all sources**: Don't stop at first result - check issues, docs, AND Git
4. **Link discoveries**: When you find related work, link it in your new work
5. **Update indexes**: When creating new documentation, update relevant index pages

## Configuration

Set these environment variables based on your project setup:

```bash
# Issue Tracker
export ISSUE_TRACKER_URL="https://your-issue-tracker.com"
export ISSUE_TRACKER_TOKEN="your_token_here"

# Documentation System
export DOCS_URL="https://your-docs-system.com"
export DOCS_TOKEN="your_token_here"
export DOCS_SPACE_KEY="your_space_key"  # if applicable
```

## Notes

- Search is case-insensitive by default
- Results are limited to 20 per source to keep output manageable
- Recent updates are weighted higher in result ordering
- Requires appropriate authentication tokens for external systems
- Git search only works when run from within a git repository
- PR search requires appropriate CLI tools (gh for GitHub, glab for GitLab)
