# Tintinallis RAG

Ask questions about the Tintinalli's Emergency Medicine textbook. The text is summarized by GPT, stored in a Chroma vector database, and searched from a Gradio chat app.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then put your OpenAI key in .env
```

## Commands

```bash
python -m tintinallis extract --pdf book.pdf --section "Section 1"   # PDF -> data/raw/section_01.txt
python -m tintinallis summarize --section "Section 1"               # -> data/summaries/section_01.md
python -m tintinallis index                                         # summaries -> vector_db/
python -m tintinallis app                                           # open the chat app
python -m tintinallis all --pdf book.pdf --sections "Section 1" "Section 2"
```

Run tests with `pytest` (no API key needed).

## Flow

```
PDF -> extract -> data/raw/*.txt -> summarize (gpt-4o-mini) -> data/summaries/*.md
    -> index (3000 char chunks, embeddings) -> vector_db/
    -> app: question -> top matches -> GPT answer with sources
```

The original notebooks are in `notebooks/` for reference.
