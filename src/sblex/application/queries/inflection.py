import abc
from typing import Iterable, TypedDict


class InflectionTableRow(TypedDict):
    form: str
    gf: str
    pos: str
    inhs: list[str]
    msd: str
    p: str


class GenerateInflectionTable(abc.ABC):
    @abc.abstractmethod
    def query(self, paradigm: str, word: str) -> Iterable[InflectionTableRow]: ...
