import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.anyio
async def test_notebooks_read(ac: AsyncClient, session: AsyncSession) -> None:
    response = await ac.get(
        f"/api/v1/pokemons/",
    )
    assert 200 == response.status_code
