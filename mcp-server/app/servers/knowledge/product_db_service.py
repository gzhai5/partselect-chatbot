from pymongo import MongoClient
from typing import Optional
from loguru import logger
from app.config import settings


class ProductDatabase:

    def __init__(self):
        self.error_address = "Product Database"
        self.client = MongoClient(settings.mongo_uri)
        self.db = self.client["Product"]
        self.collections = self.db["Parts"]

    def find_product_by_number(self, partselect_number: str) -> Optional[dict]:
        partselect_number = partselect_number.strip().upper()
        logger.info(f"Looking up product by number: {repr(partselect_number)}")
        product_data = self.collections.find_one({"partselect_number": partselect_number})
        return product_data

product_db = ProductDatabase()