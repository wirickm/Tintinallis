import gradio as gr
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_chroma import Chroma

from tintinallis.app import build_app


def test_build_app_returns_blocks(tmp_path):
    store = Chroma.from_documents([Document(page_content="x", metadata={"section": "s"})],
                                  DeterministicFakeEmbedding(size=32), persist_directory=str(tmp_path / "db"))
    assert isinstance(build_app(store, llm=FakeListChatModel(responses=["ok"])), gr.Blocks)
