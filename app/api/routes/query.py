from fastapi import APIRouter,HTTPException
import logging

from app.services.query_service import QueryService
from app.api.schemas.query import QueryRequest,QueryResponse

logger=logging.getLogger(__name__)

router=APIRouter(prefix="/query",tags=['query'])

@router.post("/",response_model=QueryResponse)
async def query_documents(request:QueryRequest):
    """
    Query uploaded documents and get an AI-generated answer.
    
    This endpoint uses RAG (Retrieval-Augmented Generation) to:
    1. Find relevant document chunks
    2. Generate an answer based on those chunks
    """
    try:
        service=QueryService()

        result=service.query(question=request.question,
            n_results=request.n_results)

        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            question=request.question
        )
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )

        


