from types import SimpleNamespace

from tintinallis import summarize


class FakeCompletions:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        content = f"  summary {len(self.calls)}  "
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


def test_chunk_text():
    assert summarize.chunk_text("a" * 12, size=5) == ["aaaaa", "aaaaa", "aa"]
    assert summarize.chunk_text("") == []


def test_create_messages():
    msgs = summarize.create_messages("hello", "sys")
    assert msgs[0] == {"role": "system", "content": "sys"}
    assert msgs[1] == {"role": "user", "content": "hello"}


def test_summarize_chunk():
    client = FakeClient()
    assert summarize.summarize_chunk("text", client) == "summary 1"
    assert client.chat.completions.calls[0]["model"] == summarize.MODEL


def test_summarize_chunk_error_returns_empty():
    def boom(**kwargs):
        raise RuntimeError("fail")
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=boom)))
    assert summarize.summarize_chunk("text", client) == ""


def test_summarize_file(tmp_path):
    raw = tmp_path / "section_01.txt"
    raw.write_text("x" * 12000, encoding="utf-8")
    client = FakeClient()
    out = summarize.summarize_file(raw, out_dir=tmp_path / "sum", client=client)
    assert out.name == "section_01.md"
    assert out.read_text(encoding="utf-8") == "summary 1\n\nsummary 2\n\nsummary 3"
