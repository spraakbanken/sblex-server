from typing import Any

from json_arrays import jsonlib
from sblex.application.queries import LookupLid
from sblex.fm import Morphology


class LookupService:
    def __init__(self, *, morphology: Morphology, lookup_lid: LookupLid) -> None:
        self._morphology = morphology
        self._lookup_lid = lookup_lid

    async def lookup_ff(self, segment: str) -> list[dict[str, Any]]:
        return jsonlib.loads(await self._morphology.lookup(segment))["a"]

    async def lookup_lid(self, lid: str) -> dict[str, Any]:
        return await self._lookup_lid.get_by_lid(lid)
