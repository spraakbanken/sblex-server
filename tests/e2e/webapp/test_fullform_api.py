from typing import Union

import pytest
from fastapi import status
from httpx import AsyncClient


class TestFullformRoutes:
    @pytest.mark.parametrize(
        "fragment, expected",
        [
            (
                "dväljs",
                {
                    "a": [
                        {
                            "gf": "dväljas",
                            "id": "dväljas..vb.1",
                            "pos": "vb",
                            "is": [],
                            "msd": "pres ind s-form",
                            "p": "vb_vs_dväljas",
                        },
                        {
                            "gf": "dväljas",
                            "id": "dväljas..vb.1",
                            "pos": "vb",
                            "is": [],
                            "msd": "imper",
                            "p": "vb_vs_dväljas",
                        },
                    ],
                    "c": "",
                },
            ),
            ("dv", {"a": [], "c": "äa"}),
            ("dvä", {"a": [], "c": "l"}),
            ("dväl", {"a": [], "c": "jt"}),
        ],
    )
    @pytest.mark.asyncio
    async def test_json_valid_input_returns_200(
        self, client: AsyncClient, fragment: str, expected: dict
    ):
        res = await client.get(f"/ff/json/{fragment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/json"

        result = res.json()
        print(f"{result=}")
        assert result == expected

    @pytest.mark.parametrize(
        "fragment, expected",
        [
            (
                "dväljs",
                {
                    "a": [
                        {
                            "gf": "dväljas",
                            "id": "dväljas..vb.1",
                            "pos": "vb",
                            "is": [],
                            "msd": "pres ind s-form",
                            "p": "vb_vs_dväljas",
                        },
                        {
                            "gf": "dväljas",
                            "id": "dväljas..vb.1",
                            "pos": "vb",
                            "is": [],
                            "msd": "imper",
                            "p": "vb_vs_dväljas",
                        },
                    ],
                    "c": "",
                },
            ),
            ("dv", {"a": [], "c": "äa"}),
            ("dvä", {"a": [], "c": "l"}),
            ("dväl", {"a": [], "c": "jt"}),
        ],
    )
    @pytest.mark.asyncio
    async def test_html_valid_input_returns_200(
        self, client: AsyncClient, fragment: str, expected: dict
    ):
        res = await client.get(f"/ff/html/{fragment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"

        result = res.text
        print(f"{result=}")
        assert f"<title>{fragment}</title>" in result
        assert f"<p>segment: {fragment}</p>" in result
        # assert result == expected

    @pytest.mark.parametrize(
        "fragment, expected",
        [
            (
                "dväljs",
                [
                    "<gf>dväljas</gf>",
                    "<msd>imper</msd>",
                ],
            ),
            ("dv", "<c>äa</c>"),
            ("dvä", "<c>l</c>"),
            ("dväl", "<c>jt</c>"),
        ],
    )
    @pytest.mark.asyncio
    async def test_xml_valid_input_returns_200(
        self, client: AsyncClient, fragment: str, expected: Union[str, list]
    ):
        res = await client.get(f"/ff/xml/{fragment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/xml"

        result = res.text
        print(f"{result=}")
        if isinstance(expected, list):
            for expectation in expected:
                assert expectation in result
        else:
            assert expected in result
