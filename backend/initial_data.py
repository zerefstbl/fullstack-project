import asyncio
import httpx
from app.models.pokemon import Pokemon, Type
from asyncio import Semaphore
from app.db import AsyncSessionLocal
from app.api.v1.pokemons.repository import PokemonRepository

async def fetch_pokemon_data():
    url = "https://pokeapi.co/api/v2/pokemon?limit=999999"
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
    async with AsyncSessionLocal() as session:
        print('Adding initial pokemons')
        pokemons_count = await PokemonRepository(session=session).get_count()
        print(pokemons_count)
        if pokemons_count:
            print('Finished.')
            return

        pokemons_data = await fetch_pokemon_data()

        semaphore = Semaphore(5)  # Limita o número de tarefas simultâneas

        tasks = [fetch_pokemon_details(semaphore, pokemon["url"].split('/')[-2]) for pokemon in pokemons_data]

        batch_size = 50  # Tamanho de lote adequado para o sistema
        sleep_time = 1  # Tempo de espera entre os lotes

        for i in range(0, len(tasks), batch_size):
            batch_tasks = tasks[i:i+batch_size]
            results = await asyncio.gather(*batch_tasks)

            # Processamento dos resultados em lotes
            for poke in results:
                if poke:  # Verifica se o resultado não é None
                    data = format_data(data=poke)
                    pokemon = Pokemon(**data)
                    session.add(pokemon)

                    types = [type_info for type_info in poke.get('types', [])]
                    for type_info in types:
                        type_obj = Type(pokemon_id=pokemon.id, name=type_info['type']['name'])
                        session.add(type_obj)

                # Commit a cada lote processado
                if (i + batch_size) % batch_size == 0 or i + len(batch_tasks) == len(tasks):
                    await session.commit()

            await asyncio.sleep(sleep_time)  # Atraso antes do próximo lote

        try:
            await session.commit()  # Commit final para itens restantes
        except Exception as e:
            print('Commit error:', e)
            pass
        import time
        time.sleep(90)
        print('Finished')


asyncio.run(async_upgrade())
