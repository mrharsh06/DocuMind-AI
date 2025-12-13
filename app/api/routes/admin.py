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

