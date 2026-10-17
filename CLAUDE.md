# CLAUDE.md

Dev guidance for Claude Code in this repo. See README.md for setup and usage commands.

## Layout

- `tintinallis/` - pipeline package (`python -m tintinallis <extract|summarize|index|app|all>`, see `cli.py`)
  - `config.py` holds all paths (`data/raw`, `data/summaries`, `vector_db/`, `data/chat_log.csv`), the model (`gpt-4o-mini`) and the summarize system prompt
  - `extract.py` PDF -> text, `sections.py` section page ranges and slugs, `summarize.py` GPT summaries, `index.py` Chroma build, `rag.py` retrieval + answer, `viz.py` t-SNE plot, `app.py` Gradio UI
- `tests/` - pytest suite, mocks OpenAI so no API key is needed
- `data/raw/`, `data/summaries/` - generated pipeline data (tracked; treat as data, do not hand-edit). Only Section 1 is extracted so far (source PDF not in repo)
- `notebooks/` - original exploratory notebooks, kept for reference only; do not maintain them

## Conventions

- `OPENAI_API_KEY` comes from `.env` (see `.env.example`), loaded in `config.py`
- All paths are relative to the repo root via `config.ROOT`; do not hardcode absolute paths
- Run `python -m pytest -q` before committing
- Generated/local files are gitignored: `.env`, `vector_db/`, `data/chat_log.csv`, caches
