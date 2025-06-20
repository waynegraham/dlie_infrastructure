# api/models.py

from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.types import JSON
from api.database import Base


class ResourceModel(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    # avoid shadowing built-in 'type'; use attribute resource_type mapped to column 'type'
    resource_type = Column('type', String, nullable=False)
    date = Column(Date, nullable=False)
    authors = Column(JSON, nullable=False)      # list of author names
    abstract = Column(Text, nullable=False)
    doi = Column(String, nullable=True)
    url = Column(String, nullable=True)
    keywords = Column(JSON, nullable=False)     # list of keywords
    provider = Column(String, nullable=False)
    fulltext = Column(Text, nullable=True)


class ExhibitModel(Base):
    __tablename__ = "exhibits"
    slug = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    narrative = Column(Text, nullable=False)
    resources = Column(JSON,  nullable=False)  # list of resource IDs
