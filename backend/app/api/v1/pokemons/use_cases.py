from typing import AsyncIterator

from fastapi import HTTPException

from app.db import AsyncSession
# from app.models import Pokemon, Type
from .repository import PokemonRepository
from .schemas import BasePokemonSchema, FullPokemonDetailSchema

class ListAllPokemons:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self) -> AsyncIterator[BasePokemonSchema]:
        async with self.async_session.begin() as session:
            async for pokemon in PokemonRepository(session=session).get_all():
                yield BasePokemonSchema.model_validate(pokemon)

class ReadPokemon:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, pokemon_id: int) -> FullPokemonDetailSchema:
        async with self.async_session.begin() as session:
            pokemon = await PokemonRepository(session=session).get_by_id(id=pokemon_id, include_types=True)
            if not pokemon:
                raise HTTPException(status_code=404)
            return FullPokemonDetailSchema.model_validate(pokemon)
