from app.base.base_repository import BaseRepository
from app.models.pokemon import Pokemon, Type
from sqlalchemy.ext.asyncio import AsyncSession

class PokemonRepository(BaseRepository[Pokemon]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Pokemon)

class TypeRepository(BaseRepository[Type]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Type)
