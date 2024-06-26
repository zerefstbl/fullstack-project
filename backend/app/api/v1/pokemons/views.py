from fastapi import APIRouter, Depends, Path, Request, Response, Query
from .use_cases import ListAllPokemons, ReadPokemon, ExportPokemonsToXML
from .schemas import FullPokemonDetailSchema, ReadAllPokemonSchema, Pagination
from .repository import PokemonRepository

router = APIRouter(prefix="/pokemons")

@router.get("", response_model=ReadAllPokemonSchema)
async def read_all(
    request: Request,
    use_case: ListAllPokemons = Depends(ListAllPokemons),
    limit: int = Query(0, ge=1),
    offset: int = Query(0, ge=0),
) -> ReadAllPokemonSchema:
    pokemons = [nb async for nb in use_case.execute(limit=limit, offset=offset)]
    total_pokemons = await use_case.count()
    next_offset = offset + limit if total_pokemons > offset + limit else None
    previous_offset = offset - limit if offset - limit >= 0 else None

    return ReadAllPokemonSchema(
        pokemons=pokemons,
        pagination=Pagination(
            total=total_pokemons,
            next=next_offset,
            previous=previous_offset
        )
    )

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
