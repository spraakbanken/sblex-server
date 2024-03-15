import abc
from typing import TypedDict


class InflectionTableRow(TypedDict):
    form: str
    gf: str
    pos: str
    inhs: list[str]
    msd: str
    p: str


class InflectionTableQuery(abc.ABC):
    @abc.abstractmethod
    def query(self, paradigm: str, word: str) -> list[InflectionTableRow]: ...
