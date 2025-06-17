import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker, declarative_base

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
class Resource(BaseModel):
    id: int
    title: str
    type: str
    date: date
    authors: List[str]
    abstract: str
    doi: str
    url: str
    keywords: List[str]
    provider: str
    fulltext: str

    class Config:
        from_attributes = True

class ResourceList(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[Resource]

    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(
    title="Integral Ecology Library API",
    description="API serving open-access Integral Ecology resources via PostgreSQL",
    version="0.3.0"
)

# Enable CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Seed initial data
    db = SessionLocal()
    if not db.query(ResourceModel).first():
        sample = [
            ResourceModel(
                id=1,
                title="Ecology and Society",
                type="Journal",
                date=date(2025, 6, 17),
                authors=["Author One", "Author Two"],
                abstract="Interdisciplinary resilience of socio-ecological systems.",
                doi="10.5751/ES-0",
                url="https://www.ecologyandsociety.org",
                keywords=["resilience", "ecology", "systems"],
                provider="Ecology and Society",
                fulltext="https://www.ecologyandsociety.org/vol20/iss3/art45.pdf"
            ),
            ResourceModel(
                id=2,
                title="Global Biodiversity Information Facility",
                type="Dataset",
                date=date(2025, 6, 17),
                authors=["GBIF Team"],
                abstract="Massive open data repository for species occurrence records.",
                doi="10.15468/dl.8zsqxr",
                url="https://www.gbif.org",
                keywords=["biodiversity", "dataset", "open data"],
                provider="GBIF",
                fulltext=""
            ),
            ResourceModel(
                id=3,
                title="The Sustainability Agenda Podcast",
                type="Podcast",
                date=date(2025, 6, 17),
                authors=["Sustainability Agenda Team"],
                abstract="Monthly interviews on sustainability and systems change.",
                doi="",
                url="https://www.thesustainabilityagenda.com",
                keywords=["podcast", "sustainability", "interview"],
                provider="The Sustainability Agenda",
                fulltext=""
            ),
        ]
        db.add_all(sample)
        db.commit()
    db.close()

@app.get("/resources", response_model=ResourceList)
def list_resources(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Return paginated list of resources."""
    db = SessionLocal()
    total = db.query(func.count(ResourceModel.id)).scalar()
    items = (
        db.query(ResourceModel)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    db.close()
    return ResourceList(total=total, page=page, page_size=page_size, items=items)

@app.get("/resources/{resource_id}", response_model=Resource)
def get_resource(resource_id: int):
    """Return a single resource by its ID."""
    db = SessionLocal()
    item = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
    db.close()
    if not item:
        raise HTTPException(status_code=404, detail="Resource not found")
    return item