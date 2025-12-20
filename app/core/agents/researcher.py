"""
Researcher Agent Node for LangGraph.

This agent retrieves relevant document chunks from the vector store.
It's implemented as a LangGraph node function.

"""
import logging
from app.core.agents.state import AgentState
from app.core.rag.vector_store import ChromaVectorStore
from app.services.embedding_service import EmbeddingService
from app.config import settings

logger=logging.getLogger(__name__)

def researcher_node(state: AgentState)->AgentState:

    logger.info(f"Researcher Agent: Starting retrieval for question: {state['question'][:50]}...")

    state["current_step"]="researcher"

    vector_store=ChromaVectorStore()
    embedding_service=EmbeddingService()

    try:
        question_embedding=None
        try:
            if settings.gemini_api_key:
                question_embedding=embedding_service.generate_embeddings([state['question']])[0]
                logging.info("Reseacher Agent:Using Gemini embeddings")
            else:
                logger.info("Researcher Agent: No Gemini API key, using ChromaDB default embeddings")
        except Exception as e:
            logger.warning(f"Researcher Agent: Failed to generate Gemini embeddings: {str(e)}. Using ChromaDB default.")
            question_embedding = None

        if question_embedding:
            results = vector_store.query(
                query_texts=[state['question']],
                n_results=state['n_results'],
                embeddings=[question_embedding]
            )
        else:
            results = vector_store.query(
                query_texts=[state['question']],
                n_results=state['n_results']
            )
        if not results['documents'] or len(results['documents'][0]) == 0:
            logger.warning("Researcher Agent: No relevant documents found")
            state["chunks"] = []
            state["metadatas"] = []
            state["formatted_sources"] = []
            state["error"] = "No relevant documents found"
            return state
        retrieved_chunks = results['documents'][0]  # First query result
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results['distances'] else []
        
        # Step 5: Format sources for easy use by other agents
        formatted_sources = []
        for i, chunk in enumerate(retrieved_chunks):
            metadata = metadatas[i] if i < len(metadatas) else {}
            distance = distances[i] if i < len(distances) else 1.0
            
            source_info = {
                "chunk": chunk,
                "file_name": metadata.get("file_name", "Unknown"),
                "chunk_index": metadata.get("chunk_index", i),
                "similarity_score": 1.0 - distance  # Convert distance to similarity (0-1 scale)
            }
            formatted_sources.append(source_info)
        state["chunks"] = retrieved_chunks
        state["metadatas"] = metadatas
        state["formatted_sources"] = formatted_sources
        state["error"] = None  # Clear any previous errors
        
        logger.info(f"Researcher Agent: Retrieved {len(retrieved_chunks)} chunks")
        
    except Exception as e:
        logger.error(f"Researcher Agent: Error during retrieval: {str(e)}")
        state["chunks"] = []
        state["metadatas"] = []
        state["formatted_sources"] = []
        state["error"] = f"Researcher Agent failed: {str(e)}"
    
    return state
        

        






