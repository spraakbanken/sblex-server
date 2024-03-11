import logging
from contextlib import asynccontextmanager
from typing import Callable

import httpx
from fastapi import FastAPI
from sblex.fm import MemMorphology
from sblex.infrastructure.queries import MemLookupLid

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        load_lookup_lid(app)
        load_morphology(app)

    return start_app


def load_lookup_lid(app: FastAPI) -> None:
    logger.info("loading lookup lid")
    lookup_lid = MemLookupLid.from_tsv_path(app.state.settings.semantic_path)
    app.state._lookup_lid = lookup_lid


def load_morphology(app: FastAPI) -> None:
    logger.info("loading morphology")
    morphology = MemMorphology.from_path(app.state.config["morphology.path"])
    app.state._morph = morphology


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup")
    app.state._fm_client = httpx.AsyncClient(base_url=app.state.settings.fm_server_url)
    load_lookup_lid(app)
    yield
    await app.state._fm_client.aclose()
    logger.info("shutdown")
