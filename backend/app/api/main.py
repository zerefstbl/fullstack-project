from fastapi import APIRouter
from .v1.pokemons.views import router as pokemons_router
router = APIRouter()
router.include_router(pokemons_router)
