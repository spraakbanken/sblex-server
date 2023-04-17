import os
from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sblex.webapp import routes, tasks, telemetry

from sblex.webapp import routes


def create_webapp() -> FastAPI:
    webapp = FastAPI()
    if not config:
        config = load_config()

    webapp.state.templates = Jinja2Templates(directory="templates")

    telemetry.setting_otlp(webapp, "sblex-server")

    webapp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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
