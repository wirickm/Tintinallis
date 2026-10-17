# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Emergency Medicine Knowledge Extraction and Retrieval System: a RAG pipeline over the Tintinallis Emergency Medicine textbook PDF, with semantic search and chat through a Gradio UI.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # set OPENAI_API_KEY
```

## Commands

```bash
python -m tintinallis extract --pdf book.pdf --section "Section 1"
python -m tintinallis summarize --section "Section 1"
python -m tintinallis index
python -m tintinallis app
python -m tintinallis all --pdf book.pdf --sections "Section 1" "Section 2"
pytest            # uses fakes, never calls OpenAI
```

## Layout

- `tintinallis/config.py`: paths (all relative to repo root), `MODEL`, `SYSTEM_PROMPT`
- `tintinallis/sections.py`: section page ranges, `slug()` ("Section 1" -> `section_01`)
- `tintinallis/extract.py`: PDF pages -> `data/raw/<slug>.txt`
- `tintinallis/summarize.py`: 5,000-char chunks -> gpt-4o-mini summaries -> `data/summaries/<slug>.md`
- `tintinallis/index.py`: 3,000-char chunks, 400 overlap, metadata `section` -> Chroma in `vector_db/`
- `tintinallis/rag.py`: retrieve, prompt (answer only from context), answer, chat CSV log (`data/chat_log.csv`)
- `tintinallis/viz.py`: 3D t-SNE plot of embeddings colored by section
- `tintinallis/app.py`: Gradio app with "Chat" and "3D Embeddings" tabs
- `tintinallis/cli.py`: argparse entry point
- `notebooks/`: original exploratory notebooks, kept for reference only
- `tests/`: pytest suite with fake embeddings and LLM

**Data flow:**
```
PDF -> extract -> data/raw -> summarize -> data/summaries -> index -> vector_db
                                     user query -> similarity search -> GPT -> answer + sources
```

## Notes

- Only Section 1 has been extracted and summarized so far.
- The notebooks still contain old hardcoded Windows paths; use the package instead.
