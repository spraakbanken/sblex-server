from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from sblex.webapp import routes


def create_webapp() -> FastAPI:
    webapp = FastAPI()

    webapp.state.templates = Jinja2Templates(directory="templates")

    webapp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    webapp.include_router(routes.router)

    return webapp
