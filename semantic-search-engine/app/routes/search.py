from app.schemas import SearchRequest, SearchResponse
from app.services.embedding_service import create_embedding
from app.services.vector_db import search_chunks
from app.services.query_cleaner import clean_query
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix = "/api", tags=["Semantic Search"])

router.post("/search", response_model=SearchResponse)
def semantic_search(payload: SearchRequest):
    cleaned_query = clean_query(payload.query)
    
    if not cleaned_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    query_embedding = create_embedding(cleaned_query)

    results = search_chunks(
        query_embedding=query_embedding,
        top_k=payload.top_k,
        source=payload.source,
        page=payload.page,
        max_distance=payload.max_distance
    )

    return SearchResponse(
        query=payload.query,
        total_results=len(results),
        results=results
    )

