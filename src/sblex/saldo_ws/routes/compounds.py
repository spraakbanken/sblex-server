import logging
import sys
from typing import Any

from asgi_matomo.trackers import PerfMsTracker
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from opentelemetry import trace
from sblex.application.services.lookup import LookupService
from sblex.saldo_ws import deps
from sblex.saldo_ws.responses import XMLResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/json/{segment}", response_model=None, name="compounds:sms-json")
async def lookup_lid_json(
    request: Request,
    segment: str,
    lookup_service: LookupService = Depends(deps.get_lookup_service),  # noqa: B008
) -> Response | None | dict[str, Any]:
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        with PerfMsTracker(scope=request.scope, key="pf_srv"):
            segment_compounds = await lookup_service.compound(segment)
        return segment_compounds


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
