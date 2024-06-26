import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize("segment", ["dväljas", "bo"])
@pytest.mark.asyncio
async def test_sms_json(segment: str, client: AsyncClient, snapshot_json) -> None:
    response = await client.get(f"/sms/json/{segment}")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == snapshot_json


@pytest.mark.parametrize("segment", ["dväljas", "bo"])
@pytest.mark.asyncio
async def test_sms_html(segment: str, client: AsyncClient, snapshot) -> None:
    response = await client.get(f"/sms/html/{segment}")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.text == snapshot


@pytest.mark.parametrize("segment", ["dväljas", "bo"])
@pytest.mark.asyncio
async def test_sms_xml(segment: str, client: AsyncClient, snapshot) -> None:
    response = await client.get(f"/sms/xml/{segment}")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.headers["content-type"] == "application/xml"
    assert response.text == snapshot
