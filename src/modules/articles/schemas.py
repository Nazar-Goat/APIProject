from datetime import datetime
from typing import Annotated

from pydantic import BaseModel,  Field
from beanie import PydanticObjectId


class CreateArticleSchema(BaseModel):
    title: str = Field(min_length=10, max_length=200)
    content: str = Field(min_length=10, max_length=10_000)
    tags: Annotated[list[Annotated[str, Field(min_length=1, max_length=30)]], Field(max_length=10)]


class CreateArticleOutSchema(BaseModel):
    id: PydanticObjectId
    title: str
    content: str
    tags: list[str]
    author: PydanticObjectId
    created_at: datetime


class BaseArticleSchema(BaseModel):
    id: PydanticObjectId
    title: str
    tags: list[str]
    author: PydanticObjectId


class ListArticlesSchema(BaseModel):
    articles: list[BaseArticleSchema]
    total: int


class DetailArticleSchema(BaseArticleSchema):
    content: str


class UpdateArticleSchema(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=10,
        max_length=200
    )
    content: str | None = Field(
        default=None,
        min_length=10,
        max_length=10_000
    )