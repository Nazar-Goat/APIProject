from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from beanie import PydanticObjectId

from src.modules.articles.schemas import (
    CreateArticleSchema,
    CreateArticleOutSchema,
    ListArticlesSchema,
    DetailArticleSchema,
    UpdateArticleSchema,
)
from src.modules.articles.dependencies import get_article_service as article_service
from src.dependencies import AUS
from src.modules.articles.service import ArticleService

posts_router = APIRouter(prefix="/articles", tags=["articles"])


@posts_router.post(
    "",
    response_model=CreateArticleOutSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_article(
        current_user: AUS,
        new_article_data: CreateArticleSchema,
        service: ArticleService = Depends(article_service),
):
    return await service.create_article(new_article_data, current_user.id)


@posts_router.get(
    "",
    response_model=ListArticlesSchema,
    status_code=status.HTTP_200_OK,
)
async def get_list_of_articles(
        current_user: AUS,
        service: ArticleService = Depends(article_service),
        search_query: str | None = None,
        tag: str | None = None,
):
    return await service.get_articles_list(search_query, tag)


@posts_router.get(
    "/{article_id}",
    response_model=DetailArticleSchema,
    status_code=status.HTTP_200_OK,
)
async def get_detail_article_by_id(
        article_id: PydanticObjectId,
        current_user: AUS,
        service: ArticleService = Depends(article_service),
):
    return await service.get_article(article_id)


@posts_router.put(
    "/{article_id}",
    response_model=UpdateArticleSchema,
    status_code=status.HTTP_200_OK,
)
async def update_article_data(
        article_id: PydanticObjectId,
        update_data: UpdateArticleSchema,
        current_user: AUS,
        service: ArticleService = Depends(article_service),
):
    return await service.update_article(update_data, article_id)


@posts_router.delete(
    "/{article_id}",
)
async def delete_article_by_id(
        article_id: PydanticObjectId,
        current_user: AUS,
        service: ArticleService = Depends(article_service),
):
    return await service.delete_article(article_id)