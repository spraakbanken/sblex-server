from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sblex.fm_server.main import create_fm_server
from sblex.webapp.deps import get_fm_client
from sblex.webapp.main import create_webapp


@pytest.fixture(name="webapp")
def fixture_webapp(fm_client: AsyncClient) -> FastAPI:
    webapp = create_webapp(
        config={
            "semantic.path": "assets/testing/saldo.txt",
            "morphology.path": "assets/testing/saldo.lex",
        },
        use_telemetry=False,
    )

    def overide_fm_client() -> AsyncClient:
        return fm_client

    webapp.dependency_overrides[get_fm_client] = overide_fm_client
    return webapp


@pytest_asyncio.fixture
async def client(webapp: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(webapp):
        async with AsyncClient(app=webapp, base_url="http://testserver") as client:
            yield client


@pytest.fixture(name="fm_server")
def fixture_fm_server() -> FastAPI:
    return create_fm_server(
        config={
            "semantic.path": "assets/testing/saldo.txt",
            "morphology.path": "assets/testing/saldo.lex",
        },
        use_telemetry=False,
    )


@pytest_asyncio.fixture
async def fm_client(fm_server: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(fm_server):
        async with AsyncClient(app=fm_server, base_url="http://fmserver") as fm_client:
            yield fm_client
