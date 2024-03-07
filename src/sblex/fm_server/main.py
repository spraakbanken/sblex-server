import logging

import environs
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from sblex import main
from sblex.fm_server import api, tasks
from sblex.main import telemetry

logger = logging.getLogger(__name__)


def create_fm_server(
    *,
    env: environs.Env | None = None,
    config: dict[str, str] | None = None,
) -> FastAPI:
    app_context, env = main.bootstrap_app(env=env, config=config)

    telemetry.init_otel_logging(env=env)
    logger.warning("loaded settings", extra={"settings": app_context.settings})
    logger.debug("loading telemetry")
    telemetry.init_otel_tracing("fm-server", env=env)
    app = FastAPI(title="FM-Server", redoc_url="/")

    app.state.app_context = app_context
    app.state.config = app_context.settings

    tasks.load_morphology(app)

    FastAPIInstrumentor.instrument_app(app)
    app.include_router(api.router)

    return app
