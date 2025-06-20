# api/schemas.py

from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from typing import List, Optional, Dict
from datetime import date

# --------------------------
# Resource Schemas
# --------------------------
class ResourceBase(BaseModel):
    # map ORM column 'type' via alias to avoid shadowing built-in
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    title: str
    resource_type: str = Field(..., alias='type')
    date: date
    authors: List[str]
    abstract: str
    doi: Optional[str] = None
    url: Optional[HttpUrl] = None
    keywords: List[str]
    provider: str
    fulltext: Optional[str] = None

class ResourceCreate(ResourceBase):
    """Input schema for creating or updating a resource."""
    pass

class ResourceRead(ResourceBase):
    """Output schema for reading a single resource."""
    id: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class ResourceList(BaseModel):
    """Envelope for paginated or limited resource lists."""
    total: int
    page: int
    page_size: int
    items: List[ResourceRead]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class ResourceSummary(BaseModel):
    id: str
    title: str
    authors: List[str]
    date: str  # or date if you cast it server‐side

    model_config = ConfigDict(from_attributes=True)

# --------------------------
# Exhibit Schemas
# --------------------------
class ExhibitSummary(BaseModel):
    slug: str
    title: str

    model_config = ConfigDict(from_attributes=True)

class ExhibitRead(ExhibitSummary):
    """Detailed exhibit schema including narrative and resource IDs."""
    narrative: str
    resources: List[int]

    model_config = ConfigDict(from_attributes=True)

# --------------------------
# Facet & Search Schemas
# --------------------------
class FacetOption(BaseModel):
    label: str
    value: str
    count: int

class SearchResponse(BaseModel):
    """Response schema for Solr-backed search."""
    items: List[ResourceSummary]  # or minimal summary model
    total: int
    page_size: int
    facets: Dict[str, List[FacetOption]]

    model_config = ConfigDict(from_attributes=True)
