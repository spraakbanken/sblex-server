"""FM morphology."""

import abc
import contextlib
import logging
import sys

import json_arrays
from json_arrays.utility import JsonFormat
from opentelemetry import trace

from sblex.trie import Trie

logger = logging.getLogger(__name__)


class Morphology(abc.ABC):
    @abc.abstractmethod
    async def lookup(self, word: str, n: int = 0) -> bytes | None: ...

    @abc.abstractmethod
    async def lookup_from_bytes(self, s: bytes) -> bytes | None: ...

    @abc.abstractmethod
    async def lookup_w_cont(self, word: str) -> bytes | None: ...


class MemMorphology(Morphology):
    def __init__(self, trie: Trie) -> None:
        self._trie = trie

    @classmethod
    def from_path(cls, fname: str) -> "Morphology":
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _process_api_span:
            logger.info("building morphology structure... (takes about 1 minute)")
            return cls(
                trie=Trie.from_iter(
                    json_arrays.load_from_file(fname, json_format=JsonFormat.JSON_LINES)
                )
            )

    async def lookup(self, word: str, n: int = 0) -> bytes | None:
        if data := self._trie.lookup(word, n):
            struct = json_arrays.jsonlib.loads(data)
            return json_arrays.jsonlib.dumps(struct["a"])

        return None

    async def lookup_from_bytes(self, s: bytes) -> bytes | None:
        with contextlib.suppress(Exception):
            res = s.decode("UTF-8").split(" ", 1)
            n = int(res[0])
            word = res[1]
            if r := self._trie.lookup(word, n):
                return r
        return None

    async def lookup_w_cont(self, word: str) -> bytes | None:
        return self._trie.lookup(word)
