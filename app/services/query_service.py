from typing import List,Dict,Optional
import logging
from app.core.rag.vector_store import ChromaVectorStore
from app.services.embedding_service import EmbeddingService
from app.core.llm.gemini_client import GeminiClient
from app.config import settings

logger=logging.getLogger(__name__)

class QueryService:
    """
    Service for querying documents using RAG (Retrieval-Augmented Generation).
    """
    def __init__(self):
        self.vector_store=ChromaVectorStore()
        self.embedding_service=EmbeddingService()
        self.gemini_client=GeminiClient()

    def query(self,question:str,n_results: int=5)->Dict:
        """
        Query documents using RAG (Retrieval-Augmented Generation).
        
        Args:
            question: The user's question
            n_results: Number of relevant chunks to retrieve (default: 5)
        
        Returns:
            Dictionary containing:
                - answer: AI-generated answer
                - sources: List of relevant document chunks with metadata
        """

        logger.info(f"Processing query:{question}")
    
        # Try to generate Gemini embeddings, fall back to ChromaDB default if it fails
        question_embedding = None
        try:
            if settings.gemini_api_key:
                question_embedding = self.embedding_service.generate_embeddings([question])[0]
                logger.info("Using Gemini embeddings for query")
        except Exception as e:
            logger.warning(f"Failed to generate Gemini embeddings: {str(e)}. Using ChromaDB default embeddings.")
            question_embedding = None

        # Query vector store - if we have Gemini embedding, use it; otherwise ChromaDB will use its default
        if question_embedding:
            results = self.vector_store.query(
                query_texts=[question],
                n_results=n_results,
                embeddings=[question_embedding]
            )
        else:
            # Use ChromaDB's default embedding function
            results = self.vector_store.query(
                query_texts=[question],
                n_results=n_results
            )

        if not results['documents'] or len(results['documents'][0])==0:
            logger.warning("No relevant document found")
            return {
                "answer": "I couldn't find any relevant information in the uploaded documents to answer your question.",
                "sources": []
            }
        retrieved_chunks = results['documents'][0]  # First query result
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results['distances'] else []

        context_parts = []
        sources = []

        for i, chunk in enumerate(retrieved_chunks):
            metadata = metadatas[i] if i < len(metadatas) else {}
            distance = distances[i] if i < len(distances) else 1.0
            
            # Build source info
            source_info = {
                "chunk": chunk,
                "file_name": metadata.get("file_name", "Unknown"),
                "chunk_index": metadata.get("chunk_index", i),
                "similarity_score": 1.0 - distance  # Convert distance to similarity
            }
            sources.append(source_info)
            
            # Add chunk to context
            context_parts.append(f"[Document {i+1}]: {chunk}")
        
        # Combine all chunks into context
        context = "\n\n".join(context_parts)
        
        # Step 5: Generate answer using Gemini with context
        prompt = f"""Based on the following document excerpts, please answer the question.
        
If the answer cannot be found in the provided context, please say so.

Question: {question}

Document excerpts:
{context}

Answer:"""
        
        # Try to generate answer with Gemini, but provide fallback if it fails
        try:
            if settings.gemini_api_key:
                answer = self.gemini_client.chat(prompt)
                logger.info(f"Generated answer for query: {question[:50]}...")
            else:
                # No API key, provide a simple answer based on retrieved chunks
                answer = f"I found {len(sources)} relevant document chunk(s) related to your question. Please review the sources below for the answer."
        except Exception as e:
            logger.warning(f"Failed to generate answer with Gemini: {str(e)}")
            # Fallback: provide a summary of what was found
            answer = f"I found {len(sources)} relevant document chunk(s) related to your question, but couldn't generate an AI answer due to API limitations. Please review the sources below for the answer to your question: '{question}'"
        
        return {
            "answer": answer,
            "sources": sources
        }




   
