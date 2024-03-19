from typing import Any

from json_arrays import jsonlib
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
