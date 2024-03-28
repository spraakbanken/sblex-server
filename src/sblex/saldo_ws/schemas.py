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
    version: Annotated[str, StringConstraints(pattern=r"\d+\.\d+\.\d+(-\w+\d+)?")]
    date: Annotated[str, StringConstraints(pattern=r"\d{4}-\d{2}-\d{2}")]


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


class LidLemma(BaseModel):
    gf: str
    l: list[Lexeme]  # noqa: E741
    lex: Lexeme
    p: str


class Message(BaseModel):
    message: str
