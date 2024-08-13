from pydantic import BaseModel
from sblex.sblex_server.schemas.base import Lemma, Lexeme


class FullformLex(BaseModel):
    id: Lexeme
    fm: Lexeme
    fp: Lexeme
    l: Lemma  # noqa: E741
    gf: str
    p: str
