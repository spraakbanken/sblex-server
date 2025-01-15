from pydantic import BaseModel, Field


class Morph(BaseModel):
    gf: str
    id: str
    pos: str
    is_: list[str] = Field(alias="is")
    msd: str
    p: str


class MorphWithCont(BaseModel):
    a: list[Morph]
    c: str
