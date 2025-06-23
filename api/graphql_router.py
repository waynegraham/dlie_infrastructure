import datetime
from typing import List, Optional

import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import Depends
from sqlalchemy import select

from api.dependencies import get_db
from api.models import ResourceModel


@strawberry.type
class ResourceType:
    id: int
    title: str
    resource_type: str
    date: datetime.date
    authors: List[str]
    abstract: str
    doi: Optional[str]
    url: Optional[str]
    keywords: List[str]
    provider: str
    fulltext: Optional[str]


@strawberry.type
class Query:
    @strawberry.field
    def resource(self, info, id: int) -> Optional[ResourceType]:
        db = info.context["db"]
        model = db.get(ResourceModel, id)
        if not model:
            return None
        return ResourceType(
            id=model.id,
            title=model.title,
            resource_type=model.resource_type,
            date=model.date,
            authors=model.authors,
            abstract=model.abstract,
            doi=model.doi,
            url=model.url,
            keywords=model.keywords,
            provider=model.provider,
            fulltext=model.fulltext,
        )

    @strawberry.field
    def resources(
        self,
        info,
        page: int = 1,
        page_size: int = 20,
    ) -> List[ResourceType]:
        db = info.context["db"]
        stmt = select(ResourceModel).offset((page - 1) * page_size).limit(page_size)
        models = db.execute(stmt).scalars().all()
        return [
            ResourceType(
                id=m.id,
                title=m.title,
                resource_type=m.resource_type,
                date=m.date,
                authors=m.authors,
                abstract=m.abstract,
                doi=m.doi,
                url=m.url,
                keywords=m.keywords,
                provider=m.provider,
                fulltext=m.fulltext,
            )
            for m in models
        ]


def get_context(db=Depends(get_db)):
    return {"db": db}

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphql_ide=True,
)