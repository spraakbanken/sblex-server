import logging
import subprocess
from pathlib import Path
from typing import TypedDict

from json_arrays import jsonlib
from opentelemetry import trace

tracer = trace.get_tracer(__name__)


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
        with tracer.start_as_current_span("call_fm_binary") as call_span:
            args = f'{paradigm} "{word}";'
            program = [
                self.binary_path,
                "-i",
            ]
            args = f'{paradigm} "{word}";'
            call_span.set_attribute("program", str(program))
            call_span.set_attribute("args", args)
            process = subprocess.run(
                program,  # type: ignore # noqa: S603
                input=args.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if process.returncode != 0:
                logging.error(
                    "Call to `fm-sblex` failed",
                    extra={
                        "stderr": process.stderr.decode("utf-8"),
                        "binary_path": self.binary_path,
                        "args": args,
                    },
                )

                raise RuntimeError("Call to `fm-sblex` failed")

            return jsonlib.loads(process.stdout)
