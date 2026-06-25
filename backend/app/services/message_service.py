"""Message service."""

from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageCreate
from fastapi import HTTPException, status

class MessageService:
    """Message service."""
    
    @staticmethod
    def create_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
        tokens_used: int = None
    ) -> Message:
        """Create a new message."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tokens_used=tokens_used,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    @staticmethod
    def get_conversation_messages(db: Session, conversation_id: int) -> list:
        """Get all messages in a conversation."""
        return db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
    
    @staticmethod
    def get_message_by_id(db: Session, message_id: int) -> Message:
        """Get message by ID."""
        return db.query(Message).filter(Message.id == message_id).first()
    
    @staticmethod
    def delete_message(db: Session, message_id: int) -> bool:
        """Delete a message."""
        message = MessageService.get_message_by_id(db, message_id)
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        db.delete(message)
        db.commit()
        return True
