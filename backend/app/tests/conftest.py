import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

from app.main import app
from app.db import get_session
from app.settings import settings
from dotenv import load_dotenv

load_dotenv()
import os
os.environ['TEST_DATABASE'] = 'true'
os.environ['DB_URI'] = 'postgresql+asyncpg://postgres:postgres@db-test:5432/rocketman-tech-test'

# Configuração do banco de dados de teste
@pytest.fixture(scope="module")
async def setup_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA foreign_keys=ON"))
        try:
            await conn.execute(text("DROP TABLE IF EXISTS test_table"))
            # await conn.execute(text("DROP TABLE IF EXISTS types"))
            # await conn.execute(text("DROP TABLE IF EXISTS pokemons"))
        except:
            pass

    async with engine.begin() as conn:
        """
        Using SQL in this way to create the table is not recommended
        I only used it because I didn't have time to carry out complex configurations and needed to do it in advance.
        But this is not scalable nor practical to maintain, so you must configure a test db as well as the test environment
        """
        await conn.execute(text("CREATE TABLE test_table (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)"))
        await conn.execute(text("""
                CREATE TABLE pokemons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                front_picture TEXT,
                back_picture TEXT,
                hp INTEGER NOT NULL,
                attack INTEGER NOT NULL,
                defense INTEGER NOT NULL,
                special_attack INTEGER NOT NULL,
                special_defense INTEGER NOT NULL,
                speed INTEGER NOT NULL
            );
            """))
        await conn.execute(text("""
                CREATE TABLE types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                pokemon_id INTEGER NOT NULL,
                FOREIGN KEY(pokemon_id) REFERENCES pokemons(id)
            );
            """))

    yield engine

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


@pytest.fixture(scope="module")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
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
