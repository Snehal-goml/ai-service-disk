import httpx
import pytest
import pytest_asyncio

from app.core.database import AsyncSessionLocal, engine, Base
from app.services.ticket_service import TicketService

BASE_URL = "http://127.0.0.1:8000"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture
def client():
    """Returns an httpx Client pointed at the running dev server."""
    with httpx.Client(base_url=BASE_URL) as c:
        yield c


@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def ticket_service(db_session):
    return TicketService(db_session)

