import pytest

from tintinallis.sections import SECTIONS, page_range, slug


def test_slug():
    assert slug("Section 1") == "section_01"
    assert slug("Section 22") == "section_22"
    assert slug("Index") == "index"


def test_page_range():
    assert page_range("Section 1") == (20, 74)
    assert page_range("Index") == (946, None)
    assert len(SECTIONS) == 23


def test_unknown_section():
    with pytest.raises(KeyError):
        slug("Section 99")
