from tintinallis import extract


class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class FakeReader:
    def __init__(self, f):
        self.pages = [FakePage(f"page {i}") for i in range(1, 6)]


def make_pdf(tmp_path, monkeypatch):
    monkeypatch.setattr(extract.PyPDF2, "PdfReader", FakeReader)
    pdf = tmp_path / "book.pdf"
    pdf.write_bytes(b"%PDF-fake")
    return pdf


def test_extract_section_range(tmp_path, monkeypatch):
    pdf = make_pdf(tmp_path, monkeypatch)
    assert extract.extract_section(pdf, 2, 3) == "page 2\npage 3\n"


def test_extract_section_to_end(tmp_path, monkeypatch):
    pdf = make_pdf(tmp_path, monkeypatch)
    assert extract.extract_section(pdf, 4, None) == "page 4\npage 5\n"


def test_extract_real_blank_pdf(tmp_path):
    from PyPDF2 import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    pdf = tmp_path / "blank.pdf"
    with open(pdf, "wb") as f:
        writer.write(f)
    assert extract.extract_section(pdf, 1, None) == ""


def test_extract_to_file(tmp_path, monkeypatch):
    pdf = make_pdf(tmp_path, monkeypatch)
    monkeypatch.setattr(extract, "page_range", lambda name: (1, 2))
    out = extract.extract_to_file(pdf, "Section 1", out_dir=tmp_path / "raw")
    assert out.name == "section_01.txt"
    assert out.read_text(encoding="utf-8") == "page 1\npage 2\n"
