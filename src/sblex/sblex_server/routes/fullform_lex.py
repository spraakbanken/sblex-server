import sys

from asgi_matomo.trackers import PerfMsTracker
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, ORJSONResponse, RedirectResponse
from opentelemetry import trace

from sblex.application.queries import FullformLexQuery
from sblex.sblex_server import deps, schemas, templating
from sblex.sblex_server.responses import XMLResponse

router = APIRouter()


@router.get(
    "/json/{segment}",
    response_model=list[schemas.FullformLex],
    responses={404: {"model": schemas.Message}},
)
async def fullform_lex_json(
    request: Request,
    segment: str,
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        with PerfMsTracker(scope=request.scope, key="pf_srv"):
            segment_fullform = await fullform_lex_query.query(segment=segment)
        if len(segment_fullform) == 0:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": f"'{segment}' saknas i lexikonet"},
            )
        return ORJSONResponse(segment_fullform)


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
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        templates = request.app.state.templates

        with PerfMsTracker(scope=request.scope, key="pf_srv"):
            json_data = await fullform_lex_query.query(segment=segment)
        return templates.TemplateResponse(
            request=request,
            name="fullform_lex.xml",
            context={"j": json_data},
            media_type="application/xml",
        )


@router.get("/html", response_class=HTMLResponse, name="fullform_lex:fl-html")
async def fullform_lex_html(
    request: Request,
    segment: str | None = None,
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        templates = request.app.state.templates
        segment = segment.strip() if segment else ""
        json_data = await fullform_lex_query.query(segment=segment) if segment else []
        title = (
            f"Fullform med semantisk koppling | {segment}"
            if segment
            else "Fullform med semantisk koppling"
        )
        if segment == "" or len(json_data) > 0:
            status_code = status.HTTP_200_OK
        else:
            status_code = status.HTTP_404_NOT_FOUND
        return templates.TemplateResponse(
            request=request,
            name="saldo_fullform_lex.html",
            status_code=status_code,
            context=templating.build_context(
                request=request,
                title=title,
                input=segment,
                segment=segment,
                j=json_data,
            ),
        )


@router.get(
    "/html/{segment}",
    response_class=HTMLResponse,
)
async def fullform_lex_html_orig(
    request: Request,
    segment: str,
):
    redirect_url = request.url_for("fullform_lex:fl-html").include_query_params(segment=segment)
    return RedirectResponse(redirect_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
