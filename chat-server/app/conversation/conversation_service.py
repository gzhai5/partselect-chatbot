from fastapi import HTTPException
from datetime import datetime
from loguru import logger
from app.conversation.model.conversation_model import ConversationModel
from app.conversation.database.conversation_database import conversation_database


class ConversationService:
    def __init__(self):
        self.db = conversation_database

    def start_conversation(self, startTime: datetime, userId: str):
        new_conversation = ConversationModel(
            startTime=startTime,
            userId=userId,
        )
        conversation_in_db = self.db.add_conversation(new_conversation)
        conversation_in_db.pop("_id", None)
        return conversation_in_db

    def end_conversation_from_api(self, sessionId: str):
        conversation = self.db.get_conversation_by_id(sessionId)
        if not conversation:
            raise HTTPException(status_code=404, detail=f"Conversation with id {sessionId} not found")
        conversation["endTime"] = datetime.now()
        conversation["_id"] = str(conversation["_id"])
        conversation_in_db = self.db.upsert_conversation(ConversationModel(**conversation))
        conversation_in_db.pop("_id", None)
        return conversation_in_db


    def end_conversation_from_ws(self, sessionId: str):

        # Retrieving the old conversation by sessionId
        conversation = self.db.get_conversation_by_id(sessionId)
        if not conversation:
            raise HTTPException(status_code=404, detail=f"Conversation with id {sessionId} not found")
        conversation["_id"] = str(conversation["_id"])
        
        # Updating the endTime
        conversation["endTime"] = datetime.now()
        self.db.upsert_conversation(ConversationModel(**conversation))

    def upsert_conversation_messages(self, sessionId: str, messages: list):
        conversation = self.db.get_conversation_by_id(sessionId)
        if not conversation:
            raise HTTPException(status_code=404, detail=f"Conversation with id {sessionId} not found")
        
        if "messages" not in conversation or not isinstance(conversation["messages"], list):
            raise HTTPException(status_code=400, detail="Conversation does not have a valid messages field")

        conversation["messages"].extend(messages)
        conversation["_id"] = sessionId
        conversation_in_db = self.db.upsert_conversation(ConversationModel(**conversation))
        conversation_in_db.pop("_id", None)
        return conversation_in_db


conversation_service = ConversationService()