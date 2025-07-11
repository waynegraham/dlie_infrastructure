from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.resources import router as resources_router
from api.routers.exhibits import router as exhibits_router
from api.routers.search import router as search_router
from api.routers.summary import router as summary_router
from api.graphql_router import graphql_app

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

app = FastAPI(
    title="Digital Library of Integral Ecology API",
    version="0.3.0",
    description="API for the DLIE project",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for the frontend at localhost:3000
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000", "http://localhost:3001"],  # or ["*"] in dev
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(resources_router)
app.include_router(exhibits_router)
app.include_router(search_router)
app.include_router(summary_router)

# GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")


@app.get("/healthz", tags=["observability"])
def healthz():
    """Liveness endpoint."""
    return {"status": "ok"}


@app.get("/readyz", tags=["observability"])
def readyz():
    """Readiness endpoint."""
    return {"status": "ok"}


@app.get("/metrics", tags=["observability"])
def metrics():
    """Prometheus metrics endpoint."""
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
