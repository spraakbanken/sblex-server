from typing import Iterable

from sblex.application.queries import GenerateInflectionTable
from sblex.application.queries.inflection import InflectionTableRow
from sblex.fm import FmRunner


class FmRunnerInflectionTable(GenerateInflectionTable):
    def __init__(self, *, fm_runner: FmRunner) -> None:
        super().__init__()
        self.fm_runner = fm_runner

    def query(self, paradigm: str, word: str) -> Iterable[InflectionTableRow]:
        for row in self.fm_runner.inflection(paradigm, word):
            yield {
                "form": row["word"],
                "gf": row["head"],
                "pos": row["pos"],
                "inhs": row["inhs"],
                "msd": row["param"],
                "p": row["p"],
            }
