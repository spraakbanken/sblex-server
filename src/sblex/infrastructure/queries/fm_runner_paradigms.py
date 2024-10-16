import sys
import typing

from opentelemetry import trace

from sblex.application.queries import Paradigms
from sblex.fm import FmRunner


class FmRunnerParadigms(Paradigms):
    def __init__(self, *, fm_runner: FmRunner) -> None:
        super().__init__()
        self.fm_runner = fm_runner

    def query(self, s: str) -> typing.Tuple[str, list]:
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _process_api_span:
            baseform, words = self.prepare_args(s)
            print(f"{baseform=}, {words=}")
            print(f"{type(self.fm_runner)=}")
            result = self.fm_runner.paradigms(words)
            return baseform, result
