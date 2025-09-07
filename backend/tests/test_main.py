import pytest
from httpx import AsyncClient

# The @pytest.mark.asyncio is no longer needed
async def test_health_check(test_client: AsyncClient):
    """
    Tests that the /health endpoint returns a 200 OK status.
    """
    response = await test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}