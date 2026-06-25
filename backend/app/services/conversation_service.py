"""Conversation service."""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate, ConversationUpdate
from fastapi import HTTPException, status
from datetime import datetime

class ConversationService:
    """Conversation service."""
    
    @staticmethod
    def create_conversation(db: Session, user_id: int, conversation_create: ConversationCreate) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=user_id,
            title=conversation_create.title,
            description=conversation_create.description,
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    @staticmethod
    def get_conversation_by_id(db: Session, conversation_id: int, user_id: int) -> Conversation:
        """Get conversation by ID."""
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        return conversation
    
    @staticmethod
    def get_user_conversations(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list:
        """Get all conversations for a user."""
        return db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(desc(Conversation.updated_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_conversation(db: Session, conversation_id: int, user_id: int, conversation_update: ConversationUpdate) -> Conversation:
        """Update conversation."""
        conversation = ConversationService.get_conversation_by_id(db, conversation_id, user_id)
        update_data = conversation_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(conversation, field, value)
        conversation.updated_at = datetime.utcnow()
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    @staticmethod
    def delete_conversation(db: Session, conversation_id: int, user_id: int) -> bool:
        """Delete conversation."""
        conversation = ConversationService.get_conversation_by_id(db, conversation_id, user_id)
        db.delete(conversation)
        db.commit()
        return True
    
    @staticmethod
    def search_conversations(db: Session, user_id: int, query: str) -> list:
        """Search conversations."""
        return db.query(Conversation).filter(
            Conversation.user_id == user_id,
            (Conversation.title.ilike(f"%{query}%") | Conversation.description.ilike(f"%{query}%"))
        ).order_by(desc(Conversation.updated_at)).all()
