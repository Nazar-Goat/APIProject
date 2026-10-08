from fastapi import Depends

from src.modules.articles.repository import ArticleRepository
from src.modules.articles.service import ArticleService
from src.dependencies import get_jwt_service
from src.jwt_service import JWTService


def get_article_repository() -> ArticleRepository:
    return ArticleRepository()

def get_article_service(repo: ArticleRepository = Depends(get_article_repository)) -> ArticleService:
    return ArticleService(repo)