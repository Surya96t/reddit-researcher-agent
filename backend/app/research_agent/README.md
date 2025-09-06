# Research Agent Module Structure

This document describes the refactored structure of the research agent module.

## Overview

The research agent has been refactored from a single monolithic `graph.py` file into a modular structure that improves maintainability, testability, and readability.

## File Structure

```
research_agent/
├── __init__.py          # Module exports and documentation
├── graph.py             # Main entry point (simplified)
├── models.py            # Pydantic models and schemas
├── states.py            # Graph state definitions
├── prompts.py           # LangChain prompt templates
├── chains.py            # LangChain chains and LLM configurations
├── reddit_client.py     # Reddit API client configuration
├── nodes.py             # Workflow node functions
├── workflow.py          # LangGraph workflow definition
└── README.md           # This file
```

## Module Descriptions

### `models.py`

Contains all Pydantic models used for structured data validation:

- `ExtractedIdea`: Schema for individual business ideas
- `IdeaExtractionList`: Container for multiple ideas
- `PostFilter`: Schema for post relevance filtering

### `states.py`

Defines the `GraphState` TypedDict that represents the workflow state throughout the agent execution.

### `prompts.py`

Contains all LangChain prompt templates:

- `extraction_prompt`: For extracting business ideas from posts
- `filter_prompt`: For filtering relevant posts
- `analysis_prompt`: For analyzing trends in extracted ideas
- `report_prompt`: For generating final reports

### `chains.py`

Defines LangChain chains and LLM configurations:

- LLM instances for different tasks
- Composed chains using LCEL (LangChain Expression Language)

### `reddit_client.py`

Configures and exports the Reddit API client with proper authentication.

### `nodes.py`

Contains all workflow node functions:

- `collect_posts()`: Collects posts from Reddit
- `filter_posts()`: Filters relevant posts using LLM
- `extract_ideas()`: Extracts business ideas from posts
- `analyze_trends()`: Analyzes trends across ideas
- `generate_report()`: Generates final markdown report

### `workflow.py`

Defines the LangGraph workflow structure and exports the compiled agent app.

### `graph.py`

Simplified main entry point that imports and exports the agent app.

## Usage

The refactored module maintains the same public interface. Import the agent app:

```python
from app.research_agent import agent_app

# Use the agent as before
result = agent_app.invoke({
    "query": "productivity tools",
    "subreddits": ["productivity", "getmotivated"]
})
```

## Benefits of Refactoring

1. **Separation of Concerns**: Each file has a single, clear responsibility
2. **Maintainability**: Easier to modify individual components
3. **Testability**: Smaller modules are easier to unit test
4. **Reusability**: Components can be imported and used independently
5. **Readability**: Cleaner, more focused code in each file
6. **Scalability**: Easier to add new features without bloating a single file

## Development Guidelines

- Keep models in `models.py` for all new Pydantic schemas
- Add new prompts to `prompts.py` following the existing pattern
- Create new node functions in `nodes.py` with clear docstrings
- Update the workflow in `workflow.py` when adding new nodes
- Maintain the public interface through `__init__.py` exports
