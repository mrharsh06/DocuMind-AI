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
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            query_embeddings=embeddings,
        )
        return results
    def persist(self):
        """
        Persist the vector store to disk.
        Note: PersistentClient auto-persists, but keeping this for compatibility.
        """
        # PersistentClient automatically persists, no action needed
        pass