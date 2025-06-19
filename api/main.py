# api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.resources import router as resources_router
from api.routers.exhibits import router as exhibits_router
from api.routers.search import router as search_router

app = FastAPI()

# Enable CORS for the frontend at localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(resources_router)
app.include_router(exhibits_router)
app.include_router(search_router)


@app.get("/healthz", tags=["observability"])
def healthz():
    """Liveness endpoint."""
    return {"status": "ok"}


@app.get("/readyz", tags=["observability"])
def readyz():
    """Readiness endpoint."""
    return {"status": "ok"}


from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

@app.get("/metrics", tags=["observability"])
def metrics():
    """Prometheus metrics endpoint."""
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)