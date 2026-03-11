from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor, ConsoleSpanExporter)
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
import time

# identify the service
resource = Resource.create({
    SERVICE_NAME: "flask-backend"
})

provider = TracerProvider(resource=resource)
# create exporter (prints spans to terminal)
exporter = ConsoleSpanExporter()
# create span processor
processor = BatchSpanProcessor(exporter)

otlp_exporter = OTLPSpanExporter(endpoint="localhost:4319", insecure=True)
processor = BatchSpanProcessor(otlp_exporter)

# connect processor to provider
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)


# ========== METRICS SETUP ==========
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(
        endpoint="localhost:4319",  # Same endpoint, different signal
        insecure=True
    ),
    export_interval_millis=5000  # Export every 5 seconds
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Get meter for creating metrics
meter = metrics.get_meter(__name__)

# ========== METRIC INSTRUMENTS ==========

# Counter: Total HTTP requests
http_requests_total = meter.create_counter(
    name="http_requests_total",
    description="Total number of HTTP requests",
    unit="1"
)

# Counter: Total HTTP errors
http_errors_total = meter.create_counter(
    name="http_errors_total",
    description="Total number of HTTP errors",
    unit="1"
)

# Histogram: Request duration
http_request_duration_seconds = meter.create_histogram(
    name="http_request_duration_seconds",
    description="HTTP request duration in seconds",
    unit="s"
)

# UpDownCounter: Active requests (concurrent)
http_active_requests = meter.create_up_down_counter(
    name="http_active_requests",
    description="Number of active HTTP requests",
    unit="1"
)

# Custom business metrics
activities_created_total = meter.create_counter(
    name="activities_created_total",
    description="Total number of activities created",
    unit="1"
)

messages_sent_total = meter.create_counter(
    name="messages_sent_total",
    description="Total number of messages sent",
    unit="1"
)


print("✅ Tracing and Metrics initialized")
print(f"   Traces → localhost:4319")
print(f"   Metrics → localhost:4319")