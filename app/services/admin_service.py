from typing import List, Dict, Optional
import logging
from app.core.rag.vector_store import ChromaVectorStore

logger = logging.getLogger(__name__)

class AdminService:
    """
    Service for admin operations on documents.
    Handles listing, deleting, and getting statistics about documents.
    """
    
    def __init__(self):
        """
        Initialize the admin service.
        """
        self.vector_store = ChromaVectorStore()
    
    def list_all_documents(self) -> Dict:
        """
        List all documents in the vector store.
        
        Returns:
            Dictionary containing:
                - total_count: Total number of document chunks
                - unique_files: Number of unique files
                - files: List of file details with chunk counts
        """
        logger.info("Listing all documents")
        
        # Step 1: Get all documents from vector store
        all_docs = self.vector_store.get_all_documents()
        metadatas = all_docs.get("metadatas", [])
        
        # Step 2: Count chunks per file
        file_chunk_count = {}
        for metadata in metadatas:
            if metadata and "file_name" in metadata:
                file_name = metadata["file_name"]
                file_chunk_count[file_name] = file_chunk_count.get(file_name, 0) + 1
        
        # Step 3: Build file details list
        files = [
            {
                "file_name": file_name,
                "chunk_count": count
            }
            for file_name, count in file_chunk_count.items()
        ]
        
        return {
            "total_count": len(all_docs.get("ids", [])),
            "unique_files": len(file_chunk_count),
            "files": files
        }
    
    def delete_document(self, file_name: str) -> Dict:
        """
        Delete all chunks of a specific document.
        
        Args:
            file_name: Name of the file to delete
            
        Returns:
            Dictionary containing deletion result
        """
        logger.info(f"Deleting document: {file_name}")
        
        # Call vector store to delete
        deleted_count = self.vector_store.delete_documents_by_file_name(file_name)
        
        # Check if deletion was successful
        if deleted_count == 0:
            return {
                "success": False,
                "message": f"Document '{file_name}' not found",
                "deleted_count": 0
            }
        
        return {
            "success": True,
            "message": f"Successfully deleted {deleted_count} chunk(s) for file '{file_name}'",
            "deleted_count": deleted_count,
            "file_name": file_name
        }
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the document collection.
        
        Returns:
            Dictionary containing collection statistics
        """
        logger.info("Getting collection statistics")
        
        total_count = self.vector_store.get_collection_count()
        unique_files = self.vector_store.get_unique_file_names()
        
        return {
            "total_chunks": total_count,
            "unique_files": len(unique_files),
            "file_names": unique_files
        }