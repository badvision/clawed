# Document Skills

Official Anthropic skills for working with office document formats (PDF, DOCX, PPTX, XLSX).

## Quick Setup

The document skills require Python dependencies. Run the setup script to create a virtual environment with all required packages:

```bash
cd ~/.claude/skills/document-skills
./setup.sh
```

This creates a `.venv` directory with all Python dependencies installed.

## Usage

### Option 1: Activate the virtual environment (for multiple commands)

```bash
source ~/.claude/skills/document-skills/.venv/bin/activate
python3 -m markitdown presentation.pptx
```

### Option 2: One-off commands (recommended for Claude)

```bash
~/.claude/skills/document-skills/.venv/bin/python3 -m markitdown file.pptx
```

## Python Dependencies

The following Python packages are installed in the virtual environment:

**All formats:**
- **markitdown** - Extract text from various document formats
- **defusedxml** - Secure XML parsing

**PPTX (PowerPoint):**
- **python-pptx** - Create and edit PowerPoint presentations

**XLSX (Excel):**
- **pandas** - Data analysis and manipulation
- **openpyxl** - Excel file handling with formula support

**PDF:**
- **pypdf** - PDF manipulation (merge, split, rotate)
- **pdfplumber** - Text and table extraction
- **reportlab** - PDF creation
- **pytesseract** - OCR for scanned PDFs (requires tesseract system package)
- **pdf2image** - Convert PDF pages to images

Plus supporting dependencies (lxml, Pillow, numpy, etc.)

## Skills Included

- **pptx/** - PowerPoint creation, editing, and analysis
- **docx/** - Word document handling
- **pdf/** - PDF operations
- **xlsx/** - Excel spreadsheet handling

See individual skill folders for detailed documentation.

## Node.js Dependencies

Some features (like html2pptx) require Node.js packages. These should be installed globally:

```bash
npm install -g pptxgenjs playwright react-icons react react-dom sharp
```

## System Dependencies

- **LibreOffice** - For PDF conversion (optional)
- **Poppler** - For PDF to image conversion (optional)

macOS:
```bash
brew install poppler
brew install --cask libreoffice
```

Linux:
```bash
sudo apt-get install libreoffice poppler-utils
```

## Maintenance

To update Python dependencies:

```bash
source ~/.claude/skills/document-skills/.venv/bin/activate
pip install --upgrade -r requirements.txt
```

To recreate the environment from scratch:

```bash
rm -rf ~/.claude/skills/document-skills/.venv
cd ~/.claude/skills/document-skills
./setup.sh
```
