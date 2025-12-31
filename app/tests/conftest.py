import os
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.pool import NullPool

from app.main import create_app
from app.core.db import get_db

from app.core.db import Base


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
def db_url():
    return os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@db:5432/postgres",
    )


@pytest.fixture(scope="function")
async def engine(db_url):
    # NullPool evita reaproveitar conexão entre loops/requests
    engine = create_async_engine(db_url, poolclass=NullPool)

    # DB limpo por teste (simples e robusto)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
def session_maker(engine):
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="function")
async def client(session_maker):
    app = create_app()

    async def _override_get_db():
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
