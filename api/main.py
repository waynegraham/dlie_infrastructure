import os
from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# SQLAlchemy model
class ResourceModel(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    authors = Column(JSONB, nullable=False, server_default='[]')
    abstract = Column(Text, nullable=True)
    doi = Column(String, nullable=True)
    url = Column(String, nullable=False)
    keywords = Column(JSONB, nullable=False, server_default='[]')
    provider = Column(String, nullable=True)
    fulltext = Column(Text, nullable=True)

# Pydantic schemas
class ResourceBase(BaseModel):
    title: str
    type: str
    date: date
    authors: List[str]
    abstract: Optional[str] = None
    doi: Optional[str] = None
    url: str
    keywords: List[str]
    provider: Optional[str] = None
    fulltext: Optional[str] = None

class ResourceCreate(ResourceBase):
    pass

class Resource(ResourceBase):
    id: int

    class Config:
        from_attributes = True

class ResourceList(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[Resource]

    class Config:
        from_attributes = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI(
    title="Integral Ecology Library API",
    description="API serving open-access Integral Ecology resources via PostgreSQL",
    version="0.3.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(ResourceModel).first():
        # … your db.add_all(sample) and db.commit() …

        # reset the sequence so next id = max(id)+1
        db.execute(
            "SELECT setval(pg_get_serial_sequence('resources','id'), "
            "(SELECT MAX(id) FROM resources));"
        )
        db.commit()
    db.close()

@app.get("/resources", response_model=ResourceList)
def list_resources(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(func.count(ResourceModel.id)).scalar()
    items = (
        db.query(ResourceModel)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return ResourceList(total=total, page=page, page_size=page_size, items=items)

@app.get("/resources/{resource_id}", response_model=Resource)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    item = db.query(ResourceModel).get(resource_id)
    if not item:
        raise HTTPException(status_code=404, detail="Resource not found")
    return item

# --- NEW: create a resource ---
@app.post(
    "/resources",
    response_model=Resource,
    status_code=status.HTTP_201_CREATED,
)

def create_resource(
    resource_in: ResourceCreate,
    db: Session = Depends(get_db),
):
    # Optional: check for duplicates by DOI or URL
    if resource_in.doi:
        exists = db.query(ResourceModel).filter(ResourceModel.doi == resource_in.doi).first()
        if exists:
            raise HTTPException(status_code=400, detail="Resource with this DOI already exists")
    resource = ResourceModel(**resource_in.dict())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource