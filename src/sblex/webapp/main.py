from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sblex.webapp import routes


def create_webapp() -> FastAPI:
    webapp = FastAPI()

    webapp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    webapp.include_router(routes.router)

    return webapp
