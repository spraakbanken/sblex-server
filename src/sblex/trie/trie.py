import logging
import time
from typing import Any, Iterable

from json_arrays import jsonlib

logger = logging.getLogger(__name__)


class Trie:
    def __init__(self, trie: dict[int, tuple[dict[str, int], bytes]]) -> None:
        self._trie: dict[int, tuple[dict[str, int], bytes]] = trie

    @classmethod
    def from_iter(cls, dicts: Iterable[dict[str, Any]]) -> "Trie":
        logger.info("building morphology structure... (takes about 1 minute)")
        build_started = time.perf_counter()
        trie_builder = TrieBuilder()
        for j in dicts:
            w = j["word"]
            a = {
                "gf": j["head"],
                "id": j["id"],
                "pos": j["pos"],
                "is": j["inhs"],
                "msd": j["param"],
                "p": j["p"],
            }
            trie_builder.insert(w, jsonlib.dumps(a))

        logger.info("number of word forms read: %d", trie_builder.number_of_insertions())
        logger.info("number of states: %d", trie_builder.state)
        logger.info("initiating precomputation...")
        trie = trie_builder.build()
        elapsed = time.perf_counter() - build_started
        logger.info("building morphology took %d s", elapsed)
        return trie

    def lookup(self, word: str, start_state=0) -> bytes:
        st = start_state  # traversal state
        for c in word:
            try:
                st = self._trie[st][0][c]
            except:  # noqa: E722
                return b""
        return self._trie[st][1]


def wrap(s: bytes) -> bytes:
    return b"\n" + s + b"\n" if s else s


class TrieBuilder:
    def __init__(self) -> None:
        self.trie: dict[int, tuple[dict[str, int], list[bytes]]] = {0: ({}, [])}
        self.state = 0  # state counter
        self.count = 0  # number of insertions

    def insert(self, word: str, decoration: bytes):
        self.count += 1
        st = 0  # traversal state
        for i in range(len(word)):
            try:
                st = self.trie[st][0][word[i]]
            except:  # noqa: E722
                self.complete(st, word[i:], decoration)
                return
        self.trie[st][1].append(decoration)

    # create a new branch
    def complete(self, st: int, word: str, decoration: bytes):
        for c in word:
            self.state += 1
            self.trie[st][0][c] = self.state
            self.trie[self.state] = ({}, [])
            st = self.state
        self.trie[st][1].append(decoration)

    def number_of_insertions(self):
        return self.count

    def precompute(self) -> dict[int, tuple[dict[str, int], bytes]]:
        trie_precomputed = {}
        max_num_transitions = 0
        for i in range(self.state + 1):
            tr = self.trie[i][0]
            max_num_transitions = max(max_num_transitions, len(tr))
            dec = self.trie[i][1]
            # ys  = [x.encode('UTF-8') for x in dec]
            ys = b",".join(dec)
            cont = ("".join(self.continuation(i))).encode("UTF-8")
            trie_precomputed[i] = (
                tr,
                b'{"a":[%s],"c":"%s"}' % (ys, cont),
            )
        logger.info("max number of transitions in trie: %d", max_num_transitions)
        return trie_precomputed

    def continuation(self, state: int):
        return list(self.trie[state][0].keys())

    def build(self) -> Trie:
        trie = self.precompute()
        logger.info("precomputing: done")
        return Trie(trie=trie)
