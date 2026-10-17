"""Retrieval augmented question answering over the vector store."""

import csv
from datetime import datetime
from pathlib import Path

from tintinallis.config import CHAT_LOG, MODEL

INSTRUCTIONS = (
    "You are an emergency medicine assistant. Answer the question using only the "
    "context below from Tintinalli's Emergency Medicine summaries. If the answer is "
    "not in the context, say you could not find it in the provided material."
)


def retrieve(store, query, k=4):
    """Return the k most similar chunks for the query."""
    return store.similarity_search(query, k=k)


def _text(content):
    """Flatten Gradio message content (str or list of parts) to plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return str(content.get("text", ""))
    if isinstance(content, (list, tuple)):
        return " ".join(t for t in (_text(c) for c in content) if t)
    return "" if content is None else str(content)


def build_prompt(query, docs, history=None):
    """Build chat messages with the retrieved context and the question."""
    context = "\n\n".join(
        f"[{d.metadata.get('section', 'unknown')}]\n{d.page_content}" for d in docs
    )
    messages = [{"role": "system", "content": f"{INSTRUCTIONS}\n\nContext:\n{context}"}]
    for turn in history or []:
        if isinstance(turn, dict) and turn.get("role") in ("user", "assistant"):
            messages.append({"role": turn["role"], "content": _text(turn.get("content"))})
    messages.append({"role": "user", "content": query})
    return messages


def answer(query, store, llm=None, history=None):
    """Answer a question and return (text, source docs)."""
    if llm is None:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model=MODEL)
    docs = retrieve(store, query)
    response = llm.invoke(build_prompt(query, docs, history))
    return getattr(response, "content", str(response)), docs


def log_chat(question, answer_text, path=CHAT_LOG):
    """Append a timestamp,question,answer row to the chat log CSV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp", "question", "answer"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), question, answer_text])
