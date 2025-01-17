from pydantic_settings import BaseSettings, SettingsConfigDict

from sblex.telemetry import OTelSettings


class Settings(BaseSettings):
    morphology_path: str
    otel: OTelSettings
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__", env_prefix="FM_SERVER__"
    )


def read_settings_from_env() -> Settings:
    otel = OTelSettings(_env_prefix="FM_SERVER__")  # type:ignore
    settings = Settings(otel=otel)  # type:ignore
    return settings
