import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from sblex.application.queries import NoPartOfSpeechOnBaseform, Paradigms
from sblex.saldo_ws import deps

router = APIRouter()


@router.get("/json/{words}", response_model=list[str])
async def get_para_json(words: str, paradigms: Paradigms = Depends(deps.get_paradigms)):  # noqa: B008
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        try:
            _baseform, result = paradigms.query(words)
        except NoPartOfSpeechOnBaseform:
            return ORJSONResponse(
                {"msg": "First word has no Part-of-Speech tag. Use the form 'word:pos'"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return result
