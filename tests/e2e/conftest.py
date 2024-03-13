from typing import AsyncGenerator

import environs
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sblex.fm_server.config import Settings as FmSettings
from sblex.fm_server.server import create_fm_server
from sblex.saldo_ws.config import MatomoSettings, Settings as SaldoWsSettings
from sblex.saldo_ws.deps import get_fm_client
from sblex.saldo_ws.server import create_saldo_ws_server
from sblex.telemetry.settings import OTelSettings


@pytest.fixture(name="env")
def fixture_env() -> environs.Env:
    env = environs.Env()
    env.read_env("assets/testing/env")
    return env


@pytest.fixture(name="webapp")
def fixture_webapp(env: environs.Env, fm_client: AsyncClient) -> FastAPI:
    webapp = create_saldo_ws_server(
        settings=SaldoWsSettings(
            semantic_path="assets/testing/saldo.txt",
            fm_server_url="not-used",
            tracking=MatomoSettings(matomo_url=None),
            otel=OTelSettings(
                otel_service_name="saldo-ws",
                debug_log_otel_to_console=False,
                debug_log_otel_to_provider=False,
            ),
        )
        # config={
        #     "semantic.path": "assets/testing/saldo.txt",
        #     "morphology.path": "assets/testing/saldo.lex",
        # },
        # env=env,
    )

    def override_fm_client() -> AsyncClient:
        return fm_client

    webapp.dependency_overrides[get_fm_client] = override_fm_client
    return webapp


@pytest_asyncio.fixture
async def client(webapp: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(webapp):
        async with AsyncClient(
            transport=ASGITransport(webapp), base_url="http://testserver"
        ) as client:
            yield client


@pytest.fixture(name="fm_server")
def fixture_fm_server(env: environs.Env) -> FastAPI:
    return create_fm_server(
        settings=FmSettings(
            morphology_path="assets/testing/saldo.lex",
            otel=OTelSettings(
                otel_service_name="fm-server",
                debug_log_otel_to_console=False,
                debug_log_otel_to_provider=False,
            ),
        )
    )


@pytest_asyncio.fixture
async def fm_client(fm_server: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(fm_server):
        async with AsyncClient(
            transport=ASGITransport(fm_server), base_url="http://fmserver"
        ) as fm_client:
            yield fm_client
