import os
import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Set the environment to "test" BEFORE any application code is imported.
# This is crucial for loading the correct .env.test settings.
os.environ["ENVIRONMENT"] = "test"

from app.main import app
from app.db.models import Base
from app.dependencies import get_db
from app.core.config import settings

# --- Database Setup for Testing ---

# Create a synchronous engine for setting up/tearing down the test database schema
sync_engine = create_engine(str(settings.DATABASE_URL))

# Create an asynchronous engine that our test client will use to talk to the DB
async_engine = create_async_engine(str(settings.DATABASE_URL))
AsyncTestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the entire test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    A session-scoped fixture to create and destroy the test database schema.
    'autouse=True' means this runs automatically for the test session.
    """
    # Create all database tables
    Base.metadata.create_all(bind=sync_engine)
    print("\n--- Test database created. ---")
    yield
    # Drop all database tables after tests are done
    Base.metadata.drop_all(bind=sync_engine)
    print("\n--- Test database dropped. ---")


@pytest.fixture
async def db_session():
    """
    Provides a clean database session for a single test function.
    """
    async with AsyncTestingSessionLocal() as session:
        yield session


@pytest.fixture
async def test_client(db_session):
    """
    Provides a fully configured test client for making API requests.
    It's wired up to use the test database and a clean session for each test.
    """
    def override_get_db():
        """
        This is the dependency override. When the API endpoint asks for a DB session
        via `Depends(get_db)`, FastAPI will run this function instead.
        """
        try:
            yield db_session
        finally:
            # The session is automatically closed by the db_session fixture
            pass

    # Apply the override to our FastAPI app
    app.dependency_overrides[get_db] = override_get_db
    
    # Create the async client using the correct transport for ASGI apps
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    # Clean up the override after the test is complete
    del app.dependency_overrides[get_db]