import sys

from asgi_matomo.trackers import PerfMsTracker
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from json_arrays import jsonlib
from opentelemetry import trace

from sblex.fm import Morphology
from sblex.saldo_ws import deps, templating
from sblex.saldo_ws.responses import XMLResponse

router = APIRouter()

tracer = trace.get_tracer(__name__)


@router.get("/json/{fragment}")
async def fullform_json(
    request: Request,
    fragment: str,
    morphology: Morphology = Depends(deps.get_morphology),  # noqa: B008
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        with PerfMsTracker(scope=request.scope, key="pf_srv"):
            json_data = await morphology.lookup_w_cont(fragment)
        return Response(json_data, media_type="application/json")


@router.get(
    "/xml/{fragment}",
    response_class=XMLResponse,
)
async def fullform_xml(
    request: Request,
    fragment: str,
    morphology: Morphology = Depends(deps.get_morphology),  # noqa: B008
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        templates = request.app.state.templates

        with PerfMsTracker(scope=request.scope, key="pf_srv"):
            json_data = jsonlib.loads(await morphology.lookup(fragment))

        return templates.TemplateResponse(
            request=request,
            name="saldo_fullform.xml",
            context={
                "j": json_data,
            },
            media_type="application/xml",
        )


@router.get("/html", response_class=HTMLResponse, name="fullform:ff-html")
async def fullform_html(
    request: Request,
    fragment: str | None = None,
    morphology: Morphology = Depends(deps.get_morphology),  # noqa: B008
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        templates = request.app.state.templates
        fragment = fragment.strip() if fragment else ""
        json_data = {}
        if fragment:
            json_data = jsonlib.loads(await morphology.lookup(fragment))
        title = f"Fullform | {fragment}" if fragment else "Fullform"
        return templates.TemplateResponse(
            request=request,
            name="saldo_fullform.html",
            context=templating.build_context(
                request=request,
                title=title,
                input=fragment,
                segment=fragment,
                j=json_data,
            ),
        )


@router.get(
    "/html/{fragment}",
    response_class=HTMLResponse,
)
async def fullform_html_orig(
    request: Request,
    fragment: str,
):
    redirect_url = request.url_for("fullform:ff-html").include_query_params(fragment=fragment)
    return RedirectResponse(redirect_url)
