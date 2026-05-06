import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from sblex.fm.fm_runner import FmRunner
from sblex.infrastructure.queries import FjallMorphology, MemLookupLid

logger = logging.getLogger(__name__)


def load_lookup_lid(app: FastAPI) -> None:
    logger.info("loading lookup lid")
    lookup_lid = MemLookupLid.from_tsv_path(app.state.settings.semantic_path)
    app.state._lookup_lid = lookup_lid


def load_morphology(app: FastAPI) -> None:
    logger.warning("loading morphology")
    morphology = FjallMorphology(app.state.settings.morphology_path)
    app.state._morph = morphology


def setup_fmrunner(app: FastAPI) -> None:
    logger.info("setup fm-runner")
    fm_runner = FmRunner(app.state.settings.fm_bin.path, locale=app.state.settings.fm_bin.locale)
    app.state._fm_runner = fm_runner


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup")
    # app.state._fm_client = httpx.AsyncClient(base_url=app.state.settings.fm_server_url)
    load_lookup_lid(app)
    setup_fmrunner(app)
    load_morphology(app)
    yield
    # await app.state._fm_client.aclose()
    logger.info("shutdown")
