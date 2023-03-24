from fastapi import APIRouter, Depends

from sblex.application.queries import FullformLexQuery
from sblex.webapp import deps

router = APIRouter()


@router.get("/json/{segment}")
async def fullform_lex_json(
    segment: str,
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    return fullform_lex_query.query(segment=segment)
