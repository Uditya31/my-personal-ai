"""Token schemas."""

from pydantic import BaseModel

class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    """Token refresh schema."""
    refresh_token: str
