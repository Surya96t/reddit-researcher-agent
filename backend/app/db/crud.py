import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.future import select
from app.db.models import ResearchTask, Report, TaskLog, SourcePost, ExtractedIdea # <-- Add new models

# --- ASYNC Functions for FastAPI ---

async def get_task(db: AsyncSession, task_id: uuid.UUID):
    """(Async) Fetches a task by its ID."""
    result = await db.execute(select(ResearchTask).where(ResearchTask.id == task_id))
    return result.scalar_one_or_none()

async def get_task_with_details(db: AsyncSession, task_id: uuid.UUID):
    """(Async) Fetches a task and all its related logs, posts, and ideas."""
    result = await db.execute(
        select(ResearchTask)
        .where(ResearchTask.id == task_id)
        .options(
            joinedload(ResearchTask.logs),
            joinedload(ResearchTask.source_posts),
            joinedload(ResearchTask.extracted_ideas),
            joinedload(ResearchTask.report) # Also good to explicitly load the report
        )
    )
    # --- THIS IS THE FIX ---
    # Call .unique() to handle the cartesian product from the JOINs
    return result.unique().scalar_one_or_none()


# --- SYNC Functions for Celery Worker ---

def get_task_sync(db: Session, task_id: uuid.UUID):
    """(Sync) Fetches a task by its ID."""
    return db.query(ResearchTask).filter(ResearchTask.id == task_id).first()

def update_task_status_sync(db: Session, task_id: uuid.UUID, status: str):
    """(Sync) Updates the status of a task."""
    task = get_task_sync(db, task_id)
    if task:
        task.status = status
        db.commit()
    return task

def create_report_sync(db: Session, task_id: uuid.UUID, content: str):
    """(Sync) Creates a new report and links it to a task."""
    report = Report(task_id=task_id, content=content)
    db.add(report)
    db.commit()
    return report

def create_task_log_sync(db: Session, task_id: uuid.UUID, type: str, message: str, data: Dict[str, Any] | None = None):
    """(Sync) Creates a new structured log entry for a task."""
    log_entry = TaskLog(task_id=task_id, type=type, message=message, data=data)
    db.add(log_entry)
    db.commit()
    return log_entry

# --- ADD NEW SYNC FUNCTIONS ---

def create_source_post_sync(db: Session, task_id: uuid.UUID, post_data: Dict[str, Any]) -> SourcePost:
    """(Sync) Creates a new source post entry."""
    # Check if post already exists to avoid duplicates
    existing_post = db.query(SourcePost).filter(SourcePost.post_id == post_data['id']).first()
    if existing_post:
        return existing_post
    
    source_post = SourcePost(
        task_id=task_id,
        post_id=post_data['id'],
        title=post_data['title'],
        url=post_data['url'],
        score=post_data['score'],
        num_comments=post_data['num_comments']
    )
    db.add(source_post)
    db.commit()
    db.refresh(source_post) # To get the auto-generated ID
    return source_post

def create_extracted_idea_sync(db: Session, task_id: uuid.UUID, source_post_id: int, idea_data: Dict[str, Any]):
    """(Sync) Creates a new extracted idea entry."""
    idea = ExtractedIdea(
        task_id=task_id,
        source_post_id=source_post_id,
        pain_point=idea_data['pain_point'],
        solution_idea=idea_data['solution_idea'],
        target_audience=idea_data['target_audience'],
        business_model=idea_data['business_model']
    )
    db.add(idea)
    db.commit()
    return idea