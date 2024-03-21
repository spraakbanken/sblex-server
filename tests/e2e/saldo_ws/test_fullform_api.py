import pytest
from fastapi import status
from httpx import AsyncClient


class TestFullformRoutes:
    @pytest.mark.parametrize("fragment", ["dväljs", "dv", "dvä", "dväl"])
    @pytest.mark.asyncio
    async def test_json_valid_input_returns_200(
        self, client: AsyncClient, fragment: str, snapshot_json
    ):
        res = await client.get(f"/ff/json/{fragment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.json() == snapshot_json

    @pytest.mark.parametrize("fragment", ["dväljs", "dv", "dvä", "dväl"])
    @pytest.mark.asyncio
    async def test_html_valid_input_returns_200(
        self, client: AsyncClient, fragment: str, snapshot
    ):
        res = await client.get(f"/ff/html?fragment={fragment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        assert res.text == snapshot

    @pytest.mark.parametrize("fragment", ["dväljs", "dv", "dvä", "dväl"])
    @pytest.mark.asyncio
    async def test_html_orig_valid_input_returns_307(
        self,
        client: AsyncClient,
        fragment: str,
    ):
        res = await client.get(f"/ff/html/{fragment}")
        assert res.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    @pytest.mark.parametrize("fragment", ["dväljs", "dv", "dvä", "dväl"])
    @pytest.mark.asyncio
    async def test_xml_valid_input_returns_200(
        self, client: AsyncClient, fragment: str, snapshot
    ):
        res = await client.get(f"/ff/xml/{fragment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/xml"
        assert res.text == snapshot
