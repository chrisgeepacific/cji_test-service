# routes.py (hoặc api.py)
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .models import Message, MessageResponse

router = APIRouter()

# Simple in-memory database
messages: dict[int, dict] = {}
message_counter: int = 0


class ServerTimeResponse(BaseModel):
    epoch_ms: int
    iso_utc: str
    iso_server_tz: str
    server_tz: str


@router.get("/messages", tags=["messages"], response_model=List[MessageResponse])
def get_messages():
    """Get all messages"""
    return list(messages.values())


@router.get("/messages/{message_id}", tags=["messages"], response_model=MessageResponse)
def get_message(message_id: int):
    """Get a specific message by ID"""
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    return messages[message_id]


@router.post("/messages", tags=["messages"], status_code=201, response_model=MessageResponse)
def create_message(message: Message):
    """Create a new message"""
    global message_counter
    message_counter += 1

    new_message = {
        "id": message_counter,
        "content": message.content,
        "timestamp": datetime.now().isoformat()
    }
    messages[message_counter] = new_message
    return new_message


@router.delete("/messages/{message_id}", tags=["messages"], status_code=204)
def delete_message(message_id: int):
    """Delete a message"""
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")

    del messages[message_id]
    return None


@router.get("/public/check-time", tags=["system"], response_model=ServerTimeResponse)
def public_check_time():
    """Return server time (UTC and server TZ)."""
    now_utc = datetime.now(timezone.utc)
    now_server = datetime.now().astimezone()  # timezone của máy chủ

    return {
        "epoch_ms": int(now_utc.timestamp() * 1000),
        "iso_utc": now_utc.isoformat(),
        "iso_server_tz": now_server.isoformat(),
        "server_tz": str(now_server.tzinfo),
    }
