from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
      model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

      OPENAI_API_KEY: str
      OPENAI_EMBEDDING_MODEL: str = 'text-embedding-3-small'

      CHUNKS_FILE: str = "output/chunks.json"
      CHROMA_DB_PATH: str = "chroma_db"
      COLLECTION_NAME: str = "pdf_chunks"

settings = Settings()
