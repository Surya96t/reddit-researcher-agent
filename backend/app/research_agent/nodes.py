# backend/app/research_agent/nodes.py

import json
import uuid
from praw import exceptions as praw_exceptions
from app.db.crud import (
    get_task_sync,
    create_task_log_sync,
    create_source_post_sync,
    create_extracted_idea_sync
)
from app.research_agent.chains import filter_chain, extraction_chain, analysis_chain, report_chain
from app.research_agent.reddit_client import reddit_client
# --- Import the centralized settings object ---
from app.core.config import settings

class UUIDEncoder(json.JSONEncoder):
    """ Custom JSON encoder to handle UUID objects. """
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # If the object is a UUID, convert it to a string.
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def collect_posts(state):
    """
    Collects initial posts from Reddit based on the query.
    """
    task_id = state["task_id"]
    db = state["db"]
    query = state["query"]
    subreddits_list = state["subreddits"]

    create_task_log_sync(db, task_id, 'STEP', "---AGENT: COLLECTING POSTS---")
    
    subreddit_search_string = "+".join(subreddits_list)
    subreddit = reddit_client.subreddit(subreddit_search_string)
    
    create_task_log_sync(db, task_id, 'INFO', f"Searching subreddits: '{subreddit_search_string}' for query: '{query}'")
    
    collected_posts = []
    
    try:
        # --- THIS IS THE CORRECTED LINE ---
        # Use the AGENT_POST_FETCH_LIMIT from our settings file
        for submission in subreddit.search(query, limit=settings.AGENT_POST_FETCH_LIMIT, sort="relevance", time_filter="year"):
            if submission.num_comments > 10: 
                post_data = {
                    "id": submission.id, "title": submission.title, "selftext": submission.selftext,
                    "url": submission.url, "score": submission.score, "num_comments": submission.num_comments,
                }
                collected_posts.append(post_data)
                
    except praw_exceptions.PRAWException as e:
        error_message = f"Failed to fetch data from Reddit. The API may be down or one of the subreddits is invalid/private. (Error: {e})"
        print(f"[AGENT ERROR] {error_message}")
        create_task_log_sync(db, task_id, 'ERROR', error_message)
        raise e

    create_task_log_sync(db, task_id, 'INFO', f"---AGENT: Found {len(collected_posts)} initial posts with >10 comments.---")
    return {"posts": collected_posts}


def filter_posts(state):
    """
    Filters the collected posts for relevance and saves the relevant ones to the database.
    """
    task_id = state["task_id"]
    db = state["db"]
    query = state["query"]
    posts_to_filter = state["posts"]

    create_task_log_sync(db, task_id, 'STEP', "---AGENT: FILTERING POSTS---")
    
    relevant_posts_data = []
    for post_data in posts_to_filter:
        create_task_log_sync(db, task_id, 'INFO', f"Filtering post: '{post_data['title']}'")
        result = filter_chain.invoke({
            "query": query, "post_title": post_data["title"], "post_content": post_data["selftext"][:2000]
        })
        
        if result.is_relevant:
            create_task_log_sync(db, task_id, 'POST_FOUND', f"  -> Relevant: {post_data['title']}", data={"url": post_data['url'], "title": post_data['title']})
            create_source_post_sync(db, task_id, post_data)
            relevant_posts_data.append(post_data)
        else:
            create_task_log_sync(db, task_id, 'INFO', f"  -> Not Relevant: {result.reasoning}")

    create_task_log_sync(db, task_id, 'STEP', f"---AGENT: Filtered down to {len(relevant_posts_data)} relevant posts.---")
    return {"filtered_posts": relevant_posts_data}


def extract_ideas(state):
    """
    Extracts structured business ideas from filtered posts and saves them to the database.
    """
    task_id = state["task_id"]
    db = state["db"]
    posts_to_analyze = state["filtered_posts"]

    create_task_log_sync(db, task_id, 'STEP', "---AGENT: EXTRACTING IDEAS---")
    
    total_ideas = 0
    for post_data in posts_to_analyze:
        source_post = create_source_post_sync(db, task_id, post_data)
        
        create_task_log_sync(db, task_id, 'INFO', f"Extracting ideas from post: '{post_data['title']}'", data={"url": post_data['url']})
        try:
            result = extraction_chain.invoke({"post_title": post_data["title"], "post_content": post_data["selftext"]})
            for idea_model in result.ideas:
                idea_data = idea_model.dict()
                create_extracted_idea_sync(db, task_id, source_post.id, idea_data)
                total_ideas += 1
                create_task_log_sync(db, task_id, 'IDEA_EXTRACTED', f"  -> Found Idea: {idea_data['solution_idea']}", data=idea_data)
        except Exception as e:
            create_task_log_sync(db, task_id, 'ERROR', f"  -> Error extracting ideas from post {post_data['id']}: {e}")
            continue
            
    create_task_log_sync(db, task_id, 'STEP', f"---AGENT: Extracted a total of {total_ideas} ideas.---")
    return {}


def analyze_trends(state):
    """
    Analyzes all extracted ideas for the task from the database to find trends.
    """
    task_id = state["task_id"]
    db = state["db"]
    create_task_log_sync(db, task_id, 'STEP', "---AGENT: ANALYZING TRENDS---")
    
    task = get_task_sync(db, task_id)
    ideas_from_db = [idea.to_dict() for idea in task.extracted_ideas]

    if not ideas_from_db:
        summary = "No business ideas were extracted, so no trend analysis could be performed."
        create_task_log_sync(db, task_id, 'INFO', summary)
        return {"analysis_summary": summary}

    ideas_json = json.dumps(ideas_from_db, indent=2, cls=UUIDEncoder)
    summary = analysis_chain.invoke({"ideas_json": ideas_json})
    
    create_task_log_sync(db, task_id, 'STEP', "---AGENT: Analysis complete.---")
    return {"analysis_summary": summary}


def generate_report(state):
    """
    Generates the final report using all data fetched from the database for the task.
    """
    task_id = state["task_id"]
    db = state["db"]
    query = state["query"]
    analysis_summary = state["analysis_summary"]
    create_task_log_sync(db, task_id, 'STEP', "---AGENT: GENERATING REPORT---")

    task = get_task_sync(db, task_id)
    ideas_from_db = [idea.to_dict() for idea in task.extracted_ideas]
    
    if not ideas_from_db:
        report = f"""# Reddit Research Report for "{query}"\n\n## No Opportunities Found\nUnfortunately, no specific business ideas or significant user pain points could be extracted from the Reddit posts based on your query."""
    else:
        ideas_json = json.dumps(ideas_from_db, indent=2, cls=UUIDEncoder)
        report = report_chain.invoke({
            "query": query, 
            "analysis_summary": analysis_summary, 
            "ideas_json": ideas_json
        })
    
    create_task_log_sync(db, task_id, 'STEP', "---AGENT: Report generation complete.---")
    return {"final_report": report}