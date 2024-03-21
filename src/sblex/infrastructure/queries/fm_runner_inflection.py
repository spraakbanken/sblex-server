import sys

from opentelemetry import trace
from sblex.application.queries import InflectionTableQuery
from sblex.application.queries.inflection import InflectionTableRow
from sblex.fm import FmRunner


class FmRunnerInflectionTable(InflectionTableQuery):
    def __init__(self, *, fm_runner: FmRunner) -> None:
        super().__init__()
        self.fm_runner = fm_runner

    def query(self, paradigm: str, word: str) -> list[InflectionTableRow]:
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _process_api_span:
            return [
                {
                    "form": row["word"],
                    "gf": row["head"],
                    "pos": row["pos"],
                    "inhs": row["inhs"],
                    "msd": row["param"],
                    "p": row["p"],
                }
                for row in self.fm_runner.inflection(paradigm, word)
            ]
