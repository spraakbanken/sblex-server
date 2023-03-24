from fastapi import APIRouter, Depends, Request

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
