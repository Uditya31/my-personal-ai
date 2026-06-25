"""Application configuration module."""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings."""
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"
    app_name: str = "My Personal AI"
    app_version: str = "1.0.0"
    debug: bool = False
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    max_upload_size: int = 52428800
    allowed_file_types: List[str] = ["pdf", "docx", "txt"]
    upload_dir: str = "./uploads"
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    ai_temperature: float = 0.7
    ai_max_tokens: int = 2000
    ai_top_p: float = 0.9
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
