from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from sblex.dalin_ws import routes
from sblex.sblex_server.shared import version_info


def create_dalin_ws_server() -> FastAPI:
    webapp = FastAPI(
        title="Dalin WS",
        version=version_info.get_version(),
        default_response_class=ORJSONResponse,
    )

    webapp.include_router(routes.router)
    webapp.mount("/static", StaticFiles(directory="static"), name="static")

    return webapp
