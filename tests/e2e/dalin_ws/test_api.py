import pytest
from fastapi import status
from httpx import AsyncClient
from syrupy.matchers import path_type


@pytest.mark.asyncio
async def test_version(client: AsyncClient, snapshot_json) -> None:
    response = await client.get("/version")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot_json(
        matcher=path_type({"version": (str,), "date": (str,)})
    )


@pytest.mark.asyncio
async def test_version_json(client: AsyncClient, snapshot) -> None:
    response = await client.get("/version/json")
    assert response == snapshot


@pytest.mark.asyncio
async def test_static_saldo_css(client: AsyncClient) -> None:
    response = await client.get("/static/saldo.css")
    assert response.status_code == status.HTTP_200_OK
