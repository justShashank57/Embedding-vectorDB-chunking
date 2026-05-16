from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(PROJECT_ROOT / ".env", BASE_DIR / ".env"),
        extra="ignore",
    )

    OPENAI_API_KEY: str
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHUNKS_FILE: str = str(PROJECT_ROOT / "pdf-chunker" / "output" / "chunks.json")
    CHROMA_DB_PATH: str = str(BASE_DIR / "chroma_db")
    COLLECTION_NAME: str = "pdf_chunks"


settings = Settings()
