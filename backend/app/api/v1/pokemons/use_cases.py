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

import xml.etree.ElementTree as ET

class ExportPokemonsToXML:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self) -> str:
        root = ET.Element("Pokemons")
        async with self.async_session.begin() as session:
            async for pokemon in PokemonRepository(session=session).get_all():
                pokemon_element = ET.SubElement(root, "Pokemon")
                ET.SubElement(pokemon_element, "id").text = str(pokemon.id)
                ET.SubElement(pokemon_element, "name").text = pokemon.name
                ET.SubElement(pokemon_element, "front_picture").text = pokemon.front_picture
                ET.SubElement(pokemon_element, "back_picture").text = pokemon.back_picture
                ET.SubElement(pokemon_element, "hp").text = str(pokemon.hp)
                ET.SubElement(pokemon_element, "attack").text = str(pokemon.attack)
                ET.SubElement(pokemon_element, "defense").text = str(pokemon.defense)
                ET.SubElement(pokemon_element, "special_attack").text = str(pokemon.special_attack)
                ET.SubElement(pokemon_element, "special_defense").text = str(pokemon.special_defense)
                ET.SubElement(pokemon_element, "speed").text = str(pokemon.speed)
        tree = ET.ElementTree(root)
        xml_str = ET.tostring(tree.getroot(), encoding='utf-8', method='xml').decode()
        return xml_str
