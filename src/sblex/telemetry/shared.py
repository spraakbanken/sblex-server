from typing import Sequence

from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

from sblex.telemetry.settings import OTelSettings

DEFAULT_HTTP_ENDPOINT = "http://localhost:4318/"
DEFAULT_GRPC_ENDPOINT = "http://localhost:4317/"
DEFAULT_LOGS_EXPORT_PATH = "v1/logs"
DEFAULT_TRACES_EXPORT_PATH = "v1/traces"


def detect_resource(settings: OTelSettings, *, fallback_name: str | None = None) -> Resource:
    service_name = settings.otel_service_name or fallback_name or "unknown"
    attributes: dict[
        str,
        str
        | bool
        | int
        | float
        | Sequence[str]
        | Sequence[bool]
        | Sequence[int]
        | Sequence[float],
    ] = {
        ResourceAttributes.SERVICE_NAME: service_name,
        "compose_service": service_name,
    }
    if service_version := settings.otel_service_version:
        attributes[ResourceAttributes.SERVICE_VERSION] = service_version
    if service_namespace := settings.otel_service_namespace:
        attributes[ResourceAttributes.SERVICE_NAMESPACE] = service_namespace
    if service_instance_id := settings.otel_service_instance_id:
        attributes[ResourceAttributes.SERVICE_INSTANCE_ID] = service_instance_id
    return Resource.create(attributes=attributes)


def read_otel_headers_from_settings(settings: OTelSettings) -> dict[str, str]:
    return parse_headers(settings.otel_exporter_otlp_headers)


def parse_headers(headers_as_str: str) -> dict[str, str]:
    headers: dict[str, str] = {}
    if not headers_as_str:
        return headers
    key_values = headers_as_str.split(",")
    for key_value in key_values:
        key, value = key_value.split("=")
        headers[key] = value
    return headers
