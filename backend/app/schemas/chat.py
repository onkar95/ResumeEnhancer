from pydantic import BaseModel, Field
from datetime import datetime


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatReviseRequest(BaseModel):
    message: str