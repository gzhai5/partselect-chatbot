from fastapi import HTTPException
from loguru import logger
from datetime import datetime
from app.message.database.message_database import message_database
from app.message.model.message_model import MessageModel
from app.conversation.conversation_service import conversation_service


class MessageService:
    def __init__(self):
        self.db = message_database

    def send_message(self, id: str, sessionId: str, sender: str, content:str, action: any, timestamp: datetime):
        new_message = MessageModel(
            **{
                "_id": id,
                "sessionId": sessionId,
                "sender": sender,
                "content": content,
                "action": action,
                "timestamp": timestamp,
            }
        )
        message_in_db = self.db.add_message(new_message)
        message_in_db.pop("_id", None)
        conversation_service.upsert_conversation_messages(sessionId, [message_in_db])
        return message_in_db
    

message_service = MessageService()