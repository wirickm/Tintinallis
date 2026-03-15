# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Emergency Medicine Knowledge Extraction and Retrieval System — a RAG (Retrieval Augmented Generation) pipeline that processes the Tintinallis Emergency Medicine textbook PDF to enable semantic search and chat-based queries via a Gradio UI.

## Setup

**Environment variable required:**
```
OPENAI_API_KEY=<your key>
```
Place in a `.env` file at the project root (loaded via `python-dotenv`).

**Install dependencies (no requirements.txt yet — inferred from notebooks):**
```
pip install PyPDF2 openai python-dotenv langchain langchain-openai langchain-chroma gradio numpy scikit-learn plotly matplotlib pandas
```

**Run notebooks:**
```bash
jupyter notebook
```

## Pipeline Architecture

The project is a three-stage Jupyter notebook pipeline:

### Stage 1 — Text Extraction & Summarization (`01_clean.ipynb`)
- Extracts pages 20–74 from the PDF (Section 1: Advanced Airway Support)
- Chunks text into ~5,000-character segments (~26 chunks)
- Sends each chunk to `gpt-4o-mini` for summarization with the system prompt: *"Retain relevant information, ignore chapter/section headers"*
- Outputs `Section 1_summaries.md` and `02_Section 1_summaries.md`

### Stage 2 — Vector Database (`03_clean2.ipynb`)
- Loads the summaries markdown file
- Re-chunks into 3,000-character segments with 400-character overlap (~46 chunks)
- Generates OpenAI embeddings (1,536 dimensions) and persists to `/vector_db` via Chroma
- Visualizes embedding space with t-SNE dimensionality reduction (3D Plotly)

### Stage 3 — Chat Interface (`cleanv3 gradio.ipynb`)
- Loads the persisted Chroma vectorstore from `/vector_db`
- RAG flow: user query → similarity search → top matches as context → ChatGPT response
- Gradio UI with two tabs: **Chat** and **3D Embedding Graph**
- Saves conversation history to CSV

**Data flow:**
```
PDF → extract text → GPT summarize → Markdown
                                         ↓
                               re-chunk + embed → Chroma DB
                                                      ↓
                          user query → similarity search → GPT → response
```

## Known Issues / TODOs

- Hardcoded Windows file paths (`C:/Users/MichaelJWirickJr/...`) in notebooks — must be updated to relative paths when running on other machines
- No `requirements.txt` — should be created
- `cleanv3 gradio.ipynb` has undefined function errors in the last few cells
- Vector DB path (`/vector_db`) may need to be adjusted to a relative path
