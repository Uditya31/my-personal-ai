"""File upload routes."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.file import FileUploadResponse
from app.services.file_service import FileService
from app.utils.file_handler import save_upload_file, extract_text
from app.utils.security import decode_token
from app.api.users import get_current_user
from app.config import settings
import os

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a file."""
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in settings.allowed_file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.allowed_file_types)}"
        )
    contents = await file.read()
    if len(contents) > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size"
        )
    stored_filename = await save_upload_file(file, settings.upload_dir)
    file_path = os.path.join(settings.upload_dir, stored_filename)
    extracted_text = extract_text(file_path, file_ext)
    file_record = FileService.create_file_record(
        db,
        current_user.id,
        file.filename,
        stored_filename,
        file_ext,
        len(contents),
        file_path,
        extracted_text
    )
    return file_record

@router.get("/", response_model=list[FileUploadResponse])
async def get_user_files(
    skip: int = 0,
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all files for current user."""
    files = FileService.get_user_files(db, current_user.id, skip, limit)
    return files

@router.get("/{file_id}", response_model=FileUploadResponse)
async def get_file(
    file_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get file by ID."""
    file_record = FileService.get_file_by_id(db, file_id, current_user.id)
    return file_record

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a file."""
    FileService.delete_file(db, file_id, current_user.id)
