"""Condense extracted text with an OpenAI chat model."""

from pathlib import Path

from .config import MODEL, SUMMARY_DIR, SYSTEM_PROMPT


def chunk_text(text, size=5000):
    """
    Split text into stripped chunks of at most size characters.
    """
    chunks = [text[i:i + size].strip() for i in range(0, len(text), size)]
    return [c for c in chunks if c]


def create_messages(chunk, system_prompt):
    """
    Create the message list for the OpenAI API.
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": chunk},
        {"role": "assistant", "content": "Please retain relevant information from the chunk."},
    ]


def summarize_chunk(chunk, client, model=MODEL):
    """
    Summarize one chunk. Returns an empty string on API errors.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=create_messages(chunk, SYSTEM_PROMPT),
            max_tokens=5000,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""


def summarize_file(raw_path, out_dir=SUMMARY_DIR, client=None):
    """
    Summarize a raw text file and write out_dir/<stem>.md.

    Returns:
        Path: The written markdown file.
    """
    if client is None:
        import openai
        client = openai.OpenAI()
    raw_path = Path(raw_path)
    chunks = chunk_text(raw_path.read_text(encoding="utf-8"))
    summaries = []
    for i, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {i}/{len(chunks)}...")
        summaries.append(summarize_chunk(chunk, client))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{raw_path.stem}.md"
    out_path.write_text("\n\n".join(summaries), encoding="utf-8")
    return out_path
