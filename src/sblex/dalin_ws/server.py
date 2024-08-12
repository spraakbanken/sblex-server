from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sblex.dalin_ws import routes


def create_dalin_ws_server() -> FastAPI:
    webapp = FastAPI(
        title="Dalin WS",
    )

    webapp.include_router(routes.router)
    webapp.mount("/static", StaticFiles(directory="static"), name="static")

    return webapp
