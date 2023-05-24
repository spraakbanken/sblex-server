import pytest
from httpx import AsyncClient


class TestFmServerMorphRoutes:
    @pytest.mark.asyncio
    async def test_morph_get(self, fm_client: AsyncClient) -> None:
        response = await fm_client.get("/morph/dväljes/0")
        assert response.status_code == 200
