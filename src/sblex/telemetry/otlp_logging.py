import logging
import sys
from logging.config import dictConfig
from typing import Optional, Tuple

from opentelemetry._logs import (
    set_logger_provider,
)
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter as OTLPLogExporterGRPC,
)
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    OTLPLogExporter as OTLPLogExporterHTTP,
)
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    ConsoleLogExporter,
    SimpleLogRecordProcessor,
)

from sblex.telemetry import shared
from sblex.telemetry.settings import OTelSettings

logger = logging.getLogger(__name__)


def init_otel_logging(settings: OTelSettings) -> None:
    msg = "Using log level:"
    match settings.otel_python_log_level or "INFO":
        case "CRITICAL":
            log_level = logging.CRITICAL
            msg = f"{msg} CRITICAL / {log_level}"
        case "ERROR":
            log_level = logging.ERROR
            msg = f"{msg} ERROR / {log_level}"
        case "WARNING":
            log_level = logging.WARNING
            msg = f"{msg} WARNING / {log_level}"
        case "INFO":
            log_level = logging.INFO
            msg = f"{msg} INFO / {log_level}"
        case "DEBUG":
            log_level = logging.DEBUG
            msg = f"{msg} DEBUG / {log_level}"
        case _:
            log_level = logging.INFO
            msg = f"{msg} NOTSET / {log_level}"
    print(msg, file=sys.stderr)
    logger_provider = LoggerProvider(resource=shared.detect_resource(settings))
    set_logger_provider(logger_provider)

    if settings.debug_log_otel_to_console:
        console_log_exporter = ConsoleLogExporter()
        logger_provider.add_log_record_processor(SimpleLogRecordProcessor(console_log_exporter))
    if settings.debug_log_otel_to_provider:
        (maybe_protocol, maybe_endpoint) = read_logs_protocol_and_endpoint_from_settings(
            settings
        )
        (protocol, endpoint) = infer_logs_protocol_and_endpoint(maybe_protocol, maybe_endpoint)
        headers = read_logs_headers_from_settings(settings)
        print(f"{headers=}")
        match protocol:
            case "grpc":
                otel_log_exporter = OTLPLogExporterGRPC(endpoint=endpoint, headers=headers)
            case "http":
                otel_log_exporter = OTLPLogExporterHTTP(endpoint=endpoint, headers=headers)  # type: ignore [assignment]
            case _:
                print(
                    f"Unknown OTEL_EXPORTER_LOGS_EXPORTER_PROTOCOL '{protocol}'. Using 'grpc'",
                    file=sys.stderr,
                )
                otel_log_exporter = OTLPLogExporterGRPC(endpoint=endpoint, headers=headers)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(otel_log_exporter))

    otel_log_handler = LoggingHandler(logger_provider=logger_provider, level=log_level)

    # This has to be called first before logger.getLogger().addHandler()
    # so that it can call logging.basicConfig first to set the logging format
    # based on the environment variable OTEL_PYTHON_LOG_FORMAT
    LoggingInstrumentor(
        log_level=log_level,
    ).instrument()
    logFormatter = logging.Formatter(settings.otel_python_log_format)
    otel_log_handler.setFormatter(logFormatter)
    logging.getLogger().addHandler(otel_log_handler)


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


def read_logs_protocol_and_endpoint_from_settings(
    settings: OTelSettings,
) -> Tuple[Optional[str], Optional[str]]:
    maybe_protocol = (
        settings.otel_exporter_otlp_logs_protocol or settings.otel_exporter_otlp_protocol
    )
    maybe_endpoint = settings.otel_exporter_otlp_logs_endpoint
    if not maybe_endpoint:
        maybe_endpoint = settings.otel_exporter_otlp_endpoint
        if maybe_protocol == "http":
            maybe_endpoint = _append_http_logs_path(
                maybe_endpoint or shared.DEFAULT_HTTP_ENDPOINT
            )

    return maybe_protocol, maybe_endpoint


def read_logs_headers_from_settings(
    settings: OTelSettings,
) -> dict[str, str]:
    headers = shared.read_otel_headers_from_settings(settings)
    headers.update(shared.parse_headers(settings.otel_exporter_otlp_logs_headers))
    return headers


def infer_logs_protocol_and_endpoint(
    maybe_protocol: Optional[str], maybe_endpoint: Optional[str]
) -> Tuple[str, str]:
    if maybe_protocol is not None:
        protocol = maybe_protocol
    elif maybe_endpoint and ":4317" in maybe_endpoint:
        protocol = "grpc"
    else:
        protocol = "http"

    match protocol:
        case "http":
            endpoint = maybe_endpoint or _append_http_logs_path(shared.DEFAULT_HTTP_ENDPOINT)
        case _:
            endpoint = maybe_endpoint or shared.DEFAULT_GRPC_ENDPOINT
    return protocol, endpoint


def _append_http_logs_path(endpoint: str) -> str:
    if endpoint.endswith("/"):
        return endpoint + shared.DEFAULT_LOGS_EXPORT_PATH
    return endpoint + f"/{shared.DEFAULT_LOGS_EXPORT_PATH}"
