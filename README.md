# Job Hunting AI Helper

A Streamlit app that analyzes your resume against a job description using Claude AI, providing actionable feedback and a match score.

## Features

- Resume analysis with tailored improvement suggestions
- Job match scoring with detailed breakdown
- Built-in Typst editor with live PDF preview, edit your resume and see the result instantly
- Re-score after edits to track your improvement
- Supports `.typ` (Typst) resume format

> **Note:** The AI does not rewrite your resume for you. It provides suggestions: missing keywords, risky gaps, section-level comments, etc. You apply the changes yourself in the editor. Only apply suggestions that genuinely reflect your background and experience. 

## Requirements

- Python 3.12+
- [Typst](https://typst.app/) installed
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

```bash
# Install dependencies
pip install uv
uv sync

# Configure environment
cp .env.example .env
# Add your Anthropic API key to .env
```

## Usage

```bash
uv run streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

## Examples

Two example resumes are included in `data/examples/` to help you get started with the Typst format:

| Resume | Preview |
|--------|---------|
| Quant researcher — École Polytechnique, Vitol & SquarePoint Capital | [resume-quant.pdf](data/examples/resume-quant.pdf) |
| Software engineer — MIT, HRT & Anthropic | [resume-tech.pdf](data/examples/resume-tech.pdf) |

Place your own `.typ` resume files in `data/personal/` to use them in the app.
