from pydantic import BaseModel
from typing import List
import uuid

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatChoice(BaseModel):
    message: ChatMessage

class ChatUsage(BaseModel):
    input_tokens: int
    output_tokens: int

class ChatResponse(BaseModel):
    id: str
    model: str
    choices: List[ChatChoice]
    usage: ChatUsage
