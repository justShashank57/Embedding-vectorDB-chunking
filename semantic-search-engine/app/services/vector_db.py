import chromadb
from typing import Any

from app.config import settings
from app.schemas import SearchResult

client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)

collection = client.get_or_create_collection(
    name = settings.COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)

def build_where_filter(
    source: str | None = None,
    page: int | None = None
) -> dict[str,Any]:
    filters = []
    if source:
        filters.append({"source":{"$eq": source}})
    if page:
        filters.append({"page": {"$eq": page}})

    if not filters:
        return None
    
    if len(filters) == 1:
        return filters[0]
    
    return {"$and": filters}

def search_chunks(
    query_embedding: list[float],
    top_k: int = 5,
    source: str | None = None,
    page: int | None = None,
    max_distance: float = 0.7
) -> list[SearchResult]:
    where_filter = build_where_filter(source, page)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter,
        include=["documents", "metadatas", "distances"]
    )
    output: list[SearchResult] = []

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for id, doc, meta, dist in zip(ids, documents, metadatas, distances):
        if dist > max_distance:
           continue

        output.append(
            SearchResult(
                id=id,
                text=doc,
                source=meta["source"],
                page=meta["page"],
                chunk_index=meta["chunk_index"],
                distance=round(dist, 4)
            )
        )

    return output