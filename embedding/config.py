from pydantic_settings import BaseSettings

class Settings(BaseSettings):
      OPENAI_API_KEY: str
      OPENAI_EMBEDDING_MODEL: str = 'text-embedding-3-small'

      CHUNKS_FILE: str = "output/chunks.json"
      CHROMA_DB_PATH: str = "chroma_db"
      COLLECTION_NAME: str = "pdf_chunks"

      class config:
            env_file = "C:\Users\SHASHANK\Desktop\Current Projects\Python\Embedding-vectorDB-chunking\.env"

settings = Settings()