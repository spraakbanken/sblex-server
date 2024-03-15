import sys

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from sblex.application.queries.inflection import InflectionTableQuery
from sblex.saldo_ws import deps, schemas

router = APIRouter()


@router.get(
    "/json/{paradigm}/{word}",
    response_model=list[schemas.InflectionRow],
    response_class=ORJSONResponse,
    name="inflections:gen-json",
)
async def inflection_table_json(
    paradigm: str,
    word: str,
    inflection_table_query: InflectionTableQuery = Depends(deps.get_inflection_table_query),  # noqa: B008
) -> ORJSONResponse:
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        return ORJSONResponse(inflection_table_query.query(paradigm, word))
