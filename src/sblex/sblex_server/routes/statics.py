from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/static{path:path}", response_class=FileResponse, name="static")
async def staticfiles_workaround(path: str):
    return f"static{path}"
