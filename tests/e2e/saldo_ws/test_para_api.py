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

    @pytest.mark.asyncio
    async def test_html_invalid_input_return_400(self, client: AsyncClient, snapshot) -> None:
        res = await client.get("/para/html?words=dväljes")
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.text == snapshot

    @pytest.mark.asyncio
    async def test_orig_html_return_307(self, client: AsyncClient) -> None:
        res = await client.get("/para/html/dväljes")
        assert res.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    @pytest.mark.asyncio
    async def test_html_no_input_return_200(self, client: AsyncClient, snapshot) -> None:
        res = await client.get("/para/html")
        assert res.status_code == status.HTTP_200_OK
        assert res.text == snapshot

    @pytest.mark.asyncio
    async def test_html_valid_input_return_200(self, client: AsyncClient, snapshot) -> None:
        res = await client.get("/para/html?words=dväljes:vb")
        assert res.status_code == status.HTTP_200_OK
        assert res.text == snapshot
