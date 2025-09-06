"""
Pydantic models for the research agent.
"""
from typing import List
from pydantic import BaseModel, Field


class ExtractedIdea(BaseModel):
    """Schema for a single extracted business idea."""
    pain_point: str = Field(description="The specific problem, need, or frustration mentioned by the user.")
    solution_idea: str = Field(description="A clear, concise business or product idea that solves the pain point.")
    target_audience: str = Field(description="The specific group of people who would benefit from this solution.")
    business_model: str = Field(description="A suggested business model (e.g., SaaS, Marketplace, One-time Purchase, Ad-Supported).")


class IdeaExtractionList(BaseModel):
    """A list of business ideas extracted from a single Reddit post."""
    ideas: List[ExtractedIdea]


class PostFilter(BaseModel):
    """A tool to determine if a Reddit post is relevant to a user's query."""
    is_relevant: bool = Field(description="True if the post is relevant, False otherwise.")
    reasoning: str = Field(description="A brief explanation for the relevance decision.")
