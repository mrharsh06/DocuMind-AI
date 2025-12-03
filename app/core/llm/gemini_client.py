from typing import List, Optional
import google.generativeai as genai
from app.config import settings

class GeminiClient:
    """
    Wrapper class for Google Gemini API.
    Handles both chat completions and embeddings generation.
    """
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model_name)
        # Note: Embeddings use a different API, not GenerativeModel
    
    def chat(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate a chat response from Gemini.
        
        Args:
            prompt: The user's question/prompt
            context: Optional context to include in the prompt
            
        Returns:
            The generated text response
        """
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        response = self.model.generate_content(full_prompt)
        return response.text
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Gemini.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (each is a list of floats)
        """
        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model=settings.gemini_embed_model,
                content=text
            )
            embeddings.append(result['embedding'])
        return embeddings