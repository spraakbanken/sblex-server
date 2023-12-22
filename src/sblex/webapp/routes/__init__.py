from fastapi import APIRouter
from sblex.webapp.routes import compounds, fullform, fullform_lex, lids

router = APIRouter()


router.include_router(fullform.router, prefix="/ff", tags=["fullform"])
router.include_router(fullform_lex.router, prefix="/fl", tags=["fullform_lex"])
router.include_router(lids.router, prefix="/lid", tags=["lid", "lemma-id"])
router.include_router(
    compounds.router, prefix="/sms", tags=["sms", "sammansättning", "compound"]
)
