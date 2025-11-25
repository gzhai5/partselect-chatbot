from pydantic import BaseModel, Field
from datetime import datetime

class ConversationModel(BaseModel):
    sessionId: str | None = Field(default= None, alias= "_id")
    startTime: datetime
    endTime: datetime  | None = Field(default=None, alias="endTime")
    userId: str = Field(default="", alias="userId")
    messages: list[dict] = Field(default_factory=list)
