from fastapi import APIRouter
from sblex.sblex_server.routes import fullform_lex, system_info

router = APIRouter()

router.include_router(fullform_lex.router, prefix="/fl", tags=["fullform_lex"])
router.include_router(system_info.router, tags=["system-info"])
