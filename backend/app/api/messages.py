"""Message routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService
from app.services.conversation_service import ConversationService
from app.utils.ai_service import ai_service
from app.api.users import get_current_user
import json

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.get("/conversation/{conversation_id}", response_model=list[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation."""
    ConversationService.get_conversation_by_id(db, conversation_id, current_user.id)
    messages = MessageService.get_conversation_messages(db, conversation_id)
    return messages

@router.post("/conversation/{conversation_id}/send", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    message_create: MessageCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message and get AI response."""
    conversation = ConversationService.get_conversation_by_id(db, conversation_id, current_user.id)
    user_message = MessageService.create_message(
        db, conversation_id, "user", message_create.content
    )
    messages = MessageService.get_conversation_messages(db, conversation_id)
    ai_messages = [
        ai_service.create_system_prompt(),
        *[{"role": msg.role, "content": msg.content} for msg in messages]
    ]
    try:
        response = await ai_service.get_response(ai_messages)
        MessageService.create_message(
            db,
            conversation_id,
            "assistant",
            response["content"],
            response["tokens_used"]
        )
    except Exception as e:
        MessageService.create_message(
            db,
            conversation_id,
            "assistant",
            f"Error: {str(e)}"
        )
    return user_message

@router.post("/conversation/{conversation_id}/stream")
async def stream_message(
    conversation_id: int,
    message_create: MessageCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message and get streaming AI response."""
    conversation = ConversationService.get_conversation_by_id(db, conversation_id, current_user.id)
    MessageService.create_message(
        db, conversation_id, "user", message_create.content
    )
    messages = MessageService.get_conversation_messages(db, conversation_id)
    ai_messages = [
        ai_service.create_system_prompt(),
        *[{"role": msg.role, "content": msg.content} for msg in messages]
    ]
    
    async def stream_generator():
        try:
            full_response = ""
            async for chunk in ai_service.get_streaming_response(ai_messages):
                full_response += chunk
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            MessageService.create_message(
                db,
                conversation_id,
                "assistant",
                full_response
            )
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(stream_generator(), media_type="text/event-stream")

@router.delete("/message/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a message."""
    MessageService.delete_message(db, message_id)
