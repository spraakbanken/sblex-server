from typing import AsyncGenerator

import environs
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sblex.fm_server.config import Settings as FmSettings
from sblex.fm_server.server import create_fm_server
from sblex.telemetry.settings import OTelSettings
from sblex.webapp.deps import get_fm_client
from sblex.webapp.main import create_webapp


@pytest.fixture(name="env")
def fixture_env() -> environs.Env:
    env = environs.Env()
    env.read_env("assets/testing/env")
    return env


@pytest.fixture(name="webapp")
def fixture_webapp(env: environs.Env, fm_client: AsyncClient) -> FastAPI:
    webapp = create_webapp(
        config={
            "semantic.path": "assets/testing/saldo.txt",
            "morphology.path": "assets/testing/saldo.lex",
        },
        env=env,
    )

    def override_fm_client() -> AsyncClient:
        return fm_client

    webapp.dependency_overrides[get_fm_client] = override_fm_client
    return webapp


@pytest_asyncio.fixture
async def client(webapp: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(webapp):
        async with AsyncClient(app=webapp, base_url="http://testserver") as client:
            yield client


@pytest.fixture(name="fm_server")
def fixture_fm_server(env: environs.Env) -> FastAPI:
    return create_fm_server(
        settings=FmSettings(
            morphology_path="assets/testing/saldo.lex",
            otel=OTelSettings(debug_log_otel_to_console=False, debug_log_otel_to_provider=False),
        )
    )


@pytest_asyncio.fixture
async def fm_client(fm_server: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(fm_server):
        async with AsyncClient(app=fm_server, base_url="http://fmserver") as fm_client:
            yield fm_client
