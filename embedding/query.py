from embedding_service import create_embedding
from vector_db import search_similar_chunks


def main():
    print("Semantic PDF Search with Metadata Filtering")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if not query:
            continue

        source = input("Filter by source PDF? Leave empty for all: ").strip()
        page_input = input("Filter by page? Leave empty for all: ").strip()

        page = int(page_input) if page_input else None
        source = source if source else None

        query_embedding = create_embedding(query)

        results = search_similar_chunks(
            query_embedding=query_embedding,
            top_k=5,
            source=source,
            page=page,
        )

        print("\nTop results:\n")

        if not results:
            print("No matching chunks found.\n")
            continue

        for index, result in enumerate(results, start=1):
            print("=" * 80)
            print(f"Result #{index}")
            print(f"Source: {result.source}")
            print(f"Page: {result.page}")
            print(f"Chunk: {result.chunk_index}")
            print(f"Distance: {result.distance}")
            print("-" * 80)
            print(result.text[:1000])
            print()

        print("=" * 80)
        print()


if __name__ == "__main__":
    main()