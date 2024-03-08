import logging
from typing import Any

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from sblex.saldo_ws.responses import XMLResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/json/{segment}", response_model=None, name="compounds:sms-json")
async def lookup_lid_json(
    request: Request,
    segment: str,
) -> Response | None | dict[str, Any]:
    raise NotImplementedError("compounds:sms-json")


@router.get("/xml/{segment}", response_class=XMLResponse, name="compounds:sms-xml")
async def lookup_lid_xml(
    request: Request,
    segment: str,
):
    raise NotImplementedError("compounds:sms-xml")


@router.get("/html/{segment}", response_class=HTMLResponse, name="compounds:sms-html")
async def lookup_lid_html(
    request: Request,
    segment: str,  # Union[Lexeme, Lemma],
):
    raise NotImplementedError("compounds:sms-html")


@router.get("/graph/{segment}", response_class=HTMLResponse, name="compounds:sms-graph")
async def lookup_lid_graph(
    request: Request,
    segment: str,
):
    raise NotImplementedError("compounds:sms-graph")
