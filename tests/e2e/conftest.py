from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from syrupy.extensions.json import JSONSnapshotExtension

from sblex.fm.fm_runner import FmRunner
from sblex.fm_server.config import Settings as FmSettings
from sblex.fm_server.server import create_fm_server
from sblex.saldo_ws.server import create_saldo_ws_server
from sblex.sblex_server.deps import get_fm_client, get_fm_runner
from sblex.sblex_server.settings import AppSettings, FmBinSettings, MatomoSettings
from sblex.sblex_server.settings import Settings as SaldoWsSettings
from sblex.telemetry.settings import OTelSettings
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
            app=AppSettings(template_directory="templates/saldo_ws"),
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
            },
            word_to_paradigm={
                "dväljes:vb": [
                    "vb_0d_lyss",
                    "vb_0d_lyster",
                    "vb_0d_nåde",
                    "vb_0d_vederböra",
                    "vb_0d_värdes",
                    "vb_1a_beundra",
                    "vb_1a_hitta",
                    "vb_1a_häda",
                    "vb_1a_klaga",
                    "vb_1a_laga",
                    "vb_1a_skapa",
                    "vb_1a_spara",
                    "vb_1a_ugnsbaka",
                    "vb_1a_unna",
                    "vb_1a_vissla",
                    "vb_1a_vänta",
                    "vb_1m_existera",
                    "vb_1m_hisna",
                    "vb_1m_kackla",
                    "vb_1m_svira",
                    "vb_1m_vånna",
                    "vb_1s_andas",
                    "vb_1s_gillas",
                    "vb_2a_ansöka",
                    "vb_2a_genmäla",
                    "vb_2a_göra",
                    "vb_2a_hyra",
                    "vb_2a_känna",
                    "vb_2a_leda",
                    "vb_2a_leva",
                    "vb_2a_lyfta",
                    "vb_2a_lägga",
                    "vb_2a_mista",
                    "vb_2a_motsäga",
                    "vb_2a_spörja",
                    "vb_2a_städja",
                    "vb_2a_stödja",
                    "vb_2a_säga",
                    "vb_2a_sälja",
                    "vb_2a_sända",
                    "vb_2a_sätta",
                    "vb_2a_tämja",
                    "vb_2a_viga",
                    "vb_2a_välja",
                    "vb_2d_må",
                    "vb_2d_rädas",
                    "vb_2d_torde",
                    "vb_2m_böra",
                    "vb_2m_gitta",
                    "vb_2m_glädja",
                    "vb_2m_ha",
                    "vb_2m_hända",
                    "vb_2m_höta",
                    "vb_2m_mysa",
                    "vb_2m_väga",
                    "vb_2s_blygas",
                    "vb_2s_giftas",
                    "vb_2s_glädjas",
                    "vb_2s_hövas",
                    "vb_2s_idas",
                    "vb_2s_minnas",
                    "vb_2s_nöjas",
                    "vb_2s_rymmas",
                    "vb_2s_skiljas",
                    "vb_2s_synas",
                    "vb_2s_trivas",
                    "vb_2s_töras",
                    "vb_2s_vämjas",
                    "vb_3a_sy",
                    "vb_3s_brås",
                    "vb_4a_be",
                    "vb_4a_bli",
                    "vb_4a_bottenfrysa",
                    "vb_4a_bära",
                    "vb_4a_dricka",
                    "vb_4a_emotstå",
                    "vb_4a_falla",
                    "vb_4a_fara",
                    "vb_4a_flyga",
                    "vb_4a_förgäta",
                    "vb_4a_ge",
                    "vb_4a_gå",
                    "vb_4a_hålla",
                    "vb_4a_komma",
                    "vb_4a_missförstå",
                    "vb_4a_rida",
                    "vb_4a_se",
                    "vb_4a_skjuta",
                    "vb_4a_slå",
                    "vb_4a_stinga",
                    "vb_4a_stjäla",
                    "vb_4a_svära",
                    "vb_4a_ta",
                    "vb_4a_tillåta",
                    "vb_4a_äta",
                    "vb_4d_vederfås",
                    "vb_4m_angå",
                    "vb_4m_bekomma",
                    "vb_4m_erfara",
                    "vb_4m_förevara",
                    "vb_4m_förslå",
                    "vb_4m_gråta",
                    "vb_4m_innebära",
                    "vb_4m_le",
                    "vb_4m_ligga",
                    "vb_4m_ljuda",
                    "vb_4m_ryta",
                    "vb_4m_sitta",
                    "vb_4m_skåpäta",
                    "vb_4m_småsvära",
                    "vb_4m_sova",
                    "vb_4m_stå",
                    "vb_4m_svälta_1",
                    "vb_4m_vara",
                    "vb_4m_vina",
                    "vb_4s_bitas",
                    "vb_4s_finnas",
                    "vb_4s_hållas",
                    "vb_4s_munhuggas",
                    "vb_4s_slåss",
                    "vb_4s_tas",
                    "vb_4s_umgås",
                    "vb_4s_vederfaras",
                    "vb_id_månde",
                    "vb_ik_bevare",
                    "vb_oa_varda",
                    "vb_om_heta",
                    "vb_om_kunna",
                    "vb_om_måste",
                    "vb_om_skola",
                    "vb_om_veta",
                    "vb_om_vilja",
                    "vb_va_begrava",
                    "vb_va_besluta",
                    "vb_va_bestrida",
                    "vb_va_besvärja",
                    "vb_va_bringa",
                    "vb_va_framtvinga",
                    "vb_va_frysa",
                    "vb_va_förlöpa",
                    "vb_va_förmäla",
                    "vb_va_förse",
                    "vb_va_gälda",
                    "vb_va_gälla_kastrera",
                    "vb_va_klyva",
                    "vb_va_klä",
                    "vb_va_koka",
                    "vb_va_kväda",
                    "vb_va_lyda",
                    "vb_va_löpa",
                    "vb_va_mala",
                    "vb_va_nypa",
                    "vb_va_nästa",
                    "vb_va_simma",
                    "vb_va_skvätta",
                    "vb_va_smälta",
                    "vb_va_snusmala",
                    "vb_va_sprida",
                    "vb_va_strypa",
                    "vb_va_stupa",
                    "vb_va_svälta_2",
                    "vb_va_tala",
                    "vb_va_träda",
                    "vb_va_tvinga",
                    "vb_va_två",
                    "vb_va_tälja",
                    "vb_va_utlöpa",
                    "vb_va_vika",
                    "vb_va_växa",
                    "vb_vm_avvara",
                    "vb_vm_drypa",
                    "vb_vm_drösa",
                    "vb_vm_duga",
                    "vb_vm_fnysa",
                    "vb_vm_gala",
                    "vb_vm_klinga",
                    "vb_vm_kvida",
                    "vb_vm_nysa",
                    "vb_vm_ryka",
                    "vb_vm_samvara",
                    "vb_vm_sluta",
                    "vb_vm_smälla",
                    "vb_vm_snika",
                    "vb_vm_strida",
                    "vb_vm_undvara",
                    "vb_vm_upphäva",
                    "vb_vs_dväljas",
                ]
            },
        )

    webapp.dependency_overrides[get_fm_client] = override_fm_client
    webapp.dependency_overrides[get_fm_runner] = override_fm_runner
    return webapp


@pytest_asyncio.fixture
async def client(webapp: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(webapp):
        async with AsyncClient(
            transport=ASGITransport(webapp),  # type: ignore [arg-type]
            base_url="http://testserver.saldo_ws",
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
            base_url="http://fmserver.saldo-ws",
        ) as fm_client:
            yield fm_client
