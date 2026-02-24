#!/bin/bash

# Clawed Setup Script
# This script creates all necessary symlinks from ~/.claude to the repository

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$SCRIPT_DIR"

echo "================================================"
echo "Claude Agentic Workflow Setup"
echo "================================================"
echo ""
echo "Repository: $REPO_DIR"
echo "Target: ~/.claude"
echo ""

# Create .claude directories if they don't exist
echo "Creating ~/.claude directories..."
mkdir -p ~/.claude/skills
mkdir -p ~/.claude/agents
mkdir -p ~/.claude/commands

# Function to create symlink with safety checks
create_symlink() {
    local source="$1"
    local target="$2"
    local description="$3"

    # Check if source exists
    if [ ! -e "$source" ]; then
        echo -e "${RED}ERROR: Source not found: $source${NC}"
        return 1
    fi

    # Check if target already exists
    if [ -e "$target" ] || [ -L "$target" ]; then
        if [ -L "$target" ]; then
            # It's a symlink - check if it points to the right place
            current_target=$(readlink "$target")
            if [ "$current_target" = "$source" ]; then
                echo -e "${GREEN}✓${NC} $description (already exists)"
                return 0
            else
                echo -e "${YELLOW}⚠${NC}  $description (exists, pointing to different location)"
                echo "   Current: $current_target"
                echo "   Expected: $source"
                read -p "   Replace? (y/n) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rm "$target"
                else
                    return 0
                fi
            fi
        else
            echo -e "${YELLOW}⚠${NC}  $description (file/directory exists, not a symlink)"
            read -p "   Replace with symlink? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                rm -rf "$target"
            else
                return 0
            fi
        fi
    fi

    # Create the symlink
    ln -s "$source" "$target"
    echo -e "${GREEN}✓${NC} $description"
}

# Symlink skills
echo ""
echo "Setting up skills..."
create_symlink "$REPO_DIR/skills/research" ~/.claude/skills/research "research skill"
create_symlink "$REPO_DIR/skills/socratize" ~/.claude/skills/socratize "socratize skill"
create_symlink "$REPO_DIR/skills/brainstorm" ~/.claude/skills/brainstorm "brainstorm skill"
create_symlink "$REPO_DIR/skills/concilize" ~/.claude/skills/concilize "concilize skill"
create_symlink "$REPO_DIR/skills/skill-creator" ~/.claude/skills/skill-creator "skill-creator skill"
create_symlink "$REPO_DIR/skills/webapp-testing" ~/.claude/skills/webapp-testing "webapp-testing skill"
create_symlink "$REPO_DIR/skills/document-skills" ~/.claude/skills/document-skills "document-skills skill"

# Symlink agents
echo ""
echo "Setting up agents..."
create_symlink "$REPO_DIR/agents/product-owner-task-planner.md" ~/.claude/agents/product-owner-task-planner.md "product-owner-task-planner agent"
create_symlink "$REPO_DIR/agents/product-owner-validator.md" ~/.claude/agents/product-owner-validator.md "product-owner-validator agent"
create_symlink "$REPO_DIR/agents/qa-test-validator.md" ~/.claude/agents/qa-test-validator.md "qa-test-validator agent"
create_symlink "$REPO_DIR/agents/software-architect.md" ~/.claude/agents/software-architect.md "software-architect agent"
create_symlink "$REPO_DIR/agents/tdd-software-engineer.md" ~/.claude/agents/tdd-software-engineer.md "tdd-software-engineer agent"
create_symlink "$REPO_DIR/agents/technical-analyst.md" ~/.claude/agents/technical-analyst.md "technical-analyst agent"
create_symlink "$REPO_DIR/agents/research-lead.md" ~/.claude/agents/research-lead.md "research-lead agent"
create_symlink "$REPO_DIR/agents/claude-researcher.md" ~/.claude/agents/claude-researcher.md "claude-researcher agent"
create_symlink "$REPO_DIR/agents/gemini-researcher.md" ~/.claude/agents/gemini-researcher.md "gemini-researcher agent"
create_symlink "$REPO_DIR/agents/openai-researcher.md" ~/.claude/agents/openai-researcher.md "openai-researcher agent"
create_symlink "$REPO_DIR/agents/perplexity-researcher.md" ~/.claude/agents/perplexity-researcher.md "perplexity-researcher agent"
create_symlink "$REPO_DIR/agents/peer-reviewer.md" ~/.claude/agents/peer-reviewer.md "peer-reviewer agent"
create_symlink "$REPO_DIR/agents/self-review-checklist.md" ~/.claude/agents/self-review-checklist.md "self-review-checklist reference"

# Symlink commands
echo ""
echo "Setting up commands..."
create_symlink "$REPO_DIR/commands/discover.md" ~/.claude/commands/discover.md "/discover command"
create_symlink "$REPO_DIR/commands/orchestrate.md" ~/.claude/commands/orchestrate.md "/orchestrate command"
create_symlink "$REPO_DIR/commands/search-work.md" ~/.claude/commands/search-work.md "/search-work command"
create_symlink "$REPO_DIR/commands/work-next.md" ~/.claude/commands/work-next.md "/work-next command"
create_symlink "$REPO_DIR/commands/plato.md" ~/.claude/commands/plato.md "/plato command"

# Install git hooks
echo ""
echo "Installing git hooks..."
if [ -f "$REPO_DIR/hooks/pre-commit" ]; then
    if [ -d "$REPO_DIR/.git" ]; then
        cp "$REPO_DIR/hooks/pre-commit" "$REPO_DIR/.git/hooks/pre-commit"
        chmod +x "$REPO_DIR/.git/hooks/pre-commit"
        echo -e "${GREEN}✓${NC} pre-commit hook installed"
    else
        echo -e "${YELLOW}⚠${NC}  Not a git repository, skipping hook installation"
    fi
else
    echo -e "${YELLOW}⚠${NC}  No pre-commit hook found in hooks/ directory"
fi

# Verification
echo ""
echo "================================================"
echo "Verifying Installation"
echo "================================================"
echo ""

error_count=0

# Check skills
echo "Checking skills..."
for skill in research socratize brainstorm concilize skill-creator webapp-testing document-skills; do
    if [ -L ~/.claude/skills/$skill ]; then
        echo -e "${GREEN}✓${NC} ~/.claude/skills/$skill"
    else
        echo -e "${RED}✗${NC} ~/.claude/skills/$skill (missing or not a symlink)"
        ((error_count++))
    fi
done

# Check agents
echo ""
echo "Checking agents..."
for agent in product-owner-task-planner product-owner-validator qa-test-validator software-architect tdd-software-engineer technical-analyst research-lead claude-researcher gemini-researcher openai-researcher perplexity-researcher peer-reviewer self-review-checklist; do
    if [ -L ~/.claude/agents/$agent.md ]; then
        echo -e "${GREEN}✓${NC} ~/.claude/agents/$agent.md"
    else
        echo -e "${RED}✗${NC} ~/.claude/agents/$agent.md (missing or not a symlink)"
        ((error_count++))
    fi
done

# Check commands
echo ""
echo "Checking commands..."
for command in discover orchestrate search-work work-next plato; do
    if [ -L ~/.claude/commands/$command.md ]; then
        echo -e "${GREEN}✓${NC} ~/.claude/commands/$command.md"
    else
        echo -e "${RED}✗${NC} ~/.claude/commands/$command.md (missing or not a symlink)"
        ((error_count++))
    fi
done

# Configuration check
echo ""
echo "================================================"
echo "Configuration"
echo "================================================"
echo ""

if [ -f ~/.claude/CLAUDE.md ]; then
    echo -e "${GREEN}✓${NC} ~/.claude/CLAUDE.md exists"
else
    echo -e "${YELLOW}⚠${NC}  ~/.claude/CLAUDE.md not found"
    echo ""
    echo "To complete setup, copy the example configuration:"
    echo "  cp $REPO_DIR/CLAUDE.md.example ~/.claude/CLAUDE.md"
    echo ""
    echo "  - Configure any required API tokens in your environment (see skills/research/SETUP.md for LLM research keys)"
fi

# Final summary
echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""

if [ $error_count -eq 0 ]; then
    echo -e "${GREEN}All symlinks created successfully!${NC}"
    echo ""
    echo "You can now use the following commands in Claude Code:"
    echo "  /discover    - Requirements gathering and planning"
    echo "  /work-next   - Implementation workflow"
    echo "  /orchestrate - Task orchestration"
    echo "  /search-work - Search across issue tracker/docs/Git"
    echo "  /plato       - Prompt purification pipeline"
    echo ""
    echo "You can also use the following skills:"
    echo "  /socratize   - Multi-agent consensus building via Socratic dialogue"
    echo "  /brainstorm  - Alias for /socratize"
    echo "  /research    - LLM Council multi-model research (Claude, GPT, Gemini, Sonar)"
    echo "  /concilize   - Hybrid Socratic deliberation + LLM Council research"
    echo "  /skill-creator   - Create new skills for your workflow"
    echo "  /webapp-testing  - Web application testing utilities"
    echo "  /document-skills - Document and manage your skills"
    echo ""
    echo "Note: You may need to restart Claude Code for changes to take effect."
else
    echo -e "${RED}Setup completed with $error_count errors.${NC}"
    echo "Please review the errors above and try running the script again."
    exit 1
fi
