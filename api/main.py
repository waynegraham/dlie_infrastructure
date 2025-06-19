from fastapi import FastAPI, Depends, Query, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from database import SessionLocal, engine, Base
from models import ResourceModel
from schemas import ResourceList, ResourceCreate, ResourceRead

from solr_client import index_resource, delete_resource

app = FastAPI()

# Add this CORS middleware right after creating the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all origins in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/resources", response_model=ResourceList)
def list_resources(
    limit: Optional[int] = Query(None, ge=1, title="Limit", description="…"),
    page: int = Query(1, ge=1, title="Page", description="…"),
    page_size: int = Query(20, ge=1, le=100, title="Page Size", description="…"),
    db: Session = Depends(get_db),
):
    total = db.query(func.count(ResourceModel.id)).scalar()
    query = db.query(ResourceModel)
    if limit is not None:
        items = query.order_by(ResourceModel.id.desc()).limit(limit).all()
        return ResourceList(total=total, page=1, page_size=limit, items=items)
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return ResourceList(total=total, page=page, page_size=page_size, items=items)

# ← NEW: single-resource endpoint
@app.get("/resources/{resource_id}", response_model=ResourceRead)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single resource by its ID.
    """
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
      "id":      str(resource.id),
      "title":   resource.title,
      "abstract":resource.abstract,
      "authors": resource.authors,
      "date":    resource.date.isoformat(),
      "provider":resource.provider,
      "keywords":resource.keywords,
      "fulltext":resource.fulltext or "",
      "url":     resource.url or "",
    }
    background.add_task(index_resource, doc)
    return resource

# … your update and delete endpoints follow …