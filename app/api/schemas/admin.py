from pydantic import BaseModel,Field
from typing import List,Optional

class FileInfo(BaseModel):
    file_name: str=Field(..., description="Name of the file")
    chunk_count: int=Field(..., description="Number of chunks for this file")

class DocumentListResponse(BaseModel):
    total_count: int=Field(..., description="Total number of document chunks in the database")
    unique_files: int=Field(..., description="Number of unique files")
    files: List[FileInfo]=Field(..., description="List of files with their chunk counts")

class DocumentDeleteResponse(BaseModel):
    success: bool =Field(..., description="Whether the deletion was successful")
    message: str = Field(..., description="Message describing the result")
    deleted_count: int = Field(..., description="Number of chunks deleted")
    file_name: Optional[str] = Field(None, description="Name of the deleted file (only if successful)")

class StatisticsResponse(BaseModel):    
    total_chunks: int = Field(..., description="Total number of chunks in the collection")    
    unique_files: int = Field(..., description="Number of unique files")
    file_names: List[str] = Field(..., description="List of all unique file names")







