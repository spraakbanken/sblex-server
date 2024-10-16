import logging

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from sblex import telemetry
from sblex.fm_server import api, config, tasks

logger = logging.getLogger(__name__)


def create_fm_server(*, settings: config.Settings) -> FastAPI:
    # app_context, env = main.bootstrap_app(env=env, config=config)

    telemetry.init_otel_logging(settings.otel)
    logger.warning("loaded settings", extra={"settings": str(settings)})
    logger.debug("loading telemetry")
    telemetry.init_otel_tracing(settings.otel, fallback_name="fm-server")
    app = FastAPI(title="FM-Server", redoc_url="/")

    # app.state.app_context = app_context
    app.state.settings = settings

    tasks.load_morphology(app)

    FastAPIInstrumentor.instrument_app(app)
    app.include_router(api.router)

    return app
