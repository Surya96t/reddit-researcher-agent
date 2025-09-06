"""
LangGraph workflow definition for the research agent.
"""
from langgraph.graph import StateGraph, END
from .states import GraphState
from .nodes import (
    collect_posts,
    filter_posts,
    extract_ideas,
    analyze_trends,
    generate_report
)


def create_workflow():
    """
    Creates and returns the compiled research agent workflow.
    """
    workflow = StateGraph(GraphState)
    
    # Add nodes to the workflow
    workflow.add_node("collect_posts", collect_posts)
    workflow.add_node("filter_posts", filter_posts)
    workflow.add_node("extract_ideas", extract_ideas)
    workflow.add_node("analyze_trends", analyze_trends)
    workflow.add_node("generate_report", generate_report)
    
    # Define the workflow edges
    workflow.set_entry_point("collect_posts")
    workflow.add_edge("collect_posts", "filter_posts")
    workflow.add_edge("filter_posts", "extract_ideas")
    workflow.add_edge("extract_ideas", "analyze_trends")
    workflow.add_edge("analyze_trends", "generate_report")
    workflow.add_edge("generate_report", END)
    
    return workflow.compile()


# Create the compiled agent app
agent_app = create_workflow()
