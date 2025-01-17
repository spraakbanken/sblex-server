import logging

from asgi_matomo import MatomoMiddleware
from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from sblex import telemetry
from sblex.saldo_ws import config, routes, tasks, templating
from sblex.saldo_ws.shared import version_info

logger = logging.getLogger(__name__)


def create_saldo_ws_server(*, settings: config.Settings) -> FastAPI:
    # app_context, env = main.bootstrap_app(env=env, config=config)

    telemetry.init_otel_logging(settings.otel)
    logger.warning("loaded settings", extra={"settings": str(settings)})
    logger.debug("loading telemetry")
    telemetry.init_otel_tracing(settings.otel, fallback_name="saldo-ws")
    HTTPXClientInstrumentor().instrument()

    logger.debug("creating app")
    webapp = FastAPI(
        title="Saldo WS",
        version=version_info.get_version(),
        # openapi_url=f"{settings.app.root_path}/openapi.json",
        docs_url=None,
        redoc_url="/",
        root_path=settings.app.root_path,
        lifespan=tasks.lifespan,
        default_response_class=ORJSONResponse,
    )  # , lifespan=lifespan)

    # webapp.state.app_context = app_context
    webapp.state.settings = settings

    # Configure templates
    webapp.state.templates = templating.init_template_engine(settings.app)

    # Add middlewares (in reverse order)
    webapp.add_middleware(BrotliMiddleware, gzip_fallback=True)

    webapp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if webapp.state.settings.tracking.matomo_url:
        if webapp.state.settings.tracking.matomo_idsite is None:
            logger.error("TRACKING_MATOMO_URL is set but not TRACKING_MATOMO_IDSITE")
        else:
            logger.info("adding MatomoMiddleware")
            webapp.add_middleware(
                MatomoMiddleware,  # type: ignore [arg-type]
                idsite=webapp.state.settings.tracking.matomo_idsite,  # type: ignore
                matomo_url=webapp.state.settings.tracking.matomo_url,
                access_token=webapp.state.settings.tracking.matomo_token,
                exclude_patterns=[".*/html.*"],
            )
    else:
        logger.warning(
            "NOT tracking to Matomo, please set TRACKING_MATOMO_URL and TRACKING_MATOMO_IDSITE."
        )

    FastAPIInstrumentor.instrument_app(webapp)

    webapp.include_router(routes.router)
    # Workaround for fastapi.staticfiles.StaticFiles not working,
    # added in saldo_ws.routes instead
    # webapp.mount("/static", StaticFiles(directory="static"), name="static")

    return webapp
