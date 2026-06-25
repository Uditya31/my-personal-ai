"""Message schemas."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    """Message creation schema."""
    content: str = Field(..., min_length=1, max_length=4000)

class MessageResponse(BaseModel):
    """Message response schema."""
    id: int
    conversation_id: int
    role: str
    content: str
    is_edited: bool
    tokens_used: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
