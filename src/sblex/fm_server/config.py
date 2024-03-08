from pydantic_settings import BaseSettings, SettingsConfigDict
from sblex.telemetry import OTelSettings


class Settings(BaseSettings):
    morphology_path: str
    otel: OTelSettings = OTelSettings()
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def read_settings_from_env() -> Settings:
    otel = OTelSettings(_env_prefix="FM_SERVER_")
    settings = Settings(otel=otel)
    return settings
