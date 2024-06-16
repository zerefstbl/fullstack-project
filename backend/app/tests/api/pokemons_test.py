import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import copy
from app.api.v1.pokemons.repository import PokemonRepository

bulbassaur = {
    'id': 1,
    'name': "bulbasaur",
    'front_picture': "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
    'back_picture': "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
    'hp': 45,
    'attack': 49,
    'defense': 49,
    'special_attack': 65,
    'special_defense': 65,
    'speed': 45
}

ivyssaur = {
    'id': 2,
    'name': "ivyssaur",
    'front_picture': "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
    'back_picture': "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
    'hp': 67,
    'attack': 56,
    'defense': 56,
    'special_attack': 76,
    'special_defense': 73,
    'speed': 54
}

@pytest.fixture(scope="module")
async def setup_data(session: AsyncSession):
    from app.models import Pokemon, Type

    pokemon = Pokemon(
       **bulbassaur
    )
    pokemon2 = Pokemon(
        **ivyssaur
    )
    session.add(pokemon)
    session.add(pokemon2)
    await session.flush()
    await session.refresh(pokemon)
    await session.refresh(pokemon2)
    print(f"Inserted Pokemon with ID: {pokemon.id}")

    type1 = Type(name="Poison", pokemon_id=pokemon.id)
    type2 = Type(name="Grass", pokemon_id=pokemon.id)
    session.add_all([type1, type2])
    await session.commit()

    yield

@pytest.mark.anyio
async def test_pokemons_read_all(ac: AsyncClient, session: AsyncSession, setup_data) -> None:
    response = await ac.get("/api/v1/pokemons")
    response_json = response.json()
    pokemon = await PokemonRepository(session=session).get_by_id(id=1, include_types=True)

    assert response.status_code == 200
    assert len(response_json['pokemons']) == 2
    bulbassaur.update({
        'types': [
            {
                'id': type.id,
                'name': type.name
            }
            for type in pokemon.types
        ]
    })
    ivyssaur.update({
        'types': []
    })

    expected_value = {
        'pokemons': [
            bulbassaur,
            ivyssaur,
        ],
        "pagination": {
            "total": 2,
            "next": 0,
            "previous": 0
        }
    }


    assert response_json == expected_value

@pytest.mark.anyio
async def test_pokemons_read_details(ac: AsyncClient, session: AsyncSession, setup_data) -> None:
    pokemon = await PokemonRepository(session=session).get_by_id(id=1, include_types=True)
    expected_value = {
        'id': pokemon.id,
        'name': pokemon.name,
        'front_picture': pokemon.front_picture,
        'back_picture': pokemon.back_picture,
        'hp': pokemon.hp,
        'attack': pokemon.attack,
        'defense': pokemon.defense,
        'special_attack': pokemon.special_attack,
        'special_defense': pokemon.special_defense,
        'speed': pokemon.speed,
        'types': [
            {
                'id': type.id,
                'name': type.name
            }
            for type in pokemon.types
        ]
    }

    response = await ac.get("/api/v1/pokemons/1")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == expected_value
