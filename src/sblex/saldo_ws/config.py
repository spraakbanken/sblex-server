import typing
from pathlib import Path

from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

from sblex.telemetry.settings import OTelSettings


class AppSettings(BaseModel):
    base_url: typing.Optional[str] = None
    root_path: str = ""
    template_directory: str = "templates"
    # model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class MatomoSettings(BaseModel):
    matomo_url: typing.Optional[str] = None
    matomo_idsite: typing.Optional[int] = None
    matomo_token: typing.Optional[str] = None
    # model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="TRACKING_")

    @model_validator(mode="after")
    def check_idsite_is_set_if_url_is_set(self) -> Self:
        url = self.matomo_url
        idsite = self.matomo_idsite

        if url is not None and (idsite is None or not isinstance(idsite, int)):
            raise ValueError(f"MATOMO_IDSITE must be an INT, got: '{idsite}' ({type(idsite)})")
        return self


class FrontendSettings(BaseModel):
    tracking: MatomoSettings = MatomoSettings()


class FmBinSettings(BaseModel):
    path: Path
    locale: str | None = None


class Settings(BaseSettings):
    semantic_path: str
    fm_server_url: str
    fm_bin: FmBinSettings
    korp_url: str = "https://spraakbanken.gu.se/korp"
    otel: OTelSettings
    app: AppSettings = AppSettings()
    frontend: FrontendSettings = FrontendSettings()
    tracking: MatomoSettings
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__", env_prefix="SALDO_WS__"
    )


def read_settings_from_env() -> Settings:
    otel = OTelSettings(_env_prefix="SALDO_WS__")  # type: ignore
    return Settings(otel=otel)  # type: ignore
