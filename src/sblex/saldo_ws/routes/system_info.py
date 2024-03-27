import sys

from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from opentelemetry import trace
from sblex.saldo_ws import schemas

router = APIRouter()


__version__ = "0.2.3"
__date__ = "2023-05-10"


@router.get("/version", response_model=schemas.Version, name="system_info:version")
async def get_version():
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        return {"version": __version__, "date": __date__}


@router.get("/version/json")
async def get_version_old(request: Request):
    redirect_url = request.url_for("system_info:version")
    return RedirectResponse(redirect_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
