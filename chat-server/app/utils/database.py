from pymongo import MongoClient
from loguru import logger
from app.config import settings


# Connect to the MongoDB server & check the connection
def test_mongodb_connection():
    try:
        client = MongoClient(settings.mongo_uri)
        info = client.server_info()
        logger.info("INFO: Database connected successfully")
    except Exception as e:
        logger.error(f"ERROR: Database connection failed: {e}")
        raise e