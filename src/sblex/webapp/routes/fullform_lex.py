from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from sblex.application.queries import FullformLexQuery
from sblex.webapp import deps
from sblex.webapp.responses import XMLResponse

router = APIRouter()


@router.get("/json/{segment}")
async def fullform_lex_json(
    segment: str,
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    return fullform_lex_query.query(segment=segment)


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

    return templates.TemplateResponse(
        "fullform_lex.xml",
        context={"request": request, "j": fullform_lex_query.query(segment=segment)},
        media_type="application/xml",
    )


@router.get(
    "/html/",
    response_class=HTMLResponse,
)
async def fullform_lex_html_empty(
    request: Request,
):
    templates = request.app.state.templates

    return templates.TemplateResponse(
        "saldo_mata_in_ordform.html",
        {
            "request": request,
            "title": "SALDO",
            "service": "fl",
            "bar": True,
        },
    )


@router.get(
    "/html/{segment}",
    response_class=HTMLResponse,
)
async def fullform_lex_html(
    request: Request,
    segment: str,
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    templates = request.app.state.templates

    segment = segment.strip()

    if not segment:
        return templates.TemplateResponse(
            "saldo_mata_in_ordform.html",
            {
                "request": request,
                "title": "SALDO",
                "service": "fl",
                "bar": True,
            },
        )
