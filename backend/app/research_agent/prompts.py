"""
Prompt templates for the research agent.
"""
from langchain_core.prompts import ChatPromptTemplate


# Prompt for extracting business ideas from Reddit posts
extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert venture capitalist and product manager. Your task is to analyze a Reddit post to identify potential business opportunities. Extract all distinct user pain points and the corresponding solution ideas mentioned or implied in the text."),
    ("user", "Please analyze the following Reddit post and extract all business ideas according to the required format.\n\nPost Title: {post_title}\nPost Content:\n{post_content}")
])


# Prompt for filtering relevant posts
filter_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert at analyzing Reddit posts. Your task is to determine if a post is relevant to the user's query seeking new business ideas or identifying user needs."),
    ("user", "User Query: {query}\n\nPost Title: {post_title}\nPost Content:\n{post_content}\n\nBased on the post's title and content, is it a relevant source for finding business ideas or unmet user needs? A relevant post is one where people are asking for a product, suggesting an idea, or complaining about a problem that could be solved with a product.")
])


# Prompt for analyzing trends in extracted ideas
analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior market analyst. Your task is to analyze a list of business ideas extracted from Reddit and identify the top 3-5 overarching themes or trends."),
    ("user", "Here is a list of extracted business ideas:\n\n{ideas_json}\n\nPlease identify the key trends and common pain points from this list. What are the most common types of solutions being requested? Provide a concise summary of your findings.")
])


# Prompt for generating the final report
report_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert business analyst and writer. Your task is to generate a comprehensive, well-structured business opportunity report in Markdown format based on the provided data."),
    ("user", """
Please generate a final report based on the following information:

## Original User Query:
{query}

## Market Analysis Summary:
{analysis_summary}

## Extracted Business Ideas:
{ideas_json}

---

**Report Structure:**

1.  **Executive Summary:** A brief, high-level overview of the market need and the key opportunities discovered.
2.  **Key Trends and Pain Points:** Elaborate on the analysis summary. Discuss the recurring problems and needs you identified from the extracted ideas.
3.  **Top Business Opportunities:** Detail the most promising 3-5 ideas from the list. For each idea, provide the Pain Point, Solution Idea, Target Audience, and a suggested Business Model.
4.  **Conclusion:** A concluding paragraph summarizing the potential in this niche.
""")
])
