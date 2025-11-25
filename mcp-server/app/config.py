import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    load_dotenv()

    # set up mongodb database connection
    mongo_uri: str = os.getenv("MONGO_URI")

    # AI
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY")
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"
    OPENAI_MODEL: str = "gpt-4o-mini"
    MILVUS_COLLECTION_NAME: str = "knowledge_base"

settings = Settings()