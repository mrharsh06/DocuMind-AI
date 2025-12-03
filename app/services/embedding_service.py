from typing import List
import logging

from app.core.llm.gemini_client import GeminiClient

logger=logging.getLogger(__name__)

class EmbeddingService:

     """
    Service for generating embeddings from text.
    """
     def __init__(self):
        self.gemini_client=GeminiClient()
    
     def generate_embeddings(self,texts:List[str])->List[List[float]]:
         """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
         if not texts:
            return []
         
         logger.info(f"Generating embeddings for {len(texts)} texts")
         embeddings = self.gemini_client.embed(texts)
         logger.info(f"Successfully generated {len(embeddings)} embeddings")
        
         return embeddings





