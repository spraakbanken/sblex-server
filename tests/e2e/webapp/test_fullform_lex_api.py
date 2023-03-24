import pytest
from fastapi import status
from httpx import AsyncClient


class TestFullformLexRoutes:
    @pytest.mark.parametrize(
        "segment, expected_response",
        [
            ("t", []),
        ],
    )
    @pytest.mark.asyncio
    async def test_json_valid_input_returns_200(
        self,
        client: AsyncClient,
        segment: str,
        expected_response: list,
    ) -> None:
        res = await client.get(f"/fl/json/{segment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/json"

        assert res.json() == expected_response

    @pytest.mark.parametrize(
        "segment, expected_response",
        [
            ("t", '<?xml version="1.0" encoding="UTF-8"?>\n<result>\n\n</result>'),
        ],
    )
    @pytest.mark.asyncio
    async def test_xml_valid_input_returns_200(
        self,
        client: AsyncClient,
        segment: str,
        expected_response: str,
    ) -> None:
        res = await client.get(f"/fl/xml/{segment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/xml"

        assert res.text == expected_response
