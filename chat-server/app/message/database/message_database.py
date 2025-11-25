from pymongo import MongoClient
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime
from loguru import logger
from app.config import settings
from app.message.model.message_model import MessageModel


class MessageDatabase:

    def __init__(self):
        self.error_address = "Message Database"
        self.client = MongoClient(settings.mongo_uri)
        self.db = self.client["Message"]
        self.collection = self.db["message"]

    def get_message_by_id(self, message_id: str) -> dict:
        try:
            message = self.collection.find_one({"_id": ObjectId(message_id)})
            if message:
                return message
            else:
                logger.error(f"Message with id {message_id} not found")
                raise HTTPException(status_code=404, detail=f"Message with id {message_id} not found")
        except Exception as e:
            logger.error(f"Failed to get message by id: {message_id}, error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def add_message(self, message: MessageModel) -> dict | None:
        try:
            message_dict = message.model_dump()
            logger.debug(f"Adding message: {message_dict}")
            message_dict["_id"] = ObjectId(message_dict["id"])
            insert_res = self.collection.insert_one(message_dict)
            message_id = insert_res.inserted_id
            message_obj = self.collection.find_one({"_id": message_id})
            return message_obj
        except Exception as e:
            logger.error(f"Failed to add message: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    def upsert_message(self, message: MessageModel) -> dict | None:
        try:
            message_dict = message.model_dump()
            if message.id:
                message_id = ObjectId(message.id)
                self.collection.update_one({"_id": message_id}, {"$set": message_dict}, upsert=True)
                logger.info(f"Message with id {message.id} updated successfully")
                message_obj = self.collection.find_one({"_id": message_id})
                return message_obj
            else:
                return self.add_message(message)
        except Exception as e:
            logger.error(f"Failed to upsert message: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_all_messages(self, start_time: datetime, end_time: datetime) -> list[dict]:
        try:
            messages = self.collection.find({
                "timestamp": {
                    "$gte": start_time,
                    "$lte": end_time
                }
            })
            return list(messages)
        except Exception as e:
            logger.error(f"Failed to get all messages: {e}")
            raise HTTPException(status_code=500, detail=str(e))

message_database = MessageDatabase()