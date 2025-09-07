# backend/app/api/v1/endpoints/research.py

import uuid
import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.worker.tasks import run_research_agent
from app.dependencies import get_db
from app.db.models import ResearchTask
from app.db.crud import get_task_with_details


# --- Pydantic Models for API Responses ---
class TaskLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type: str
    message: str
    data: Dict[str, Any] | None = None
    created_at: datetime.datetime

class SourcePostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    url: str
    score: int
    num_comments: int

class ExtractedIdeaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    pain_point: str
    solution_idea: str
    target_audience: str
    business_model: str
    source_post_id: int

class ReportDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    content: str

class FullTaskDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID 
    status: str
    query: str
    logs: List[TaskLogResponse]
    source_posts: List[SourcePostResponse]
    extracted_ideas: List[ExtractedIdeaResponse]
    report: ReportDetailResponse | None = None

class ResearchRequest(BaseModel):
    query: str
    subreddits: str

class TaskCreationResponse(BaseModel):
    task_id: str
    status: str

# --- API Router ---
router = APIRouter()

@router.post("", response_model=TaskCreationResponse, status_code=202)
async def start_research(request: ResearchRequest, db: AsyncSession = Depends(get_db)):
    new_task = ResearchTask(query=request.query)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    run_research_agent.delay(str(new_task.id), request.subreddits)
    return {"task_id": str(new_task.id), "status": new_task.status}

@router.get("/{task_id}", response_model=FullTaskDataResponse)
async def get_full_task_data(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieves all data for a research task.
    """
    task = await get_task_with_details(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # --- RESTORE THE SIMPLE, RELIABLE RETURN ---
    return task