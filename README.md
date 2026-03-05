# Job Hunting AI Helper

A Streamlit app that analyzes your resume against a job description using AI, providing actionable feedback and a match score.\
Not with just Claude anymore, you can use OpenAI-compatible providers like Mistral, OpenRouter, Mammouth and of course OpenAI!

## Features

- Resume analysis with tailored improvement suggestions
- Job match scoring with detailed breakdown
- Built-in Typst editor with live PDF preview, edit your resume and see the result instantly
- Re-score after edits to track your improvement
- Supports `.typ` (Typst) resume format
- **Multi-provider support**: switch between Anthropic, OpenAI, Mistral, Mammouth or OpenRouter, all from the **️️️⚙️ Settings** panel

> **Note:** The AI does not rewrite your resume for you. It provides suggestions: missing keywords, risky gaps, section-level comments, etc. You apply the changes yourself in the editor. Only apply suggestions that genuinely reflect your background and experience.

![Demo](data/examples/gif-for-github.gif)

## Requirements

- Python 3.12+
- [Typst](https://typst.app/) installed
- An API key for your chosen provider

## Setup

```bash
# Install dependencies
pip install uv
uv sync

# Configure environment
cp .env.example .env
# Add your API key to .env (see Environment Variables below)
```

## Usage

```bash
uv run streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

You can set your API key and choose your provider/model from the **Settings** panel in the app.

## API Key Resolution

The app finds your API key in this order for the selected provider:

1. **Streamlit secrets** (`~/.streamlit/secrets.toml`), recommended for deployment
2. **`.env` file**, recommended for local usage
3. **️️️⚙️ Settings panel**, enter it directly in the app

The variable name depends on your selected provider:

| Provider | Variable |
|----------|----------|
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |
| Mammouth | `MAMMOUTH_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |

## Examples

Two example resumes are included in `data/examples/` to help you get started with the Typst format:

| Resume | Preview |
|--------|---------|
| Quant researcher — École Polytechnique, Vitol & SquarePoint Capital | [resume-quant.pdf](data/examples/resume-quant.pdf) |
| Software engineer — MIT, HRT & Anthropic | [resume-tech.pdf](data/examples/resume-tech.pdf) |

Place your own `.typ` resume files in `data/personal/` to use them in the app.

On Streamlit Cloud (or any environment without local file access), use the **Upload Resume** button in the sidebar to upload `.typ` files directly. Uploaded resumes are stored in the session and merged with any local ones.
