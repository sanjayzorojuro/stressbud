from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class StressCategory(str, Enum):
    SOS = "sos"
    PRESSURE = "pressure"
    SYLLABUS = "syllabus"
    GENERAL = "general"

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    reply: str
    category: StressCategory
    session_id: str
    resources: Optional[List[dict]] = []
    is_crisis: bool = False