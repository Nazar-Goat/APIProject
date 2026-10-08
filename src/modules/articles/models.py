from typing import Annotated

from beanie import Document, Link
import pymongo
from pydantic import Field
from datetime import datetime, timezone

from src.modules.auth.models import User


Tag = Annotated[str, Field(min_length=1, max_length=30)]

class Article(Document):
    title: str = Field(min_length=10, max_length=200)
    content: str = Field(min_length=10, max_length=10_000)
    tags: list[Tag] = Field(default_factory=list, max_length=10)
    author: Link[User]
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "articles"
        indexes = [
            [
                ("title", pymongo.TEXT),
                ("content", pymongo.TEXT)
            ],
            "tags"
        ]
