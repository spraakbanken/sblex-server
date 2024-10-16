import logging
import sys
from typing import Any

from asgi_matomo.trackers import PerfMsTracker  # noqa: F401
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import HTMLResponse, ORJSONResponse
from opentelemetry import trace

from sblex.application.services.lookup import LookupService
from sblex.saldo_ws import deps, templating
from sblex.saldo_ws.responses import XMLResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/json/{segment}", response_model=None, name="compounds:sms-json")
async def get_compound_json(
    request: Request,
    segment: str,
    lookup_service: LookupService = Depends(deps.get_lookup_service),  # noqa: B008
) -> Response | None | dict[str, Any]:
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        #  with PerfMsTracker(scope=request.scope, key="pf_srv"):
        #      segment_compounds = await lookup_service.compound(segment)
        # return segment_compounds
        return ORJSONResponse(
            content={
                "message": """This route is disabled due to performance reasons. 
                     Contact us if interessed in it working.
                     Tracking issue: https://github.com/spraakbanken/sblex-server/issues/110""",
            },
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@router.get("/xml/{segment}", response_class=XMLResponse, name="compounds:sms-xml")
async def get_compound_xml(
    request: Request,
    segment: str,
    lookup_service: LookupService = Depends(deps.get_lookup_service),  # noqa: B008
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        # with PerfMsTracker(scope=request.scope, key="pf_srv"):
        #     segment_compounds = await lookup_service.compound(segment)
        templates = request.app.state.templates
        return templates.TemplateResponse(
            request=request,
            name="saldo_temp_disable.xml",
            #     name="saldo_compound.xml",
            context={
                "segment": segment,
                # "j": segment_compounds,
                "reason_eng": "Disabled due to performance issues.",
                "issue_no": "110",
            },
            media_type="application/xml",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@router.get("/html/{segment}", response_class=HTMLResponse, name="compounds:sms-html")
async def get_compound_html(
    request: Request,
    segment: str,  # Union[Lexeme, Lemma],
    lookup_service: LookupService = Depends(deps.get_lookup_service),  # noqa: B008
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        # with PerfMsTracker(scope=request.scope, key="pf_srv"):
        #     segment_compounds = await lookup_service.compound(segment)
        templates = request.app.state.templates
        return templates.TemplateResponse(
            request=request,
            # name="saldo_compound.html",
            name="saldo_temp_disable.html",
            context=templating.build_context(
                request,
                title=f"Sammansättningsanalys för '{segment}' [Avstängd]",
                segment=segment,
                # j=segment_compounds,
                reason_swe="Tjänsten är stängd på grund av prestandaproblem.",
                reason_eng="Disabled due to performance issues.",
                issue_no="110",
            ),
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
