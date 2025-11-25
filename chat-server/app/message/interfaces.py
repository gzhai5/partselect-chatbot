from datetime import datetime
from pydantic import BaseModel


class MessageStoreRequest(BaseModel):
    id: str
    sessionId: str
    sender: str
    content: str
    action: dict | None = None
    timestamp: datetime