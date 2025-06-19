# api/schemas.py

from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import List, Optional
from datetime import date

class ResourceBase(BaseModel):
    title: str
    type: str
    date: date
    authors: List[str]
    abstract: str
    doi: Optional[str] = None
    url: Optional[HttpUrl] = None
    keywords: List[str]
    provider: str
    fulltext: Optional[str] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceRead(ResourceBase):
    id: int

    # Pydantic v2 ORM support:
    model_config = ConfigDict(from_attributes=True)

class ResourceList(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ResourceRead]

    # Also opt into from_attributes here so it will accept ORM items
    model_config = ConfigDict(from_attributes=True)