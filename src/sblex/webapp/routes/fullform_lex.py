from asgi_matomo.trackers import PerfMsTracker
from fastapi import APIRouter, Depends, Request, status
from fastapi.datastructures import URL
from fastapi.responses import HTMLResponse, RedirectResponse
from sblex.application.queries import FullformLexQuery
from sblex.webapp import deps, templating
from sblex.webapp.responses import XMLResponse

router = APIRouter()


@router.get("/json/{segment}")
async def fullform_lex_json(
    request: Request,
    segment: str,
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    with PerfMsTracker(scope=request.scope, key="pf_srv"):
        segment_fullform = await fullform_lex_query.query(segment=segment)
    return segment_fullform


@router.get(
    "/xml/{segment}",
    response_class=XMLResponse,
)
async def fullform_xml(
    request: Request,
    segment: str,
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    templates = request.app.state.templates

    with PerfMsTracker(scope=request.scope, key="pf_srv"):
        json_data = await fullform_lex_query.query(segment=segment)
    return templates.TemplateResponse(
        "fullform_lex.xml",
        context={"request": request, "j": json_data},
        media_type="application/xml",
    )


@router.get("/html", response_class=HTMLResponse, name="fullform_lex:fl-html")
async def fullform_lex_html(
    request: Request,
    q: str | None = None,
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    templates = request.app.state.templates
    segment = q.strip() if q else ""
    json_data = {}
    if segment:
        json_data = await fullform_lex_query.query(segment=segment)

    return templates.TemplateResponse(
        "saldo_fullform_lex.html",
        context=templating.build_context(
            request,
            title="SALDO",
            show_bar=True,
            service="fl",
            input=segment,
            segment=segment,
            j=json_data,
        ),
    )


@router.get(
    "/html/{segment}",
    response_class=HTMLResponse,
)
async def fullform_lex_html_old(
    request: Request,
    segment: str,
):
    redirect_url = request.url_for("fullform_lex:fl-html").include_query_params(
        q=segment
    )
    return RedirectResponse(
        redirect_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
