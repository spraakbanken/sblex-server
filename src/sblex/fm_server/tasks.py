import logging
import typing

from fastapi import FastAPI
from sblex.fm import MemMorphology

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI) -> typing.Callable:
    def start_app() -> None:
        load_morphology(app)

    return start_app


def load_morphology(app: FastAPI) -> None:
    logger.info("loading morphology")
    morphology = MemMorphology.from_path(app.state.config["morphology.path"])
    app.state._morph = morphology
