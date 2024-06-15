import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db import get_session
from app.settings import settings
from dotenv import load_dotenv

load_dotenv()
import os
os.environ['TEST_DATABASE'] = 'true'
os.environ['DB_URI'] = 'postgresql+asyncpg://postgres:postgres@db-test:5432/rocketman-tech-test'

@pytest.fixture(scope="module")
async def setup_db():
    engine = create_async_engine("postgresql+asyncpg://postgres:postgres@db-test:5432/rocketman-tech-test")
    async with engine.begin() as conn:
        try:
            await conn.execute(text("DROP TABLE IF EXISTS test_table"))
            await conn.execute(text("delete from types"))
            await conn.execute(text("delete from pokemons"))
        except:
            pass

    async with engine.begin() as conn:
        await conn.execute(text("CREATE TABLE test_table (id SERIAL PRIMARY KEY, name TEXT)"))

    yield engine

    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS test_table"))

    await engine.dispose()

@pytest.fixture(scope="module")
async def async_db(setup_db):
    async_engine = setup_db
    return async_engine

@pytest.fixture(scope="module")
async def get_db(async_db):
    async_session = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_db,
        future=True,
        class_=AsyncSession,
    )
    session = async_session()
    async with session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise

@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="module")
async def get_session(async_db):
    async_session = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_db,
        future=True,
        class_=AsyncSession,
    )
    session = async_session()
    async with session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise

@pytest.fixture(scope="module")
async def session(get_db) -> AsyncGenerator[AsyncSession, None]:
    async with get_db as session:
        yield session
