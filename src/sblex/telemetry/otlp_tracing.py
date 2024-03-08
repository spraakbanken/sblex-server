import logging
from typing import Optional, Tuple

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterGRPC,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterHTTP,
)
from opentelemetry.sdk.environment_variables import (
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
    OTEL_EXPORTER_OTLP_TRACES_PROTOCOL,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from sblex.telemetry import shared
from sblex.telemetry.settings import OTelSettings

logger = logging.getLogger(__name__)


def init_otel_tracing(
    settings: OTelSettings,
    *,
    fallback_name: str,
) -> None:
    resource = shared.detect_resource(settings, fallback_name=fallback_name)
    logger.debug("otel::setup", extra={"OTEL_RESOURCE": Resource})
    # set the tracer provider
    tracer = init_tracer(resource=resource, settings=settings)

    trace.set_tracer_provider(tracer)

    # if log_correlation:
    #     LoggingInstrumentor(log_level=logging.INFO).instrument(set_logging_format=False)


def init_tracer(resource: Resource, settings: OTelSettings) -> TracerProvider:
    (maybe_protocol, maybe_endpoint) = read_traces_protocol_and_endpoint_from_settings(settings)
    (protocol, endpoint) = infer_traces_protocol_and_endpoint(maybe_protocol, maybe_endpoint)
    logger.debug(
        "otel::setup",
        extra={
            OTEL_EXPORTER_OTLP_TRACES_ENDPOINT: endpoint,
            OTEL_EXPORTER_OTLP_TRACES_PROTOCOL: protocol,
        },
    )
    tracer = TracerProvider(resource=resource)
    if settings.debug_log_otel_to_console:
        tracer.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    if settings.debug_log_otel_to_provider:
        headers = read_traces_headers_from_settings(settings)
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


def read_traces_protocol_and_endpoint_from_settings(
    settings: OTelSettings,
) -> Tuple[Optional[str], Optional[str]]:
    maybe_protocol = (
        settings.otel_exporter_otlp_traces_protocol or settings.otel_exporter_otlp_protocol
    )

    maybe_endpoint = settings.otel_exporter_otlp_traces_endpoint
    if not maybe_endpoint:
        maybe_endpoint = settings.otel_exporter_otlp_endpoint
        if maybe_protocol == "http":
            maybe_endpoint = _append_http_traces_path(
                maybe_endpoint or shared.DEFAULT_HTTP_ENDPOINT
            )

    return maybe_protocol, maybe_endpoint


def read_traces_headers_from_settings(
    settings: OTelSettings,
) -> dict[str, str]:
    headers = shared.read_otel_headers_from_settings(settings)
    headers.update(shared.parse_headers(settings.otel_exporter_otlp_traces_headers))
    return headers


def infer_traces_protocol_and_endpoint(
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
            endpoint = maybe_endpoint or _append_http_traces_path(shared.DEFAULT_HTTP_ENDPOINT)
        case _:
            endpoint = maybe_endpoint or shared.DEFAULT_GRPC_ENDPOINT
    return protocol, endpoint


def _append_http_traces_path(endpoint: str) -> str:
    if endpoint.endswith("/"):
        return endpoint + shared.DEFAULT_TRACES_EXPORT_PATH
    return endpoint + f"/{shared.DEFAULT_TRACES_EXPORT_PATH}"
