from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sblex.telemetry.settings import OTelSettings


class AppSettings(BaseModel):
    base_url: Optional[str] = None
    root_path: str = ""
    template_directory: str = "templates"
    # model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class MatomoSettings(BaseModel):
    matomo_url: Optional[str] = None
    matomo_idsite: Optional[int] = None
    matomo_token: Optional[str] = None
    # model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="TRACKING_")


class FrontendSettings(BaseModel):
    tracking: MatomoSettings = MatomoSettings()


class Settings(BaseSettings):
    semantic_path: str
    fm_server_url: str
    fm_server_url: str
    otel: OTelSettings
    app: AppSettings = AppSettings()
    frontend: FrontendSettings = FrontendSettings()
    tracking: MatomoSettings
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__", env_prefix="SALDO_WS__"
    )


def read_settings_from_env() -> Settings:
    otel = OTelSettings(_env_prefix="SALDO_WS_")
    settings = Settings(otel=otel)
    return settings
