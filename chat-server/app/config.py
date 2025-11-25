import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    load_dotenv()

    # set up mongodb database connection
    mongo_uri: str = os.getenv("MONGO_URI")

    # set up OpenAI API key
    openai_api_key: str = os.getenv("OPENAI_API_KEY")


settings = Settings()