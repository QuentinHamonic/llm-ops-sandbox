from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from app.config import get_settings
from app.llm import LLMBackendError, build_backend
from app.metrics import LLM_REQUEST_COUNT, MetricsMiddleware, metrics_response

app = FastAPI(
    title="LLM Ops Sandbox",
    version="0.4.0",
    summary="API locale pour experimenter une stack LLM Ops observable.",
    description=(
        "LLM Ops Sandbox expose une API FastAPI minimale avec un backend LLM mock "
        "par defaut, un backend Ollama optionnel et des metriques Prometheus. "
        "Le projet privilegie la reproductibilite, l'observabilite et la confidentialite."
    ),
)
app.add_middleware(MetricsMiddleware)


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=4000,
        description="Message utilisateur envoye au backend LLM configure.",
        examples=["Bonjour, explique moi le role du backend mock."],
    )


class ChatResponse(BaseModel):
    reply: str = Field(
        description="Reponse generee par le backend LLM.",
        examples=["Mock reply: the local API is running. Received 42 characters."],
    )
    backend: str = Field(
        description="Backend utilise pour produire la reponse.",
        examples=["mock"],
    )


class BackendStatusResponse(BaseModel):
    backend: str = Field(description="Backend configure.", examples=["mock"])
    available: bool = Field(description="Disponibilite observee du backend.")
    model: str = Field(
        description="Modele configure ou nom logique du backend.",
        examples=["mistral:latest"],
    )
    detail: str = Field(description="Diagnostic court sans prompt, reponse ou secret.")


@app.get(
    "/health",
    tags=["Health"],
    summary="Verifier que l'API est vivante",
    description=(
        "Retourne un statut simple pour les humains, Docker Compose et les futurs probes "
        "Kubernetes. Ce endpoint ne contacte pas activement un backend LLM externe."
    ),
)
async def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "llm-ops-sandbox",
        "llm_backend": settings.llm_backend,
    }


@app.post(
    "/chat",
    response_model=ChatResponse,
    tags=["Chat"],
    summary="Envoyer un message au backend LLM configure",
    description=(
        "Utilise le backend `mock` par defaut pour garantir une demo stable. "
        "Si `LLM_BACKEND=ollama`, l'API appelle Ollama et retourne `502` si le backend "
        "ne repond pas correctement."
    ),
    responses={
        422: {"description": "Requete invalide, par exemple message vide ou absent."},
        502: {"description": "Backend LLM configure indisponible ou reponse inutilisable."},
    },
)
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


@app.get(
    "/backend/status",
    response_model=BackendStatusResponse,
    tags=["Backend"],
    summary="Verifier le statut non-generatif du backend LLM",
    description=(
        "Retourne un diagnostic court du backend configure. Pour Ollama, ce endpoint verifie "
        "`/api/tags` sans envoyer de prompt utilisateur au modele."
    ),
)
async def backend_status() -> BackendStatusResponse:
    settings = get_settings()
    backend = build_backend(settings)
    try:
        status = await backend.status()
    except LLMBackendError as exc:
        return BackendStatusResponse(
            backend=backend.name,
            available=False,
            model=settings.ollama_model if backend.name == "ollama" else backend.name,
            detail=str(exc),
        )

    return BackendStatusResponse(
        backend=status.name,
        available=status.available,
        model=status.model,
        detail=status.detail,
    )


@app.get(
    "/metrics",
    tags=["Observability"],
    summary="Exposer les metriques Prometheus",
    description=(
        "Expose les compteurs et histogrammes Prometheus. Les labels doivent rester bornes "
        "et ne jamais contenir les prompts, reponses, secrets ou identifiants utilisateur."
    ),
    response_class=PlainTextResponse,
    responses={
        200: {
            "description": "Metriques Prometheus au format texte.",
            "content": {
                "text/plain": {
                    "example": "# HELP http_requests_total Total HTTP requests.\n"
                    "# TYPE http_requests_total counter\n"
                }
            },
        }
    },
)
async def metrics():
    return metrics_response()
