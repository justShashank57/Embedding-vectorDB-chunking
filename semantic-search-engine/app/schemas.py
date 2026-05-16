from pydantic import BaseModel, Field


class PDFChunk(BaseModel):
    id: str
    source: str
    page: int
    text: str
    chunk_index: int


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=5, ge=1, le=20)
    source: str | None = None
    page: int | None = Field(default=None, ge=1)
    max_distance: float = Field(default=0.7, ge=0)


class SearchResult(BaseModel):
    id: str
    text: str
    source: str
    page: int
    chunk_index: int
    distance: float


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResult]
