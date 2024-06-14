import pytest
from fastapi import status
from httpx import AsyncClient


class TestFullformLexRoutes:
    @pytest.mark.parametrize("segment", ["dväljs"])
    @pytest.mark.asyncio
    async def test_json_valid_input_returns_200(
        self, client: AsyncClient, segment: str, snapshot_json
    ) -> None:
        res = await client.get(f"/fl/json/{segment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.json() == snapshot_json

    @pytest.mark.parametrize("segment", ["tt"])
    @pytest.mark.asyncio
    async def test_json_missing_segment_returns_404(
        self, client: AsyncClient, segment: str, snapshot_json
    ) -> None:
        res = await client.get(f"/fl/json/{segment}")
        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.json() == snapshot_json

    @pytest.mark.parametrize("segment", ["t", "dväljs"])
    @pytest.mark.asyncio
    async def test_xml_valid_input_returns_200(
        self, client: AsyncClient, segment: str, snapshot
    ) -> None:
        res = await client.get(f"/fl/xml/{segment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/xml"
        assert res.text == snapshot

    @pytest.mark.parametrize("segment", ["", " ", "dväljas", "femrumslägenhet"])
    @pytest.mark.asyncio
    async def test_html_valid_input_returns_200(
        self, client: AsyncClient, segment: str, snapshot
    ) -> None:
        res = await client.get(f"/fl/html?segment={segment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        assert res.text == snapshot

    @pytest.mark.parametrize("segment", ["löparsko"])
    @pytest.mark.asyncio
    async def test_html_missing_input_returns_404(
        self, client: AsyncClient, segment: str, snapshot
    ) -> None:
        res = await client.get(f"/fl/html?segment={segment}")
        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        assert res.text == snapshot

    @pytest.mark.parametrize("segment", ["", " ", "dväljas", "dväljsxdf"])
    @pytest.mark.asyncio
    async def test_html_orig_valid_input_returns_307(
        self,
        client: AsyncClient,
        segment: str,
    ) -> None:
        res = await client.get(f"/fl/html/{segment}")
        assert res.status_code == status.HTTP_307_TEMPORARY_REDIRECT
