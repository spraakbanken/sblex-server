from typing import Callable

from fastapi import FastAPI
from sblex.fm import MemMorphology
from sblex.infrastructure.queries import MemLookupLid


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        load_lookup_lid(app)
        load_morphology(app)

    return start_app


def load_lookup_lid(app: FastAPI) -> None:
    lookup_lid = MemLookupLid.from_tsv_path(app.state.config["semantic.path"])
    app.state._lookup_lid = lookup_lid


def load_morphology(app: FastAPI) -> None:
    morphology = MemMorphology.from_path(app.state.config["morphology.path"])
    app.state._morph = morphology
