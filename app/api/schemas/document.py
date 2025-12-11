from pydantic import BaseModel
from typing import List

class DocumentUploadResponse(BaseModel):
    """Response a Model for Document Upload"""
    message: str
    file_name: str
    chunk_count: int
    chunks: List[str]
