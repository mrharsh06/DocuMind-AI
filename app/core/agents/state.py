"""
State model for LangGraph multi-agent workflow.

This defines the shared state that flows between agents in the workflow.
"""
from typing import TypedDict, List, Dict, Optional


class AgentState(TypedDict):
    """
    Shared state between agents in the multi-agent workflow.
    
    This state is passed from one agent to the next, allowing each agent
    to access and modify the shared information.
    """
    # Input
    question: str  # User's original question
    n_results: int  # Number of chunks to retrieve
    
    # Researcher Agent output
    chunks: List[str]  # Retrieved document chunks
    metadatas: List[Dict]  # Metadata for each chunk
    formatted_sources: List[Dict]  # Formatted source information
    
    # Analyzer Agent output
    insights: Optional[List[Dict]]  # Key insights extracted from chunks
    analyzed_chunks: Optional[List[Dict]]  # Chunks with analysis
    
    # Synthesizer Agent output
    answer: Optional[str]  # Final generated answer
    sources: Optional[List[Dict]]  # Final sources with citations
    
    # Workflow control
    current_step: str  # Current step in workflow (for debugging)
    error: Optional[str]  # Error message if any step fails

