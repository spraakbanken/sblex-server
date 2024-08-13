from pydantic_settings import SettingsConfigDict

from sblex.sblex_server.settings import Settings
from sblex.telemetry.settings import OTelSettings


class SaldoWsSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__", env_prefix="SALDO_WS__"
    )


def read_settings_from_env() -> SaldoWsSettings:
    otel = OTelSettings(_env_prefix="SALDO_WS__")
    return SaldoWsSettings(otel=otel)
