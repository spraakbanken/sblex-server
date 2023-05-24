from fastapi import APIRouter, Depends, Response
from sblex.fm.morphology import Morphology
from sblex.fm_server import deps

router = APIRouter()


@router.get("/morph/{fragment}/{n}")
async def get_morph(
    fragment: str,
    n: int = 0,
    morphology: Morphology = Depends(deps.get_morphology),  # noqa: B008
):
    json_data = await morphology.lookup(fragment, n)
    return Response(json_data, media_type="application/json")
