from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class OTelSettings(BaseSettings):
    debug_log_otel_to_console: bool = False
    debug_log_otel_to_provider: bool = False
    otel_exporter_otlp_endpoint: Optional[str] = None
    otel_exporter_otlp_headers: str = ""
    otel_exporter_otlp_logs_endpoint: Optional[str] = None
    otel_exporter_otlp_logs_headers: str = ""
    otel_exporter_otlp_logs_protocol: Optional[str] = None
    otel_exporter_otlp_protocol: Optional[str] = None
    otel_exporter_otlp_traces_endpoint: Optional[str] = None
    otel_exporter_otlp_traces_headers: str = ""
    otel_exporter_otlp_traces_protocol: Optional[str] = None
    otel_python_log_format: Optional[str] = None
    otel_python_log_level: Optional[str] = None
    otel_service_instance_id: Optional[str] = None
    otel_service_name: str
    otel_service_namespace: Optional[str] = None
    otel_service_version: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
