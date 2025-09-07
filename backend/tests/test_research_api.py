import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import crud
from app.db.models import ResearchTask

async def test_start_research(test_client: AsyncClient, db_session: AsyncSession, monkeypatch):
    """
    Tests the POST /api/v1/research endpoint.
    """
    # We must "monkeypatch" the Celery task so it doesn't actually run
    monkeypatch.setattr("app.api.v1.endpoints.research.run_research_agent.delay", lambda *args, **kwargs: None)

    test_query = "test query for starting research"
    test_subreddits = "testsub1,testsub2"

    response = await test_client.post(
        "/api/v1/research",
        json={"query": test_query, "subreddits": test_subreddits}
    )

    # 1. Check the API response
    assert response.status_code == 202
    response_data = response.json()
    assert "task_id" in response_data
    assert response_data["status"] == "PENDING"

    # 2. Check that the task was actually created in the database
    task_id = response_data["task_id"]
    db_task = await crud.get_task(db_session, task_id)
    assert db_task is not None
    assert db_task.query == test_query
    assert db_task.status == "PENDING"