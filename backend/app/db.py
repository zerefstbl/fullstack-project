import logging
from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.settings import settings
import os
from dotenv import load_dotenv
load_dotenv()

if os.environ['APP_CONFIG_FILE'] == 'test':
    settings.DB_URI='postgresql+asyncpg://postgres:postgres@db-test:5432/rocketman-tech-test'

logger = logging.getLogger(__name__)
async_engine = create_async_engine(
    settings.DB_URI,
    pool_pre_ping=True,
    echo=settings.ECHO_SQL,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)

async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)

AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]
