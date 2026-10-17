from langchain_core.embeddings import DeterministicFakeEmbedding

from tintinallis.index import build_index, load_chunks, load_index


def _write(d):
    d.mkdir()
    (d / "section_01.md").write_text(("Airway management text. " * 50 + "\n\n") * 6)
    (d / "section_02.md").write_text("Shock and resuscitation.")
    return d


def test_load_chunks_metadata(tmp_path):
    chunks = load_chunks(_write(tmp_path / "s"))
    assert len(chunks) > 2
    assert {c.metadata["section"] for c in chunks} == {"section_01", "section_02"}
    assert all(len(c.page_content) <= 3000 for c in chunks)


def test_build_and_load_index(tmp_path):
    emb = DeterministicFakeEmbedding(size=32)
    s = _write(tmp_path / "s")
    db = tmp_path / "db"
    n = build_index(s, db, emb)._collection.count()
    assert build_index(s, db, emb)._collection.count() == n
    assert load_index(db, emb)._collection.count() == n
