from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sblex.webapp.main import create_webapp


@pytest.fixture(name="webapp")
def fixture_webapp() -> FastAPI:
    return create_webapp(
        config={
            "semantic.path": "assets/testing/saldo.txt",
            "morphology.path": "assets/testing/saldo.lex",
        },
        use_telemetry=False,
    )


@pytest_asyncio.fixture
async def client(webapp: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(webapp):
        async with AsyncClient(app=webapp, base_url="http://testserver") as client:
            yield client
