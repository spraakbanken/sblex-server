from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient, Response

from sblex.infrastructure.queries.http_morpology import HttpMorphology


@pytest.mark.asyncio
async def test_lookup_from_bytes() -> None:
    mock_client = AsyncMock(spec=AsyncClient)
    attrs = {"get.return_value": Response(400, content="error")}
    mock_client.configure_mock(**attrs)

    http_morphology = HttpMorphology(mock_client)
    result = await http_morphology.lookup("dväljes")

    assert result is None
