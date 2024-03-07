import logging
import sys
from logging.config import dictConfig
from typing import Optional, Tuple

import environs
from opentelemetry import trace
from opentelemetry._logs import (
    SeverityNumber,
    get_logger,
    get_logger_provider,
    set_logger_provider,
    std_to_otel,
)
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter as OTLPLogExporterGRPC,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterGRPC,
)
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    OTLPLogExporter as OTLPLogExporterHTTP,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterHTTP,
)
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    ConsoleLogExporter,
    SimpleLogRecordProcessor,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

logger = logging.getLogger(__name__)


def init_otel_tracing(
    app_name: str,
    *,
    env: environs.Env,
) -> None:
    resource = detect_resource(env, fallback_name=app_name)
    logger.debug("otel::setup", extra={"OTEL_RESOURCE": Resource})
    # set the tracer provider
    tracer = init_tracer(resource=resource, env=env)

    trace.set_tracer_provider(tracer)

    # if log_correlation:
    #     LoggingInstrumentor(log_level=logging.INFO).instrument(set_logging_format=False)


# The default Otel SDK completely ignores formatters when outputting the message being logged.
# We overcome this by creating our own LoggingHandler class which respects formatters.
class FormattedLoggingHandler(LoggingHandler):
    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        record.msg = msg
        record.args = None
        self._logger.emit(self._translate(record))


def init_otel_logging(*, env: environs.Env) -> None:
    log_level_str = env("OTEL_PYTHON_LOG_LEVEL", "INFO").upper()
    match log_level_str:
        case "CRITICAL":
            log_level = logging.CRITICAL
            print_err(f"Using log level: CRITICAL / {log_level}")
        case "ERROR":
            log_level = logging.ERROR
            print_err(f"Using log level: ERROR / {log_level}")
        case "WARNING":
            log_level = logging.WARNING
            print_err(f"Using log level: WARNING / {log_level}")
        case "INFO":
            log_level = logging.INFO
            print_err(f"Using log level: INFO / {log_level}")
        case "DEBUG":
            log_level = logging.DEBUG
            print_err(f"Using log level: DEBUG / {log_level}")
        case _:
            log_level = logging.INFO
            print_err(f"Using log level: NOTSET / {log_level}")

    logger_provider = LoggerProvider(resource=detect_resource(env))
    set_logger_provider(logger_provider)

    if env.bool("DEBUG_LOG_OTEL_TO_CONSOLE", False):
        console_log_exporter = ConsoleLogExporter()
        logger_provider.add_log_record_processor(SimpleLogRecordProcessor(console_log_exporter))
    if env.bool("DEBUG_LOG_OTEL_TO_PROVIDER", False):
        (maybe_protocol, maybe_endpoint) = read_logs_protocol_and_endpoint_from_env(env)
        (protocol, endpoint) = infer_protocol_and_endpoint(maybe_protocol, maybe_endpoint)
        headers = read_logs_headers_from_env(env)
        match protocol:
            case "grpc":
                otel_log_exporter = OTLPLogExporterGRPC(endpoint=endpoint, headers=headers)
            case "http":
                otel_log_exporter = OTLPLogExporterHTTP(endpoint=endpoint, headers=headers)
            case _:
                print_err(
                    f"Unknown OTEL_EXPORTER_LOGS_EXPORTER_PROTOCOL '{protocol}'. Using 'grpc' ..."
                )
                otel_log_exporter = OTLPLogExporterGRPC(endpoint=endpoint, headers=headers)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(otel_log_exporter))

    otel_log_handler = FormattedLoggingHandler(logger_provider=logger_provider, level=log_level)

    # This has to be called first before logger.getLogger().addHandler() so that it can call logging.basicConfig first to set the logging format
    # based on the environment variable OTEL_PYTHON_LOG_FORMAT
    LoggingInstrumentor(log_level=log_level).instrument()
    logFormatter = logging.Formatter(env("OTEL_PYTHON_LOG_FORMAT", None))
    otel_log_handler.setFormatter(logFormatter)
    logging.getLogger().addHandler(otel_log_handler)


def print_err(msg: str) -> None:
    print(msg, file=sys.stderr)


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
    (protocol, endpoint) = infer_protocol_and_endpoint(maybe_protocol, maybe_endpoint)
    logger.debug(
        "otel::setup",
        extra={
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT": endpoint,
            "OTEL_EXPORTER_OTLP_TRACES_PROTOCOL": protocol,
        },
    )
    tracer = TracerProvider(resource=resource)
    if env.bool("DEBUG_LOG_OTEL_TO_CONSOLE", False):
        tracer.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    if env.bool("DEBUG_LOG_OTEL_TO_PROVIDER", False):
        headers = read_traces_headers_from_env(env)
        match protocol:
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


def read_logs_protocol_and_endpoint_from_env(
    env: environs.Env,
) -> Tuple[Optional[str], Optional[str]]:
    maybe_endpoint = env("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT", None) or env(
        "OTEL_EXPORTER_OTLP_ENDPOINT", None
    )
    maybe_protocol = env("OTEL_EXPORTER_OTLP_LOGS_PROTOCOL", None) or env(
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


def read_logs_headers_from_env(
    env: environs.Env,
) -> dict[str, str]:
    headers = read_otel_headers_from_env(env)
    headers.update(parse_headers(env("OTEL_EXPORTER_LOGS_HTTP_HEADERS", "")))
    return headers


def infer_protocol_and_endpoint(
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
