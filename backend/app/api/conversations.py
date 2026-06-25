"""Conversation routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationUpdate
from app.services.conversation_service import ConversationService
from app.api.users import get_current_user

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_create: ConversationCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new conversation."""
    conversation = ConversationService.create_conversation(db, current_user.id, conversation_create)
    return conversation

@router.get("/", response_model=list[ConversationResponse])
async def get_conversations(
    skip: int = 0,
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for current user."""
    conversations = ConversationService.get_user_conversations(db, current_user.id, skip, limit)
    return conversations

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get conversation details."""
    conversation = ConversationService.get_conversation_by_id(db, conversation_id, current_user.id)
    return conversation

@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    conversation_update: ConversationUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update conversation."""
    conversation = ConversationService.update_conversation(
        db, conversation_id, current_user.id, conversation_update
    )
    return conversation

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete conversation."""
    ConversationService.delete_conversation(db, conversation_id, current_user.id)

@router.get("/search/{query}", response_model=list[ConversationResponse])
async def search_conversations(
    query: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search conversations."""
    conversations = ConversationService.search_conversations(db, current_user.id, query)
    return conversations
