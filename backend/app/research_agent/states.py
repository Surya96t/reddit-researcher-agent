"""
State definitions for the research agent graph.
"""
from typing import TypedDict, List, Dict, Any
from sqlalchemy.orm import Session

class GraphState(TypedDict):
    """State schema for the research agent workflow."""
    task_id: str
    db: Session
    query: str
    subreddits: List[str]
    posts: List[Dict[str, Any]]
    filtered_posts: List[Dict[str, Any]]
    extracted_ideas: List[Dict[str, Any]]
    analysis_summary: str
    final_report: str
