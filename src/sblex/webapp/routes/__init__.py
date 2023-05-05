from fastapi import APIRouter
from sblex.webapp.routes import fullform, fullform_lex, lids

router = APIRouter()


# router.include_router(fullform.router, prefix="/ff", tags=["fullform"])
# router.include_router(fullform_lex.router, prefix="/fl", tags=["fullform_lex"])
router.include_router(lids.router, prefix="/lid", tags=["lid", "lemma-id"])
