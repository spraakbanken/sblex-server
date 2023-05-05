import logging
import os
from typing import Any

import environs
from asgi_matomo import MatomoMiddleware
from brotli_asgi import BrotliMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sblex import main
from sblex.webapp import routes, tasks

logger = logging.getLogger(__name__)


def create_webapp(
    *,
    env: environs.Env | None = None,
    config: dict | None = None,
    use_telemetry: bool = True
) -> FastAPI:
    app_context = main.bootstrap_app(
        env=env, config=config, use_telemetry=use_telemetry
    )

    webapp = FastAPI()

    webapp.state.app_context = app_context
    webapp.state.config = app_context.settings
    # Configure templates
    webapp.state.templates = Jinja2Templates(directory="templates")

    if use_telemetry:
        main.telemetry.setting_otlp(webapp, "sblex-server")

    webapp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if webapp.state.config["tracking.matomo.url"]:
        webapp.add_middleware(
            MatomoMiddleware,
            idsite=webapp.state.config["tracking.matomo.idsite"],
            matomo_url=webapp.state.config["tracking.matomo.url"],
            access_token=webapp.state.config["tracking.matomo.token"],
        )
    else:
        logger.warning(
            "Tracking to Matomo is not enabled, please set TRACKING_MATOMO_URL and TRACKING_MATOMO_IDSITE."
        )
    webapp.add_middleware(BrotliMiddleware, gzip_fallback=True)

    webapp.add_event_handler("startup", tasks.create_start_app_handler(webapp))

    webapp.include_router(routes.router)

    return webapp


def load_config() -> dict[str, Any]:
    load_dotenv(".env", verbose=True)
    config = {
        "MORPHOLOGY_PATH": os.environ.get(
            "MORPHOLOGY_PATH", "assets/testing/saldo.lex"
        ),
        "SEMANTIC_PATH": os.environ.get("SEMANTIC_PATH", "assets/testing/saldo.txt"),
    }

    return config
