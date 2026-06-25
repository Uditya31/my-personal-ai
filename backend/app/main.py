"""FastAPI application initialization."""

from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine
from app.middleware.cors_middleware import setup_cors
from app.middleware.error_handler import setup_error_handlers
from app.api import auth, users, conversations, messages, files

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Full-stack AI Assistant application",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

setup_cors(app)
setup_error_handlers(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(messages.router)
app.include_router(files.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to My Personal AI",
        "version": settings.app_version,
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
