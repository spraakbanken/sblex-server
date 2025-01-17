from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from sblex.fm.morphology import Morphology
from sblex.fm_server import deps, schemas

router = APIRouter()


@router.get("/morph/{fragment}", response_model=list[schemas.Morph])
async def get_morph(
    fragment: str,
    morphology: Morphology = Depends(deps.get_morphology),  # noqa: B008
):
    if json_data := await morphology.lookup(fragment):
        return Response(json_data, media_type="application/json")
    return JSONResponse(
        {"msg": f"fragment '{fragment}' not found"},
        status_code=status.HTTP_404_NOT_FOUND,
        media_type="application/json",
    )


@router.get("/morph-w-cont/{fragment}", response_model=schemas.MorphWithCont)
async def get_morph_w_cont(
    fragment: str,
    morphology: Morphology = Depends(deps.get_morphology),  # noqa: B008
):
    if json_data := await morphology.lookup_w_cont(fragment):
        return Response(json_data, media_type="application/json")
    return JSONResponse(
        {"msg": f"fragment '{fragment}' not found"},
        status_code=status.HTTP_404_NOT_FOUND,
        media_type="application/json",
    )
