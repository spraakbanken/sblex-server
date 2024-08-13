from pydantic import BaseModel
from sblex.sblex_server.schemas import Lexeme


class LidLemma(BaseModel):
    gf: str
    l: list[Lexeme]  # noqa: E741
    lex: Lexeme
    p: str
