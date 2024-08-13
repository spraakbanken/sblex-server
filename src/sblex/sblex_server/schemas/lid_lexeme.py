from pydantic import BaseModel
from sblex.sblex_server.schemas import Lemma, Lexeme


class LidLexeme(BaseModel):
    fm: Lexeme
    fp: Lexeme
    l: list[Lemma]  # noqa: E741
    lex: Lexeme
    mf: list[str]
    path: list[Lexeme]
    pf: list[str]
    ppath: list[str]
    fs: list[str] | None = None
