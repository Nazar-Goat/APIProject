from fastapi import HTTPException, status
from loguru import logger
from beanie import PydanticObjectId
from fastapi.responses import JSONResponse

from src.modules.articles.repository import ArticleRepository
from src.modules.articles.schemas import (
    CreateArticleSchema,
    CreateArticleOutSchema,
    BaseArticleSchema,
    ListArticlesSchema,
    DetailArticleSchema,
    UpdateArticleSchema,
)


class ArticleService:
    def __init__(self, repo: ArticleRepository):
        self._repo = repo

    async def create_article(self, article_data: CreateArticleSchema, user_id: PydanticObjectId) -> CreateArticleOutSchema:
        new_article = await self._repo.create(
            title=article_data.title,
            content=article_data.content,
            tags=article_data.tags,
            author=user_id,
        )

        return CreateArticleOutSchema(
                id=new_article.id,
                title=new_article.title,
                content=new_article.content,
                tags=new_article.tags,
                author=new_article.author.ref.id,
                created_at=new_article.created_at,
            )

    async def get_article(self, article_id: PydanticObjectId) -> DetailArticleSchema:
        article_exists = await self._repo.get_by_id(article_id)

        if article_exists is None:
            logger.warning(f"Article with id {article_id} does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article does not exist"
            )

        return DetailArticleSchema(
            id=article_exists.id,
            title=article_exists.title,
            content=article_exists.content,
            tags=article_exists.tags,
            author=article_exists.author.id,
        )

    async def get_articles_list(self, search_query: str | None, tag: str | None) -> ListArticlesSchema:
        articles_list = await self._repo.search(search_query=search_query, tag=tag)
        list_data = []

        for article in articles_list:
            list_data.append(
                BaseArticleSchema(
                    id = article.id,
                    title = article.title,
                    tags  = article.tags,
                    author = article.author.ref.id,
                )
            )

        return ListArticlesSchema(articles=list_data, total=len(list_data))


    async def update_article(self, data: UpdateArticleSchema, article_id: PydanticObjectId) -> DetailArticleSchema:
        article = await self._repo.get_by_id(article_id)

        if article is None:
            logger.warning(f"Article with id {article_id} does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article does not exist"
            )

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            logger.warning(f"No update data for article with id {article_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data"
            )

        updated_article = await self._repo.update(article=article, update_data=update_data)

        return DetailArticleSchema(
            id=updated_article.id,
            title=updated_article.title,
            content=updated_article.content,
            tags=updated_article.tags,
            author=updated_article.author.id,
        )


    async def delete_article(self, article_id: PydanticObjectId) -> JSONResponse:
            article = await self._repo.get_by_id(article_id)

            if article is None:
                logger.warning(f"Article with id {article_id} does not exist")
                raise HTTPException(status_code=404, detail="Article does not exist")

            await self._repo.delete(article)

            logger.info("Deleted article with id %s", article_id)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Order deleted successfully"},
            )