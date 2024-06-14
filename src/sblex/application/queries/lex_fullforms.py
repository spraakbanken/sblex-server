import abc
from typing import TypedDict


class FullformLex(TypedDict):
    id: str
    fm: str
    fp: list[str]
    l: str  # noqa: E741
    gf: str
    p: str


class FullformLexQuery(abc.ABC):
    @abc.abstractmethod
    async def query(self, segment: str) -> list[FullformLex]: ...
