from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# --- ASYNC SETUP for FastAPI ---
async_engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)

# --- SYNC SETUP for Celery ---
sync_engine = create_engine(
    str(settings.DATABASE_URL).replace("postgresql+psycopg", "postgresql+psycopg"),
)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
