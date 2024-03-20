from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from sblex.saldo_ws import schemas

router = APIRouter()


@router.get("/version", response_model=schemas.Version, name="system_info:version")
async def get_version():
    return {"version": "0.2.2"}


@router.get("/version/json")
async def get_version_old(request: Request):
    redirect_url = request.url_for("system_info:version")
    return RedirectResponse(redirect_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
