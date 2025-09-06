import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session # <-- Import the synchronous Session
from sqlalchemy.future import select
from app.db.models import ResearchTask, Report, TaskLog


# --- ASYNC Functions for FastAPI ---

async def get_task(db: AsyncSession, task_id: uuid.UUID):
    """(Async) Fetches a task by its ID."""
    result = await db.execute(select(ResearchTask).where(ResearchTask.id == task_id))
    return result.scalar_one_or_none()

async def get_task_logs(db: AsyncSession, task_id: uuid.UUID):
    """(Async) Fetches all logs for a given task, ordered by creation time."""
    result = await db.execute(
        select(TaskLog)
        .where(TaskLog.task_id == task_id)
        .order_by(TaskLog.created_at)
    )
    return result.scalars().all()

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

def create_task_log_sync(db: Session, task_id: uuid.UUID, message: str):
    """(Sync) Creates a new log entry for a task."""
    log_entry = TaskLog(task_id=task_id, message=message)
    db.add(log_entry)
    db.commit()
    return log_entry