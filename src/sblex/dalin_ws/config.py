from pydantic_settings import SettingsConfigDict
from sblex.fm_server.config import Settings
from sblex.telemetry.settings import OTelSettings


class DalinWsSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__", env_prefix="DALIN_WS__"
    )


def read_settings_from_env() -> DalinWsSettings:
    otel = OTelSettings(_env_prefix="DALIN_WS__")
    return DalinWsSettings(otel=otel)
