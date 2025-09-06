"""
Node functions for the research agent workflow.
"""
import json
from typing import Dict, Any
from .states import GraphState
from .reddit_client import reddit_client
from .chains import filter_chain, extraction_chain, analysis_chain, report_chain
from .models import PostFilter, IdeaExtractionList
from app.db.crud import create_task_log_sync


def collect_posts(state):
    task_id = state["task_id"]
    db = state["db"]
    query = state["query"]
    subreddits_list = state["subreddits"]

    create_task_log_sync(db, task_id, "---AGENT: COLLECTING POSTS---")
    
    subreddit_search_string = "+".join(subreddits_list)
    subreddit = reddit_client.subreddit(subreddit_search_string)
    
    create_task_log_sync(db, task_id, f"Searching subreddits: '{subreddit_search_string}' for query: '{query}'")
    
    collected_posts = []
    for submission in subreddit.search(query, limit=25, sort="relevance", time_filter="year"):
        if submission.num_comments > 10: 
            post_data = {
                "id": submission.id, "title": submission.title, "selftext": submission.selftext,
                "url": submission.url, "score": submission.score, "num_comments": submission.num_comments,
            }
            collected_posts.append(post_data)

    create_task_log_sync(db, task_id, f"---AGENT: Found {len(collected_posts)} relevant posts with >10 comments.---")
    return {"posts": collected_posts}

def filter_posts(state):
    task_id = state["task_id"]
    db = state["db"]
    query = state["query"]
    posts_to_filter = state["posts"]

    create_task_log_sync(db, task_id, "---AGENT: FILTERING POSTS---")
    
    filtered_posts = []
    for post in posts_to_filter:
        create_task_log_sync(db, task_id, f"Filtering post: '{post['title']}'")
        result = filter_chain.invoke({
            "query": query, "post_title": post["title"], "post_content": post["selftext"][:2000]
        })
        if result.is_relevant:
            create_task_log_sync(db, task_id, "  -> Relevant")
            filtered_posts.append(post)
        else:
            create_task_log_sync(db, task_id, f"  -> Not Relevant: {result.reasoning}")

    create_task_log_sync(db, task_id, f"---AGENT: Filtered down to {len(filtered_posts)} posts.---")
    return {"filtered_posts": filtered_posts}

def extract_ideas(state):
    task_id = state["task_id"]
    db = state["db"]
    posts_to_analyze = state["filtered_posts"]

    create_task_log_sync(db, task_id, "---AGENT: EXTRACTING IDEAS---")
    
    all_extracted_ideas = []
    for post in posts_to_analyze:
        create_task_log_sync(db, task_id, f"Extracting ideas from post: '{post['title']}'")
        try:
            result = extraction_chain.invoke({"post_title": post["title"], "post_content": post["selftext"]})
            for idea in result.ideas:
                all_extracted_ideas.append(idea.dict())
                create_task_log_sync(db, task_id, f"  -> Found Idea: {idea.solution_idea}")
        except Exception as e:
            create_task_log_sync(db, task_id, f"  -> Error extracting ideas from post {post['id']}: {e}")
            continue
            
    create_task_log_sync(db, task_id, f"---AGENT: Extracted a total of {len(all_extracted_ideas)} ideas.---")
    return {"extracted_ideas": all_extracted_ideas}

def analyze_trends(state):
    task_id = state["task_id"]
    db = state["db"]
    extracted_ideas = state["extracted_ideas"]
    
    create_task_log_sync(db, task_id, "---AGENT: ANALYZING TRENDS---")
    
    if not extracted_ideas:
        summary = "No business ideas were extracted. Skipping trend analysis."
        create_task_log_sync(db, task_id, summary)
        return {"analysis_summary": summary}

    ideas_json = json.dumps(extracted_ideas, indent=2)
    summary = analysis_chain.invoke({"ideas_json": ideas_json})
    
    create_task_log_sync(db, task_id, f"---AGENT: Analysis complete.---")
    return {"analysis_summary": summary}

def generate_report(state):
    task_id = state["task_id"]
    db = state["db"]
    create_task_log_sync(db, task_id, "---AGENT: GENERATING REPORT---")

    query = state["query"]
    analysis_summary = state["analysis_summary"]
    extracted_ideas = state["extracted_ideas"]

    if not extracted_ideas:
        report = f"# Report for \"{query}\"\n\n## No Opportunities Found\nNo specific business ideas could be extracted."
    else:
        ideas_json = json.dumps(extracted_ideas, indent=2)
        report = report_chain.invoke({"query": query, "analysis_summary": analysis_summary, "ideas_json": ideas_json})
    
    create_task_log_sync(db, task_id, "---AGENT: Report generation complete.---")
    return {"final_report": report}