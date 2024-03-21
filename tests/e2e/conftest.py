from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sblex.fm.fm_runner import FmRunner
from sblex.fm_server.config import Settings as FmSettings
from sblex.fm_server.server import create_fm_server
from sblex.saldo_ws.config import FmBinSettings, MatomoSettings
from sblex.saldo_ws.config import Settings as SaldoWsSettings
from sblex.saldo_ws.deps import get_fm_client, get_fm_runner
from sblex.saldo_ws.server import create_saldo_ws_server
from sblex.telemetry.settings import OTelSettings
from syrupy.extensions.json import JSONSnapshotExtension

from tests.adapters.mem_fm_runner import MemFmRunner


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


@pytest.fixture(name="webapp")
def fixture_webapp(fm_client: AsyncClient) -> FastAPI:
    webapp = create_saldo_ws_server(
        settings=SaldoWsSettings(
            semantic_path="assets/testing/saldo.txt",
            fm_server_url="not-used",
            fm_bin=FmBinSettings(path="not used"),
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

    def override_fm_runner() -> FmRunner:
        return MemFmRunner(
            paradigms={
                "vb_vs_dväljas": {
                    "dväljas": [
                        {
                            "word": "dväljes",
                            "head": "dväljas",
                            "pos": "vb",
                            "param": "pres ind s-form",
                            "inhs": [],
                            "id": "dväljes_vb",
                            "p": "vb_vs_dväljas",
                            "attr": "0",
                        },
                        {
                            "word": "dväljs",
                            "head": "dväljas",
                            "pos": "vb",
                            "param": "pres ind s-form",
                            "inhs": [],
                            "id": "dväljes_vb",
                            "p": "vb_vs_dväljas",
                            "attr": "0",
                        },
                        {
                            "word": "dvaldes",
                            "head": "dväljas",
                            "pos": "vb",
                            "param": "pret ind s-form",
                            "inhs": [],
                            "id": "dväljes_vb",
                            "p": "vb_vs_dväljas",
                            "attr": "0",
                        },
                        {
                            "word": "dväljdes",
                            "head": "dväljas",
                            "pos": "vb",
                            "param": "pret ind s-form",
                            "inhs": [],
                            "id": "dväljes_vb",
                            "p": "vb_vs_dväljas",
                            "attr": "0",
                        },
                        {
                            "word": "dväljes",
                            "head": "dväljas",
                            "pos": "vb",
                            "param": "imper",
                            "inhs": [],
                            "id": "dväljes_vb",
                            "p": "vb_vs_dväljas",
                            "attr": "0",
                        },
                        {
                            "word": "dväljs",
                            "head": "dväljas",
                            "pos": "vb",
                            "param": "imper",
                            "inhs": [],
                            "id": "dväljes_vb",
                            "p": "vb_vs_dväljas",
                            "attr": "0",
                        },
                        {
                            "word": "dväljas",
                            "head": "dväljas",
                            "pos": "vb",
                            "param": "inf s-form",
                            "inhs": [],
                            "id": "dväljes_vb",
                            "p": "vb_vs_dväljas",
                            "attr": "0",
                        },
                        {
                            "word": "dvalts",
                            "head": "dväljas",
                            "pos": "vb",
                            "param": "sup s-form",
                            "inhs": [],
                            "id": "dväljes_vb",
                            "p": "vb_vs_dväljas",
                            "attr": "0",
                        },
                        {
                            "word": "dvälts",
                            "head": "dväljas",
                            "pos": "vb",
                            "param": "sup s-form",
                            "inhs": [],
                            "id": "dväljes_vb",
                            "p": "vb_vs_dväljas",
                            "attr": "0",
                        },
                    ]
                }
            }
        )

    webapp.dependency_overrides[get_fm_client] = override_fm_client
    webapp.dependency_overrides[get_fm_runner] = override_fm_runner
    return webapp


@pytest_asyncio.fixture
async def client(webapp: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(webapp):
        async with AsyncClient(
            transport=ASGITransport(webapp),  # type: ignore [arg-type]
            base_url="http://testserver",
        ) as client:
            yield client


@pytest.fixture(name="fm_server")
def fixture_fm_server() -> FastAPI:
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
            transport=ASGITransport(fm_server),  # type: ignore [arg-type]
            base_url="http://fmserver",
        ) as fm_client:
            yield fm_client
