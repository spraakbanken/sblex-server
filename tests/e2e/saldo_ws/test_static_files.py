import pytest
from fastapi import status
from httpx import AsyncClient


class TestStaticRoutes:
    @pytest.mark.asyncio
    async def test_static_saldo_css_returns_200(self, client: AsyncClient) -> None:
        res = await client.get("/static/saldo.css")
        assert res.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_root_path_and_static_saldo_css_returns_200(
        self, client_w_root_path: AsyncClient
    ) -> None:
        res = await client_w_root_path.get("/static/saldo.css")
        assert res.status_code == status.HTTP_200_OK
