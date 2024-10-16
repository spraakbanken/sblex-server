import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sblex.saldo_ws import config, routes
from sblex.sblex_server import server

logger = logging.getLogger(__name__)


def create_saldo_ws_server(*, settings: config.SaldoWsSettings) -> FastAPI:
    # app_context, env = main.bootstrap_app(env=env, config=config)

    logger.debug("creating app")
    webapp = server.create_sblex_server(title="Saldo WS", settings=settings)

    webapp.include_router(routes.router)
    webapp.mount("/static", StaticFiles(directory="static"), name="static")

    return webapp
