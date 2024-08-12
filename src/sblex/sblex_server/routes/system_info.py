import sys

from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from opentelemetry import trace

from sblex.sblex_server.schemas import version
from sblex.sblex_server.shared import version_info

router = APIRouter()


@router.get("/version", response_model=version.Version, name="system_info:version")
async def get_version():
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        return {"version": version_info.get_version(), "date": version_info.get_build_date()}


@router.get("/version/json")
async def get_version_old(request: Request):
    redirect_url = request.url_for("system_info:version")
    return RedirectResponse(redirect_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
