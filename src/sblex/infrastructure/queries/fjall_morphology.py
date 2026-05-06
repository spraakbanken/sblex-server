import logging
import sys
from pathlib import Path

from opentelemetry import trace
from sblex_fjall_morphology import FjallMorphology as SblexFjallMorphology

from sblex.fm import Morphology

logger = logging.getLogger(__name__)


class FjallMorphology(Morphology):
    def __init__(self, folder: Path) -> None:
        self._db = SblexFjallMorphology(folder)

    async def lookup(self, word: str, n: int = 0) -> bytes | None:
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _process_api_span:
            return self._db.lookup(word)

    async def lookup_from_bytes(self, s: bytes) -> bytes | None:
        return await self.lookup(s.decode("utf-8"))

    async def lookup_with_cont(self, word: str) -> bytes | None:
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _process_api_span:
            return self._db.lookup_with_cont(word)
