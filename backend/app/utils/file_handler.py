"""File handling utilities."""

import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile

try:
    from PyPDF2 import PdfReader
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

def create_upload_directory(upload_dir: str) -> None:
    """Create upload directory."""
    Path(upload_dir).mkdir(parents=True, exist_ok=True)

def generate_filename(filename: str) -> str:
    """Generate unique filename."""
    ext = Path(filename).suffix
    return f"{uuid.uuid4()}{ext}"

async def save_upload_file(file: UploadFile, upload_dir: str) -> str:
    """Save uploaded file."""
    create_upload_directory(upload_dir)
    stored_filename = generate_filename(file.filename)
    file_path = os.path.join(upload_dir, stored_filename)
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    return stored_filename

def extract_text_from_pdf(file_path: str) -> Optional[str]:
    """Extract text from PDF."""
    if not HAS_PDF:
        return None
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

def extract_text_from_docx(file_path: str) -> Optional[str]:
    """Extract text from DOCX."""
    if not HAS_DOCX:
        return None
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
        return None

def extract_text_from_txt(file_path: str) -> Optional[str]:
    """Extract text from TXT."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return None

def extract_text(file_path: str, file_type: str) -> Optional[str]:
    """Extract text based on file type."""
    if file_type.lower() == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type.lower() == "docx":
        return extract_text_from_docx(file_path)
    elif file_type.lower() == "txt":
        return extract_text_from_txt(file_path)
    return None
