import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

async def setup_data(session: AsyncSession) -> None:
    from app.models import Pokemon, Type

    pokemon = Pokemon(**{
        "name": "bulbasaur",
        "front_picture": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        "back_picture": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
        "hp": 45,
        "attack": 49,
        "defense": 49,
        "special_attack": 65,
        "special_defense": 65,
        "speed": 45
    })
    session.add_all([pokemon])
    await session.flush()
    print(pokemon.id)
    type = Type(name="Poison", pokemon_id=pokemon.id)
    type2 = Type(name="Grass", pokemon_id=pokemon.id)
    session.add_all([type, type2])
    await session.flush()

    await session.commit()

@pytest.mark.anyio
async def test_pokemons_read(ac: AsyncClient, session: AsyncSession) -> None:
    await setup_data(session=session)

    response = await ac.get(
        f"/api/v1/pokemons",
    )
    print(len(response.json()['pokemons']))
    assert 200 == response.status_code

