from fastapi import APIRouter,UploadFile,File,HTTPException
import os
import tempfile
import logging

from app.services.document_service import DocumentService
from app.api.schemas.document import DocumentUploadResponse

logger=logging.getLogger(__name__)

router=APIRouter(prefix="/documents",tags=["documents"])

@router.post("/upload",response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document (PDF,DOCX,or TXT).
    """
    #check file type
    file_ext=os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.pdf','.docx','.txt']:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type,we support only PDF,DOCS,TXT"
        )
    with tempfile.NamedTemporaryFile(delete=False,suffix=file_ext) as temp_file:
        content=await file.read()
        temp_file.write(content)
        temp_path=temp_file.name

    try:
        service=DocumentService()
        chunks=service.process_document(temp_path)

        if not chunks:
            raise HTTPException(
                status_code=500,
                detail="Failed to process Document"
            )

        return DocumentUploadResponse(
            message="Document processed successfully",
            file_name=file.filename,
            chunk_count=len(chunks),
            chunks=chunks
        )

    finally:
        #clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
