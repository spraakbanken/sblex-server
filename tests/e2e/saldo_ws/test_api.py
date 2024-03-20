import pytest
from fastapi import status
from httpx import AsyncClient
from syrupy.extensions.json import JSONSnapshotExtension


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


@pytest.mark.asyncio
async def test_version(client: AsyncClient, snapshot_json) -> None:
    response = await client.get("/version")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot_json


@pytest.mark.asyncio
async def test_version_json(client: AsyncClient, snapshot) -> None:
    response = await client.get("/version/json")
    assert response == snapshot
