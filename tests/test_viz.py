from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_chroma import Chroma

from tintinallis.viz import embedding_figure


def _store(tmp_path, n):
    docs = [Document(page_content=f"chunk {i}", metadata={"section": f"s{i % 2}"}) for i in range(n)]
    return Chroma.from_documents(docs, DeterministicFakeEmbedding(size=32), persist_directory=str(tmp_path / "db"))


def test_figure_traces(tmp_path):
    fig = embedding_figure(_store(tmp_path, 8))
    assert {t.name for t in fig.data} == {"s0", "s1"}


def test_small_store_empty_figure(tmp_path):
    fig = embedding_figure(_store(tmp_path, 2))
    assert len(fig.data) == 0 and fig.layout.title.text
