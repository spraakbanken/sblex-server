from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/saldo.css", response_class=FileResponse)
async def saldo_css(request: Request):
    return "static/saldo.css"
