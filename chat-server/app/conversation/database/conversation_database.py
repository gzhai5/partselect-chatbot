from pymongo import MongoClient
from bson import ObjectId
from fastapi import HTTPException
from loguru import logger
from app.config import settings
from datetime import datetime
from app.conversation.model.conversation_model import ConversationModel


class ConversationDatabase:

    def __init__(self):
        self.error_address = "Conversation Database"
        self.client = MongoClient(settings.mongo_uri)
        self.db = self.client["Conversation"]
        self.collection = self.db["conversation"]

    def get_conversation_by_id(self, session_id: str) -> dict:
        try:
            conversation = self.collection.find_one({"_id": ObjectId(session_id)})
            if conversation:
                return conversation
            else:
                logger.error(f"Conversation with id {session_id} not found")
                raise HTTPException(status_code=404, detail=f"Conversation with id {session_id} not found")
        except Exception as e:
            logger.error(f"Failed to get conversation by id: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def add_conversation(self, conversation: ConversationModel) -> dict | None:
        try:
            conversation_dict = conversation.model_dump()
            conversation_id = ObjectId()
            conversation_dict["_id"] = conversation_id
            conversation_dict["sessionId"] = str(conversation_id)
            insert_res = self.collection.insert_one(conversation_dict)
            conversation_id = insert_res.inserted_id
            conversation_obj = self.collection.find_one({"_id": conversation_id})
            return conversation_obj
        except Exception as e:
            logger.error(f"Failed to add conversation: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    def upsert_conversation(self, conversation: ConversationModel) -> dict | None:
        try:
            conversation_dict = conversation.model_dump()
            if conversation.sessionId:
                session_id = ObjectId(conversation.sessionId)
                self.collection.update_one({"_id": session_id}, {"$set": conversation_dict}, upsert=True)
                logger.info(f"Conversation with id {conversation.sessionId} updated successfully")
                conversation_obj = self.collection.find_one({"_id": session_id})
                return conversation_obj
            else:
                return self.add_conversation(conversation)
        except Exception as e:
            logger.error(f"Failed to upsert conversation: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    def update_conversation_failure(self, session_id: str, failure: str, failure_reason: str | None = None) -> dict | None:
        try:
            session_id_obj = ObjectId(session_id)
            update_data = {"$set": {"failure": failure}}
            if failure_reason is not None:
                update_data["$set"]["failureReason"] = failure_reason
            self.collection.update_one({"_id": session_id_obj}, update_data)
            updated_conversation = self.collection.find_one({"_id": session_id_obj})
            return updated_conversation
        except Exception as e:
            logger.error(f"Failed to update conversation failure: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_all_conversations(self, start_time: datetime, end_time: datetime) -> list[dict]:
        try:
            conversations = self.collection.find({
                "endTime": {"$gte": start_time, "$lte": end_time}
            })
            return list(conversations)
        except Exception as e:
            logger.error(f"Failed to get all conversations: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        

conversation_database = ConversationDatabase()