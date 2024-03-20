from typing import Annotated

from pydantic import BaseModel, StringConstraints

Lexeme = Annotated[str, StringConstraints(pattern=r".*\.\.\d+")]
Lemma = Annotated[str, StringConstraints(pattern=r".*\.\.\w+\.\d+")]


class FullformLex(BaseModel):
    id: Lexeme
    fm: Lexeme
    fp: Lexeme
    l: Lemma  # noqa: E741
    gf: str
    p: str


class InflectionRow(BaseModel):
    form: str
    head: str
    pos: str
    inhs: list[str]
    msd: str
    p: str


class Version(BaseModel):
    version: Annotated[str, StringConstraints(pattern=r"\d+\.\d+\.\d+")]
