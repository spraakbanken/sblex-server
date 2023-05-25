import environs
from fastapi import FastAPI
from sblex import main
from sblex.fm_server import api, tasks


def create_fm_server(
    *,
    env: environs.Env | None = None,
    config: dict[str, str] | None = None,
    use_telemetry: bool = True
) -> FastAPI:
    app_context = main.bootstrap_app(
        env=env, config=config, use_telemetry=use_telemetry
    )

    app = FastAPI(title="FM-Server", redoc_url="/")

    app.state.app_context = app_context
    app.state.config = app_context.settings

    tasks.load_morphology(app)

    if use_telemetry:
        main.telemetry.setting_otlp(app, "fm-server")

    app.include_router(api.router)

    return app
