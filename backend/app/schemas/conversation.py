"""Conversation schemas."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ConversationCreate(BaseModel):
    """Conversation creation schema."""
    title: str = Field(default="New Chat", max_length=255)
    description: Optional[str] = Field(None, max_length=500)

class ConversationUpdate(BaseModel):
    """Conversation update schema."""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    is_archived: Optional[bool] = None
    is_pinned: Optional[bool] = None

class ConversationResponse(BaseModel):
    """Conversation response schema."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    is_archived: bool
    is_pinned: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
