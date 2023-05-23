import time

from starlette.types import Scope

from asgi_matomo.trackers import PerfMsTracker
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from json_streams import jsonlib
from opentelemetry import trace
from sblex.fm import Morphology
from sblex.webapp import deps, templating
from sblex.webapp.responses import XMLResponse

router = APIRouter()

tracer = trace.get_tracer(__name__)


class PerfTracker:
    def __init__(self, state, key: str) -> None:
        self.start_ns = 0.0
        self.state = state
        try:
            _ = self.state.asgi_matomo
        except AttributeError:
            self.state.asgi_matomo = {}
        self.key = key

    def __enter__(self):
        self.start_ns = time.perf_counter_ns()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.end_ns = time.perf_counter_ns()
        self.state.asgi_matomo[self.key] = (self.end_ns - self.start_ns) / 1000


@router.get("/json/{fragment}")
async def fullform_json(
    request: Request,
    fragment: str,
    morphology: Morphology = Depends(deps.get_morphology),  # noqa: B008
):
    with PerfMsTracker(scope=request.scope, key="pf_srv"):
        json_data = morphology.lookup(fragment)
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
    templates = request.app.state.templates

    with PerfMsTracker(scope=request.scope, key="pf_srv"):
        json_data = morphology.lookup(fragment)

    return templates.TemplateResponse(
        "saldo_fullform.xml",
        context={
            "request": request,
            "j": json_data,
        },
        media_type="application/xml",
    )


@router.get(
    "/html/{fragment}",
    response_class=HTMLResponse,
)
async def fullform_html(
    request: Request,
    fragment: str,
    morphology: Morphology = Depends(deps.get_morphology),  # noqa: B008
):
    current_span = trace.get_current_span()
    current_span.set_attribute("scope", str(request.scope))

    templates = request.app.state.templates

    return templates.TemplateResponse(
        "saldo_fullform.html",
        context=templating.build_context(
            request,
            title=fragment,
            service="ff",
            input="",
            show_bar=True,
            segment=fragment,
            j=jsonlib.loads(morphology.lookup(fragment))
            # "content": htmlize(fragment, morphology.lookup(f"0 {fragment}".encode("utf-8")))
        ),
    )
