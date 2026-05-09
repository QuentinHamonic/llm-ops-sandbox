from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.config import get_settings
from app.llm import LLMBackendError, build_backend
from app.metrics import LLM_REQUEST_COUNT, MetricsMiddleware, metrics_response

app = FastAPI(title="LLM Ops Sandbox", version="0.1.0")
app.add_middleware(MetricsMiddleware)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    reply: str
    backend: str


@app.get("/health")
async def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "llm-ops-sandbox",
        "llm_backend": settings.llm_backend,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    settings = get_settings()
    backend = build_backend(settings)
    try:
        reply = await backend.generate(payload.message)
    except LLMBackendError as exc:
        LLM_REQUEST_COUNT.labels(backend.name, "error").inc()
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    LLM_REQUEST_COUNT.labels(backend.name, "success").inc()
    return ChatResponse(reply=reply, backend=backend.name)


@app.get("/metrics")
async def metrics():
    return metrics_response()
