from app.base.base_repository import BaseRepository, T
from app.models.pokemon import Pokemon, Type
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Generic, Type, Optional
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload
from typing import AsyncIterator

class PokemonRepository(BaseRepository[Pokemon]):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__(session, Pokemon)

    async def get_all(self, limit: int = 0, offset: int = 0, include_types: bool = False) -> AsyncIterator[Pokemon]:
        stmt = select(Pokemon).offset(offset=offset)
        if limit:
            stmt = stmt.limit(limit=limit)
        if include_types:
            stmt = stmt.options(selectinload(Pokemon.types))
        stream = await self.session.stream_scalars(stmt.order_by(Pokemon.name))
        async for row in stream:
            yield row

    async def get_by_id(self, id: int, include_types: bool = False) -> Optional[Pokemon]:
        stmt = select(Pokemon).where(Pokemon.id == id)
        if include_types:
            stmt = stmt.options(selectinload(Pokemon.types))
        result = await self.session.execute(stmt)
        return result.scalar()

class TypeRepository(BaseRepository[Type]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Type)
