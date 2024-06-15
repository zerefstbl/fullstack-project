from fastapi import APIRouter, Depends, Path, Request, Response

from .use_cases import ListAllPokemons, ReadPokemon, ExportPokemonsToXML
from .schemas import FullPokemonDetailSchema, ReadAllPokemonSchema

router = APIRouter(prefix="/pokemons")

@router.get("", response_model=ReadAllPokemonSchema)
async def read_all(
    request: Request, use_case: ListAllPokemons = Depends(ListAllPokemons)
) -> ReadAllPokemonSchema:
    return ReadAllPokemonSchema(pokemons=[nb async for nb in use_case.execute()])

@router.get("/{pokemon_id}", response_model=FullPokemonDetailSchema)
async def read(
    request: Request,
    pokemon_id: int = Path(..., description=""),
    use_case: ReadPokemon = Depends(ReadPokemon),
) -> FullPokemonDetailSchema:
    return await use_case.execute(pokemon_id)

@router.get("/xml/export", response_class=Response)
async def export_pokemon(
    request: Request,
    use_case: ExportPokemonsToXML = Depends(ExportPokemonsToXML),
):
    xml_str = await use_case.execute()
    return Response(content=xml_str, media_type="application/xml")
