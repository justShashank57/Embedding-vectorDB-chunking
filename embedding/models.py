from pydantic import BaseModel

class PDFChunk(BaseModel):
    id: str
    source: str
    page: int
    text: str
    chunk_index: int

class SearchResult(BaseModel):
    id: str
    source: str
    page: int
    text: str
    chunk_index: int
    distance: float