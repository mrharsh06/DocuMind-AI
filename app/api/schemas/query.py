from pydantic import BaseModel,Field
from typing import List,Optional

class QueryRequest(BaseModel):
    """
    Request model for query endpoint.
    """
    question:str=Field(..., description="The question to ask about the documents")
    n_results: Optional[int]=Field(default=5,description="Number of relevant chunks to retrieve", ge=1, le=10)

class SourceChunk(BaseModel):
    """
    Model for a source chunk with metadata.
    """
    chunk: str = Field(..., description="The text chunk")
    file_name: str = Field(..., description="Name of the source file")
    chunk_index: int = Field(..., description="Index of the chunk in the document")
    similarity_score: float = Field(..., description="Similarity score (0-1)")

class QueryResponse(BaseModel):
    """
    Response model for query endpoint.
    """
    answer: str = Field(..., description="The generated answer")
    sources: List[SourceChunk] = Field(..., description="List of source chunks used")
    question: str = Field(..., description="The original question")