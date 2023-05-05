from logging.config import dictConfig

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def setting_otlp(app: FastAPI, app_name: str, *, log_correlation: bool = True) -> None:
    resource = Resource.create(
        attributes={
            "service.name": app_name,
            "compose_service": app_name,
        }
    )

    # set the tracer provider
    tracer = TracerProvider(resource=resource)
    tracer.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(tracer)

    if log_correlation:
        LoggingInstrumentor().instrument(set_logging_format=False)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)


def configure_logging(settings: dict[str, str], *, use_telemetry: bool = True) -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            # "filters": {
            #     "correlation_id": {
            #         "()": asgi_correlation_id.CorrelationIdFilter,
            #         "uuid_length": 32,
            #     }
            # },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "format": "%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)d [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] %(message)s",
                },
                "json": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(name)s %(process)d %(funcName)s %(lineno)d %(message)s %(otelTraceID)s %(otelSpanID)s %(otelServiceName)s",
                },
                "standard": {
                    "format": "%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s",
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
                "uvicorn.access": {"handlers": ["json"], "level": "INFO"},
            },
        }
    )
