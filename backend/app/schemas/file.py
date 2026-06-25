"""File schemas."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FileUploadResponse(BaseModel):
    """File upload response schema."""
    id: int
    user_id: int
    original_filename: str
    stored_filename: str
    file_type: str
    file_size: int
    extracted_text: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
