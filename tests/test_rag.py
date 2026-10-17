import csv

from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_chroma import Chroma

from tintinallis.rag import answer, build_prompt, log_chat, retrieve


def _store(tmp_path):
    docs = [Document(page_content=f"chunk {i}", metadata={"section": f"section_0{i}"}) for i in range(5)]
    return Chroma.from_documents(docs, DeterministicFakeEmbedding(size=32), persist_directory=str(tmp_path / "db"))


def test_retrieve_and_answer(tmp_path):
    store = _store(tmp_path)
    assert len(retrieve(store, "chunk 1", k=2)) == 2
    text, docs = answer("q?", store, llm=FakeListChatModel(responses=["hi"]))
    assert text == "hi" and len(docs) == 4


def test_build_prompt():
    msgs = build_prompt("what?", [Document(page_content="ctx", metadata={"section": "s1"})],
                        history=[{"role": "user", "content": "a"}])
    assert msgs[0]["role"] == "system" and "ctx" in msgs[0]["content"]
    assert "not" in msgs[0]["content"].lower()
    assert msgs[-1] == {"role": "user", "content": "what?"} and len(msgs) == 3


def test_log_chat(tmp_path):
    p = tmp_path / "log.csv"
    log_chat("q1", "a1", p)
    log_chat("q2", "a2", p)
    rows = list(csv.reader(p.open()))
    assert rows[0] == ["timestamp", "question", "answer"]
    assert rows[2][1:] == ["q2", "a2"]
