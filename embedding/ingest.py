import json
from pathlib import Path

from config import settings
from embedding_service import create_embeddings_batch
from models import PDFChunk
from vector_db import add_chunks_to_vector_db


BATCH_SIZE = 50


def load_chunks() -> list[PDFChunk]:
    chunks_path = Path(settings.CHUNKS_FILE)

    if not chunks_path.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {chunks_path}. Run Day 1 PDF chunker first."
        )

    with open(chunks_path, "r", encoding="utf-8") as file:
        raw_chunks = json.load(file)

    return [PDFChunk.model_validate(chunk) for chunk in raw_chunks]


def batch_items(items: list[PDFChunk], batch_size: int):
    for index in range(0, len(items), batch_size):
        yield items[index:index + batch_size]


def main():
    chunks = load_chunks()

    if not chunks:
        print("No chunks found.")
        return

    print(f"Loaded {len(chunks)} chunks")

    total_added = 0

    for batch_index, chunk_batch in enumerate(batch_items(chunks, BATCH_SIZE), start=1):
        texts = [chunk.text for chunk in chunk_batch]

        print(f"Embedding batch {batch_index} with {len(chunk_batch)} chunks...")

        embeddings = create_embeddings_batch(texts)

        add_chunks_to_vector_db(
            chunks=chunk_batch,
            embeddings=embeddings,
        )

        total_added += len(chunk_batch)
        print(f"Added {total_added}/{len(chunks)} chunks")

    print("Ingestion complete.")


if __name__ == "__main__":
    main()