from datetime import datetime
from pydantic import BaseModel


class ConversationRequest(BaseModel):
    startTime: datetime
    userId: str

class ConversationFeedbackRequest(BaseModel):
    sessionId: str
    feedbackRating: int
    feedbackComment: str

class HumanEscalationRequest(BaseModel):
    sessionId: str
    method: str
    lastUserMsgId: str
    lastBotMsgId: str