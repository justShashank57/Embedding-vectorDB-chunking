from pathlib import Path
from models import PdfChunk

def chunk_words(
        text: str,
        chunk_size: int = 300,
        overlap: int = 60
) -> list[str]:
    words = text.split()
    if not words:
        return []
    
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        if end >= len(words):
            break
        start = end - overlap
    return chunks

def create_chunks_for_pdf(
    pdf_path: Path,
    pages: list[dict],
    chunk_size: int = 300,
    overlap: int = 60
    ) -> list[PdfChunk]:
    all_chunks = []
    source_name = pdf_path.name

    for page_data in pages:
        page_number = page_data["page"]
        page_text = page_data["text"]

        page_chunks = chunk_words(text=page_text, chunk_size=chunk_size, overlap=overlap)
        for chunk_index, chunk_text in enumerate(page_chunks):
            chunk_id = f"{source_name}_page{page_number}_chunk{chunk_index}"
            all_chunks.append(
                PdfChunk(
                    id=chunk_id,
                    source=source_name,
                    text=chunk_text,
                    page=page_number,
                    chunk_index=chunk_index
                ))
    return all_chunks
