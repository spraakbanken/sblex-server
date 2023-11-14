from asgi_matomo.trackers import PerfMsTracker
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from json_streams import jsonlib
from opentelemetry import trace
from sblex.fm import Morphology
from sblex.webapp import deps, templating
from sblex.webapp.responses import XMLResponse

router = APIRouter()

tracer = trace.get_tracer(__name__)


@router.get("/json/{fragment}")
async def fullform_json(
    request: Request,
    fragment: str,
    morphology: Morphology = Depends(deps.get_morphology),  # noqa: B008
):
    with PerfMsTracker(scope=request.scope, key="pf_srv"):
        json_data = await morphology.lookup(fragment)
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
        json_data = jsonlib.loads(await morphology.lookup(fragment))

    return templates.TemplateResponse(
        "saldo_fullform.xml",
        context={
            "request": request,
            "j": json_data,
        },
        media_type="application/xml",
    )


@router.get("/html", response_class=HTMLResponse, name="fullform:ff-html")
async def fullform_html(
    request: Request,
    q: str | None = None,
    morphology: Morphology = Depends(deps.get_morphology),  # noqa: B008
):
    current_span = trace.get_current_span()
    current_span.set_attribute("scope", str(request.scope))

    templates = request.app.state.templates
    fragment = q.strip() if q else ""
    json_data = {}
    if fragment:
        json_data = jsonlib.loads(await morphology.lookup(fragment))
    return templates.TemplateResponse(
        "saldo_fullform.html",
        context=templating.build_context(
            request,
            title=fragment,
            service="ff",
            input=fragment,
            show_bar=True,
            segment=fragment,
            j=json_data,
            # "content": htmlize(fragment, morphology.lookup(f"0 {fragment}".encode("utf-8")))
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
    redirect_url = request.url_for("fullform:ff-html").include_query_params(q=fragment)
    return RedirectResponse(redirect_url)
