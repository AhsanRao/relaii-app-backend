from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class ChatInput(BaseModel):
    message: str
    subject: str

class ChatResponse(BaseModel):
    messages: List[Message]