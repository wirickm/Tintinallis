# CLAUDE.md

Guidance for Claude Code when working in this repository. User-facing usage is in README.md.

## Project

RAG pipeline over the Tintinalli's Emergency Medicine textbook: PDF text is extracted per section, summarized with `gpt-4o-mini`, embedded into a Chroma vector database, and queried from a Gradio chat app.

## Layout

- `tintinallis/` - the package (run with `python -m tintinallis <command>`)
  - `cli.py` - subcommands `extract`, `summarize`, `index`, `app`, `all`
  - `config.py` - paths (`data/raw`, `data/summaries`, `vector_db/`, `data/chat_log.csv`), model, system prompt; loads `.env` from the repo root
  - `sections.py` - section names to PDF page ranges
  - `extract.py`, `summarize.py` (5000 char chunks), `index.py` (3000 char chunks, 400 overlap), `rag.py`, `app.py`, `viz.py` (3D t-SNE)
- `tests/` - pytest suite using fake embeddings and chat models; no API key or network needed
- `data/raw/`, `data/summaries/` - generated data (tracked), do not hand edit. Only Section 1 exists so far (source PDF not in repo)
- `notebooks/` - original notebooks, kept for reference only

## Commands

```bash
pip install -r requirements.txt
python -m pytest -q
```

`OPENAI_API_KEY` must be set in `.env` (see `.env.example`) for summarize, index and app. The app also reads optional `GRADIO_SERVER_NAME` and `GRADIO_SERVER_PORT`.

## Conventions

- Build paths from `config.ROOT`; never hardcode absolute paths
- Run `python -m pytest -q` before committing
- Local files are gitignored: `.env`, `vector_db/`, `data/chat_log.csv`, caches
