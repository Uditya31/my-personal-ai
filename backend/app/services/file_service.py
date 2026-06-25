"""File service."""

from sqlalchemy.orm import Session
from app.models.file import UploadedFile
from fastapi import HTTPException, status
from datetime import datetime

class FileService:
    """File service."""
    
    @staticmethod
    def create_file_record(
        db: Session,
        user_id: int,
        original_filename: str,
        stored_filename: str,
        file_type: str,
        file_size: int,
        file_path: str,
        extracted_text: str = None
    ) -> UploadedFile:
        """Create a file record."""
        file_record = UploadedFile(
            user_id=user_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_type=file_type,
            file_size=file_size,
            file_path=file_path,
            extracted_text=extracted_text,
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        return file_record
    
    @staticmethod
    def get_file_by_id(db: Session, file_id: int, user_id: int) -> UploadedFile:
        """Get file by ID."""
        file_record = db.query(UploadedFile).filter(
            UploadedFile.id == file_id,
            UploadedFile.user_id == user_id
        ).first()
        if not file_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        return file_record
    
    @staticmethod
    def get_user_files(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list:
        """Get all files for a user."""
        return db.query(UploadedFile).filter(
            UploadedFile.user_id == user_id
        ).order_by(UploadedFile.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_file(db: Session, file_id: int, user_id: int) -> bool:
        """Delete a file."""
        file_record = FileService.get_file_by_id(db, file_id, user_id)
        db.delete(file_record)
        db.commit()
        return True
