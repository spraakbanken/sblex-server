from typing import Callable

from fastapi import FastAPI
from sblex.infrastructure.queries import MemLookupLid


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        load_lookup_lid(app)

    return start_app


def load_lookup_lid(app: FastAPI) -> None:
    lookup_lid = MemLookupLid.from_tsv_path(app.state.config["SEMANTIC_PATH"])
    app.state._lookup_lid = lookup_lid
