from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, SessionTransaction

from app.db import get_session
from app.main import app
from app.models.base import Base
from app.settings import settings

@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"

@pytest.fixture
async def ac() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="https://test") as c:
        yield c
