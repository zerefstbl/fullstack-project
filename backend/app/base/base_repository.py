from typing import TypeVar, Generic, Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from typing import AsyncIterator
from sqlalchemy import func

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get_all(self) -> AsyncIterator[T]:
        stmt = select(self.model)
        stream = await self.session.stream_scalars(stmt.order_by(self.model.id))
        async for row in stream:
            yield row

    async def get_by_id(self, id: int) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def delete(self, instance: T) -> None:
        await self.session.delete(instance)
        await self.session.flush()

    async def get_count(self) -> int | None:
        stmt = select(func.count()).select_from(self.model)
        result = await self.session.scalar(stmt)
        return result
