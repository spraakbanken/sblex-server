import logging

from fastapi import FastAPI

from sblex.dalin_ws import config, routes
from sblex.sblex_server import server

logger = logging.getLogger(__name__)


def create_dalin_ws_server(*, settings: config.DalinWsSettings) -> FastAPI:
    logger.debug("creating app")
    webapp = server.create_sblex_server(title="Saldo WS", settings=settings)

    webapp.include_router(routes.router)
    # webapp.mount("/static", StaticFiles(directory="static"), name="static")

    return webapp
