import pytest
from fastapi import status
from httpx import AsyncClient


class TestParaRoutes:
    @pytest.mark.asyncio
    async def test_json_valid_input_return_200(self, client: AsyncClient, snapshot_json) -> None:
        res = await client.get("/para/json/dväljes:vb")
        assert res.status_code == status.HTTP_200_OK
        assert res.json() == snapshot_json

    @pytest.mark.asyncio
    async def test_json_invalid_input_return_400(
        self, client: AsyncClient, snapshot_json
    ) -> None:
        res = await client.get("/para/json/dväljes")
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.json() == snapshot_json
