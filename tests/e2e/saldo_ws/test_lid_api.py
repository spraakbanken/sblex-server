import pytest
from fastapi import status
from httpx import AsyncClient


class TestLidRoutes:
    @pytest.mark.parametrize("in_format", ["json", "xml", "html"])
    @pytest.mark.asyncio
    async def test_invalid_input_returns_422(self, client: AsyncClient, in_format: str) -> None:
        res = await client.get(f"/lid/{in_format}/bad-input")
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("lid", ["dväljas..vb.1", "dväljas..1"])
    @pytest.mark.asyncio
    async def test_json_valid_input_returns_200(
        self, client: AsyncClient, lid: str, snapshot_json
    ) -> None:
        res = await client.get(f"/lid/json/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.json() == snapshot_json

    @pytest.mark.parametrize("lid", ["qt..vb.1", "qt..1"])
    @pytest.mark.asyncio
    async def test_json_missing_returns_404(
        self, client: AsyncClient, lid: str, snapshot_json
    ) -> None:
        res = await client.get(f"/lid/json/{lid}")
        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.json() == snapshot_json

    @pytest.mark.asyncio
    async def test_json_rnd_returns_200(
        self,
        client: AsyncClient,
    ) -> None:
        res = await client.get("/lid/json/rnd")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/json"

        actual_data = res.json()
        print(f"{actual_data=}")
        for expected_key in ["lex", "fm", "fp", "mf", "pf", "l", "fs", "path", "ppath"]:
            assert expected_key in actual_data

    @pytest.mark.parametrize("lid", ["dväljas..vb.1", "dväljas..1"])
    @pytest.mark.asyncio
    async def test_xml_valid_input_returns_200(
        self, client: AsyncClient, lid: str, snapshot
    ) -> None:
        res = await client.get(f"/lid/xml/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/xml"

        assert res.text == snapshot

    @pytest.mark.parametrize(
        "lid",
        [
            "xxxxx..xx.1",
            "xxxxx..1",
        ],
    )
    @pytest.mark.asyncio
    async def test_xml_missing_returns_404(
        self, client: AsyncClient, lid: str, snapshot
    ) -> None:
        res = await client.get(f"/lid/xml/{lid}")
        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.headers["content-type"] == "application/xml"

        assert res.text == snapshot

    @pytest.mark.parametrize("lid", ["dväljas..vb.1"])
    @pytest.mark.asyncio
    async def test_html_valid_lemma_returns_200(
        self, client: AsyncClient, lid: str, snapshot
    ) -> None:
        res = await client.get(f"/lid/html/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        assert res.text == snapshot

    @pytest.mark.parametrize("lid", ["xxxxx..xx.1"])
    @pytest.mark.asyncio
    async def test_html_missing_lemma_returns_404(
        self, client: AsyncClient, lid: str, snapshot
    ) -> None:
        res = await client.get(f"/lid/html/{lid}")
        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        assert res.text == snapshot

    @pytest.mark.parametrize("lid", ["dväljas..1"])
    @pytest.mark.asyncio
    async def test_html_valid_lexeme_returns_200(
        self, client: AsyncClient, lid: str, snapshot
    ) -> None:
        res = await client.get(f"/lid/html/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        assert res.text == snapshot

    @pytest.mark.parametrize("lid", ["xxxxx..1"])
    @pytest.mark.asyncio
    async def test_html_missing_lexeme_returns_404(
        self, client: AsyncClient, lid: str, snapshot
    ) -> None:
        res = await client.get(f"/lid/html/{lid}")
        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        assert res.text == snapshot

    @pytest.mark.parametrize("lid", ["dväljas..vb.1", "bad-input"])
    @pytest.mark.asyncio
    async def test_protojs_non_lexeme_input_returns_422(
        self, client: AsyncClient, lid: str
    ) -> None:
        res = await client.get(f"/lid/protojs/{lid}")
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("lid", ["bo..1"])
    @pytest.mark.asyncio
    async def test_protojs_valid_input_returns_200(
        self, client: AsyncClient, lid: str, snapshot
    ) -> None:
        res = await client.get(f"/lid/protojs/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/javascript; charset=utf-8"
        assert res.text == snapshot

    @pytest.mark.parametrize("lid", ["dväljas..vb.1", "bad-input"])
    @pytest.mark.asyncio
    async def test_graph_non_lexeme_input_returns_422(
        self, client: AsyncClient, lid: str
    ) -> None:
        res = await client.get(f"/lid/graph/{lid}")
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("lid", ["bo..1"])
    @pytest.mark.asyncio
    async def test_graph_valid_input_returns_200(
        self, client: AsyncClient, lid: str, snapshot
    ) -> None:
        res = await client.get(f"/lid/graph/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        assert res.text == snapshot
