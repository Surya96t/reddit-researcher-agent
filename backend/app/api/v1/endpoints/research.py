import uuid
from typing import AsyncGenerator, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
# CHANGE THESE IMPORTS:
from app.worker.tasks import run_research_agent
from app.db.session import AsyncSessionLocal
from app.db.models import ResearchTask
from app.db.crud import get_task, get_task_logs
from datetime import datetime

# Helper for Dependency Injection
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# --- Pydantic Models for API Responses ---
class ReportDetail(BaseModel):
    id: uuid.UUID
    content: str
    created_at: str

class TaskStatusResponse(BaseModel):
    task_id: uuid.UUID
    status: str
    query: str
    report: ReportDetail | None = None

class ResearchRequest(BaseModel):
    query: str

class TaskCreationResponse(BaseModel):
    task_id: str
    status: str

# --- Add a Pydantic model for the log response ---

class TaskLogResponse(BaseModel):
    id: int
    message: str
    created_at: datetime
    
# --- API Router ---
router = APIRouter()

@router.post("", response_model=TaskCreationResponse, status_code=202)
async def start_research(request: ResearchRequest, db: AsyncSession = Depends(get_db)):
    """
    Creates a research task in the DB and dispatches it to a background worker.
    """
    # Create the task in the database first
    new_task = ResearchTask(query=request.query)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    
    # Dispatch the task to Celery
    run_research_agent.delay(str(new_task.id))
    
    return {"task_id": str(new_task.id), "status": new_task.status}

@router.get("/{task_id}", response_model=TaskStatusResponse)
async def get_research_status(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """

    Retrieves the status and result of a research task.
    """
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    report_detail = None
    if task.report:
        report_detail = ReportDetail(
            id=task.report.id,
            content=task.report.content,
            created_at=str(task.report.created_at)
        )

    return {
        "task_id": task.id,
        "status": task.status,
        "query": task.query,
        "report": report_detail
    }
    
# --- ADD THIS NEW ENDPOINT ---
@router.get("/{task_id}/logs", response_model=List[TaskLogResponse])
async def get_logs_for_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieves all log entries for a specific research task.
    """
    logs = await get_task_logs(db, task_id)
    return logs