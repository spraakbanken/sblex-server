import xml.etree.ElementTree as ET

import pytest
from fastapi import status
from httpx import AsyncClient

EXPECTED_XML_RESPONSES = {
    "empty": '<?xml version="1.0" encoding="UTF-8"?>\n<result></result>',
    ("vb_vs_dväljas", "dväljas"): """<result><table><w>
            <form>dväljes</form>
            <gf>dväljas</gf>
            <pos>vb</pos>
            <inhs></inhs>
            <msd>pres ind s-form</msd>
            <p>vb_vs_dväljas</p>
        </w><w>
            <form>dväljs</form>
            <gf>dväljas</gf>
            <pos>vb</pos>
            <inhs></inhs>
            <msd>pres ind s-form</msd>
            <p>vb_vs_dväljas</p>
        </w><w>
            <form>dvaldes</form>
            <gf>dväljas</gf>
            <pos>vb</pos>
            <inhs></inhs>
            <msd>pret ind s-form</msd>
            <p>vb_vs_dväljas</p>
        </w><w>
            <form>dväljdes</form>
            <gf>dväljas</gf>
            <pos>vb</pos>
            <inhs></inhs>
            <msd>pret ind s-form</msd>
            <p>vb_vs_dväljas</p>
        </w><w>
            <form>dväljes</form>
            <gf>dväljas</gf>
            <pos>vb</pos>
            <inhs></inhs>
            <msd>imper</msd>
            <p>vb_vs_dväljas</p>
        </w><w>
            <form>dväljs</form>
            <gf>dväljas</gf>
            <pos>vb</pos>
            <inhs></inhs>
            <msd>imper</msd>
            <p>vb_vs_dväljas</p>
        </w><w>
            <form>dväljas</form>
            <gf>dväljas</gf>
            <pos>vb</pos>
            <inhs></inhs>
            <msd>inf s-form</msd>
            <p>vb_vs_dväljas</p>
        </w><w>
            <form>dvalts</form>
            <gf>dväljas</gf>
            <pos>vb</pos>
            <inhs></inhs>
            <msd>sup s-form</msd>
            <p>vb_vs_dväljas</p>
        </w><w>
            <form>dvälts</form>
            <gf>dväljas</gf>
            <pos>vb</pos>
            <inhs></inhs>
            <msd>sup s-form</msd>
            <p>vb_vs_dväljas</p>
        </w></table></result>
    """,
}


class TestGenRoutes:
    @pytest.mark.parametrize(
        "paradigm, word, expected_response",
        [
            (
                "vb_vs_dväljas",
                "dväljas",
                [
                    {
                        "form": "dväljes",
                        "gf": "dväljas",
                        "pos": "vb",
                        "inhs": [],
                        "msd": "pres ind s-form",
                        "p": "vb_vs_dväljas",
                    },
                    {
                        "form": "dväljs",
                        "gf": "dväljas",
                        "pos": "vb",
                        "inhs": [],
                        "msd": "pres ind s-form",
                        "p": "vb_vs_dväljas",
                    },
                    {
                        "form": "dvaldes",
                        "gf": "dväljas",
                        "pos": "vb",
                        "inhs": [],
                        "msd": "pret ind s-form",
                        "p": "vb_vs_dväljas",
                    },
                    {
                        "form": "dväljdes",
                        "gf": "dväljas",
                        "pos": "vb",
                        "inhs": [],
                        "msd": "pret ind s-form",
                        "p": "vb_vs_dväljas",
                    },
                    {
                        "form": "dväljes",
                        "gf": "dväljas",
                        "pos": "vb",
                        "inhs": [],
                        "msd": "imper",
                        "p": "vb_vs_dväljas",
                    },
                    {
                        "form": "dväljs",
                        "gf": "dväljas",
                        "pos": "vb",
                        "inhs": [],
                        "msd": "imper",
                        "p": "vb_vs_dväljas",
                    },
                    {
                        "form": "dväljas",
                        "gf": "dväljas",
                        "pos": "vb",
                        "inhs": [],
                        "msd": "inf s-form",
                        "p": "vb_vs_dväljas",
                    },
                    {
                        "form": "dvalts",
                        "gf": "dväljas",
                        "pos": "vb",
                        "inhs": [],
                        "msd": "sup s-form",
                        "p": "vb_vs_dväljas",
                    },
                    {
                        "form": "dvälts",
                        "gf": "dväljas",
                        "pos": "vb",
                        "inhs": [],
                        "msd": "sup s-form",
                        "p": "vb_vs_dväljas",
                    },
                ],
            ),
            #             ("d..nn.1", {}),
        ],
    )
    @pytest.mark.asyncio
    async def test_json_valid_input_returns_200(
        self,
        client: AsyncClient,
        paradigm: str,
        word: str,
        expected_response: list,
    ) -> None:
        res = await client.get(f"/gen/json/{paradigm}/{word}")

        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/json"
        assert res.json() == expected_response

    @pytest.mark.parametrize(
        "paradigm, word, expected_response_name",
        [
            (
                "xx_xx_xxx",
                "xxx",
                "empty",
            ),
            ("vb_vs_dväljas", "dväljas", None),
        ],
    )
    @pytest.mark.asyncio
    async def test_xml_valid_input_returns_200(
        self,
        client: AsyncClient,
        paradigm: str,
        word: str,
        expected_response_name: str,
    ) -> None:
        res = await client.get(f"/gen/xml/{paradigm}/{word}")

        assert res.status_code == status.HTTP_200_OK

        assert res.headers["content-type"] == "application/xml"

        if expected_response_name is None:
            expected_response_name = (paradigm, word)
        expected_xml = ET.canonicalize(EXPECTED_XML_RESPONSES[expected_response_name])

        response_xml = ET.canonicalize(res.text)
        assert response_xml == expected_xml

    @pytest.mark.parametrize(
        "paradigm, word, expected_in_response",
        [
            ("vb_vs_dväljas", "dväljas", ["<td>vb_vs_dväljas</td>", "<td>dväljas</td>"]),
            ("xx_xx_xxx", "xxx", ["<p>paradigm ", " finns ej.</p>"]),
        ],
    )
    @pytest.mark.asyncio
    async def test_html_valid_lemma_returns_200(
        self,
        client: AsyncClient,
        paradigm: str,
        word: str,
        expected_in_response: list[str],
    ) -> None:
        res = await client.get(f"/gen/html/{paradigm}/{word}")

        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"
        print(f"{res.text=}")
        for expect_in_response in expected_in_response:
            assert expect_in_response in res.text
