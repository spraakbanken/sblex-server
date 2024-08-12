from fastapi import APIRouter

from sblex.saldo_ws.routes import (
    compounds,
    fullform,
    fullform_lex,
    inflection,
    lids,
    paradigms,
)
from sblex.sblex_server.routes import system_info

router = APIRouter()


router.include_router(fullform.router, prefix="/ff", tags=["fullform"])
router.include_router(fullform_lex.router, prefix="/fl", tags=["fullform_lex"])
router.include_router(lids.router, prefix="/lid", tags=["lid", "lemma-id"])
router.include_router(
    compounds.router, prefix="/sms", tags=["sms", "sammansättning", "compound"]
)
router.include_router(inflection.router, prefix="/gen", tags=["inflection"])
router.include_router(paradigms.router, prefix="/para", tags=["paradigms"])
router.include_router(system_info.router, tags=["system-info"])
