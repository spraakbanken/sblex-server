import sys
from typing import Any

from json_arrays import jsonlib
from opentelemetry import trace
from sblex.application import texts
from sblex.application.queries import LookupLid
from sblex.application.queries.inflection import InflectionTableQuery, InflectionTableRow
from sblex.fm import Morphology


class LookupService:
    def __init__(
        self,
        *,
        morphology: Morphology,
        lookup_lid: LookupLid,
        inflection_table: InflectionTableQuery,
    ) -> None:
        self._morphology = morphology
        self._lookup_lid = lookup_lid
        self._inflection_table = inflection_table

    async def lookup_ff(self, segment: str) -> list[dict[str, Any]]:
        return jsonlib.loads(await self._morphology.lookup(segment))["a"]

    async def lookup_lid(self, lid: str) -> dict[str, Any]:
        return await self._lookup_lid.get_by_lid(lid)

    def lookup_table(self, paradigm: str, word: str) -> list[InflectionTableRow]:
        return self._inflection_table.query(paradigm, word)

    async def wordforms(self, sense_id: str) -> list:
        ls = (await self.lookup_lid(sense_id))["l"]
        ws = []
        for lemma in ls:
            ws.extend(await self.generate_wordforms(lemma))
        return list(set(ws))

    async def generate_wordforms(self, lemma_id: str):
        r = await self.lookup_lid(lemma_id)
        return [
            w["form"]
            for w in self.lookup_table(r["p"], r["gf"])
            if w["msd"] not in ["c", "ci", "cm", "sms"]
        ]

    async def compound(self, s, n=1):
        with trace.get_tracer(__name__).start_as_current_span(
            sys._getframe().f_code.co_name
        ) as _process_api_span:
            if len(s) < 1:
                return [[]]
            if n > 2:
                return []
            result = []
            for pre1, suf1 in texts.inits(s):
                if len(pre1) > 1:
                    for pre, suf in sandhi(pre1, suf1):
                        for a in await self.lookup_ff(pre):
                            if suf != [] or a["msd"] in ["ci", "cm", "c"]:
                                for c in await self.compound(suf, n + 1):
                                    result.append([add_prefix(a, pre1), *c])
            return sorted(result, key=comp)


def add_prefix(a, pre):
    a["segment"] = pre
    return a


def sandhi(pre, suf):
    if len(suf) < 1:
        return [(pre, suf)]
    if pre[-1] == suf[0]:
        return [(pre, suf), (pre + pre[-1], suf)]
    else:
        return [(pre, suf)]


def comp(x, y):
    x_len, y_len = len(x), len(y)
    if x_len > y_len:
        return 1
    elif x_len == y_len:
        return len_comp_parts(x, y)
    else:
        return -1


def len_comp_parts(x, y):
    n1, n2 = 0, 0
    for n in x:
        n1 += len(n["gf"])
    for n in y:
        n2 += len(n["gf"])
    if n1 > n2:
        return 1
    elif n1 == n2:
        return 0
    else:
        return -1
