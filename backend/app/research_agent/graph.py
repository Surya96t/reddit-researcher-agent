"""
Main entry point for the research agent.
This module provides a clean interface to the refactored research agent workflow.
"""
# Import the compiled agent app from the workflow module
from .workflow import agent_app

# Export the agent app for use by other modules
__all__ = ["agent_app"]