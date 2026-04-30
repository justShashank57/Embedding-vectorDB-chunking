from pathlib import Path
from pypdf import PdfReader
from text_cleaner import clean_text

def extract_pdf_pages(pdf_path: Path) -> list[dict]:
    reader = PdfReader(str(pdf_path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        raw_text = page.extract_text() or ""
        cleaned_text = clean_text(raw_text)

        if cleaned_text:
            pages.append({
                "page": index,
                "text": cleaned_text
            })
    return pages