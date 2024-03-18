# import xml.etree.ElementTree as ET

import pytest
from fastapi import status
from httpx import AsyncClient

# EXPECTED_XML_RESPONSES = {
#     "empty": '<?xml version="1.0" encoding="UTF-8"?>\n<result>\n\n</result>',
#     "dväljas..vb.1": """<result>
# <gf>dväljas</gf>
#     <p>vb_vs_dväljas</p>
#     <ls>
#     <l>dväljas..1</l>
#     </ls>

# </result>
# """,
#     "dväljas..1": """<result>
# <lex>dväljas..1</lex>
#     <fm>bo..1</fm>
#     <fp>PRIM..1</fp>
#     <mfs></mfs>
#     <pfs></pfs>
#     <ls>
#     <l>dväljas..vb.1</l>
#     </ls>
# </result>
# """,
# }


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

    #     @pytest.mark.parametrize(
    #         "lid, expected_response_name",
    #         [
    #             (
    #                 "xxxxx..xx.1",
    #                 "empty",
    #             ),
    #             ("dväljas..vb.1", "dväljas..vb.1"),
    #             (
    #                 "xxxxx..1",
    #                 "empty",
    #             ),
    #             (
    #                 "dväljas..1",
    #                 "dväljas..1",
    #             ),
    #         ],
    #     )
    #     @pytest.mark.asyncio
    #     async def test_xml_valid_input_returns_200(
    #         self,
    #         client: AsyncClient,
    #         lid: str,
    #         expected_response_name: str,
    #     ) -> None:
    #         res = await client.get(f"/gen/xml/{lid}")
    #         assert res.status_code == status.HTTP_200_OK
    #         assert res.headers["content-type"] == "application/xml"

    #         expected_xml = ET.canonicalize(EXPECTED_XML_RESPONSES[expected_response_name])

    #         response_xml = ET.canonicalize(res.text)
    #         assert response_xml == expected_xml

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
