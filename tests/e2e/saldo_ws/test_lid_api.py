import xml.etree.ElementTree as ET

import pytest
from fastapi import status
from httpx import AsyncClient

EXPECTED_XML_RESPONSES = {
    "empty": '<?xml version="1.0" encoding="UTF-8"?>\n<result>\n\n</result>',
    "dväljas..vb.1": """<result>
<gf>dväljas</gf>
    <p>vb_vs_dväljas</p>
    <ls>
    <l>dväljas..1</l>
    </ls>

</result>
""",
    "dväljas..1": """<result>
<lex>dväljas..1</lex>
    <fm>bo..1</fm>
    <fp>PRIM..1</fp>
    <mfs></mfs>
    <pfs></pfs>
    <ls>
    <l>dväljas..vb.1</l>
    </ls>
</result>
""",
}

EXPECTED_PROTOJS_RESPONSES = {
    "bo..1": """var flare = {
 'dväljas..1': 'http://testserver/lid/graph/dväljas..1', 
}"""
}


class TestLidRoutes:
    @pytest.mark.parametrize(
        "in_format",
        [
            "json",
            "xml",
            "html",
        ],
    )
    @pytest.mark.asyncio
    async def test_invalid_input_returns_422(self, client: AsyncClient, in_format: str) -> None:
        res = await client.get(f"/lid/{in_format}/bad-input")
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        "lid, expected_response",
        [
            (
                "dväljas..vb.1",
                {"gf": "dväljas", "l": ["dväljas..1"], "p": "vb_vs_dväljas"},
            ),
            (
                "dväljas..1",
                {
                    "fm": "bo..1",
                    "fp": "PRIM..1",
                    "l": ["dväljas..vb.1"],
                    "lex": "dväljas..1",
                    "mf": [],
                    "path": ["bo..1"],
                    "pf": [],
                    "ppath": [],
                },
            ),
            # ("d..nn.1", {}),
        ],
    )
    @pytest.mark.asyncio
    async def test_json_valid_input_returns_200(
        self,
        client: AsyncClient,
        lid: str,
        expected_response: list,
    ) -> None:
        res = await client.get(f"/lid/json/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/json"

        assert res.json() == expected_response

    @pytest.mark.parametrize(
        "lid, expected_response_name",
        [
            (
                "xxxxx..xx.1",
                "empty",
            ),
            ("dväljas..vb.1", "dväljas..vb.1"),
            (
                "xxxxx..1",
                "empty",
            ),
            (
                "dväljas..1",
                "dväljas..1",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_xml_valid_input_returns_200(
        self,
        client: AsyncClient,
        lid: str,
        expected_response_name: str,
    ) -> None:
        res = await client.get(f"/lid/xml/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/xml"

        expected_xml = ET.canonicalize(EXPECTED_XML_RESPONSES[expected_response_name])

        response_xml = ET.canonicalize(res.text)
        assert response_xml == expected_xml

    @pytest.mark.parametrize(
        "lid, expected_in_response",
        [
            # ("dväljs..vb.1", ["<h1>dväljas</h1>"]),
            ("xxxxx..xx.1", ["<b>xxxxx..xx.1 finns ej.</b>"]),
        ],
    )
    @pytest.mark.asyncio
    async def test_html_valid_lemma_returns_200(
        self,
        client: AsyncClient,
        lid: str,
        expected_in_response: list[str],
    ) -> None:
        res = await client.get(f"/lid/html/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        print(f"{res.text=}")
        for expect_in_response in expected_in_response:
            assert expect_in_response in res.text

    @pytest.mark.parametrize(
        "lid, expected_in_response",
        [
            ("dväljas..1", ["<h1>dväljas</h1>", '<td><a href="', "lid/html/bo..1"]),
            ("xxxxx..1", ["<center>xxxxx..1 finns ej.</center>"]),
        ],
    )
    @pytest.mark.asyncio
    async def test_html_valid_lexeme_returns_200(
        self,
        client: AsyncClient,
        lid: str,
        expected_in_response: list[str],
    ) -> None:
        res = await client.get(f"/lid/html/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        print(f"{res.text=}")
        for expect_in_response in expected_in_response:
            assert expect_in_response in res.text

    @pytest.mark.parametrize(
        "lid",
        [
            "dväljas..vb.1",
        ],
    )
    @pytest.mark.parametrize(
        "in_format, expected_content_type",
        [
            ("json", "application/json"),
            ("xml", "application/xml"),
            ("html", "text/html; charset=utf-8"),
        ],
    )
    @pytest.mark.asyncio
    async def test_valid_input_returns_200(
        self,
        client: AsyncClient,
        in_format: str,
        expected_content_type: str,
        lid: str,
    ) -> None:
        print(f"{lid=}")
        res = await client.get(f"/lid/{in_format}/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == expected_content_type

    @pytest.mark.parametrize(
        "lid",
        [
            "dväljas..vb.1",
            "bad-input",
        ],
    )
    @pytest.mark.asyncio
    async def test_protojs_non_lexeme_input_returns_422(
        self,
        client: AsyncClient,
        lid: str,
    ) -> None:
        print(f"{lid=}")
        res = await client.get(f"/lid/protojs/{lid}")
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        "lid, expected_response_name",
        [
            ("bo..1", None),
        ],
    )
    @pytest.mark.asyncio
    async def test_protojs_valid_input_returns_200(
        self,
        client: AsyncClient,
        expected_response_name: str | None,
        lid: str,
    ) -> None:
        print(f"{lid=}")
        res = await client.get(f"/lid/protojs/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/javascript; charset=utf-8"

        expected_response = EXPECTED_PROTOJS_RESPONSES[expected_response_name or lid]

        assert res.text == expected_response

    @pytest.mark.parametrize(
        "lid",
        [
            "dväljas..vb.1",
            "bad-input",
        ],
    )
    @pytest.mark.asyncio
    async def test_graph_non_lexeme_input_returns_422(
        self,
        client: AsyncClient,
        lid: str,
    ) -> None:
        res = await client.get(f"/lid/graph/{lid}")
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        "lid, expected_in_response",
        [
            (
                "bo..1",
                '<script type="text/javascript" src="http://testserver/lid/protojs/bo..1"></script>',
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_graph_valid_input_returns_200(
        self,
        client: AsyncClient,
        expected_in_response: str,
        lid: str,
    ) -> None:
        res = await client.get(f"/lid/graph/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"

        assert expected_in_response in res.text
