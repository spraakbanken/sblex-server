import os
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sblex.webapp import routes, tasks, telemetry


def create_webapp(config: dict | None = None, *, use_telemetry: bool = True) -> FastAPI:
    webapp = FastAPI()
    if not config:
        config = load_config()

    webapp.state.config = config
    # Configure templates
    webapp.state.templates = Jinja2Templates(directory="templates")

    if use_telemetry:
        telemetry.setting_otlp(webapp, "sblex-server")

    webapp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    webapp.add_event_handler("startup", tasks.create_start_app_handler(webapp))

    webapp.include_router(routes.router)

    return webapp


def load_config() -> dict[str, Any]:
    load_dotenv(".env", verbose=True)
    return {
        "MORPHOLOGY_PATH": os.environ.get(
            "MORPHOLOGY_PATH", "assets/testing/saldo.lex"
        ),
        "SEMANTIC_PATH": os.environ.get("SEMANTIC_PATH", "assets/testing/saldo.txt"),
    }
