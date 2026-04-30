from pydantic import BaseModel

class PdfChunk(BaseModel):
    id: str
    source: str
    page: int
    chunk_index: int
    text: str