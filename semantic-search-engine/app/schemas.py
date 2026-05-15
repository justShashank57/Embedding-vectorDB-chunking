from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = 5
    source: str | None = None
    page: int | None = None
    max_distance: float = 0.7


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