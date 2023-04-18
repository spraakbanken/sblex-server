from typing import Any

from json_streams import jsonlib
from sblex.application.queries import LookupLid
from sblex.fm import Morphology


class LookupService:
    def __init__(self, *, morphology: Morphology, lookup_lid: LookupLid) -> None:
        self._morphology = morphology
        self._lookup_lid = lookup_lid

    def lookup_ff(self, segment: str) -> list[dict[str, Any]]:
        return jsonlib.loads(self._morphology.lookup(segment))["a"]

    def lookup_lid(self, lid: str) -> dict[str, Any]:
        return self._lookup_lid.get_by_lid(lid)
