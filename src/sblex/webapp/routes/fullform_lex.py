from fastapi import APIRouter


router = APIRouter()


@router.get("/json/{segment}")
async def fullform_lex_json(
    segment: str,
):
    return []
