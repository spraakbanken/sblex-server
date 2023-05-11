import logging
import os
from dataclasses import dataclass
from typing import Optional, TypedDict

import environs
from sblex.main import telemetry

Settings = TypedDict(
    "Settings",
    {
        "morphology.path": str,
        "semantic.path": str,
        "tracking.matomo.url": Optional[str],
        "tracking.matomo.idsite": Optional[str],
        "tracking.matomo.token": Optional[str],
        "tracking.matomo.frontend.base_url": Optional[str],
        "tracking.matomo.frontend.site_id": Optional[str],
    },
)


logger = logging.getLogger(__name__)


@dataclass
class AppContext:
    settings: Settings


def bootstrap_app(
    *,
    env: environs.Env | None = None,
    config: dict[str, str] | None = None,
    use_telemetry: bool = True
) -> AppContext:
    if env is None:
        env = load_env()
    if config is None:
        config = {}

    settings: Settings = {
        "morphology.path": config.get("morphology.path")
        or env("MORPHOLOGY_PATH", "assets/testing/saldo.lex"),
        "semantic.path": config.get("semantic.path")
        or env("SEMANTIC_PATH", "assets/testing/saldo.txt"),
        "tracking.matomo.url": config.get("tracking.matomo.url")
        or env("TRACKING_MATOMO_URL", None),
        "tracking.matomo.idsite": config.get("tracking.matomo.idsite")
        or env("TRACKING_MATOMO_IDSITE", None),
        "tracking.matomo.token": config.get("tracking.matomo.token")
        or env("TRACKING_MATOMO_TOKEN", None),
        "tracking.matomo.frontend.base_url": config.get("tracking.matomo.base_url")
        or env("TRACKING_MATOMO_FRONTEND_BASEURL", None),
        "tracking.matomo.frontend.site_id": config.get("tracking.matomo.base_url")
        or env("TRACKING_MATOMO_FRONTEND_SITEID", None),
    }

    telemetry.configure_logging(config, use_telemetry=use_telemetry)
    logger.warning("loaded settings", extra={"settings": settings})

    return AppContext(settings=settings)


def load_env() -> environs.Env:
    config_path = os.environ.get("CONFIG_PATH", ".env")
    env = environs.Env()
    env.read_env(config_path)
    return env
