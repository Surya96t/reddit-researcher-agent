"""
Research Agent module for Reddit-based business opportunity discovery.

This module provides a complete workflow for:
1. Collecting posts from Reddit based on search queries
2. Filtering relevant posts using LLM-powered analysis
3. Extracting business ideas and pain points from posts
4. Analyzing trends across extracted ideas
5. Generating comprehensive business opportunity reports
"""

from .workflow import agent_app
from .models import ExtractedIdea, IdeaExtractionList, PostFilter
from .states import GraphState

__all__ = [
    "agent_app",
    "ExtractedIdea", 
    "IdeaExtractionList",
    "PostFilter",
    "GraphState"
]