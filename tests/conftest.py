from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.adapters.db.session import get_async_session
from app.adapters.db.tables.base import Base
from app.api.app import app


@pytest.fixture
def engine():
    engine = create_async_engine("sqlite+aiosqlite://")
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture
async def db_session(engine) -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
        async with async_session_maker(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture
def override_get_async_session(db_session: AsyncSession):
    async def _override_get_async_session():
        yield db_session

    return _override_get_async_session


@pytest.fixture
async def async_client(override_get_async_session):
    app.dependency_overrides[get_async_session] = override_get_async_session
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def anyio_backend():
    return "asyncio"
