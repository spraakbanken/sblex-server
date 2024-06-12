import pytest
import pytest_asyncio
from httpx import AsyncClient
from sblex.infrastructure.queries.http_morpology import HttpMorphology


@pytest_asyncio.fixture(name="http_morphology")
async def fixture_http_morphology(fm_client: AsyncClient) -> HttpMorphology:
    return HttpMorphology(http_client=fm_client)


class TestHttpMorphology:
    @pytest.mark.asyncio
    async def test_lookup_from_bytes(self, http_morphology: HttpMorphology, snapshot) -> None:
        result = await http_morphology.lookup_from_bytes(b"dv\xc3\xa4ljes")

        assert result == snapshot
