"""Extract text from the textbook PDF."""

from pathlib import Path

import PyPDF2

from .config import RAW_DIR
from .sections import page_range, slug


def extract_section(pdf_path, start, end):
    """
    Extract text from a range of pages in a PDF.

    Args:
        pdf_path (str or Path): Path to the PDF file.
        start (int): Starting page number (1-based).
        end (int or None): Ending page number. If None, extracts to the end.

    Returns:
        str: Extracted text.
    """
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        if end is None:
            end = len(reader.pages)
        text = ""
        for page_num in range(start - 1, min(end, len(reader.pages))):
            page_text = reader.pages[page_num].extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                print(f"Warning: No text found on page {page_num + 1}")
        return text


def extract_to_file(pdf_path, section, out_dir=RAW_DIR):
    """
    Extract a named section and save it as out_dir/<slug>.txt.

    Returns:
        Path: The written text file.
    """
    start, end = page_range(section)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug(section)}.txt"
    out_path.write_text(extract_section(pdf_path, start, end), encoding="utf-8")
    return out_path
