import logging

import environs
from asgi_matomo import MatomoMiddleware
from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from sblex import main
from sblex.main import telemetry
from sblex.webapp import routes, tasks, templating

logger = logging.getLogger(__name__)


def create_webapp(
    *,
    env: environs.Env | None = None,
    config: dict | None = None,
    use_telemetry: bool = True,
) -> FastAPI:
    app_context, env = main.bootstrap_app(env=env, config=config)

    if use_telemetry:
        logger.debug("loading telemetry")
        telemetry.init_telemetry("sblex-server", env=env)
    HTTPXClientInstrumentor().instrument()

    logger.debug("creating app")
    webapp = FastAPI(
        title="Saldo WS",
        version=main.get_version(),
        openapi_url=f"{app_context.settings['webapp.root_path']}/openapi.json",
        docs_url=None,
        redoc_url="/",
        root_path=app_context.settings["webapp.root_path"],
        lifespan=tasks.lifespan,
    )  # , lifespan=lifespan)

    webapp.state.app_context = app_context
    webapp.state.config = app_context.settings

    # Configure templates
    webapp.state.templates = templating.init_template_engine(app_context.settings)

    # Add middlewares (in reverse order)
    webapp.add_middleware(BrotliMiddleware, gzip_fallback=True)

    webapp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if webapp.state.config["tracking.matomo.url"]:
        logger.info("adding MatomoMiddleware")
        webapp.add_middleware(
            MatomoMiddleware,
            idsite=webapp.state.config["tracking.matomo.idsite"],
            matomo_url=webapp.state.config["tracking.matomo.url"],
            access_token=webapp.state.config["tracking.matomo.token"],
            exclude_patterns=[".*/html.*"],
        )
    else:
        logger.warning(
            "NOT tracking to Matomo, please set TRACKING_MATOMO_URL and TRACKING_MATOMO_IDSITE."
        )

    FastAPIInstrumentor.instrument_app(webapp)

    webapp.include_router(routes.router)
    webapp.mount("/static", StaticFiles(directory="static"), name="static")

    return webapp
