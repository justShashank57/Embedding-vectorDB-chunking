from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def create_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model=settings.OPENAI_EMBEDDING_MODEL,
    )
    return response.data[0].embedding


def create_embeddings_batch(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=texts,
    )

    return [item.embedding for item in response.data]
