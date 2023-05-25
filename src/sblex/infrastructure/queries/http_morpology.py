import httpx
from sblex.fm import Morphology


class HttpMorphology(Morphology):
    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._http_client = http_client

    async def lookup(self, word: str, n: int = 0) -> bytes:
        response = await self._http_client.get(f"/morph/{word}/{n}")
        return response.content

    async def lookup_from_bytes(self, s: bytes) -> bytes:
        response = await self._http_client.get(f"/morph/{s.decode('utf-8')}/0")
        return response.content
