from pydantic import BaseModel, Field


class Message(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)


class MessageResponse(BaseModel):
    id: int
    content: str
    timestamp: str