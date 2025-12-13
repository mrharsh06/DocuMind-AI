from fastapi import APIRouter,HTTPException
import logging

from app.services.admin_service import AdminService
from app.api.schemas.admin import(
    DocumentListResponse,
    DocumentDeleteResponse,
    StatisticsResponse
)

logger=logging.getLogger(__name__)

router=APIRouter(prefix="/admin",tags=["admin"])

@router.get("/documents", response_model=DocumentListResponse)
async def list_all_documents():
    """
    List all documents in the vector store.
    Returns total count, unique files count, and list of files with chunk counts.
    """
    try:
        service=AdminService()
        result=service.list_all_documents()

        return DocumentListResponse(
            total_count=result["total_count"],
            unique_files=result["unique_files"],
            files=result["files"]
        )
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list documents: {str(e)}"
        )

@router.delete("/documents/{file_name}", response_model=DocumentDeleteResponse)
async def delete_document(file_name: str):
    """
    Delete a document and all its chunks from the vector store.
    
    Args:
        file_name: Name of the file to delete
    """
    try:
        service = AdminService()
        result = service.delete_document(file_name)
        
        return DocumentDeleteResponse(
            success=result["success"],
            message=result["message"],
            deleted_count=result["deleted_count"],
            file_name=result.get("file_name")
        )
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        )
@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics():
    """
    Get statistics about the document collection.
    Returns total chunks, unique files count, and list of all file names.
    """
    try:
        service = AdminService()
        result = service.get_statistics()
        
        return StatisticsResponse(
            total_chunks=result["total_chunks"],
            unique_files=result["unique_files"],
            file_names=result["file_names"]
        )
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get statistics: {str(e)}"
        )


