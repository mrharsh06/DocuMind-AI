import os
from typing import List, Dict, Optional
import chromadb

from app.config import settings

class ChromaVectorStore:
    """
    wrapper around chromaDB for storing and quering document embeddings.
    """
    def __init__(self,collection_name:str="documind_documents"):
        os.makedirs(settings.vector_db_dir,exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=settings.vector_db_dir
        )

        self.collection=self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space":"cosine"},
        )
        
    def add_documents(
        self,
        ids:List[str],
        documents:List[str],
        metadatas:Optional[List[Dict]]=None,
        embeddings:Optional[List[List[float]]]=None,
    ):

        """
        Add documents to the vector store.
        """
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )
    
    def query(
        self,
        query_texts: List[str],
        n_results: int = 5,
        where: Optional[Dict] = None,
        embeddings: Optional[List[List[float]]] = None,
    ):
        """
        Query the vector store for similar documents.
        """
        # Build query parameters - only include 'where' if provided (ChromaDB doesn't accept None)
        query_params = {
            "query_texts": query_texts,
            "n_results": n_results,
        }
        
        # Only add 'where' if it's not None
        if where is not None:
            query_params["where"] = where
        
        # Only add 'query_embeddings' if provided
        if embeddings is not None:
            query_params["query_embeddings"] = embeddings
        
        results = self.collection.query(**query_params)
        return results
    def persist(self):
        """
        Persist the vector store to disk.
        Note: PersistentClient auto-persists, but keeping this for compatibility.
        """
        # PersistentClient automatically persists, no action needed
        pass
    
    def get_all_documents(self, limit: Optional[int] = None) -> Dict:
        """
        Get all documents from the collection with their metadata.
        
        Args:
            limit: Optional limit on number of documents to return
            
        Returns:
            Dictionary containing ids, documents, and metadatas
        """
        # ChromaDB doesn't have a direct "get all" method, so we query with empty query
        # We'll use a workaround: get collection count and query with a dummy query
        count = self.collection.count()
        
        if count == 0:
            return {
                "ids": [],
                "documents": [],
                "metadatas": []
            }
        
        # Get all documents by querying with a large n_results
        # Note: This is a workaround since ChromaDB doesn't have direct "get all"
        results = self.collection.get(
            limit=limit if limit else count
        )
        
        return {
            "ids": results.get("ids", []),
            "documents": results.get("documents", []),
            "metadatas": results.get("metadatas", [])
        }
    
    def delete_documents_by_file_name(self, file_name: str) -> int:
        """
        Delete all document chunks associated with a specific file name.
        
        Args:
            file_name: The name of the file to delete
            
        Returns:
            Number of documents deleted
        """
        # Get all documents to find ones matching the file name
        all_docs = self.get_all_documents()
        metadatas = all_docs.get("metadatas", [])
        ids = all_docs.get("ids", [])
        
        # Find IDs where file_name matches
        ids_to_delete = [
            doc_id 
            for doc_id, metadata in zip(ids, metadatas) 
            if metadata and metadata.get("file_name") == file_name
        ]
        
        if not ids_to_delete:
            return 0
        
        # Delete the documents
        self.collection.delete(ids=ids_to_delete)
        return len(ids_to_delete)
    
    def get_collection_count(self) -> int:
        """
        Get the total number of documents in the collection.
        
        Returns:
            Total count of documents
        """
        return self.collection.count()
    
    def get_unique_file_names(self) -> List[str]:
        """
        Get a list of all unique file names in the collection.
        
        Returns:
            List of unique file names
        """
        all_docs = self.get_all_documents()
        metadatas = all_docs.get("metadatas", [])
        
        # Extract unique file names
        file_names = set()
        for metadata in metadatas:
            if metadata and "file_name" in metadata:
                file_names.add(metadata["file_name"])
        
        return sorted(list(file_names))