"""
Endpoints for exhibits.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.models import ExhibitModel
from api.schemas import ExhibitSummary, ExhibitRead

router = APIRouter(prefix="/exhibits", tags=["exhibits"])


@router.get("", response_model=list[ExhibitSummary])
def list_exhibits(db: Session = Depends(get_db)):
    stmt = select(ExhibitModel)
    return db.execute(stmt).scalars().all()


@router.get("/{slug}", response_model=ExhibitRead)
def read_exhibit(slug: str, db: Session = Depends(get_db)):
    exhibit = db.get(ExhibitModel, slug)
    if not exhibit:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return exhibit
