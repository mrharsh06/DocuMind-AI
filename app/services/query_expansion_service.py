##will update later if i want based on the usecase currently putting on hold
from typing import List, Optional
import logging
from app.core.llm.gemini_client import GeminiClient
from app.config import settings

logger=logging.getLogger(__name__)

class QueryExpansionService:

    """
    Service for expanding and rewriting user queries to improve retrieval.
    
    This service uses LLM to generate alternative query formulations,
    which helps find relevant documents even if they use different wording.
    """
    def __init__(self):
        self.gemini_client=GeminiClient()
    
    def expand_query(self,original_query: str,num_expansions: int = 3)-> List[str]:
        """
        Expand a query into multiple alternative formulations.
        
        Args:
            original_query: The user's original question
            num_expansions: Number of alternative queries to generate (default: 3)
            
        Returns:
            List of expanded queries, including the original query
        """
        logger.info(f"Expanding query: {original_query}")

        if not settings.gemini_api_key:
            logger.warning("No Gemini Api Key found. Returning original query only.")
            return [original_query]

        try:
            expansion_prompt=f"""you are search query expert.Given a user's question,generate {num_expansions} alternative ways to ask the same question or search for the same information.
            original question:{original_query}
            Generate {num_expansions} alternative queries that:
            1.Use different wording but mean the same thing
            2.Include synonyms or related terms
            3.May be more specific or more gneral
            4.Could help find relevant documents

            Return ONLY the queries, one per line, without numbering or bullets.
Example format:
What is machine learning?
Explain machine learning
Machine learning definition

Alternative queries:"""
            response=self.gemini_client.chat(expansion_prompt)
            expanded_queries=[
                line.strip()
                for line in response.split('\n')
                if line.strip() and not line.strip().startswith(('Alternative', 'Example', 'Original'))
            ]

            expanded_queries=expanded_queries[:num_expansions]

            all_queries=[original_query]+expanded_queries
            logger.info(f"Generated {len(expanded_queries)} expanded queries")
            return all_queries
        
        except Exception as e:
            logger.error(f"Failed to expand query: {str(e)}. Returning original query only.")
            return [original_query]








        

