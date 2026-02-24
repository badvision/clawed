#!/bin/bash

# Setup script for document-skills
# Creates a Python virtual environment and installs all required dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Setting up document-skills environment..."

# Create Python virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the document-skills Python environment:"
echo "  source ~/.claude/skills/document-skills/.venv/bin/activate"
echo ""
echo "Or for one-off commands:"
echo "  ~/.claude/skills/document-skills/.venv/bin/python3 -m markitdown file.pptx"
echo ""
