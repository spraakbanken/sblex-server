from fastapi import APIRouter
from sblex.sblex_server.routes import system_info

router = APIRouter()
router.include_router(system_info.router, tags=["system-info"])
