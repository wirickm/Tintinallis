"""Build and load the Chroma vector store from section summaries."""

from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

from tintinallis.config import DB_DIR, SUMMARY_DIR


def load_chunks(summary_dir=SUMMARY_DIR):
    """Load every summary .md file and split it into 3000-char chunks."""
    splitter = CharacterTextSplitter(chunk_size=3000, chunk_overlap=400)
    docs = []
    for path in sorted(Path(summary_dir).glob("*.md")):
        text = path.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"section": path.stem}))
    return splitter.split_documents(docs)


def _embeddings(embeddings):
    if embeddings is None:
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()
    return embeddings


def build_index(summary_dir=SUMMARY_DIR, db_dir=DB_DIR, embeddings=None):
    """Embed all summary chunks into a fresh Chroma store at db_dir."""
    from langchain_chroma import Chroma

    embeddings = _embeddings(embeddings)
    db_dir = Path(db_dir)
    if db_dir.exists():
        Chroma(persist_directory=str(db_dir), embedding_function=embeddings).delete_collection()
    chunks = load_chunks(summary_dir)
    if not chunks:
        raise ValueError(f"No summary files found in {summary_dir}")
    return Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=str(db_dir))


def load_index(db_dir=DB_DIR, embeddings=None):
    """Open the persisted Chroma store."""
    from langchain_chroma import Chroma

    return Chroma(persist_directory=str(db_dir), embedding_function=_embeddings(embeddings))
