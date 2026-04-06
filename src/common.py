from fastapi import FastAPI
from .config import TEMPO
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider


def initialize_app(this):
    otlp_exporter = OTLPSpanExporter(TEMPO)
    tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: this}))
    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    set_tracer_provider(tracer_provider)

    app = FastAPI()
    FastAPIInstrumentor.instrument_app(app)

    HTTPXClientInstrumentor().instrument()

    @app.get("/")
    async def root():
        return {"message": "Hello World", "this": this}

    return app