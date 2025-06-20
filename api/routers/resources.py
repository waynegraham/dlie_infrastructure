"""
CRUD operations for resources.
"""
from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from typing import Optional

from api.dependencies import get_db
from api.models import ResourceModel
from api.schemas import ResourceList, ResourceCreate, ResourceRead
from api.solr_client import index_resource, delete_resource

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=ResourceList)
def list_resources(
    limit: Optional[int] = Query(None, ge=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.scalar(select(func.count(ResourceModel.id)))
    if limit is not None:
        stmt = select(ResourceModel).order_by(ResourceModel.id.desc()).limit(limit)
        items = db.execute(stmt).scalars().all()
        return ResourceList(total=total, page=1, page_size=limit, items=items)
    stmt = select(ResourceModel).offset((page-1)*page_size).limit(page_size)
    items = db.execute(stmt).scalars().all()
    return ResourceList(total=total, page=page, page_size=page_size, items=items)


@router.get("/{resource_id}", response_model=ResourceRead)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.get(ResourceModel, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.post("", response_model=ResourceRead, status_code=201)
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


@router.put("/{resource_id}", response_model=ResourceRead)
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


@router.delete("/{resource_id}", status_code=204)
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
