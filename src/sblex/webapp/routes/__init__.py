from fastapi import APIRouter


from sblex.webapp.routes import fullform_lex


router = APIRouter()


router.include_router(fullform_lex.router, prefix="/fl", tags=["fullform_lex"])
