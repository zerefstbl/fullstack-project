from fastapi import APIRouter, Depends, Path, Request

from .use_cases import ListAllPokemons
from .schemas import BasePokemonSchema, ReadAllPokemonSchema

router = APIRouter(prefix="/pokemons")

@router.get("", response_model=ReadAllPokemonSchema)
async def read_all(
    request: Request, use_case: ListAllPokemons = Depends(ListAllPokemons)
) -> ReadAllPokemonSchema:
    return ReadAllPokemonSchema(pokemons=[nb async for nb in use_case.execute()])
