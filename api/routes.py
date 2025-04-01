from datetime import datetime
from fastopenapi.routers import FlaskRouter
from .models import Message, MessageResponse

router = FlaskRouter()

# Simple in-memory database
messages = {}
message_counter = 0


@router.get("/messages", tags=["messages"], response_model=list[MessageResponse])
def get_messages():
    """Get all messages"""
    return list(messages.values())


@router.get("/messages/{message_id}", tags=["messages"], response_model=MessageResponse)
def get_message(message_id: int):
    """Get a specific message by ID"""
    if message_id not in messages:
        return {"error": "Message not found"}, 404
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
        return {"error": "Message not found"}, 404
    
    del messages[message_id]
    return None