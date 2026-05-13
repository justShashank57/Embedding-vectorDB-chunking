from typing import Any
import chromadb
from config import settings
from models import PDFChunk, SearchResult

client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)

collection = client.get_or_create_collection(
    name=settings.COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
    )

def add_chunks_to_vector_db(
    chunks: list[PDFChunk],
    embeddings: list[list[float]]
) -> None:
    # using batching here to optimize the upsert operation
    ids = [chunk.id for chunk in chunks]
    documents = [chunk.text for chunk in chunks]
    metadatas: list[dict[str, Any]] = [
        {
            "source": chunk.source,
            "page": chunk.page,
            "chunk_index": chunk.chunk_index
        }
        for chunk in chunks
    ]
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

def search_similar_chunks(
    query_embedding: list[float],
    top_k: int = 5,
    source: str | None = None,
    page: int | None = None,
) -> list[SearchResult]:
    where_filter = {}

    if source and page:
        where_filter = {
            "$and": [
                {"source": {"$eq": source}},
                {"page": {"$eq": page}},
            ]
        }
    elif source:
        where_filter = {"source": {"$eq": source}}
    elif page:
        where_filter = {"page": {"$eq": page}}

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter if where_filter else None,
        include=["documents", "metadatas", "distances"],
    )

    search_results: list[SearchResult] = []

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for item_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):
        search_results.append(
            SearchResult(
                id=item_id,
                text=document,
                source=metadata["source"],
                page=metadata["page"],
                chunk_index=metadata["chunk_index"],
                distance=distance,
            )
        )

    return search_results