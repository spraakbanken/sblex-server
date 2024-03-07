import logging
from logging.config import dictConfig
from typing import Optional, Tuple

import environs
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterGRPC,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterHTTP,
)
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

logger = logging.getLogger(__name__)


def init_telemetry(
    app_name: str,
    *,
    env: environs.Env,
    log_correlation: bool = True,
) -> None:
    resource = detect_resource(env, fallback_name=app_name)
    logger.debug("otel::setup", extra={"OTEL_RESOURCE": Resource})
    # set the tracer provider
    tracer = init_tracer(resource=resource, env=env)

    trace.set_tracer_provider(tracer)

    if log_correlation:
        LoggingInstrumentor(log_level=logging.INFO).instrument(set_logging_format=False)


def detect_resource(env: environs.Env, *, fallback_name: str | None = None) -> Resource:
    service_name = (
        env("OTEL_SERVICE_NAME", None)
        or env("SERVICE_NAME", None)
        or env("APP_NAME", None)
        or fallback_name
        or "unknown"
    )
    return Resource.create(
        attributes={
            "service.name": service_name,
            "compose_service": service_name,
        }
    )


def configure_logging(settings: dict[str, str]) -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            # "filters": {
            #     "correlation_id": {
            #         "()": asgi_correlation_id.CorrelationIdFilter,
            #         "uuid_length": 32,
            #     }
            # },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "format": "%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)d [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] %(message)s",  # noqa: E501
                },
                "json": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(name)s %(process)d %(funcName)s %(lineno)d %(message)s %(otelTraceID)s %(otelSpanID)s %(otelServiceName)s",  # noqa: E501
                },
                "standard": {
                    "format": "%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s",  # noqa: E501
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    # "filters": ["correlation_id"],
                    "formatter": "console",
                    "stream": "ext://sys.stderr",
                },
                "json": {
                    "class": "logging.StreamHandler",
                    # "filters": ["correlation_id"],
                    "formatter": "json",
                },
            },
            "loggers": {
                "sblex": {
                    "handlers": ["json"],
                    "level": "DEBUG",
                    "propagate": True,
                },
                # third-party package loggers
                # "sqlalchemy": {"handlers": ["json"], "level": "WARNING"},
                "asgi_matomo": {
                    "handlers": ["json"],
                    "level": "DEBUG",
                    "propagate": True,
                },
                "uvicorn.access": {"handlers": ["json"], "level": "INFO"},
            },
        }
    )


def init_tracer(resource: Resource, env: environs.Env) -> TracerProvider:
    (maybe_protocol, maybe_endpoint) = read_traces_protocol_and_endpoint_from_env(env)
    (protocol, endpoint) = infer_traces_protocol_and_endpoint(maybe_protocol, maybe_endpoint)
    logger.debug(
        "otel::setup",
        extra={
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT": endpoint,
            "OTEL_EXPORTER_OTLP_TRACES_PROTOCOL": protocol,
        },
    )
    tracer = TracerProvider(resource=resource)
    headers = read_traces_headers_from_env(env)
    match protocol:
        case "stdout":
            tracer.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
        case "http":
            tracer.add_span_processor(
                BatchSpanProcessor(OTLPSpanExporterHTTP(endpoint=endpoint, headers=headers))
            )
        case "grpc":
            tracer.add_span_processor(
                BatchSpanProcessor(OTLPSpanExporterGRPC(endpoint=endpoint, headers=headers))
            )
        case _:
            logger.warn("unknown OTLP_PROTOCOL='%s', using grpc", protocol)
            tracer.add_span_processor(
                BatchSpanProcessor(OTLPSpanExporterGRPC(endpoint=endpoint, headers=headers))
            )
    return tracer


def read_traces_protocol_and_endpoint_from_env(
    env: environs.Env,
) -> Tuple[Optional[str], Optional[str]]:
    maybe_endpoint = env("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", None) or env(
        "OTEL_EXPORTER_OTLP_ENDPOINT", None
    )
    maybe_protocol = env("OTEL_EXPORTER_OTLP_TRACES_PROTOCOL", None) or env(
        "OTEL_EXPORTER_OTLP_PROTOCOL", None
    )
    return maybe_protocol, maybe_endpoint


def read_otel_headers_from_env(env: environs.Env) -> dict[str, str]:
    return parse_headers(env("OTEL_EXPORTER_HTTP_HEADERS", ""))


def parse_headers(headers_as_str: str) -> dict[str, str]:
    headers = {}
    if not headers_as_str:
        return headers
    key_values = headers_as_str.split(",")
    for key_value in key_values:
        key, value = key_value.split("=")
        headers[key] = value
    return headers


def read_traces_headers_from_env(
    env: environs.Env,
) -> dict[str, str]:
    headers = read_otel_headers_from_env(env)
    headers.update(parse_headers(env("OTEL_EXPORTER_TRACES_HTTP_HEADERS", "")))
    return headers


def infer_traces_protocol_and_endpoint(
    maybe_protocol: Optional[str], maybe_endpoint: Optional[str]
) -> Tuple[str, str]:
    if maybe_protocol is not None:
        protocol = maybe_protocol
    elif maybe_endpoint and ":4317" in maybe_endpoint:
        protocol = "grpc"
    elif maybe_endpoint is None:
        protocol = "stdout"
    else:
        protocol = "http"

    match protocol:
        case "http":
            endpoint = maybe_endpoint or "http://localhost:4318"
        case "stdout":
            endpoint = "stdout"
        case _:
            endpoint = maybe_endpoint or "http://localhost:4317"
    return protocol, endpoint
