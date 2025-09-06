# backend/app/main.py

import asyncio
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.endpoints import research

app = FastAPI(
    title="AI Reddit Researcher API",
    version="0.1.0",
    description="API for managing and running AI Reddit research agents."
)

@app.get("/health", tags=["Status"])
def health_check():
    """
    Health check endpoint to confirm the API is running.
    """
    return {"status": "ok"}

# Include the research router with a prefix and tags
app.include_router(
    research.router, 
    prefix="/api/v1/research", 
    tags=["Research"]
)
