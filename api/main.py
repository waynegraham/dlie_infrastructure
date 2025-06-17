import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Read database URL from env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class ResourceModel(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    url = Column(String, nullable=False)

class Resource(BaseModel):
    id: int
    title: str
    type: str
    url: str

app = FastAPI(
    title="Integral Ecology Library API",
    description="API serving open-access Integral Ecology resources via PostgreSQL",
    version="0.2.0"
)

@app.on_event("startup")
def on_startup():
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Seed initial data if empty
    db = SessionLocal()
    if not db.query(ResourceModel).first():
        initial = [
            ResourceModel(id=1, title="Ecology and Society", type="Journal", url="https://www.ecologyandsociety.org"),
            ResourceModel(id=2, title="Global Biodiversity Information Facility", type="Dataset", url="https://www.gbif.org"),
            ResourceModel(id=3, title="The Sustainability Agenda", type="Podcast", url="https://www.thesustainabilityagenda.com"),
        ]
        db.add_all(initial)
        db.commit()
    db.close()

@app.get("/resources", response_model=List[Resource])
def list_resources():
    db = SessionLocal()
    items = db.query(ResourceModel).all()
    db.close()
    return items

@app.get("/resources/{resource_id}", response_model=Resource)
def get_resource(resource_id: int):
    db = SessionLocal()
    item = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
    db.close()
    if not item:
        raise HTTPException(status_code=404)
