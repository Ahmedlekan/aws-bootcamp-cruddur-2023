from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor, ConsoleSpanExporter)
from opentelemetry.sdk.resources import Resource

# identify the service
resource = Resource.create({
    "service.name": "flask-backend"
})

provider = TracerProvider(resource=resource)
# create exporter (prints spans to terminal)
exporter = ConsoleSpanExporter()
# create span processor
processor = BatchSpanProcessor(exporter)

otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
processor = BatchSpanProcessor(otlp_exporter)

# connect processor to provider
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)

