from fastapi import APIRouter
from sblex.fm_server.api import morph

router = APIRouter()

router.include_router(morph.router, tags=["morphology"])
