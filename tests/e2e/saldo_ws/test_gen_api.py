import pytest
from fastapi import status
from httpx import AsyncClient


class TestGenRoutes:
    @pytest.mark.parametrize("paradigm, word", [("vb_vs_dväljas", "dväljas")])
    @pytest.mark.asyncio
    async def test_json_valid_input_returns_200(
        self, client: AsyncClient, paradigm: str, word: str, snapshot_json
    ) -> None:
        res = await client.get(f"/gen/json/{paradigm}/{word}")

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == snapshot_json

    @pytest.mark.parametrize(
        "paradigm, word", [("xx_xx_xxx", "xxx"), ("vb_vs_dväljas", "dväljas")]
    )
    @pytest.mark.asyncio
    async def test_xml_valid_input_returns_200(
        self, client: AsyncClient, paradigm: str, word: str, snapshot
    ) -> None:
        res = await client.get(f"/gen/xml/{paradigm}/{word}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/xml"
        assert res.text == snapshot

    @pytest.mark.parametrize(
        "paradigm, word", [("vb_vs_dväljas", "dväljas"), ("xx_xx_xxx", "xxx")]
    )
    @pytest.mark.asyncio
    async def test_html_valid_lemma_returns_200(
        self, client: AsyncClient, paradigm: str, word: str, snapshot
    ) -> None:
        res = await client.get(f"/gen/html/{paradigm}/{word}")

        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        assert res.text == snapshot
