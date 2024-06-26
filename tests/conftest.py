import asyncio
from typing import AsyncGenerator

import httpx
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.database import get_async_session
from src.auth.models import Base, RoleOrm, UserOrm
from src.operations.models import Base, OperationOrm

from src.config import settings
from src.main import app

engine_test = create_async_engine(url=settings.DATABASE_URL_TEST_asyncpg, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture(scope="session")
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     policy = asyncio.WindowsSelectorEventLoopPolicy()
#     res = policy.new_event_loop()
#     asyncio.set_event_loop(res)
#     res._close = res.close
#     res.close = lambda: None
#
#     yield res
#
#     res._close()

transport = httpx.ASGITransport(app=app)
client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
