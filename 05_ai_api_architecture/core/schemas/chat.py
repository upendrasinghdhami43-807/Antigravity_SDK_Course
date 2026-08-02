from pydantic import BaseModel

class ChatResponse(BaseModel):
    message: str
    role: str
    timestamp: str
