import os
from typing import List,Optional
import logging
import uuid

from ingestion.parsers.pdf_parser import PDFParser
from ingestion.parsers.docx_parser import DOCXParser
from ingestion.parsers.text_parser import TextParser
from ingestion.chunkers.text_splitter import TextSplitter
from app.core.rag.vector_store import ChromaVectorStore
from app.services.embedding_service import EmbeddingService
from app.config import settings

logger=logging.getLogger(__name__)

class DocumentService:
    """
    Service for processing documents-parsing and chunking
    """
    def __init__(self):

        """
        Initialize the document service with parsing and splitter
        """
        self.pdf_parser=PDFParser()
        self.docx_parser=DOCXParser()
        self.text_parser=TextParser()
        self.text_splitter=TextSplitter()
        self.vector_store = ChromaVectorStore()
        self.embedding_service = EmbeddingService()


    def process_document(self,file_path: str) -> Optional[List[str]]:
        """
        it will take a file path and return a list of chunks of text based on the file type
        """
        file_extension=os.path.splitext(file_path)[1].lower()
        text=None
        if file_extension=='.pdf':
            text=self.pdf_parser.parse(file_path)
        elif file_extension=='.docx':
            text=self.docx_parser.parse(file_path)
        elif file_extension==".txt":
            text=self.text_parser.parse(file_path)
        else:
            logger.error(f"Unsupported file type: {file_extension}")
            return None
        if not text:
            logger.error(f"Failed to parse file:{file_path}")
            return None
        
        ##split text into chunks
        chunks=self.text_splitter.split_text(text)

        logger.info(f"successfully processed document: {file_path} into {len(chunks)} chunks")
        return chunks
    
    def store_document_in_vector_store(self, file_path: str) -> Optional[tuple]:
        """
        Process a document and store it in the vector store with embeddings.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Tuple of (chunks, chunk_ids) if successful, None if failed
        """
        chunks = self.process_document(file_path)
        if not chunks:
            return None
        
        # Try to generate embeddings with Gemini, but if it fails, use ChromaDB's default
        embeddings = None
        try:
            if settings.gemini_api_key:
                embeddings = self.embedding_service.generate_embeddings(chunks)
                logger.info("Using Gemini embeddings")
            else:
                logger.info("No Gemini API key, using ChromaDB default embeddings")
        except Exception as e:
            logger.warning(f"Failed to generate Gemini embeddings: {str(e)}. Using ChromaDB default embeddings.")
            embeddings = None
        
        # Create unique IDs for each chunk
        chunk_ids = [f"{uuid.uuid4()}" for _ in chunks]
        
        # Create metadata for each chunk
        file_name = os.path.basename(file_path)
        metadatas = [
            {
                "file_path": file_path,
                "file_name": file_name,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]
        
        # Store in vector store (if embeddings is None, ChromaDB will generate them)
        self.vector_store.add_documents(
            ids=chunk_ids,
            documents=chunks,
            metadatas=metadatas,
            embeddings=embeddings
        )
        
        # Persist to disk
        self.vector_store.persist()
        
        logger.info(f"Stored {len(chunks)} chunks in vector store for {file_name}")
        return (chunks, chunk_ids)
        


