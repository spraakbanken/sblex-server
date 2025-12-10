import csv
import itertools
import logging
import random
import sys
from pathlib import Path
from typing import Any

from opentelemetry import trace

from sblex.application.queries import LookupLid
from sblex.application.queries.lookup_lid import LemmaNotFound, LexemeNotFound

logger = logging.getLogger(__name__)


class MemLookupLid(LookupLid):
    def __init__(
        self,
        *,
        lex_map: dict[str, dict[str, Any]],
        lem_map: dict[str, dict[str, Any]],
        path_map: dict[str, list[str]],
    ):
        self._lex_map = lex_map
        self._lem_map = lem_map
        self._path_map = path_map

    @classmethod
    def from_tsv_path(cls, tsv_path: Path) -> "MemLookupLid":  # noqa: C901
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _process_api_span:
            lem_map: dict[str, tuple[set[str], str, str]] = {}
            lex_map: dict[str, tuple[str, str, set[str], set[str], set[str]]] = {}
            path_map: dict[str, list[str]] = {}
            with open(tsv_path, "r", encoding="utf-8") as f:
                tsv_file = csv.reader(f, delimiter="\t")
                for line in tsv_file:
                    if len(line) != 7:
                        logger.warning(
                            "Expected 7 columns, line has %d: '%s' skipping ...",
                            len(line),
                            line,
                        )
                        continue
                    (lexeme, mother, father, lemma, gf, _pos, p) = line
                    # create lemma-lexeme mappings
                    if lemma in lem_map:
                        (s, p, gf) = lem_map[lemma]
                        s.add(lexeme)
                    else:
                        lem_map[lemma] = ({lexeme}, p.strip(), gf)
                    # add mother, father and lemma
                    if lexeme in lex_map:
                        # we may have added the children already
                        (_, _, mf, pf, ls) = lex_map[lexeme]
                        ls.add(lemma)
                        lex_map[lexeme] = (mother, father, mf, pf, ls)
                    else:
                        lex_map[lexeme] = mother, father, set(), set(), {lemma}

                    # add m-children
                    if mother in lex_map:
                        (m, f, mf, pf, _) = lex_map[mother]  # type: ignore [assignment]
                        mf.add(lexeme)
                    else:
                        # we don't know the mother and the father yet.
                        lex_map[mother] = ("", "", {lexeme}, set(), set())

                    # add p-children
                    for father_ in father.split():
                        if father_ in lex_map:
                            (m, f, mf, pf, _) = lex_map[father_]  # type: ignore [assignment]
                            pf.add(lexeme)
                        else:
                            lex_map[father_] = ("", "", set(), {lexeme}, set())

                # add path
                for sense in lex_map:
                    pth = []
                    sns = sense
                    while sns not in ["PRIM..1", ""] and sns not in pth:
                        (primary, _, _, _, _) = lex_map[sns]
                        sns = primary
                        if sns != "PRIM..1":
                            pth.append(sns)
                    path_map[sense] = pth

                final_lem_map = {}
                for lem, lem_values in lem_map.items():
                    (s, p, gf) = lem_values
                    final_lem_map[lem] = {"l": sorted(s), "p": p, "gf": gf}
                final_lex_map = {}
                for lex, lex_values in lex_map.items():
                    (m, f, mchildren, pchildren, lemmas) = lex_values  # type: ignore [assignment]
                    final_lex_map[lex] = {
                        "lex": lex,
                        "fm": m,
                        "fp": f,
                        "mf": sorted(mchildren),
                        "pf": sorted(pchildren),
                        "l": sorted(lemmas),
                        "path": path_map[lex],
                        "ppath": father_path(f, path_map),
                    }
                    #  % (l,m,f,pr_set(mchildren),pr_set(pchildren),pr_set(lemmas),
                    #     pr_list(path_map[l]),father_path(f))
            return cls(lex_map=final_lex_map, lem_map=final_lem_map, path_map=path_map)

    async def get_lemma(self, lid: str) -> dict[str, Any]:
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _process_api_span:
            try:
                logger.debug("lookup lemma", extra={"lemma": lid})
                result = self._lem_map[lid]
                logger.debug("lemma", extra={"lemma": lid, "result": result})
                return result
            except KeyError as exc:
                raise LemmaNotFound(lid) from exc

    async def get_lexeme(self, lid: str) -> dict[str, Any]:
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _process_api_span:
            if lid == "rnd":
                rnd_key_index = random.randrange(0, len(self._lex_map))  # noqa: S311
                rnd_key = next(itertools.islice(self._lex_map.keys(), rnd_key_index, None))
                return self._lex_map[rnd_key]
            try:
                return self._lex_map[lid]
            except KeyError as exc:
                raise LexemeNotFound(lid) from exc

    def process(self, command: str, key: str) -> dict[str, Any]:
        try:
            if command == "lem":
                return self._lem_map[key]
            elif command == "lex":
                return (
                    self._lex_map[
                        list(self._lex_map.keys())[
                            random.randint(0, len(self._lex_map) - 1)  # noqa: S311
                        ]
                    ]
                    if key == "rnd"
                    else self._lex_map[key]
                )

            elif command == "rel":
                raise NotImplementedError("return relations(key)")
            raise UnknownCommand(command)
        except:  # noqa: E722
            return {}


def father_path(fathers, path_map: dict[str, list[str]]) -> list[list[str]]:
    result = []
    for s in fathers.split(" "):
        if s != "PRIM..1" and s != "":
            result.append(path_map[s])
    return result


class UnknownCommand(Exception):
    """Raised when process is getting an unknown command."""
