from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class BasePokemonSchema(BaseModel):
    id: int
    name: str
    front_picture: str | None
    back_picture: str | None
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

    model_config = ConfigDict(from_attributes=True)

class TypeSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class FullPokemonDetailSchema(BasePokemonSchema):
    types: List[TypeSchema]

class Pagination(BaseModel):
    total: int
    next: Optional[int] = None
    previous: Optional[int] = None

class ReadAllPokemonSchema(BaseModel):
    pokemons: List[FullPokemonDetailSchema]
    pagination: Pagination
