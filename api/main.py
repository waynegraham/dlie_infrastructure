# api/main.py

from fastapi import FastAPI, Depends, Query, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from api.database import SessionLocal, engine, Base
from api.models import ResourceModel, ExhibitModel
from api.schemas import (
    ResourceList,
    ResourceCreate,
    ResourceRead,
    ResourceSummary,
    ExhibitSummary,
    ExhibitRead,
    SearchResponse,
)
from api.solr_client import index_resource, delete_resource, search_resources

app = FastAPI()

# Enable CORS for the frontend at localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------
# Resource Endpoints
# --------------------------

@app.get("/resources", response_model=ResourceList)
def list_resources(
    limit: Optional[int] = Query(None, ge=1, title="Limit", description="Return up to this many most-recent resources"),
    page: int = Query(1, ge=1, title="Page", description="Page number for pagination (ignored if `limit` is set)"),
    page_size: int = Query(20, ge=1, le=100, title="Page Size", description="Number of items per page (ignored if `limit` is set)"),
    db: Session = Depends(get_db),
):
    total = db.query(func.count(ResourceModel.id)).scalar()
    query = db.query(ResourceModel)
    if limit is not None:
        items = query.order_by(ResourceModel.id.desc()).limit(limit).all()
        return ResourceList(total=total, page=1, page_size=limit, items=items)
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return ResourceList(total=total, page=page, page_size=page_size, items=items)


@app.get("/resources/{resource_id}", response_model=ResourceRead)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.get(ResourceModel, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@app.post("/resources", response_model=ResourceRead, status_code=201)
def create_resource(
    resource_in: ResourceCreate,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
):
    resource = ResourceModel(**resource_in.dict())
    db.add(resource)
    db.commit()
    db.refresh(resource)

    doc = {
        "id": str(resource.id),
        "title": resource.title,
        "abstract": resource.abstract,
        "authors": resource.authors,
        "date": resource.date.isoformat(),
        "provider": resource.provider,
        "keywords": resource.keywords,
        "fulltext": resource.fulltext or "",
        "url": resource.url or "",
    }
    background.add_task(index_resource, doc)
    return resource


@app.put("/resources/{resource_id}", response_model=ResourceRead)
def update_resource(
    resource_id: int,
    resource_in: ResourceCreate,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
):
    resource = db.get(ResourceModel, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    for field, value in resource_in.dict().items():
        setattr(resource, field, value)
    db.commit()
    db.refresh(resource)

    doc = {
        "id": str(resource.id),
        "title": resource.title,
        "abstract": resource.abstract,
        "authors": resource.authors,
        "date": resource.date.isoformat(),
        "provider": resource.provider,
        "keywords": resource.keywords,
        "fulltext": resource.fulltext or "",
        "url": resource.url or "",
    }
    background.add_task(index_resource, doc)
    return resource


@app.delete("/resources/{resource_id}", status_code=204)
def delete_resource_endpoint(
    resource_id: int,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
):
    resource = db.get(ResourceModel, resource_id)
    if resource:
        db.delete(resource)
        db.commit()
        background.add_task(delete_resource, resource_id)
    return None


# --------------------------
# Exhibit Endpoints
# --------------------------

@app.get("/exhibits", response_model=List[ExhibitSummary])
def list_exhibits(db: Session = Depends(get_db)):
    return db.query(ExhibitModel).all()


@app.get("/exhibits/{slug}", response_model=ExhibitRead)
def read_exhibit(slug: str, db: Session = Depends(get_db)):
    exhibit = db.get(ExhibitModel, slug)
    if not exhibit:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return exhibit


# --------------------------
# Search Endpoint
# --------------------------

@app.get("/search", response_model=SearchResponse)
def search(
    query: Optional[str] = Query("", alias="query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Solr-backed search with faceting on type, provider, and keywords.
    """
    # Fields must exist in your Solr schema
    facets = ["type", "provider", "keywords"]
    return search_resources(
        q=f"title:*{query}* OR abstract:*{query}*",
        page=page,
        page_size=page_size,
        facet_fields=facets,
    )