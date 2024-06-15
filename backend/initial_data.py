from alembic import op
import asyncio
from sqlalchemy.orm import Session
import httpx
from app.models.pokemon import Pokemon, Type
from asyncio import Semaphore
from app.db import AsyncSessionLocal
# revision identifiers, used by Alembic.

async def fetch_pokemon_data():
    url = "https://pokeapi.co/api/v2/pokemon?limit=9999999"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from PokeAPI: {response.status_code}")
        data = response.json()
        return data["results"]

async def fetch_pokemon_details(semaphore: Semaphore, id: str):
    async with semaphore, httpx.AsyncClient() as client:
        try:
            response = await client.get(f'https://pokeapi.co/api/v2/pokemon/{id}/')
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data from PokeAPI: {response.status_code}")
            data = response.json()
            return data
        except Exception as error:
            print('ERROR: ', str(error))
            pass

def format_data(data: dict) -> dict:
    return {
        'id': data['id'],
        'name': data['name'],
        'front_picture': data['sprites']['front_default'],
        'back_picture': data['sprites']['back_default'],
        'hp': next((stat for stat in data['stats'] if stat['stat']['name'] == 'hp'), None).get('base_stat', None),
        'attack': next((stat for stat in data['stats'] if stat['stat']['name'] == 'attack'), None).get('base_stat', None),
        'defense': next((stat for stat in data['stats'] if stat['stat']['name'] == 'defense'), None).get('base_stat', None),
        'special_attack': next((stat for stat in data['stats'] if stat['stat']['name'] == 'special-attack'), None).get('base_stat', None),
        'special_defense': next((stat for stat in data['stats'] if stat['stat']['name'] == 'special-defense'), None).get('base_stat', None),
        'speed': next((stat for stat in data['stats'] if stat['stat']['name'] == 'speed'), None).get('base_stat', None),
    }

async def async_upgrade() -> None:
    # Inicie uma nova sessão do SQLAlchemy
    async with AsyncSessionLocal() as session:

        # Fetch the list of pokemons
        pokemons = await fetch_pokemon_data()

        # Create a semaphore to limit the number of simultaneous requests
        semaphore = Semaphore(20)

        # Fetch the details of each pokemon in parallel
        tasks = [fetch_pokemon_details(semaphore, pokemon["url"].split('/')[-2]) for pokemon in pokemons]
        pokemons = await asyncio.gather(*tasks)

        batch_size = 300  # Ajuste este valor para o que melhor se adequa ao seu caso
        for i, poke in enumerate(pokemons, start=1):
            data = format_data(data=poke)
            pokemon = Pokemon(**data)
            session.add(pokemon)
            await session.flush()  # Sincronize a sessão para obter o ID do pokemon

            type = Type(pokemon_id=pokemon.id, name=pokemon.name)  # Substitua 'pokemon_id' pelo nome real da sua chave estrangeira
            session.add(type)

            if i % batch_size == 0:
                await session.commit()  # Faça commit a cada 'batch_size' inserções
            await session.commit()

asyncio.run(async_upgrade())
