# backend/app/db/models.py

import uuid
from datetime import datetime
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

class ResearchTask(Base):
    __tablename__ = "research_task"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="PENDING")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # --- RELATIONSHIPS ---
    report = relationship("Report", back_populates="task", uselist=False, cascade="all, delete-orphan")
    logs = relationship("TaskLog", back_populates="task", order_by="TaskLog.created_at", cascade="all, delete-orphan")
    source_posts = relationship("SourcePost", back_populates="task", cascade="all, delete-orphan")
    extracted_ideas = relationship("ExtractedIdea", back_populates="task", cascade="all, delete-orphan")

class Report(Base):
    __tablename__ = "report"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("research_task.id"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    task = relationship("ResearchTask", back_populates="report")

class TaskLog(Base):
    __tablename__ = "task_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("research_task.id"))
    
    # --- MODIFIED COLUMNS ---
    type: Mapped[str] = mapped_column(String(50)) # e.g., 'STEP', 'INFO', 'POST_FOUND'
    message: Mapped[str] = mapped_column(String)
    data: Mapped[dict | None] = mapped_column(JSON, nullable=True) # For structured data
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    task = relationship("ResearchTask", back_populates="logs")

# --- NEW TABLE ---
class SourcePost(Base):
    __tablename__ = "source_post"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("research_task.id"))
    
    # Reddit-specific data
    post_id: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    score: Mapped[int] = mapped_column(Integer)
    num_comments: Mapped[int] = mapped_column(Integer)

    task = relationship("ResearchTask", back_populates="source_posts")
    # A single source post can lead to multiple extracted ideas
    ideas = relationship("ExtractedIdea", back_populates="source_post", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "task_id": str(self.task_id),  # Convert UUID to string
            "post_id": self.post_id,
            "title": self.title,
            "url": self.url,
            "score": self.score,
            "num_comments": self.num_comments
        }

# --- NEW TABLE ---
class ExtractedIdea(Base):
    __tablename__ = "extracted_idea"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("research_task.id"))
    source_post_id: Mapped[int] = mapped_column(ForeignKey("source_post.id"))
    
    pain_point: Mapped[str] = mapped_column(Text)
    solution_idea: Mapped[str] = mapped_column(Text)
    target_audience: Mapped[str] = mapped_column(String)
    business_model: Mapped[str] = mapped_column(String)

    task = relationship("ResearchTask", back_populates="extracted_ideas")
    source_post = relationship("SourcePost", back_populates="ideas")
    
    def to_dict(self):
        return {
            "id": self.id,
            "task_id": str(self.task_id),  # Convert UUID to string
            "source_post_id": self.source_post_id,
            "pain_point": self.pain_point,
            "solution_idea": self.solution_idea,
            "target_audience": self.target_audience,
            "business_model": self.business_model
        }