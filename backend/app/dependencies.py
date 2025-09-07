from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injector that provides a database session for API endpoints.
    """
    async with AsyncSessionLocal() as session:
        yield session
        