import pytest

from tintinallis import cli


@pytest.mark.parametrize("argv,func,attrs", [
    (["extract", "--pdf", "a.pdf", "--section", "Index"], "cmd_extract", {"pdf": "a.pdf", "section": "Index"}),
    (["summarize", "--section", "Index"], "cmd_summarize", {"section": "Index"}),
    (["index"], "cmd_index", {}),
    (["app"], "cmd_app", {}),
    (["all", "--pdf", "a.pdf", "--sections", "A", "B"], "cmd_all", {"sections": ["A", "B"]}),
])
def test_dispatch(monkeypatch, argv, func, attrs):
    called = []
    monkeypatch.setattr(cli, func, lambda args: called.append(args))
    cli.main(argv)
    assert len(called) == 1
    for k, v in attrs.items():
        assert getattr(called[0], k) == v


def test_requires_command():
    with pytest.raises(SystemExit):
        cli.main([])
