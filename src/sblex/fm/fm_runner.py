import logging
import subprocess
import sys
import typing
from pathlib import Path
from typing import TypedDict

from json_arrays import jsonlib
from opentelemetry import trace

logger = logging.getLogger(__name__)


class InflectionRow(TypedDict):
    word: str
    head: str
    pos: str
    inhs: list[str]
    param: str
    id: str
    p: str
    attr: str


class FmRunner:
    def __init__(self, binary_path: Path, *, locale: str | None = None) -> None:
        self.binary_path = binary_path.resolve()
        self.locale = locale or 'LC_ALL="sv_SE.UTF-8"'

    def inflection(self, paradigm: str, word: str) -> list[InflectionRow]:
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _call_span:
            program: list[typing.Union[str, Path]] = [
                self.binary_path,
                "-i",
            ]
            args = f'{paradigm} "{word}";'
            return self._call_fm_binary(program=program, args=args)

    def _call_fm_binary(self, program: list[typing.Union[str, Path]], args: str):
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as call_span:
            call_span.set_attribute("program", str(program))
            call_span.set_attribute("args", args)
            process = subprocess.run(
                program,  # type: ignore # noqa: S603
                input=args.encode("utf-8"),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if process.returncode != 0:
                logger.error(
                    "Call to `fm-sblex` failed",
                    extra={
                        "stderr": process.stderr.decode("utf-8"),
                        "binary_path": self.binary_path,
                        "program": str(program),
                        "args": args,
                    },
                )

                raise RuntimeError("Call to `fm-sblex` failed")
            raw_data = process.stdout
            return jsonlib.loads(raw_data) if len(raw_data) > 0 else []

    def paradigms(self, words: list[str]) -> list[str]:
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _call_span:
            program: list[typing.Union[str, Path]] = [
                self.binary_path,
                "-f",
            ]
            args = ",".join(words)
            return self._call_fm_binary(
                program=program,
                args=args,
            )
