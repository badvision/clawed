# Research Skill Setup & Verification

This guide covers configuring the LLM Council providers and verifying that the research agent team is correctly set up.

## Prerequisites

### Python Dependencies

```bash
pip install httpx google-genai
```

### Agent Files

The research team requires 6 agent definitions symlinked into `~/.claude/agents/`:

| Agent File | Role |
|-----------|------|
| `research-lead.md` | Orchestrator — decomposes queries, delegates, synthesizes |
| `openai-researcher.md` | Thin wrapper — shells out to OpenAI API |
| `perplexity-researcher.md` | Thin wrapper — shells out to Perplexity API |
| `claude-researcher.md` | Answers directly using Claude's own reasoning (no API key needed) |
| `gemini-researcher.md` | Thin wrapper — shells out to Vertex AI API |
| `peer-reviewer.md` | Evaluates anonymized responses for accuracy and depth |

Verify all are present:

```bash
for agent in research-lead openai-researcher perplexity-researcher claude-researcher gemini-researcher peer-reviewer; do
  if [ -L ~/.claude/agents/${agent}.md ] || [ -f ~/.claude/agents/${agent}.md ]; then
    echo "  OK  ${agent}.md"
  else
    echo "  MISSING  ${agent}.md"
  fi
done
```

If any are missing, symlink them from the repository:

```bash
ln -s ~/Documents/code/claude-workflow/agents/research-lead.md ~/.claude/agents/research-lead.md
ln -s ~/Documents/code/claude-workflow/agents/openai-researcher.md ~/.claude/agents/openai-researcher.md
ln -s ~/Documents/code/claude-workflow/agents/perplexity-researcher.md ~/.claude/agents/perplexity-researcher.md
ln -s ~/Documents/code/claude-workflow/agents/claude-researcher.md ~/.claude/agents/claude-researcher.md
ln -s ~/Documents/code/claude-workflow/agents/gemini-researcher.md ~/.claude/agents/gemini-researcher.md
ln -s ~/Documents/code/claude-workflow/agents/peer-reviewer.md ~/.claude/agents/peer-reviewer.md
```

### Skill Directory

The research skill itself must be symlinked:

```bash
ls -la ~/.claude/skills/research
# Should point to: ~/Documents/code/claude-workflow/skills/research
```

If missing:

```bash
ln -s ~/Documents/code/claude-workflow/skills/research ~/.claude/skills/research
```

## Provider Configuration

You need at least one external provider. Missing providers are skipped automatically. The system works best with all four.

### 1. OpenAI

```bash
export OPENAI_API_KEY=sk-proj-...
```

**Verify:**

```bash
python -m research query openai "Say hello in one sentence"
```

### 2. Perplexity

```bash
export PERPLEXITY_API_KEY=pplx-...
```

This is the highest-value single provider to configure. Perplexity is the only Council member with real-time web search — responses include citations and source URLs.

**Verify:**

```bash
python -m research query perplexity "What is the latest version of Node.js?"
```

### 3. Claude

No configuration needed. The `claude-researcher` agent answers directly — it IS Claude. Always available.

**Verify:**

```bash
python -m research query anthropic "Say hello in one sentence"
```

Note: The `ANTHROPIC_API_KEY` is only needed for monolithic CLI mode. In team mode, `claude-researcher` uses its own reasoning directly.

### 4. Google Gemini (via Vertex AI)

```bash
export GOOGLE_CLOUD_PROJECT=your-gcp-project-id
export GOOGLE_CLOUD_LOCATION=global
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

> **The location must be `global` for Gemini 3.x models.** Region-specific locations like `us-central1` will fail silently.

**Verify:**

```bash
python -m research query gemini "Say hello in one sentence"
```

## Full Verification

Run a complete council query to verify the entire pipeline (collect, peer review, synthesize):

```bash
cd ~/.claude/skills/research
python -m research research "What are the pros and cons of monorepos?"
```

Expected output includes responses from each available provider, peer review rankings, and a final synthesis. Providers that fail or are unconfigured will be skipped with a warning.

## Troubleshooting

**"No providers available"**
No API keys are configured. Set at least one of `OPENAI_API_KEY`, `PERPLEXITY_API_KEY`, or the Gemini environment variables.

**Gemini queries fail silently**
Check that `GOOGLE_CLOUD_LOCATION` is set to `global`, not a region like `us-central1`.

**"ModuleNotFoundError: No module named 'httpx'"**
Run `pip install httpx google-genai`.

**Agent not found when running `/research` in Claude Code**
Check that the agent symlinks exist in `~/.claude/agents/` and that Claude Code has been restarted after creating them.

**Peer review returns empty**
This usually means only one provider responded. The peer review stage needs at least 2 responses to compare.
