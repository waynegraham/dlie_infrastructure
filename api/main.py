import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Date, JSON, Text
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
default_authors = []
default_keywords = []

class ResourceModel(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    authors = Column(JSON, default=default_authors)
    abstract = Column(Text, nullable=True)
    doi = Column(String, nullable=True)
    url = Column(String, nullable=False)
    keywords = Column(JSON, default=default_keywords)
    provider = Column(String, nullable=True)
    fulltext = Column(Text, nullable=True)

# Pydantic schema
class Resource(BaseModel):
    id: int
    title: str
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

# FastAPI app
title = "Integral Ecology Library API"
app = FastAPI(title=title, version="0.2.0")

@app.on_event("startup")
def on_startup():
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Seed initial data if empty
    db = SessionLocal()
    if not db.query(ResourceModel).first():
        sample = [
            ResourceModel(
                id=1,
                title="Ecology and Society",
                date=date(2025, 6, 17),
                authors=["Author One", "Author Two"],
                abstract="Interdisciplinary resilience of socio-ecological systems.",
                doi="10.5751/ES-0",  # example DOI
                url="https://www.ecologyandsociety.org",
                keywords=["resilience", "ecology", "systems"],
                provider="Ecology and Society",
                fulltext="https://www.ecologyandsociety.org/vol20/iss3/art45.pdf"
            ),
            ResourceModel(
                id=2,
                title="Global Biodiversity Information Facility",
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

@app.get("/resources", response_model=List[Resource])
def list_resources():
    """Return all resources."""
    db = SessionLocal()
    items = db.query(ResourceModel).all()
    db.close()
    return items

@app.get("/resources/{resource_id}", response_model=Resource)
def get_resource(resource_id: int):
    """Return a single resource by its ID."""
    db = SessionLocal()
    item = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
    db.close()
    if not item:
        raise HTTPException(status_code=404, detail="Resource not found")
    return item